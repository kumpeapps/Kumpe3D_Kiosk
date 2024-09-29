"""Add to Stock"""

import pymysql
import flet as ft
import flet_easy as fs  # pylint: disable=import-error
from pluggins.helpers import get_sku_array
from core.params import Params as params
import sounds.beep as beep
import pluggins.scan_list_builder as slb

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
        db = pymysql.connect(
            db=sql_params.database,
            user=sql_params.username,
            passwd=sql_params.password,
            host=sql_params.server,
            port=3306,
        )
        cursor = db.cursor(pymysql.cursors.DictCursor)
        scanned_list = slb.build_k3d_item_dict(sku.value, "to_stock_translation", cursor)
        quantity = int(qty.value)
        try:
            while quantity > 0:
                for item in scanned_list:
                    sku_array = get_sku_array(item["sku"])
                    sql = """INSERT INTO `Web_3dprints`.`stock`
                                (`sku`,
                                `swatch_id`,
                                `qty`)
                            VALUES
                                (%s, %s, %s)
                            ON DUPLICATE KEY UPDATE qty = qty + %s;"""
                    cursor.execute(
                        sql,
                        (sku_array["base_sku"], sku_array["color"], item["qty"], item["qty"]),
                    )
                quantity -= 1
            db.commit()
            sku.value = ""
            updating(False)
            sku.focus()
            page.update()
            beep.success(page)
        except (KeyError, pymysql.IntegrityError):
            beep.error(page)
            show_banner_click(f"Invalid SKU in [{sku.value}]")
            updating(False)
        finally:
            cursor.close()
            db.close()

    text = ft.Container(
        content=ft.Text(
            "Scan/Enter SKU to add to stock", text_align=ft.TextAlign.CENTER
        ),
        alignment=ft.alignment.center,
    )
    qty = ft.TextField(
        label="Qty",
        autofocus=False,
        autocorrect=False,
        enable_suggestions=False,
        prefix_icon=ft.icons.NUMBERS_SHARP,
        text_align=ft.TextAlign.LEFT,
        input_filter=ft.InputFilter(
            allow=True, regex_string=r"[0-9]", replacement_string=""
        ),
        width=100,
        value=1,
        keyboard_type=ft.KeyboardType.NUMBER,
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
        if not updating:
            sku.value = ""
            qty.value = 1
        page.update()
        sku.focus()

    return ft.View(
        route="/add_stock",
        controls=[
            ft.SafeArea(menu_button, bottom=False),
            text,
            qty,
            sku,
            submit_container,
            progress_ring,
        ],
        drawer=view.drawer,
    )
