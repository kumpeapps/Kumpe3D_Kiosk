"""Home/Login Page"""

import socket
import requests  # type: ignore
import flet as ft  # type: ignore
import flet_easy as fs  # type: ignore
import assets.logo as logo  # pylint: disable=import-error
from core.params import Params as params
from core.params import logger
import sounds.beep as beep
from helpers.is_port_open import rw_sql
from models.user import User
from api import login as api_login

login = fs.AddPagesy()
hf = ft.HapticFeedback()


@login.page(route="/login")
def login_page(data: fs.Datasy):
    """Login Page"""
    page = data.page
    view = data.view
    page.overlay.append(hf)
    pr = ft.ProgressRing(width=16, height=16, stroke_width=2, visible=False)
    pr_container = ft.Container(
        content=pr,
        alignment=ft.alignment.center,
    )

    def show_drawer(_):
        view.drawer.open = True
        page.update()

    img_container = ft.Container(
        content=ft.Image(src_base64=logo.logo_base64, height=page.height / 5),
        alignment=ft.alignment.top_center,
    )

    def did_login(_):
        server_up = rw_sql()
        logging_in()
        if server_up:
            send_request(username_field.value, password_field.value)
        else:
            show_banner_click(
                "Server Unreachable. Please check internet and VPN connection."
            )
            logging_in(False)
        page.update()

    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=False,
        adaptive=True,
        autocorrect=True,
        enable_suggestions=True,
        prefix_icon=ft.icons.PASSWORD,
        on_submit=did_login,
        visible=True,
        text_align=ft.TextAlign.CENTER,
        width=250,
        autofill_hints=ft.AutofillHint.PASSWORD,
    )

    def username_submit(_):
        """Activate Password Field on Submit"""
        password_field.focus()

    username_field = ft.TextField(
        label="Username",
        autofocus=True,
        autocorrect=True,
        enable_suggestions=True,
        prefix_icon=ft.icons.PERSON,
        adaptive=True,
        on_submit=username_submit,
        visible=True,
        text_align=ft.TextAlign.CENTER,
        width=250,
        autofill_hints=ft.AutofillHint.USERNAME,
    )

    submit_container = ft.Container(
        content=ft.ElevatedButton(text="Login", on_click=did_login),
        alignment=ft.alignment.center,
        visible=True,
    )

    menu_button = ft.Container(
        content=ft.IconButton(icon=ft.icons.MENU, on_click=show_drawer),
        alignment=ft.alignment.top_left,
        disabled=True,
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
        logger.debug(f"Sending Login Request for {username}")
        try:
            api_login.login(page, username, password)
            if not page.session.contains_key("user"):
                show_banner_click("Access Denied")
                beep.error(page, hf)
                logging_in(False)
            else:
                user: User = page.session.get("user")
                computername = socket.gethostname()
                if user.Access.admin:
                    access_granted(user, computername, "admin")
                elif user.Access.order_filler:
                    access_granted(user, computername, "order_filler")
                elif user.Access.basic:
                    access_granted(user, computername, "basic")
                else:
                    show_banner_click("Access Denied")
                    beep.error(page, hf)
                    log_access(f"{user.user_id}", f"/{computername}/denied")
                    password_field.value = ""
                    logging_in(False)
                    page.update()

        except requests.exceptions.RequestException:
            logger.exception("KumpeApps SSO Login Failed")

    def access_granted(user: User, computername: str, access_level: str):
        """Access Granted"""
        logger.success("Access Granted!")
        page.session.set("username", user.username)
        params.SHIPPO.get_values()
        params.SQL.get_values()
        log_access(f"{user.user_id}", f"/{computername}/granted/{access_level}")
        logging_in(False)
        page.update()
        page.session.set("selected_page", "home")
        page.go("/home")

    def logging_in(loggingin: bool = True):
        pr.visible = loggingin
        username_field.disabled = loggingin
        password_field.disabled = loggingin
        submit_container.disabled = loggingin
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
            ft.SafeArea(menu_button, bottom=False),
            img_container,
            username_field,
            password_field,
            submit_container,
            pr_container,
        ],
        drawer=view.drawer,
        horizontal_alignment="center",
    )
