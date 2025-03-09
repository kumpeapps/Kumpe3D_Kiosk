"""Pending Orders"""

from functools import partial
import flet as ft  # type: ignore
import flet_easy as fs  # type: ignore
import sounds.beep as beep
from api.get import get_pending_orders as get_orders
from models.order import Orders
from core.params import logger


pendingorders = fs.AddPagesy()


@pendingorders.page(route="/orders/pending", protected_route=True)
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
        icon: ft.icons = ft.Icons.ERROR_ROUNDED,
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
        content=ft.IconButton(icon=ft.Icons.MENU, on_click=show_drawer),
        alignment=ft.alignment.top_left,
    )

    progress_ring = ft.Container(
        content=pr,
        alignment=ft.alignment.center,
    )
    tiles = ft.Row(wrap=True, scroll="always", expand=True)
    canvas = [ft.SafeArea(menu_button, bottom=False), progress_ring]

    def view_order_clicked(order_id, _):
        page.go(f"/orders/pending/order_items/{order_id}")

    def update_status_clicked(order_id, _):
        page.go(f"/order_status_update/{order_id}")

    def get_pending_orders():
        """Add's Roll to Stock"""

        try:
            orders: Orders = get_orders(page).data # type: ignore
            for order in orders.orders:
                idorders = order["id"]
                tile = ft.CupertinoListTile(
                    additional_info=ft.Text(order["status"]),
                    bgcolor_activated=ft.colors.AMBER_ACCENT,
                    leading=ft.Icon(name=ft.cupertino_icons.SHOPPING_CART),
                    title=ft.Text(
                        f"{order['id']}: {order['company_name']} {order['first_name']} {order['last_name']} ({order['country']})"  # pylint: disable=line-too-long
                    ),
                    subtitle=ft.Text(f"{order['email']}"),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(
                                text="View Order",
                                on_click=partial(view_order_clicked, idorders),
                            ),  # pylint: disable=cell-var-from-loop),
                            ft.PopupMenuItem(
                                text="Change Status",
                                on_click=partial(update_status_clicked, idorders),
                            ),
                        ],
                    ),
                )
                tiles.controls.append(tile)
            page.update()
        except (KeyError, TypeError) as error:
            logger.error(error)
            beep.error(page)
            show_banner_click("Unknown Error")

    get_pending_orders()
    canvas.append(tiles)
    return ft.View(
        route="/add_roll",
        controls=canvas,
        drawer=view.drawer,
    )
