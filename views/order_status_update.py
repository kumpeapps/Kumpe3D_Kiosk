"""Update Order Status"""

import pymysql
import flet as ft
import flet_easy as fs # pylint: disable=import-error
from core.params import Params as params
import sounds.beep as beep

order_status_update = fs.AddPagesy()


@order_status_update.page(route="/order_status_update", protected_route=True)
def addroll_page(data: fs.Datasy):
    """Main Function for Update Order Status"""
    page = data.page
    view = data.view
    pr = ft.ProgressRing(width=16, height=16, stroke_width=2, visible=False)

    def show_drawer(_):
        view.drawer.open = True
        page.update()

    page.title = "Update Order Status"

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

    def update_status(_):
        """Update Order Status"""
        updating()
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

        try:
            sql = """
                UPDATE filament
                SET
                    instock = 1,
                    backorder = 0,
                    discontinued = 0,
                    full_rolls_instock = full_rolls_instock + 1,
                    coming_soon = 0
                WHERE manufacture_barcode = %s OR swatch_id = %s;
            """
            cursor.execute(sql, (sku.value, sku.value))
            db.commit()
            verify_sql = """
                SELECT
                    idfilament,
                    swatch_id
                FROM filament
                WHERE 1=1
                    AND manufacture_barcode = %s OR swatch_id = %s
            """
            cursor.execute(verify_sql, (sku.value, sku.value))
            filament = cursor.fetchone()
            int(filament["idfilament"])
            sku.value = ""
            page.update()
            updating(False)
            beep.success(page)
        except (KeyError, TypeError):
            beep.error(page)
            show_banner_click(f"Invalid SKU {sku.value}")
            updating(False)

    text = ft.Container(
        content=ft.Text(
            "Update Order Status",
            text_align=ft.TextAlign.CENTER,
        ),
        alignment=ft.alignment.center,
    )
    pounds = ft.TextField(
        label="Pounds",
        autofocus=True,
        autocorrect=False,
        enable_suggestions=False,
        prefix_icon=ft.icons.SCALE_SHARP,
        on_submit=submit_pounds,
        text_align=ft.TextAlign.CENTER,
    )
    ounces = ft.TextField(
        label="Ounces",
        autofocus=True,
        autocorrect=False,
        enable_suggestions=False,
        prefix_icon=ft.icons.SCALE_SHARP,
        on_submit=submit_ounces,
        text_align=ft.TextAlign.CENTER,
    )
    length = ft.TextField(
        label="Length",
        autofocus=True,
        autocorrect=False,
        enable_suggestions=False,
        on_submit=submit_length,
        text_align=ft.TextAlign.CENTER,
    )
    width = ft.TextField(
        label="Width",
        autofocus=True,
        autocorrect=False,
        enable_suggestions=False,
        on_submit=submit_width,
        text_align=ft.TextAlign.CENTER,
    )
    height = ft.TextField(
        label="Height",
        autofocus=True,
        autocorrect=False,
        enable_suggestions=False,
        on_submit=submit_height,
        text_align=ft.TextAlign.CENTER,
    )
    select_status = ft.Dropdown(
        label="Order Status",
        options=[
            ft.dropdown.Option(
                "Product_Label_Printer",
                text="Product Label Printer (50x80mm)",
            ),
        ],
        value="Product_Label_Printer",
        prefix_icon=ft.icons.PRINT_ROUNDED,
    )

    submit_container = ft.Container(
        content=ft.ElevatedButton(text="Submit", on_click=add_roll),
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
        sku.focus()

    return ft.View(
        route="/add_roll",
        controls=[ft.SafeArea(menu_button, bottom=False), text, sku, submit_container, progress_ring],
        drawer=view.drawer,
    )
