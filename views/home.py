"""Home/Login Page"""

import socket
import requests  # type: ignore
import flet as ft  # type: ignore
import flet_easy as fs  # type: ignore
import assets.logo as logo  # pylint: disable=import-error
from core.params import Params as params
import sounds.beep as beep

home = fs.AddPagesy()


@home.page(route="/home", title="Home", protected_route= True)
def home_page(data: fs.Datasy):
    """Login Page"""
    page = data.page
    view = data.view
    print(page.padding)

    def show_drawer(_):
        view.drawer.open = True
        page.update()

    img_container = ft.Container(
        content=ft.Image(src_base64=logo.logo_base64, height=page.height / 5),
        alignment=ft.alignment.top_center,
    )

    menu_button = ft.Container(
        content=ft.IconButton(icon=ft.icons.MENU, on_click=show_drawer),
        alignment=ft.alignment.top_left,
        disabled=not params.Access.basic,
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

    return ft.View(
        controls=[
            ft.SafeArea(menu_button, bottom=False),
            img_container,
        ],
        drawer=view.drawer,
    )
