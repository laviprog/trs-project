import os

from src.config import settings
import requests


def get_video_from_archive(start_time: int, dur: int) -> str | None:
    url = f"{settings.ARCHIVE_URL}/archive-{start_time}-{dur}.mp4?token={settings.TOKEN}"
    save_path = f"data/{start_time}-{dur}.mp4"

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Video saved to {save_path}")
        return save_path
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None
