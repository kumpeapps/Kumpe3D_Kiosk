"""Main Function for Kumpe3D Kiosk"""

import flet_easy as fs
import flet as ft
from views.addroll import addroll
from views.login import login
from views.addstock import addstock
from views.openroll import openroll
from views.emptyroll import emptyroll
from views.productionq import productionq
from views.productlabel import printproductlabel
from core.config import ConfigApp
from core.params import Params as params

app = fs.FletEasy(route_init="/login", route_login="/login")


@app.login
def login_x(page: ft.Page):
    """Require Login Function"""
    dlg = ft.AlertDialog(
        title=ft.Text(
            f"Access Denied!!!\nYou do not have access to {page.title}",
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

    if not params.Access.basic:
        open_dlg()
        return False

    match (
        page.title,
        params.Access.basic,
        params.Access.production,
        params.Access.orders,
        params.Access.print_labels,
        params.Access.filament_stock,
        params.Access.admin,
    ):
        case (_, _, _, _, _, _, True):
            return True
        case ("Add Filament Roll", True, _, _, _, _, _):
            return True
        case ("Empty Filament Roll", True, _, _, _, True, _):
            return True
        case ("Open Filament Roll", True, _, _, _, True, _):
            return True
        case ("Add To Stock", True, True, _, _, _, _):
            return True
        case ("Production Queue", True, True, _, _, _, _):
            return True
        case ("Production Queue", True, _, True, _, _, _):
            return True
        case ("Add to Stock & Print Label", True, True, _, True, _, _):
            return True
        case ("Print Product Label", True, _, _, True, _, _):
            return True
        case ("Print Filament Colors Card", True, _, _, True, _, True):
            return True
    return False


app.add_pages(
    [login, addstock, addroll, openroll, emptyroll, productionq, printproductlabel]
)
ConfigApp(app)


# We run the application
app.run()
