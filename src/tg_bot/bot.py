from telebot import TeleBot

from src.config import settings


class TGBot:
    def __init__(self):
        self.bot = TeleBot(settings.BOT_TOKEN, parse_mode="HTML")
        self.chat_id = settings.CHANNEL_NAME

    def send_message(self, text: str) -> None:
        self.bot.send_message(chat_id=self.chat_id, text=text)

    def send_video_from_file(self, video_file_name: str) -> None:
        with open(video_file_name, "rb") as video:
            self.bot.send_video(chat_id=self.chat_id, video=video)
