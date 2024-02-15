"""Bottom Bar"""

import flet as ft
from menu import load_menu


def bottom_bar(page: ft.Page):
    """Add Menu Bar"""

    def show_drawer(_):
        """Show Menu"""
        page.drawer.open = True
        page.drawer.update()

    page.horizontal_alignment = page.vertical_alignment = "center"
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

    page.bottom_appbar = ft.BottomAppBar(
        bgcolor=ft.colors.GREEN,
        shape=ft.NotchShape.CIRCULAR,
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.MENU, icon_color=ft.colors.WHITE, on_click=show_drawer
                ),
                ft.Container(expand=True),
            ]
        ),
    )
    load_menu(page)
