"""Main Function for Kumpe3D Kiosk"""

import flet as ft
from flet_easy import FletEasy  # pylint: disable=import-error
from views.addroll import addroll
from views.login import login
from views.addstock import addstock
from views.openroll import openroll
from views.emptyroll import emptyroll
from views.productionq import productionq
from views.productlabel import printproductlabel
from views.pendingorders import pendingorders
from views.orderitems import orderitems
from core.config import ConfigApp

app = FletEasy(route_init="/login", route_login="/login")


@app.login
def login_x(page: ft.Page):
    """Require Login Function"""
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


app.add_pages(
    [login, addstock, addroll, openroll, emptyroll, productionq, printproductlabel, pendingorders, orderitems]
)
ConfigApp(app)


# We run the application
app.run(assets_dir="assets")
