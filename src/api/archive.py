import os

import requests

from src.config import settings


def get_video_from_archive(start_time: int, dur: int) -> str:
    url = f"{settings.ARCHIVE_URL}/archive-{start_time}-{dur}.mp4?token={settings.TOKEN}"
    save_path = f"data/{start_time}-{dur}.mp4"

    response = requests.get(url, stream=True)
    response.raise_for_status()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"Video saved to {save_path}")
    return save_path
