"""KumpeApps Login"""

import time
import base64
import requests  # type: ignore
import flet as ft  # type: ignore
from core.params import Params as params


# Configuration
TOKEN_URL = f"{params.API.url}/oauth/token"
CLIENT_ID = params.API.client_id
CLIENT_SECRET = params.API.client_secret


def get_basic_auth_header(client_id: str, client_secret: str) -> dict:
    """
    Generate the Basic Authentication header.

    Args:
        client_id (str): The client ID.
        client_secret (str): The client secret.

    Returns:
        dict: A dictionary containing the Authorization header.
    """
    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    return {"Authorization": f"Basic {b64_auth_str}"}


def get_token(username: str, password: str) -> dict:
    """
    Obtain an OAuth token using the Resource Owner Password Credentials Grant.

    Args:
        username (str): The username.
        password (str): The password.

    Returns:
        dict: A dictionary containing the token information.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
    """
    data = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "scope": "profile access",
    }
    headers = get_basic_auth_header(CLIENT_ID, CLIENT_SECRET)
    response = requests.post(TOKEN_URL, data=data, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()


def refresh_token(refresh_token_str: str) -> dict:
    """
    Refresh the OAuth token using the refresh token.

    Args:
        refresh_token_str (str): The refresh token.

    Returns:
        dict: A dictionary containing the new token information.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
    """
    data = {"grant_type": "refresh_token", "refresh_token": refresh_token_str}
    headers = get_basic_auth_header(CLIENT_ID, CLIENT_SECRET)
    response = requests.post(TOKEN_URL, data=data, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()


def is_token_expired(token_data: dict) -> bool:
    """
    Check if the token is expired.

    Args:
        token_data (dict): The token data.

    Returns:
        bool: True if the token is expired, False otherwise.
    """
    return token_data["expires_at"] < time.time()


def login(page: ft.Page, username: str, password: str) -> dict:
    """
    Main function to obtain or refresh the OAuth token and return user profile 
    and access information.

    Args:
        page (ft.Page): The Flet page object containing the session.
        username (str): The username.
        password (str): The password.

    Returns:
        dict: A dictionary containing the token data, user profile, and user access information.
    """
    token_data = page.session.get("token_data")
    if token_data is None or is_token_expired(token_data):
        if token_data and "refresh_token" in token_data:
            token_data = refresh_token(token_data["refresh_token"])
        else:
            token_data = get_token(username, password)

        token_data["expires_at"] = time.time() + token_data["expires_in"]

    page.session.set("token_data", token_data)

    user_profile = get_user_profile(token_data)
    user_access = get_user_access(token_data)

    return {
        "token_data": token_data,
        "user_profile": user_profile,
        "user_access": user_access,
    }


def get_user_profile(token_data: dict) -> dict:
    """
    Get the user profile using the saved OAuth credentials.

    Args:
        token_data (dict): The token data containing the access token.

    Returns:
        dict: A dictionary containing the user profile information.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
    """
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    response = requests.get(
        f"{params.API.url}/v1/profile", headers=headers, timeout=10
    )
    response.raise_for_status()
    return response.json()


def get_user_access(token_data: dict) -> dict:
    """
    Get the user access information using the saved OAuth credentials.

    Args:
        token_data (dict): The token data containing the access token.

    Returns:
        dict: A dictionary containing the user access information.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
    """
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    response = requests.get(f"{params.API.url}/v1/access", headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()