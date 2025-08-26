from abc import ABC, abstractmethod

import requests
from requests import Response

from src.api.utils import retry_on_unauthorized


class BaseClient(ABC):
    """
    Base class for API clients.
    """

    def __init__(self, base_url: str, credentials: dict[str, str]):
        """
        Initialize the client with base URL and credentials.

        :param base_url: The base URL for the API.
        :param credentials: A dictionary containing authentication credentials.
        """
        self._base_url = base_url
        self._credentials = credentials
        self._headers = {"Authorization": None}

    @retry_on_unauthorized
    def _post(self, endpoint: str, **kwargs) -> Response:
        """
        Send a POST request to the specified endpoint with the given parameters.
        :param endpoint: The endpoint to send the POST request to.
        :param kwargs: Additional parameters to pass to the request, such as `data`, `files`, etc.
        :return: Response object containing the server's response.
        """
        return requests.post(endpoint, headers=self._headers, **kwargs)

    @abstractmethod
    def login(self) -> None:
        """
        Authenticate and set the Authorization header.
        :return: None
        """
        pass
