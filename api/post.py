"""KumpeApps API - Post"""

import requests  # type: ignore
import flet as ft  # type: ignore
import api.oauth
from core.params import Params as params
from models.print_label import K3DPrintLabelItem
from models.kumpeapi_response import KumpeApiResponse
from core.params import logger


def post(page: ft.Page, endpoint, data) -> KumpeApiResponse:
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

    response: requests.Response = requests.post(
        url, json=data, headers=headers, timeout=10
    )
    logger.debug(f"Status code: {response.status_code}")
    print(response.json())

    return KumpeApiResponse(response)


def print_label(page: ft.Page, label: dict) -> KumpeApiResponse:
    """
    Print a product label using the API.

    Args:
        page (ft.Page): The Flet page object containing the session.
        label (dict): The label object containing the label details.

    Returns:
        dict: The response from the API.
    """
    return post(page, "/v1/k3d/printq", label)


def add_label_item(page: ft.Page, item: K3DPrintLabelItem) -> KumpeApiResponse:
    """
    Add a label item to the product label using the API.

    Args:
        page (ft.Page): The Flet page object containing the session.
        item (K3DPrintLabelItem): The label item object containing the item details.

    Returns:
        dict: The response from the API.
    """
    response = post(page, "/v1/k3d/build_label", item.to_dict())
    response.model = K3DPrintLabelItem
    return response


def add_stock(page: ft.Page, sku: str, qty: int) -> KumpeApiResponse:
    """
    Add stock to the inventory using the API.

    Args:
        page (ft.Page): The Flet page object containing the session.
        sku (str): The SKU of the product.
        qty (int): The quantity to add to the stock.

    Returns:
        KumpeApiResponse: The response from the API.
    """
    return post(page, f"/v1/k3d/product/{sku}/stock/increment/{qty}", {})
