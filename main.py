"""Kumpe3D Main"""

from pathlib import Path
import flet as ft  # type: ignore
import flet_easy as fs  # type: ignore
from helpers.is_port_open import rw_sql
from models.user import User

app = fs.FletEasy(
    route_init="/login",
    route_login="/login",
    path_views=Path(__file__).parent / "views",
)


@app.login
def login_x(data: fs.Datasy):
    """Require Login Function"""
    server_up = rw_sql()
    page = data.page
    if page.session.contains_key("user"):
        user: User = page.session.get("user")
    else:
        return False
    dlg = ft.AlertDialog(
        title=ft.Text(
            "Access Denied!!!",
            text_align=ft.TextAlign.CENTER,
        ),
        on_dismiss=lambda e: print("Dialog dismissed!"),
        adaptive=False,
        bgcolor=ft.colors.RED_300,
    )

    dlg_nointernet = ft.AlertDialog(
        title=ft.Text(
            "Server Unreachable. Please confirm VPN is connected!",
            text_align=ft.TextAlign.CENTER,
        ),
        on_dismiss=lambda e: print("Dialog dismissed!"),
        adaptive=False,
        bgcolor=ft.colors.RED_300,
    )

    if not server_up:
        page.dialog = dlg_nointernet
        dlg_nointernet.open = True
        page.update()
        return False

    def open_dlg():
        page.dialog = dlg
        dlg.open = True
        page.update()

    if not user.Access.basic:
        open_dlg()
        return False

    match (
        page.session.get("selected_page"),
        user.Access.basic,
        user.Access.admin,
        user.Access.production,
        user.Access.order_filler,
        user.Access.cashier,
    ):

        case ("productlabel", False, _, _, _, _):
            open_dlg()
            return False
        case ("home", True, _, _, _, _, _):
            return True
        case ("addstock", True, _, True, _, _):
            return True
        case ("productionq", True, True, _, _, _):
            return True
        case ("productionq", True, _, True, _, _):
            return True
        case ("productlabel", True, _, True, _, _):
            return True
        case ("pendingorders", True, _, _, True, _):
            return True
        case ("register", True, _, _, _, True):
            return True

    open_dlg()
    return False


@app.view
def view(data: fs.Datasy):
    """View"""
    page = data.page

    def home_go(_):
        page.session.set("selected_page", "home")
        page.go("/home")

    def logout(_):
        page.session.clear()
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
                            text="Pending Orders", on_click=pendingorders_go
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
