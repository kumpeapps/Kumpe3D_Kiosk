"""KumpeApps API - Response"""

from typing import Any, Dict, Optional
from requests import Response  # type: ignore


class KumpeApiResponse:
    """KumpeApps API Response

    This class wraps around the Response object from the requests library
    and provides additional properties and methods to easily access
    response data and status information.
    """

    def __init__(self, response: Response, model: Optional[Any] = None) -> None:
        """
        Initialize the KumpeApiResponse object.

        Args:
            response (Response): The response object from the requests library.
            model (Optional[Any]): An optional model to parse the response data.
        """
        self.response: Response = response
        self.status_code: int = response.status_code
        self.__data: Dict[str, Any] = response.json()
        self.model = model

    @property
    def data(self) -> Any:
        """Response Data

        Returns:
            Any: The parsed data from the response, either as a model instance or a dictionary.
        """
        if self.model and self.success:
            if isinstance(self.__data, list):
                return self.model(self.__data)
            return self.model(**self.__data)
        return self.__data

    @property
    def json(self) -> Dict[str, Any]:
        """Alias for data property

        Returns:
            Dict[str, Any]: The JSON data from the response.
        """
        return self.__data

    @property
    def success(self) -> bool:
        """Indicates if the response was successful (status code 2xx).

        Returns:
            bool: True if the status code is between 200 and 299, False otherwise.
        """
        return self.status_code >= 200 and self.status_code < 300

    @property
    def response_message(self) -> str:
        """Provides a human-readable message for the response status code.

        Returns:
            str: The message corresponding to the status code.
        """
        switcher = {
            200: "OK",
            201: "Created",
            202: "Accepted",
            204: "No Content",
            205: "Reset Content",
            206: "Partial Content",
            400: "Bad Request",
            401: "Unauthorized",
            402: "Payment Required",
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            406: "Not Acceptable",
            407: "Proxy Authentication Required",
            408: "Request Timeout",
            409: "Conflict",
            410: "Gone",
            412: "Precondition Failed",
            413: "Payload Too Large",
            414: "URI Too Long",
            418: "I'm a teapot",
            423: "Locked",
            426: "Upgrade Required",
            429: "Too Many Requests",
            451: "Unavailable For Legal Reasons",
            500: "Internal Server Error",
            501: "Not Implemented",
            502: "Bad Gateway",
            503: "Service Unavailable",
            504: "Gateway Timeout",
            511: "VPN Authentication Required",
        }
        return switcher.get(self.status_code, "Unknown Status Code")

    @property
    def error_message(self) -> str:
        """Error Message"""
        if self.success:
            return "No error"
        return self.data.get("error", self.response_message)

    def __str__(self):
        return f"Status: {self.status_code}, Data: {self.data}"

    def __repr__(self):  # pragma: no cover
        return f"KumpeAPIResponse({self.response})"

    def __getitem__(self, key):
        return self.data[key]

    def __contains__(self, key):
        return key in self.data

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)
