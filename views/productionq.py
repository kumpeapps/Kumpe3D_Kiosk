"""Production Queue"""

import flet as ft  # type: ignore
import flet_easy as fs  # type: ignore
import api.get
from models.production_q import ProductionQ

productionq = fs.AddPagesy()


@productionq.page(route="/production_queue", protected_route=True)
def productionq_page(data: fs.Datasy):
    """Main Function for Add Roll"""
    page = data.page
    view = data.view
    pr = ft.ProgressRing(width=16, height=16, stroke_width=2, visible=False)

    def show_drawer(_):
        view.drawer.open = True
        page.update()

    page.title = "Production Queue"

    production_q: ProductionQ = api.get.get_production_q(page).data
    data_table = ft.DataTable(
        data_row_color={"hovered": "0x30FF0000"},
        show_checkbox_column=True,
        width=page.window_width - 5,
        columns=[
            ft.DataColumn(ft.Text("QTY")),
            ft.DataColumn(ft.Text("SKU")),
            ft.DataColumn(ft.Text("Description")),
        ],
        rows=production_q.data_rows,
    )

    menu_button = ft.Container(
        content=ft.IconButton(icon=ft.icons.MENU, on_click=show_drawer),
        alignment=ft.alignment.top_left,
    )

    progress_ring = ft.Container(
        content=pr,
        alignment=ft.alignment.center,
    )

    table_container = ft.SafeArea(
        ft.Container(
            content=data_table, alignment=ft.alignment.top_left, width=page.width
        )
    )

    return ft.View(
        route="/production_queue",
        controls=[
            progress_ring,
            ft.SafeArea(menu_button, bottom=False),
            table_container,
        ],
        drawer=view.drawer,
    )
