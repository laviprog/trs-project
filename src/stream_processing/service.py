import json
import time
from datetime import datetime, timezone
from json import JSONDecodeError

import requests
from requests import HTTPError

from src.api import AIClient, TranscriptionClient, get_video_from_archive
from src.log import log
from src.stream_processing.utils import delete_file
from src.tg_bot import TGBot


class StreamService:
    def __init__(self, chunk_duration: int = 60):
        self._chunk_duration = chunk_duration
        self._time = int(datetime.now(timezone.utc).timestamp()) - self._chunk_duration * 2
        self._ai_client = AIClient()
        self._transcription_client = TranscriptionClient()
        self._bot = TGBot()

    def process(self) -> None:
        while True:
            start_time_counter = time.perf_counter()
            try:
                file_path = get_video_from_archive(self._time, self._chunk_duration - 5)
            except requests.HTTPError as http_err:
                log.error("HTTP error occurred: %s", http_err)
            except Exception as err:
                log.error("An error occurred: %s", err)
            else:
                try:
                    log.info("Transcribing...")
                    segments = self._transcription_client.transcribe(file_path)
                except HTTPError as e:
                    log.error("Transcribing process error: %s", e)
                else:
                    delete_file(file_path)
                    if segments:
                        content = "\n".join(
                            f"[{(self._time + segment['start']):.2f} - "
                            f"{(self._time + segment['end']):.2f}] "
                            f"{segment['text']}"
                            for segment in segments
                        )
                        log.info("content: %s", content)
                        try:
                            result = self._ai_client.chat_completions(content=content)
                        except HTTPError as e:
                            log.error(f"HTTP error: {e}")
                        except Exception as e:
                            log.error(f"Unexpected error: {e}")
                        else:
                            if result:
                                log.info("Chat result: %s", result)
                                if not result.strip() == "-":
                                    result = (
                                        result.replace("```json", "")
                                        .replace("```text", "")
                                        .replace("```", "")
                                        .replace("“", '"')
                                        .replace("”", '"')
                                        .strip("`")
                                    )
                                try:
                                    result_json = json.loads(result)
                                except JSONDecodeError as e:
                                    log.error("JSONDecodeError: %s", e)
                                else:
                                    log.info("JSON result: %s", result_json)
                                    start_time, end_time = map(
                                        int,
                                        map(
                                            float,
                                            [
                                                t.strip()
                                                for t in result_json["time_range"].split("-")
                                            ],
                                        ),
                                    )

                                    start_time_normal = datetime.fromtimestamp(
                                        start_time + 60 * 60 * 3
                                    ).strftime("%H:%M:%S")
                                    end_time_normal = datetime.fromtimestamp(
                                        end_time + 60 * 60 * 3
                                    ).strftime("%H:%M:%S")

                                    caption = (
                                        f"<b>News</b>\n\n"
                                        f"{start_time_normal}-{end_time_normal}\n\n"
                                        f"<b>Summary</b>: {result_json['summary']}\n\n"
                                        f"<blockquote><b>Краткая выжимка</b>: "
                                        f"{result_json['summary_ru']}</blockquote>\n\n"
                                        f"<b>Temperature</b>: {result_json['temperature']}\n\n"
                                        + " ".join(f"#{tag}" for tag in result_json["tags"])
                                    )

                                    video_path = get_video_from_archive(
                                        start_time, min(end_time - start_time, 60)
                                    )

                                    self._bot.send_video_from_file(video_path)
                                    self._bot.send_message(caption)
                                    log.info("Send message: %s", caption)

            end_time_counter = time.perf_counter()
            duration_execution = end_time_counter - start_time_counter
            log.info("Duration execution: %s", str(duration_execution))
            if duration_execution < self._chunk_duration:
                time.sleep(self._chunk_duration - duration_execution)
            self._time += self._chunk_duration
