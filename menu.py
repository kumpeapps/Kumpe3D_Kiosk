"""Menu"""

import flet as ft
from libgravatar import Gravatar  # pylint: disable=import-error
from params import Params


def load_menu(page: ft.Page):
    """Load Side Menu"""
    if page.drawer is not None:
        page.drawer.clean()
    gravatar = Gravatar(Params.Access.email)
    avatar = ft.CircleAvatar(
        foreground_image_url=gravatar.get_image(default="mp"),
        content=ft.Text(Params.Access.username),
    )
    avatar_container = ft.Container(
        content=avatar,
        alignment=ft.alignment.top_center,
    )
    name_container = ft.Container(
        content=ft.Text(Params.Access.name), alignment=ft.alignment.top_center
    )

    def page_change(_):
        index = page.drawer.selected_index
        if index == 0:
            page.go("home")
        elif index == 1:
            page.go("logout")
        elif index == 3:
            page.go("addroll")

    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.Row(
                controls=[avatar_container, name_container],
                alignment=ft.alignment.top_center,
            ),
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.HOME),
                label="Home",
                selected_icon_content=ft.Icon(ft.icons.HOME_OUTLINED),
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.LOGOUT),
                label="Logout",
                selected_icon_content=ft.Icon(ft.icons.LOGOUT_OUTLINED),
            ),
            ft.Divider(thickness=2),
        ],
        on_change=page_change,
    )
    if Params.Access.product_stock:
        page.drawer.controls.append(
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.LIBRARY_ADD),
                label="Add to Stock",
                selected_icon=ft.icons.LIBRARY_ADD_OUTLINED,
            )
        )
    if Params.Access.filament_stock:
        page.drawer.controls.append(
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.ADD_BOX),
                label="Add Roll",
                selected_icon=ft.icons.ADD_BOX_OUTLINED,
            )
        )
        if not Params.Access.orders_desk:
            page.drawer.controls.append(
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.REMOVE_CIRCLE),
                    label="Open Roll",
                    selected_icon=ft.icons.REMOVE_CIRCLE_OUTLINE,
                )
            )
            page.drawer.controls.append(
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.DELETE_FOREVER),
                    label="Empty Roll",
                    selected_icon=ft.icons.DELETE_FOREVER_OUTLINED,
                )
            )
    if Params.Access.production:
        if Params.Access.print_room or Params.Access.admin:
            page.drawer.controls.append(
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.QUEUE),
                    label="Production Queue",
                    selected_icon=ft.icons.QUEUE_ROUNDED,
                )
            )
    if Params.Access.product_stock and Params.Access.print_labels:
        page.drawer.controls.append(
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.LIBRARY_ADD_CHECK),
                label="Add Stock & Print Label",
                selected_icon=ft.icons.LIBRARY_ADD_CHECK_OUTLINED,
            )
        )
    if Params.Access.print_labels:
        page.drawer.controls.append(
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.PRINT),
                label="Print Lables",
                selected_icon=ft.icons.PRINT_OUTLINED,
            )
        )
    if Params.Access.admin:
        if not Params.Access.orders_desk:
            page.drawer.controls.append(
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.icons.PRINT),
                    label="Print Filament Card",
                    selected_icon=ft.icons.PRINT_OUTLINED,
                )
            )
