"""Add to Stock"""

import pymysql

try:
    from beepy import beep
except ImportError:
    pass
import flet as ft
import flet_easy as fs
from pluggins.helpers import get_sku_array
from core.params import Params as params

addstock = fs.AddPagesy()


@addstock.page(route="/add_stock", protected_route=True)
def addstock_page(data: fs.Datasy):
    """Increments SKU Stock Qty"""
    page = data.page
    view = data.view
    pr = ft.ProgressRing(width=16, height=16, stroke_width=2, visible=False)

    page.title = "Add to Stock"
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

    def show_drawer(_):
        view.drawer.open = True
        page.update()

    def close_banner(_):
        """Close Banner"""
        page.banner.open = False
        page.update()

    def show_banner_click(
        message: str,
        color: ft.colors = ft.colors.RED_400,
        icon: ft.icons = ft.icons.ERROR_ROUNDED,
    ):
        """Show Banner"""
        page.banner = ft.Banner(
            bgcolor=color,
            leading=ft.Icon(icon, color=ft.colors.RED_900, size=40),
            content=ft.Text(message),
            actions=[
                ft.TextButton("Dismiss", on_click=close_banner),
            ],
        )
        page.banner.open = True
        page.update()

    def add_stock(_):
        updating()
        try:
            sku_array = get_sku_array(sku.value)
            sql = """INSERT INTO `Web_3dprints`.`stock`
                        (`sku`,
                        `swatch_id`,
                        `qty`)
                    VALUES
                        (%s, %s, 1)
                    ON DUPLICATE KEY UPDATE qty = qty + 1;"""
            cursor.execute(sql, (sku_array["base_sku"], sku_array["color"]))
            db.commit()
            sku.value = ""
            sku.focus()
            updating(False)
            try:
                beep(1)
            except NameError:
                pass
        except KeyError:
            try:
                beep(3)
            except NameError:
                pass
            show_banner_click(f"Invalid SKU {sku.value}")
            updating(False)

    text = ft.Container(
        content=ft.Text(
            "Scan/Enter SKU to add to stock", text_align=ft.TextAlign.CENTER
        ),
        alignment=ft.alignment.center,
    )
    sku = ft.TextField(
        label="sku",
        autofocus=True,
        autocorrect=False,
        enable_suggestions=False,
        prefix_icon=ft.icons.BARCODE_READER,
        on_submit=add_stock,
        text_align=ft.TextAlign.CENTER,
    )
    submit_container = ft.Container(
        content=ft.ElevatedButton(text="Submit", on_click=add_stock),
        alignment=ft.alignment.center,
    )

    menu_button = ft.Container(
        content=ft.IconButton(icon=ft.icons.MENU, on_click=show_drawer),
        alignment=ft.alignment.top_left,
    )

    progress_ring = ft.Container(
        content=pr,
        alignment=ft.alignment.center,
    )

    def updating(updating: bool = True):
        sku.disabled = updating
        submit_container.disabled = updating
        progress_ring.visible = updating
        page.update()

    return ft.View(
        route="/add_stock",
        controls=[menu_button, text, sku, submit_container, progress_ring],
        drawer=view.drawer,
    )
