"""Pending Orders"""

import pymysql
import flet as ft
import flet_easy as fs  # pylint: disable=import-error
from core.params import Params as params
import sounds.beep as beep
from functools import partial

pendingorders = fs.AddPagesy()


@pendingorders.page(route="/pending_orders", protected_route=True)
def pendingorders_page(data: fs.Datasy):
    """Main Function for Pending Orders"""
    page = data.page
    view = data.view
    pr = ft.ProgressRing(width=16, height=16, stroke_width=2, visible=False)

    def show_drawer(_):
        view.drawer.open = True
        page.update()

    page.title = "Pending Orders"

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
    tiles = ft.Row(wrap=True, scroll="always", expand=True)
    canvas = [ft.SafeArea(menu_button, bottom=False), progress_ring]

    def tile_clicked(order_id, _):
        page.go(f"/order_items/{order_id}")

    def get_pending_orders():
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
                    idorders,
                    idcustomers,
                    first_name,
                    last_name,
                    company_name,
                    email,
                    street_address,
                    street_address_2,
                    city,
                    state,
                    zip,
                    country,
                    subtotal,
                    taxes,
                    shipping_cost,
                    discount,
                    total,
                    order_date,
                    timestamp,
                    status_id,
                    os.status,
                    payment_method,
                    paypal_transaction_id,
                    paypal_capture_id,
                    notes,
                    sales_channel,
                    referral,
                    state_tax,
                    city_tax,
                    county_tax,
                    taxable_state,
                    taxable_city,
                    taxable_county,
                    client_ip,
                    client_browser,
                    printed
                FROM Web_3dprints.orders orders
                LEFT JOIN Web_3dprints.orders__statuses os ON orders.status_id = os.idorders__statuses
                WHERE 1=1
                    AND status_id < 14
            """
            cursor.execute(sql)
            orders = cursor.fetchall()
            for order in orders:
                idorders = order['idorders']
                tile = ft.CupertinoListTile(
                    additional_info=ft.Text(order["status"]),
                    bgcolor_activated=ft.colors.AMBER_ACCENT,
                    leading=ft.Icon(name=ft.cupertino_icons.SHOPPING_CART),
                    title=ft.Text(
                        f"{order['idorders']}: {order['first_name']} {order['last_name']} ({order['country']})"
                    ),
                    subtitle=ft.Text(f"{order['email']}"),
                    trailing=ft.Icon(name=ft.cupertino_icons.ARROW_RIGHT),
                    on_click=partial(tile_clicked, idorders), # pylint: disable=cell-var-from-loop
                )
                tiles.controls.append(tile)
            page.update()
        except (KeyError, TypeError):
            beep.error(page)
            show_banner_click("Unknown Error")

    get_pending_orders()
    canvas.append(tiles)
    return ft.View(
        route="/add_roll",
        controls=canvas,
        drawer=view.drawer,
    )
