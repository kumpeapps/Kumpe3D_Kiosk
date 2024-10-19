"""Core Class"""

import flet as ft # type: ignore
import flet_easy as fs # type: ignore
from core.params import Params as params

app = fs.FletEasy(route_init="/login")

@app.view
def view(data: fs.Datasy):
    return fs.Viewsy(
        appbar=ft.AppBar(
            title=ft.Text("AppBar Example"),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            text="🔥 Home",
                            on_click=data.go(data.route_init)
                            ),
                        ft.PopupMenuItem(
                            text="🔥 Dasboard",
                            on_click=data.go("/dasboard")
                            ),
                    ]
                ),
            ],
        ),
        vertical_alignment="center",
        horizontal_alignment="center",
    )

@app.page(route="/home", title="Flet-Easy", page_clear=True)
def home_page(data: fs.Datasy):
    # we obtain the values
    view = data.view
    # We can change the values of the appBar object, for example in title.
    view.appbar.title = ft.Text("Home")

    return ft.View(
        controls=[
            ft.Text("Home page", size=50),
        ],
        appbar=view.appbar,  # We reuse control
        vertical_alignment="center",
        horizontal_alignment="center",
    )

@app.page(route="/dasboard", title="Dasboard")
def dasboard_page(data: fs.Datasy):
    # we obtain the values
    view = data.view
    # We can change the values of the appBar object, for example in title.
    view.appbar.title = ft.Text("Dasboard")

    return ft.View(
        controls=[
            ft.Text("Dasboard page", size=50),
        ],
        appbar=view.appbar,  # We reuse control
        vertical_alignment="center",
        horizontal_alignment="center",
    )

app.run()