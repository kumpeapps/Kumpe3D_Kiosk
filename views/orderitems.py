"""Order Items"""

import flet as ft  # type: ignore
import flet_easy as fs  # type: ignore
from core.params import logger
import sounds.beep as beep
import pluggins.scan_list_builder as slb
from models.order import Order
from api.get import get_order
from api.put import update_order_item

orderitems = fs.AddPagesy()
COMPANY_USE_ORDER = "240"
DEFECTIVE_ORDER = "241"


@orderitems.page(route="/orders/pending/order_items/{order_id}", protected_route=True)
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
        if order_id == COMPANY_USE_ORDER:
            translation = "company_use_translation"
        elif order_id == DEFECTIVE_ORDER:
            translation = "defective_translation"
        else:
            translation = "to_order_translation"
        logger.debug(f"Translation: {translation}")
        scanned_list = slb.build_k3d_item_dict(scan_field.value, translation, page)

        for item in scanned_list:
            sku = item["sku"]
            qty = item["qty"]
            user = page.session.get("username")
            try:
                update_order_item(page, sku, order_id, qty, user)
                beep.success(page)
            except:  # pylint: disable=bare-except
                show_banner_click(f"Invalid SKU: {sku}")
                beep.error(page)
                break
        scan_field.value = ""
        tiles.clear()
        get_items()
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
                ft.Text(order_id, size=10, weight=ft.FontWeight.BOLD),
            ],
            spacing=60,
        ),
        bottom=False,
    )
    tiles = []

    def get_items():
        """Populates Order Items"""

        try:
            order: Order = get_order(page, order_id).data  # type: ignore
            items = order.items
            for item in items:
                tile = ft.ListTile(
                    bgcolor_activated=ft.colors.AMBER_ACCENT,
                    leading=ft.Image(
                        src=f"https://images.kumpeapps.com/filament?sku={item.sku}"
                    ),
                    title=ft.Text(item.sku),
                    subtitle=ft.Text(
                        f"{item.title}\nOrdered: {item.qty}, Filled: {item.qty_filled}"
                    ),
                    is_three_line=True,
                    # on_click=lambda orderid: tile_clicked(idorders), # pylint: disable=cell-var-from-loop
                )
                tiles.append(tile)
            page.update()
        except (KeyError, TypeError) as error:
            logger.error(error)
            beep.error(page)
            show_banner_click("Unknown Error")

    get_items()

    list_view = ft.Row(wrap=True, scroll="always", expand=True, controls=tiles)

    return ft.View(
        route="/order",
        controls=[top_row, progress_ring, list_view],
        drawer=view.drawer,
    )
