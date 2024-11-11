"""KumpeApps API - Post"""

import requests  # type: ignore
import flet as ft  # type: ignore
from api import login as api_login
from core.params import Params as params
from models.print_label import K3DPrintLabel


def post_to_api(page: ft.Page, endpoint, data):
    """
    Posts data to the specified API endpoint using OAuth credentials.

    Args:
        page (ft.Page): The page object.
        endpoint (str): The API endpoint.
        data (dict): The data to be posted.

    Returns:
        Response: The response from the API.
    """
    base_url = params.API.url
    url = f"{base_url}{endpoint}"
    api_login.check_and_refresh_token(page)
    token_data = page.session.get("token_data")
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    response = requests.post(url, json=data, headers=headers, timeout=10)

    if response.status_code != 200:
        response.raise_for_status()

    return response.json()


def print_label(page: ft.Page, label: K3DPrintLabel):
    """
    Print a product label using the API.

    Args:
        page (ft.Page): The Flet page object containing the session.
        label (K3DPrintLabel): The label object containing the label details.

    Returns:
        dict: The response from the API.
    """
    return post_to_api(page, "/v1/k3d/printq", label.to_dict())
