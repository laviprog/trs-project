import requests

from src.api.base_client import BaseClient
from src.api.transcription.schemas import Segment
from src.config import settings


class TranscriptionClient(BaseClient):
    def __init__(self):
        super().__init__(
            settings.TRANSCRIPTION_BASE_URL,
            {
                "username": settings.TRANSCRIPTION_USERNAME,
                "password": settings.TRANSCRIPTION_PASSWORD,
            },
        )

    def login(self) -> None:
        """
        Login to the transcription service using credentials.
        :return: None
        """
        ENDPOINT = self._base_url + "/api/v1/auth/login"
        DATA = self._credentials

        response = requests.post(ENDPOINT, json=DATA)
        response.raise_for_status()

        token = response.json()["access_token"]
        self._headers["Authorization"] = f"Bearer {token}"

    def transcribe(
        self,
        audio_file_path: str,
        language: str = "en",
        result_format: str = "srt",
        model: str = "turbo",
    ) -> list[Segment]:
        """
        Transcribe an audio file using the transcription service.
        :param audio_file_path: Path to the audio file to be transcribed.
        :param language: Language of the audio file (default is "en").
        :param result_format: Format of the transcription result (default is "srt").
        :param model: Model to use for transcription (default is "turbo").
        :return: List of dictionaries containing transcription results.
        """
        if not self._headers["Authorization"]:
            self.login()

        ENDPOINT = self._base_url + "/api/v1/transcription/transcribe"

        DATA = {
            "language": language,
            "result_format": result_format,
            "model": model,
        }

        with open(audio_file_path, "rb") as audio_file:
            FILES = {"file": audio_file}
            response = self._post(endpoint=ENDPOINT, files=FILES, data=DATA)

        response.raise_for_status()

        return response.json()["srt"]
