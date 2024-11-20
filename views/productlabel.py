"""Print Product Labels"""

import flet as ft  # type: ignore
import flet_easy as fs  # type: ignore
import sounds.beep as beep
import pluggins.scan_list_builder as slb
from models.print_label import K3DPrintLabelItem, K3DPrintLabel
from models.kumpeapi_response import KumpeApiResponse
from core.params import logger
import api.post
import api.get
import api.delete

printproductlabel = fs.AddPagesy()
items_list = ""  # pylint: disable=invalid-name


@printproductlabel.page(route="/print_product_label", protected_route=True)
def printproductlabel_page(data: fs.Datasy):
    """Main Function for Printing Product Labels"""
    page = data.page
    view = data.view
    pr = ft.ProgressRing(width=16, height=16, stroke_width=2, visible=False)

    def show_drawer(_):
        view.drawer.open = True
        page.update()

    page.title = "Print Product Labels"

    def close_banner(_):
        """Close Banner"""
        page.banner.open = False
        page.update()

    def show_banner_click(
        message: str,
        color: ft.colors = ft.colors.RED_400,
        icon: ft.icons = ft.icons.ERROR_ROUNDED,
        icon_color: ft.colors = ft.colors.RED_900,
    ):
        """Show Banner"""
        page.banner = ft.Banner(
            bgcolor=color,
            leading=ft.Icon(icon, color=icon_color, size=40),
            content=ft.Text(message),
            actions=[
                ft.TextButton("Dismiss", on_click=close_banner),
            ],
        )
        page.banner.open = True
        page.update()

    def print_clicked(_):
        progress_ring.visible = True
        print_button.disabled = True
        page.update()
        qr_data = items_list
        items = slb.build_k3d_item_dict(qr_data, "to_order_translation", page)
        sku = items[0]["sku"]
        if shelf_label_check.value:
            add_label_to_printq(sku, sku, "product_label")
        if product_label_check.value:
            add_label_to_printq(sku, qr_data, "square_product_label")
        if case_label_check.value:
            add_label_to_printq(sku, qr_data, "case_label")
        if wide_barcode_label_check.value:
            add_label_to_printq(sku, sku, "wide_barcode_label")

    def add_label_to_printq(sku: str, qr_data: str, label_type: str):
        qty = qty_field.value
        label = {
            "sku": sku,
            "qty": qty,
            "label_type": label_type,
            "qr_data": qr_data,
        }
        response = api.post.print_label(page, label)
        if response.success:
            show_banner_click(
                "Print Job Sent. May take a couple of min to print",
                ft.colors.GREEN_200,
                ft.icons.CHECK_BOX_ROUNDED,
                ft.colors.GREEN_900,
            )
            beep.success(page)
        else:
            show_banner_click(response.error_message, ft.colors.RED_200)
            beep.error(page)
        get_items()

    def clear_clicked(_):
        response = api.delete.clear_build_label(page)
        if response.success:
            beep.success(page)
        else:
            show_banner_click(response.error_message, ft.colors.RED_200)
            beep.error(page)
        get_items()

    print_button = ft.IconButton(
        icon=ft.icons.PRINT_ROUNDED,
        icon_color="green500",
        icon_size=50,
        tooltip="Print Label",
        on_click=print_clicked,
        disabled=True,
    )
    clear_button = ft.IconButton(
        icon=ft.icons.DELETE_SWEEP_ROUNDED,
        icon_color="red400",
        icon_size=50,
        tooltip="Clear List",
        on_click=clear_clicked,
        disabled=True,
    )
    button_row = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        controls=[
            print_button,
            clear_button,
        ],
    )

    menu_button = ft.Container(
        content=ft.IconButton(icon=ft.icons.MENU, on_click=show_drawer),
        alignment=ft.alignment.top_left,
    )

    progress_ring = ft.Container(
        content=pr,
        alignment=ft.alignment.center,
    )

    def scanned(_):
        """Add Item to Label"""
        success = True

        scanned_list = slb.build_k3d_item_dict(
            scan_field.value, "to_order_translation", page
        )

        for item in scanned_list:
            sku = item["sku"]
            qty = item["qty"]
            item = K3DPrintLabelItem(
                sku=sku, qty=qty, username=page.session.get("username")
            )
            logger.trace(f"Adding {item} to label")
            try:
                response = api.post.add_label_item(page, item)
                if not response.success:
                    raise ValueError(response.error_message)
            except ValueError as error:
                success = False
                show_banner_click(error)
                break
            logger.trace(f"Added {item} to label")
        scan_field.value = ""
        if success:
            beep.success(page)
        else:
            beep.error(page)
        tiles.clear()
        get_items()
        scan_field.focus()

    scan_field = ft.TextField(
        autocorrect=False,
        enable_suggestions=False,
        autofocus=True,
        on_submit=scanned,
        width=page.width / 2,
        height=30,
        capitalization=ft.TextCapitalization.CHARACTERS,
        label="Scan SKU",
        icon=ft.icons.BARCODE_READER,
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
        ),
        bottom=False,
    )
    tiles: list = []
    list_view = ft.Row(wrap=True, scroll="always", expand=True, controls=tiles)

    product_label_check = ft.Checkbox(label="Product Label", value=True)
    wide_barcode_label_check = ft.Checkbox(label="Wide Barcode Label")
    shelf_label_check = ft.Checkbox(label="Shelf Label")
    case_label_check = ft.Checkbox(label="Case Label")

    qty_field = ft.TextField(
        label="Qty",
        width=50,
        value=1,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    options_row = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        wrap=True,
        controls=[
            qty_field,
            product_label_check,
            wide_barcode_label_check,
            shelf_label_check,
            case_label_check,
        ],
    )

    def get_items():
        """Populates existing items for label"""
        logger.trace("Getting items for label")
        progress_ring.visible = True
        tiles.clear()
        get_label: KumpeApiResponse = api.get.get_build_label(page)  # type: ignore
        if get_label.success:
            logger.debug(get_label.data.items)
            items: K3DPrintLabel = get_label.data  # type: ignore
            global items_list  # pylint: disable=global-statement
            items_list = ""
            for item in items.items:
                if items_list == "":
                    items_list = f"{item.qty};;{item.sku}"
                else:
                    items_list = f"{items_list}|{item.qty};;{item.sku}"

                logger.debug(f"https://images.kumpeapps.com/filament?sku={item.sku}")
                tile = ft.ListTile(
                    bgcolor_activated=ft.colors.AMBER_ACCENT,
                    leading=ft.Image(
                        src=f"https://images.kumpeapps.com/filament?sku={item.sku}"
                    ),
                    title=ft.Text(item.title),
                    subtitle=ft.Text(f"{item.sku}\nQty: {item.qty}"),
                    is_three_line=True,
                )
                tiles.append(tile)
            if len(items.items) == 0:
                print_button.disabled = True
                clear_button.disabled = True
            else:
                print_button.disabled = False
                clear_button.disabled = False
            page.update()
            logger.trace("Items for label retrieved")
        else:
            beep.error(page)
            show_banner_click(get_label.error_message)
            print_button.disabled = True
            page.update()
        progress_ring.visible = False
        list_view.controls = tiles
        page.update()

    get_items()

    return ft.View(
        route="/print_product_label",
        controls=[top_row, button_row, options_row, progress_ring, list_view],
        drawer=view.drawer,
    )
