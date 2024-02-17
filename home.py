"""Home/Login Page"""

import os
import socket
import requests
import flet as ft
from dotenv import load_dotenv
# import logo  # pylint: disable=import-error
from params import Params

# from ip_host import get_ip
from menu import load_menu

load_dotenv()
userid = os.getenv(key="USERID", default="")


def main(page: ft.Page, active: bool = True, login: bool = False):
    """Main Function"""
    # img_container = ft.Container(
    #     content=ft.Image(src_base64=logo.logo_base64), alignment=ft.alignment.top_center
    # )

    def did_login(_):
        send_request(username_field.value, password_field.value)
        page.update()

    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        autocorrect=False,
        enable_suggestions=False,
        prefix_icon=ft.icons.PASSWORD,
        on_submit=did_login,
    )

    def username_submit(_):
        """Activate Password Field on Submit"""
        password_field.focus()

    username_field = ft.TextField(
        label="Username",
        autofocus=True,
        autocorrect=False,
        enable_suggestions=False,
        prefix_icon=ft.icons.PERSON,
        on_submit=username_submit,
    )

    submit_container = ft.Container(
        content=ft.ElevatedButton(text="Login", on_click=did_login),
        alignment=ft.alignment.center,
    )
    page.controls = [username_field, password_field, submit_container]
    # img_container.visible = active
    username_field.visible = login
    password_field.visible = login
    submit_container.visible = login

    page.update()

    def show_banner_click(
        message: str,
        color: ft.colors = ft.colors.RED_400,
        icon: ft.icons = ft.icons.ERROR_ROUNDED,
    ):
        page.banner = ft.Banner(
            bgcolor=color,
            leading=ft.Icon(icon, color=ft.colors.RED_900, size=40),
            content=ft.Text(message),
            actions=[
                ft.TextButton("Dismiss", on_click=close_banner),
            ],
        )
        page.banner.open = True
        page.update()

    def close_banner(_):
        page.banner.open = False
        page.update()

    def send_request(username: str, password: str):
        """KumpeApps SSO Login"""
        # Login
        # GET https://www.kumpeapps.com/api/check-access/by-login-pass

        try:
            response = requests.get(
                url=f"{Params.KumpeApps.api_url}/check-access/by-login-pass",
                params={
                    "_key": Params.KumpeApps.api_key,
                    "login": username,
                    "pass": password,
                },
                timeout=10,
            )

            data = response.json()
            success = data["ok"]
            if not success:
                show_banner_click(data["msg"])
            else:
                subscriptions = data["subscriptions"]
                user_id = data["user_id"]
                email = data["email"]
                name = data["name"]
                Params.Access.user_id = user_id
                Params.Access.email = email
                Params.Access.name = name
                is_admin = "213" in subscriptions
                is_basic = "214" in subscriptions
                is_orderfiller = "215" in subscriptions
                computername = socket.gethostname()
                if is_admin:
                    access_granted(user_id, computername, "admin")
                elif is_orderfiller:
                    access_granted(user_id, computername, "order_filler")
                elif is_basic:
                    access_granted(user_id, computername, "basic")
                else:
                    Params.Access.set_access_level("unauthenticated")
                    show_banner_click("Access Denied")
                    log_access(user_id, f"/{computername}/denied")
                    password_field.value = ""
                    page.update()

        except requests.exceptions.RequestException:
            show_banner_click(
                message="Unknown Error. This COULD mean you do not have an internet connection."
            )

    def access_granted(user_id: str, computername: str, access_level: str):
        """Access Granted"""
        Params.Access.set_access_level(access_level)
        log_access(user_id, f"/{computername}/granted/{access_level}")
        load_menu(page)
        page.bottom_appbar.visible = True
        username_field.visible = False
        password_field.visible = False
        submit_container.visible = False
        password_field.value = ""
        page.update()

    def log_access(user_id: str, note: str):
        """Send Access Log to KumpeApps SSO"""
        # POST Access Log
        # POST https://www.kumpeapps.com/api/access-log

        try:
            _ = requests.post(
                url=f"{Params.KumpeApps.api_url}/access-log",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                },
                data={
                    "_key": Params.KumpeApps.api_key,
                    "user_id": user_id,
                    "referrer": "Kumpe3D Kiosk",
                    "url": note,
                    "remote_addr": format(
                        requests.get(
                            "https://api.ipify.org", timeout=10
                        ).content.decode("utf8")
                    ),
                },
                timeout=10,
            )
        except requests.exceptions.RequestException:
            print("HTTP Request failed")
