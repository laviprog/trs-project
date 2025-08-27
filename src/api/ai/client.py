import requests

from src.api.ai.schemas import Message
from src.api.base_client import BaseClient
from src.config import settings


class AIClient(BaseClient):
    def __init__(self, message_context: int = 100):
        super().__init__(
            settings.AI_BASE_URL,
            {
                "email": settings.AI_EMAIL,
                "password": settings.AI_PASSWORD,
            },
        )
        self._model = settings.AI_MODEL
        self._messages: list[Message] = []
        self._message_context = message_context

    def login(self) -> None:
        """
        Login to the AI service using credentials.
        :return: None
        """
        ENDPOINT = self._base_url + "/api/v1/auths/signin"
        DATA = self._credentials

        response = requests.post(ENDPOINT, json=DATA)
        response.raise_for_status()

        token = response.json()["token"]
        self._headers["Authorization"] = f"Bearer {token}"

    def _add_message(self, message: Message) -> None:
        if len(self._messages) >= self._message_context:
            self._pop_message()
        self._messages.append(message)

    def _pop_message(self) -> Message:
        return self._messages.pop(0)

    def chat_completions(self, content: str) -> str:
        """
        Get chat completions from the AI service.
        :return: The response content from the AI service
        """
        self._add_message(
            Message(
                role="user",
                content=content,
            )
        )

        if not self._headers["Authorization"]:
            self.login()

        ENDPOINT = self._base_url + "/api/chat/completions"

        DATA = {
            "model": self._model,
            "messages": [message.to_dict() for message in self._messages],
        }

        response = self._post(endpoint=ENDPOINT, json=DATA)
        response.raise_for_status()
        result = response.json()
        result_message = result["choices"][0]["message"]
        self._add_message(
            Message(
                role=result_message["role"],
                content=result_message["content"],
            )
        )

        return result_message["content"]
