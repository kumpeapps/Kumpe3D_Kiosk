"""KumpeApps API - Get"""

from typing import Optional
import requests  # type: ignore
import flet as ft  # type: ignore
import api.oauth
from core.params import Params
from models.print_label import K3DPrintLabel
from models.user import User


def get(page: ft.Page, endpoint: str, params: Optional[dict]) -> dict:
    """
    Perform a GET request to the API.

    Args:
        page (ft.Page): The Flet page object containing session data.
        endpoint (str): The API endpoint.
        params (dict, optional): The query parameters for the GET request. Defaults to None.

    Returns:
        dict: The response from the API.
    """
    base_url = Params.API.url
    url = f"{base_url}{endpoint}"
    api.oauth.check_and_refresh_token(page)
    token_data = page.session.get("token_data")
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    response = requests.get(url, headers=headers, params=params, timeout=10)

    if response.status_code != 200:
        response.raise_for_status()

    return response.json()


def get_build_label(page: ft.Page) -> K3DPrintLabel:
    """
    Get a product label using the API.

    Args:
        page (ft.Page): The Flet page object containing the session.

    Returns:
        K3DPrintLabel: The product label object.
    """
    user: User = page.session.get("user")
    username = user.username
    items = get(page, f"/v1/k3d/build_label/{username}", None)
    label = K3DPrintLabel(items["build_label"])
    return label
