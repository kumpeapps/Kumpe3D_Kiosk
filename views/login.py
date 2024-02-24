"""Home/Login Page"""

import socket
import requests
import flet as ft
import flet_easy as fs
import assets.logo as logo  # pylint: disable=import-error
from core.params import Params as params


login = fs.AddPagesy()


@login.page(route="/login")
def login_page(data: fs.Datasy):
    """Login Page"""
    page = data.page
    view = data.view

    def show_drawer(_):
        view.drawer.open = True
        page.update()

    if params.Access.basic:
        page.title = "Home"
    else:
        page.title = "Login"

    img_container = ft.Container(
        content=ft.Image(src_base64=logo.logo_base64, height=page.height / 2),
        alignment=ft.alignment.top_center,
    )

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
        visible=not params.Access.basic,
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
        visible=not params.Access.basic,
    )

    submit_container = ft.Container(
        content=ft.ElevatedButton(text="Login", on_click=did_login),
        alignment=ft.alignment.center,
        visible=not params.Access.basic,
    )

    menu_button = ft.Container(
        content=ft.FilledButton("Menu", on_click=show_drawer),
        alignment=ft.alignment.top_right,
        visible=params.Access.basic,
    )

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
                url=f"{params.KumpeApps.api_url}/check-access/by-login-pass",
                params={
                    "_key": params.KumpeApps.api_key,
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
                params.Access.user_id = user_id
                params.Access.email = email
                params.Access.name = name
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
                    params.Access.set_access_level("unauthenticated")
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
        params.Access.set_access_level(access_level)
        log_access(user_id, f"/{computername}/granted/{access_level}")
        username_field.visible = False
        password_field.visible = False
        submit_container.visible = False
        password_field.value = ""
        menu_button.visible = True
        page.title = "Home"
        page.update()

    def log_access(user_id: str, note: str):
        """Send Access Log to KumpeApps SSO"""
        # POST Access Log
        # POST https://www.kumpeapps.com/api/access-log

        try:
            _ = requests.post(
                url=f"{params.KumpeApps.api_url}/access-log",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                },
                data={
                    "_key": params.KumpeApps.api_key,
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

    return ft.View(
        route="/login",
        controls=[
            menu_button,
            img_container,
            username_field,
            password_field,
            submit_container,
        ],
        drawer=view.drawer,
    )
