"""KumpeApps API - Get"""

from typing import Optional
import requests  # type: ignore
import flet as ft  # type: ignore
import api.oauth
from core.params import Params, logger
from models.print_label import K3DPrintLabel
from models.user import User
from models.kumpeapi_response import KumpeApiResponse
from models.scan_translation import ScanTranslations
from models.production_q import ProductionQ
from models.order import Orders


def get(
    page: ft.Page, endpoint: str, params: Optional[dict], model: Optional[type] = None
) -> KumpeApiResponse:
    """
    Perform a GET request to the API.

    Args:
        page (ft.Page): The Flet page object containing session data.
        endpoint (str): The API endpoint.
        params (dict, optional): The query parameters for the GET request. Defaults to None.

    Returns:
        KumpeApiResponse: The response from the API.
    """
    base_url = Params.API.url
    url = f"{base_url}{endpoint}"
    api.oauth.check_and_refresh_token(page)
    token_data = page.session.get("token_data")
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    response = requests.get(url, headers=headers, params=params, timeout=10)
    logger.debug(f"GET {url} {response.status_code}")
    logger.debug(response.json())
    response = KumpeApiResponse(response, model)

    return response


def get_build_label(page: ft.Page) -> KumpeApiResponse:
    """
    Get a product label using the API.

    Args:
        page (ft.Page): The Flet page object containing the session.

    Returns:
        KumpeApiResponse: The product label object.
    """
    user: User = page.session.get("user")
    username = user.username
    label = get(page, f"/v1/k3d/build_label/{username}", None, K3DPrintLabel)
    return label


def get_scan_translations(page: ft.Page) -> KumpeApiResponse:
    """
    Get Scan translations List.

    Args:
        page (ft.Page): The Flet page object containing the session.

    Returns:
        KumpeApiResponse: The response from the API.
    """
    translations = get(page, "/v1/k3d/scan_translations", None, ScanTranslations)
    return translations


def get_production_q(page: ft.Page) -> KumpeApiResponse:
    """
    Get the production queue.

    Args:
        page (ft.Page): The Flet page object containing the session.

    Returns:
        KumpeApiResponse: The response from the API.
    """
    production_q = get(page, "/v1/k3d/production_q", None, ProductionQ)
    return production_q


def get_pending_orders(page: ft.Page) -> KumpeApiResponse:
    """
    Get the pending orders.

    Args:
        page (ft.Page): The Flet page object containing the session.

    Returns:
        KumpeApiResponse: The response from the API.
    """
    pending_orders = get(
        page, "/v1/k3d/orders?status_id_min=3&status_id_max=13", None, Orders
    )
    return pending_orders
