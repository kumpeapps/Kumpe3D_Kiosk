"""Kumpe3D Kiosk"""

import flet as ft
import home
import addroll
from params import Params
from bottom_bar import bottom_bar

def main(page: ft.Page):
    """Main Function"""
    page.title = "Kumpe3D Kiosk"
    bottom_bar(page)

    def change_page(_):
        page.drawer.open = False
        if page.route == "home":
            addroll.main(page, False)
            home.main(page)
            page.update()
        elif page.route == "addroll":
            home.main(page, False)
            addroll.main(page)
            page.update()
        elif page.route == "logout":
            page.bottom_appbar.visible = False
            Params.Access.set_access_level("unauthenticated")
            home.main(page, True, True)
            page.update()

    page.on_route_change = change_page
    page.go("logout")


ft.app(main)
