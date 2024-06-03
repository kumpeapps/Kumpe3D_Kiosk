"""Print Product Labels"""

import pymysql
import flet as ft
import flet_easy as fs  # pylint: disable=import-error
from core.params import Params as params
import sounds.beep as beep
import pluggins.scan_list_builder as slb

printproductlabel = fs.AddPagesy()
items_list = ""


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
        print("Print")
        if distributor_dropdown.value is None:
            show_banner_click("Please Select Distributor")
            beep.error(page)
        else:
            progress_ring.visible = True
            print_button.disabled = True
            page.update()
            qr_data = items_list
            items = slb.build_k3d_item_dict(qr_data)
            sku = items[0]["sku"]
            if shelf_label_check.value:
                add_label_to_printq(sku, sku, "product_label")
            if product_label_check.value:
                add_label_to_printq(sku, qr_data, "square_product_label")
            if barcode_label_check.value:
                add_label_to_printq(sku, sku, "barcode_label")

    def add_label_to_printq(sku: str, qr_data: str, label_type: str):
        print("PrintQ")
        distributor_id = distributor_dropdown.value
        qty = qty_field.value
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
            INSERT INTO `Automation_PrintQueue`.`kumpe3d_labels`
                (`sku`,
                `qr_data`,
                `label_type`,
                `distributor_id`,
                `qty`)
            VALUES
                (%s,
                %s,
                %s,
                %s,
                %s);
        """
        cursor.execute(sql, (sku, qr_data, label_type, distributor_id, qty))
        db.commit()
        cursor.close()
        db.close()
        show_banner_click(
            "Print Job Sent. May take a couple of min to print",
            ft.colors.GREEN_200,
            ft.icons.CHECK_BOX_ROUNDED,
            ft.colors.GREEN_900
        )
        beep.success(page)
        get_items()

    def clear_clicked(_):
        print("Clear")
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
            DELETE
            FROM
                Web_3dprints.temp__build_label
            WHERE 1=1
                AND username = %s;
        """
        cursor.execute(sql, page.client_storage.get("username"))
        db.commit()
        cursor.close()
        db.close()
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
        scanned_list = slb.build_k3d_item_dict(scan_field.value)
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
            INSERT INTO Web_3dprints.temp__build_label
            (
                sku,
                qty,
                username
                )
            VALUES
            (
                %s,
                %s,
                %s
            )
            ON DUPLICATE KEY UPDATE qty = qty + %s;
        """
        for item in scanned_list:
            sku = item["sku"]
            qty = item["qty"]
            values = (
                sku,
                qty,
                page.client_storage.get("username"),
                qty,
            )
            try:
                cursor.execute(sql, values)
            except:  # pylint: disable=bare-except
                success = False
                show_banner_click(f"Invalid SKU: {sku}")
                break
        scan_field.value = ""
        if success:
            beep.success(page)
            db.commit()
            db.close()
        else:
            beep.error(page)
            db.close()
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
    tiles = []
    distributor_list = {}

    def get_distributors() -> list:
        """Populates Distributor Dropdown"""

        if params.SQL.username == "":
            params.SQL.get_values()
        sql_params = params.SQL
        db = pymysql.connect(
            db=sql_params.database,
            user=sql_params.username,
            passwd=sql_params.password,
            host=sql_params.ro_server,
            port=3306,
        )
        cursor = db.cursor(pymysql.cursors.DictCursor)
        distributor_options = []

        try:
            sql = """
                SELECT 
                    *
                FROM
                    Web_3dprints.distributors
                WHERE 1=1
                    AND active = 1;
            """
            cursor.execute(sql)
            distributors = cursor.fetchall()
            for distributor in distributors:
                distributor_list[distributor["iddistributors"]] = distributor
                option = ft.dropdown.Option(
                    distributor["iddistributors"], distributor["name"]
                )
                distributor_options.append(option)
            cursor.close()
            db.close()
            return distributor_options
        except (KeyError, TypeError):
            beep.error(page)
            show_banner_click("Unknown Error getting distributor list")
            cursor.close()
            db.close()
            return [ft.dropdown.Option(0, "Kumpe3D")]

    product_label_check = ft.Checkbox(label="Product Label", value=True)
    barcode_label_check = ft.Checkbox(label="Barcode Label")
    shelf_label_check = ft.Checkbox(label="Shelf Label")

    def distributor_dropdown_change(_):
        """Distributor Dropdown onchange"""
        require_barcode = bool(
            distributor_list[int(distributor_dropdown.value)]["requires_upc"]
        )
        barcode_label_check.value = require_barcode
        get_items()

    distributor_dropdown = ft.Dropdown(
        width=200,
        options=get_distributors(),
        label="Distributor",
        on_change=distributor_dropdown_change,
    )

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
            distributor_dropdown,
            product_label_check,
            barcode_label_check,
            shelf_label_check,
        ],
    )

    def get_items():
        """Populates existing items for label"""
        progress_ring.visible = True
        tiles.clear()
        if distributor_dropdown.value is None:
            dist_id = 0
        else:
            dist_id = distributor_dropdown.value
        if params.SQL.username == "":
            params.SQL.get_values()
        sql_params = params.SQL
        db = pymysql.connect(
            db=sql_params.database,
            user=sql_params.username,
            passwd=sql_params.password,
            host=sql_params.ro_server,
            port=3306,
        )
        cursor = db.cursor(pymysql.cursors.DictCursor)

        try:
            sql = """
                SELECT 
                    `label`.`idtemp__build_label` AS `idtemp__build_label`,
                    products.title as `title`,
                    `label`.`sku` AS `sku`,
                    `label`.`qty` AS `qty`,
                    `label`.`username` AS `username`,
                    IFNULL(`upc`.`upc`, '') AS `upc`,
                    IFNULL(`skus`.`dist_sku`, '') AS `dist_sku`,
                    CASE
                        WHEN `upc`.`upc` IS NULL THEN 0
                        ELSE 1
                    END AS `has_upc`,
                    CASE
                        WHEN `skus`.`dist_sku` IS NULL THEN 0
                        ELSE 1
                    END AS `has_dist_sku`
                FROM
                    ((`temp__build_label` `label`
                    LEFT JOIN `upc_codes` `upc` ON (`upc`.`sku` = `label`.`sku`))
                    LEFT JOIN `distributor_skus` `skus` ON (`skus`.`sku` = `label`.`sku`
                        AND `skus`.`iddistributors` = %s)
					left join products on products.sku = label.sku or products.sku = concat(left(label.sku,12),'000'))
                WHERE 1=1
                    AND username = %s
                ORDER BY idtemp__build_label;
            """
            cursor.execute(sql, (dist_id, page.client_storage.get("username")))
            items = cursor.fetchall()
            global items_list  # pylint: disable=global-statement
            items_list = ""
            for item in items:
                has_upc = bool(item["has_upc"])
                has_dist_sku = bool(item["has_dist_sku"])
                if has_upc and has_dist_sku:
                    integrity_icon = ft.Icon(
                        name=ft.icons.CHECK_CIRCLE_ROUNDED, color=ft.colors.GREEN_300
                    )
                elif has_upc:
                    integrity_icon = ft.Icon(
                        name=ft.icons.WARNING_ROUNDED, color=ft.colors.AMBER_300
                    )
                else:
                    integrity_icon = ft.Icon(
                        name=ft.icons.ERROR_ROUNDED, color=ft.colors.RED_300
                    )
                if items_list == "":
                    items_list = f"{item['qty']};;{item['sku']}"
                else:
                    items_list = f"{items_list}|{item['qty']};;{item['sku']}"
                tile = ft.ListTile(
                    bgcolor_activated=ft.colors.AMBER_ACCENT,
                    leading=ft.Image(
                        src=f"https://images.kumpeapps.com/filament?sku={item['sku']}"
                    ),
                    title=ft.Text(item["title"]),
                    subtitle=ft.Text(f"{item['sku']}\nQty: {item['qty']}"),
                    is_three_line=True,
                    trailing=integrity_icon,
                    # on_click=lambda orderid: tile_clicked(idorders), # pylint: disable=cell-var-from-loop
                )
                tiles.append(tile)
                print(f"Items Count: {len(items)}")
            if len(items) == 0:
                print_button.disabled = True
                clear_button.disabled = True
            else:
                print_button.disabled = False
                clear_button.disabled = False
            page.update()
        except (KeyError, TypeError):
            beep.error(page)
            show_banner_click("Unknown Error")
            print_button.disabled = True
            page.update()
        cursor.close()
        db.close()
        progress_ring.visible = False

    get_items()

    list_view = ft.Row(wrap=True, scroll="always", expand=True, controls=tiles)

    return ft.View(
        route="/print_product_label",
        controls=[top_row, button_row, options_row, progress_ring, list_view],
        drawer=view.drawer,
    )
