"""Add Roll"""

import os
import pymysql

try:
    from beepy import beep
except ImportError:
    pass
import flet as ft
from dotenv import load_dotenv
from params import Params
from menu import load_menu

load_dotenv()
userid = os.getenv(key="USERID", default="")


def main(page: ft.Page, active: bool = True):
    """Main Function for Add Roll"""
    load_menu(page)

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

    def add_roll(_):
        """Add's Roll to Stock"""
        sql_params = Params.SQL
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

    text = ft.Text(
        "Scan/Enter Filament ID/Manufacture Barcode to add filament roll to stock"
    )
    sku = ft.TextField(
        label="sku",
        autofocus=True,
        autocorrect=False,
        enable_suggestions=False,
        prefix_icon=ft.icons.BARCODE_READER,
        on_submit=add_roll,
        text_align=ft.TextAlign.CENTER,
    )
    submit_container = ft.Container(
        content=ft.ElevatedButton(text="Submit", on_click=add_roll),
        alignment=ft.alignment.center,
    )
    page.controls = [text, sku, submit_container]
    text.visible = active
    sku.visible = active
    submit_container.visible = active
    page.update()
    sku.focus()
