"""Kumpe3D Main"""

import socket
from pathlib import Path
import requests  # type: ignore
import flet as ft  # type: ignore
import flet_easy as fs  # type: ignore
from core.params import Params as params
import sounds.beep as beep
import assets.logo as logo  # pylint: disable=import-error
import views.login as login_view

app = fs.FletEasy(
    route_init="/login",
    route_login="/login",
    path_views=Path(__file__).parent / "views",
)


@app.login
def login_x(data: fs.Datasy):
    """Require Login Function"""
    page = data.page
    dlg = ft.AlertDialog(
        title=ft.Text(
            "Access Denied!!!",
            text_align=ft.TextAlign.CENTER,
        ),
        on_dismiss=lambda e: print("Dialog dismissed!"),
        adaptive=False,
        bgcolor=ft.colors.RED_300,
    )

    def open_dlg():
        page.dialog = dlg
        dlg.open = True
        page.update()

    from core.params import Params as params  # pylint: disable=import-outside-toplevel

    if not params.Access.basic:
        open_dlg()
        return False

    match (
        page.session.get("selected_page"),
        params.Access.basic,
        params.Access.production,
        params.Access.orders,
        params.Access.print_labels,
        params.Access.filament_stock,
        params.Access.admin,
    ):

        case ("productlabel", _, _, _, False, _, _):
            open_dlg()
            return False
        case ("addroll", True, _, _, _, _, _):
            return True
        case ("emptyroll", True, _, _, _, True, _):
            return True
        case ("openroll", True, _, _, _, True, _):
            return True
        case ("addstock", True, True, _, _, _, _):
            return True
        case ("productionq", True, True, _, _, _, _):
            return True
        case ("productionq", True, _, True, _, _, _):
            return True
        case ("productlabel", True, _, _, True, _, _):
            return True
        case ("pendingorders", _, _, True, _, _, _):
            return True

    open_dlg()
    return False


@app.page(route="/dashboard", title="Dashboard", protected_route=True)
def dashboard_page(data: fs.Datasy):
    return ft.View(
        controls=[
            ft.Text("Dash", size=30),
            # We delete the key that we have previously registered
            ft.ElevatedButton("Logaut", on_click=data.logout("login")),
            ft.ElevatedButton("Home", on_click=data.go("/login")),
        ],
        vertical_alignment="center",
        horizontal_alignment="center",
        appbar=data.view.appbar,
    )


# @app.page(route="/login", title="Login")
# def login_page(data: fs.Datasy):
#     # create login stored user
#     username = ft.TextField(label="Username")

#     def store_login(e):
#         # db.append(username.value)  # We add to the simulated database

#         """First the values must be stored in the browser, then in the login
#         decorator the value must be retrieved through the key used and then
#         validations must be used."""
#         data.login(key="login", value=username.value, next_route="/dashboard")

#     return ft.View(
#         controls=[
#             ft.Text("login", size=30),
#             username,
#             ft.ElevatedButton("store login in browser", on_click=store_login),
#             ft.ElevatedButton("go Dasboard", on_click=data.go("/dashboard")),
#         ],
#         vertical_alignment="center",
#         horizontal_alignment="center",
#     )


@app.view
def view(data: fs.Datasy):
    """View"""
    page = data.page

    def home_go(_):
        page.session.set("selected_page", "home")
        page.go("/home")

    def logout(_):
        params.Access.set_access_level("unauthenticated")
        page.client_storage.clear()
        page.session.set("selected_page", "login")
        page.go("/login")

    def addstock_go(_):
        page.session.set("selected_page", "addstock")
        page.go("/add_stock")
        print("add_stock")

    def productionq_go(_):
        page.session.set("selected_page", "productionq")
        page.go("/production_queue")

    def productlabel_go(_):
        page.session.set("selected_page", "productlabel")
        page.go("/print_product_label")

    def pendingorders_go(_):
        page.session.set("selected_page", "pendingorders")
        page.go("/orders/pending")

    return fs.Viewsy(
        drawer=ft.NavigationDrawer(
            controls=[
                ft.Container(height=12),
                ft.Column(
                    controls=[
                        ft.Text("Navigation", size=25),
                        ft.Divider(thickness=2),
                        ft.FilledButton(
                            text="Home",
                            on_click=home_go,
                        ),
                        ft.FilledButton(
                            text="Add to Stock",
                            on_click=addstock_go,
                        ),
                        ft.FilledButton(
                            text="Production Queue",
                            on_click=productionq_go,
                        ),
                        ft.FilledButton(
                            text="Print Product Label",
                            on_click=productlabel_go,
                        ),
                        ft.FilledButton(
                            text="Pending Orders",
                            on_click=pendingorders_go
                        ),
                        ft.FilledButton(
                            text="Logout",
                            on_click=logout,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
        ),
        vertical_alignment="center",
        horizontal_alignment="center",
    )


app.run()
