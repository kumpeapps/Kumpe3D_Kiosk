"""Order Items"""

import pymysql
import flet as ft
import flet_easy as fs  # pylint: disable=import-error
from core.params import Params as params
import sounds.beep as beep

orderitems = fs.AddPagesy()


@orderitems.page(route="/order_items/{order_id:d}", protected_route=True)
def orderitems_page(data: fs.Datasy, order_id: int):
    """Main Function for Pending Orders"""
    page = data.page
    view = data.view
    pr = ft.ProgressRing(width=16, height=16, stroke_width=2, visible=False)

    def show_drawer(_):
        view.drawer.open = True
        page.update()

    page.title = f"Order: {order_id}"

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

    menu_button = ft.Container(
        content=ft.IconButton(icon=ft.icons.MENU, on_click=show_drawer),
        alignment=ft.alignment.top_left,
    )

    progress_ring = ft.Container(
        content=pr,
        alignment=ft.alignment.center,
    )

    def scanned(_):
        """Add Item as Picked"""
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
            INSERT INTO Web_3dprints.orders__items
            (
                idorders
                ,title
                ,sku
                ,qty
                ,qty_filled
                ,customization
                ,price
                ,last_updated_by
                )
            VALUES
            (
                %s,
                (SELECT title from Web_3dprints.products where sku = %s OR sku = CONCAT(LEFT(%s,11),"-000")),
                %s,
                0,
                1,
                '',
                0,
                %s
            )
            ON DUPLICATE KEY UPDATE qty_filled=qty_filled + 1;
        """

        values = (
            order_id,
            scan_field.value,
            scan_field.value,
            scan_field.value,
            page.client_storage.get("username"),
        )
        try:
            cursor.execute(sql, values)
            db.commit()
            db.close()
            scan_field.value = ""
            tiles.clear()
            get_items()
            beep.success(page)
            scan_field.focus()
        except:  # pylint: disable=bare-except
            beep.error(page)
            show_banner_click(f"Invalid SKU: {scan_field.value}")
            scan_field.value = ""
            scan_field.focus()

    scan_field = ft.TextField(
        autocorrect=False,
        enable_suggestions=False,
        autofocus=True,
        on_submit=scanned,
        width=page.width / 4,
        height=30,
    )

    scan_container = ft.Container(alignment=ft.alignment.top_center, content=scan_field)

    top_row = ft.SafeArea(
        ft.Row(
            controls=[
                ft.Column(controls=[menu_button]),
                ft.Column(
                    controls=[scan_container], alignment=ft.MainAxisAlignment.CENTER
                ),
            ],
            spacing=60,
        ), bottom=False
    )
    tiles = []

    def tile_clicked(order_id):
        page.go(f"/order/{order_id}")

    def get_items():
        """Add's Roll to Stock"""
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
                SELECT 
                    *
                FROM
                    Web_3dprints.orders__items
                WHERE 1=1
                    AND idorders = %s;
            """
            cursor.execute(sql, order_id)
            items = cursor.fetchall()
            for item in items:
                tile = ft.ListTile(
                    bgcolor_activated=ft.colors.AMBER_ACCENT,
                    leading=ft.Image(
                        src=f"https://images.kumpeapps.com/filament?sku={item['sku']}"
                    ),
                    title=ft.Text(item["sku"]),
                    subtitle=ft.Text(
                        f"{item['title']}\nOrdered: {item['qty']}, Filled: {item['qty_filled']}"
                    ),
                    is_three_line=True,
                    # on_click=lambda orderid: tile_clicked(idorders), # pylint: disable=cell-var-from-loop
                )
                tiles.append(tile)
            page.update()
        except (KeyError, TypeError):
            beep.error(page)
            show_banner_click("Unknown Error")

    get_items()

    list_view = ft.Row(wrap=True, scroll="always", expand=True, controls=tiles)

    return ft.View(
        route="/add_roll",
        controls=[top_row, progress_ring, list_view],
        drawer=view.drawer,
    )
