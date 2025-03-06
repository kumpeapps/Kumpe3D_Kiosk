"""KumpeApps API - Put"""

import requests  # type: ignore
import flet as ft  # type: ignore
import api.oauth
from core.params import Params as params
from models.print_label import K3DPrintLabelItem
from models.kumpeapi_response import KumpeApiResponse
from core.params import logger


def put(page: ft.Page, endpoint, data) -> KumpeApiResponse:
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
    api.oauth.check_and_refresh_token(page)
    token_data = page.session.get("token_data")
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    response: requests.Response = requests.put(
        url, json=data, headers=headers, timeout=10
    )
    logger.debug(f"Status code: {response.status_code}")
    logger.debug(f"Response: {response.json()}")

    return KumpeApiResponse(response)


def update_order_item(
    page: ft.Page, sku: str, order_id: int, qty: int, user: str
) -> KumpeApiResponse:
    """
    Update an order item using the API.

    Args:
        page (ft.Page): The Flet page object containing the session.
        sku (str): The SKU of the item to be updated.
        order_id (int): The ID of the order.
        qty (int): The quantity to update.

    Returns:
        dict: The response from the API.
    """
    return put(
        page,
        f"/v1/k3d/order/{order_id}/items/{sku}",
        {"qty": qty, "last_updated_by": user},
    )
