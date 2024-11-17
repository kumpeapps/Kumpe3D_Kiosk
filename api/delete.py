"""KumpeApps API - Delete"""

from typing import Optional
import requests  # type: ignore
import flet as ft  # type: ignore
import api.oauth
from core.params import Params
from models.kumpeapi_response import KumpeApiResponse
from models.user import User


def delete(
    page: ft.Page, endpoint: str, params: Optional[dict] = None
) -> KumpeApiResponse:
    """
    Perform a DELETE request to the API.

    Args:
        page (ft.Page): The Flet page object containing session data.
        endpoint (str): The API endpoint.
        params (dict, optional): The query parameters for the DELETE request. Defaults to None.

    Returns:
        dict: The response from the API.
    """
    base_url = Params.API.url
    url = f"{base_url}{endpoint}"
    api.oauth.check_and_refresh_token(page)
    token_data = page.session.get("token_data")
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    response = requests.delete(url, headers=headers, params=params, timeout=10)
    response = KumpeApiResponse(response)

    return response


def clear_build_label(page: ft.Page) -> KumpeApiResponse:
    """
    Clear the product label using the API.

    Args:
        page (ft.Page): The Flet page object containing the session.

    Returns:
        dict: The response from the API.
    """
    user: User = page.session.get("user")
    username = user.username
    return delete(page, f"/v1/k3d/build_label/{username}")
