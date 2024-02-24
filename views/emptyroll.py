"""Empty Roll"""

import pymysql

try:
    from beepy import beep
except ImportError:
    pass
import flet as ft
import flet_easy as fs
from core.params import Params as params

emptyroll = fs.AddPagesy()


@emptyroll.page(route="/empty_roll", protected_route=True)
def emptyroll_page(data: fs.Datasy):
    """Main Function for Empty Roll"""
    page = data.page
    view = data.view

    def show_drawer(_):
        view.drawer.open = True
        page.update()

    page.title = "Empty Filament Roll"

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

    def empty_roll(_):
        """Removes Roll From Partial Roll"""
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
                    partial_rolls_instock = partial_rolls_instock - 1
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
                    AND (manufacture_barcode = %s OR swatch_id = %s)
            """
            cursor.execute(verify_sql, (sku.value, sku.value))
            filament = cursor.fetchone()
            int(filament['idfilament'])
            sku.value = ""
            page.update()
            sku.focus()
            try:
                beep(1)
            except NameError:
                pass
        except (KeyError, TypeError):
            try:
                beep(3)
            except NameError:
                pass
            show_banner_click(f"Invalid SKU {sku.value}")

    text = ft.Container(
        content=ft.Text(
        "Scan Filament SKU to remove roll from partial",
        text_align=ft.TextAlign.CENTER
    ),
        alignment=ft.alignment.center
    )
    sku = ft.TextField(
        label="sku",
        autofocus=True,
        autocorrect=False,
        enable_suggestions=False,
        prefix_icon=ft.icons.BARCODE_READER,
        on_submit=empty_roll,
        text_align=ft.TextAlign.CENTER,
    )
    submit_container = ft.Container(
        content=ft.ElevatedButton(text="Submit", on_click=empty_roll),
        alignment=ft.alignment.center,
    )

    menu_button = ft.Container(
        content=ft.FilledButton("Menu", on_click=show_drawer),
        alignment=ft.alignment.top_right
    )

    return ft.View(
        route="/empty_roll",
        controls=[menu_button, text, sku, submit_container],
        drawer=view.drawer,
    )
