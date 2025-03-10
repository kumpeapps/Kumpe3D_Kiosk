"""Home/Login Page"""

import flet as ft  # type: ignore
import flet_easy as fs  # type: ignore

home = fs.AddPagesy()


@home.page(route="/home", title="Home", protected_route=True)
def home_page(data: fs.Datasy):
    """Login Page"""
    page = data.page
    view = data.view
    print(page.padding)

    def show_drawer(_):
        view.drawer.open = True
        page.update()

    img_container = ft.Container(
        content=ft.Image(src="/logo.png", height=page.height / 5),
        alignment=ft.alignment.top_center,
    )

    menu_button = ft.Container(
        content=ft.IconButton(icon=ft.Icons.MENU, on_click=show_drawer),
        alignment=ft.alignment.top_left,
        disabled=False,
    )

    return ft.View(
        controls=[
            ft.SafeArea(menu_button, bottom=False),
            img_container,
        ],
        drawer=view.drawer,
    )
