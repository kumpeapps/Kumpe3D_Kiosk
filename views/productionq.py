"""Production Queue"""

import pymysql
import flet as ft
import flet_easy as fs
from core.params import Params as params

productionq = fs.AddPagesy()


@productionq.page(route="/production_queue", protected_route=True)
def productionq_page(data: fs.Datasy):
    """Main Function for Add Roll"""
    page = data.page
    view = data.view

    def show_drawer(_):
        view.drawer.open = True
        page.update()

    page.title = "Production Queue"

    if params.SQL.username == "":
        params.SQL.get_values()
    sql_params = params.SQL
    db = pymysql.connect(
        db=sql_params.database,
        user=sql_params.username,
        passwd=sql_params.password,
        host=sql_params.server,
        port=3306,
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """
        SELECT 
            CONCAT(sku, '-', swatch_id) AS sku,
            `name`,
            0 - qty AS qty
        FROM
            Web_3dprints.vw_stock__production_queue;
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    data_table = ft.DataTable(
        width=page.width,
        data_row_color={"hovered": "0x30FF0000"},
        show_checkbox_column=True,
    )
    data_table.columns = [
        ft.DataColumn(ft.Text("QTY")),
        ft.DataColumn(ft.Text("SKU")),
        ft.DataColumn(ft.Text("Description")),
    ]
    data_rows = []
    for result in results:
        row = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(int(result["qty"]))),
                ft.DataCell(ft.Text(result["sku"])),
                ft.DataCell(ft.Text(result["name"])),
            ]
        )
        data_rows.append(row)
    data_table.rows = data_rows

    menu_button = ft.Container(
        content=ft.IconButton(icon=ft.icons.MENU, on_click=show_drawer),
        alignment=ft.alignment.top_left,
    )

    return ft.View(
        route="/production_queue",
        controls=[menu_button, data_table],
        drawer=view.drawer,
    )
