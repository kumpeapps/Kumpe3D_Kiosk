"""Print Product Labels"""

import pymysql
import flet as ft  # type: ignore
import flet_easy as fs  # type: ignore
from core.params import Params as params
import sounds.beep as beep
import pluggins.scan_list_builder as slb

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

    show_banner_click(page.session.get("username"))
    def print_clicked(_):
        progress_ring.visible = True
        print_button.disabled = True
        page.update()
        qr_data = items_list
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
        items = slb.build_k3d_item_dict(qr_data, "to_order_translation", cursor)
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
                0,
                %s);
        """
        cursor.execute(sql, (sku, qr_data, label_type, qty))
        db.commit()
        cursor.close()
        db.close()
        show_banner_click(
            "Print Job Sent. May take a couple of min to print",
            ft.colors.GREEN_200,
            ft.icons.CHECK_BOX_ROUNDED,
            ft.colors.GREEN_900,
        )
        beep.success(page)
        get_items()

    def clear_clicked(_):

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
        cursor.execute(sql, page.session.get("username"))
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
        scanned_list = slb.build_k3d_item_dict(
            scan_field.value, "to_order_translation", cursor
        )
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
                page.session.get("username"),
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
    tiles: list = []

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

    def assign_upc(item: dict) -> bool:
        if item["L3"] == "K3D":
            try:
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

                sku = item["sku"]
                short_sku_base = item["short_sku"]
                short_sku = short_sku_base.replace("000", item["R3"])
                psd_sku = f"K3D {short_sku.replace('-','')}"
                upc_sql = """
                        SELECT 
                            upc,
                            ean
                        FROM
                            Web_3dprints.upc_codes
                        WHERE
                            sku IS NULL
                        LIMIT 1;
                """
                cursor.execute(upc_sql)
                upc_data = cursor.fetchone()
                upc = upc_data["upc"]  # type: ignore
                assign_upc_sql = """
                    UPDATE Web_3dprints.upc_codes
                    SET
                        sku = %s,
                        short_sku = %s,
                        psd_sku = %s
                    WHERE 1=1
                        AND upc = %s;
                """
                cursor.execute(assign_upc_sql, (sku, short_sku, psd_sku, upc))
                db.commit()
                db.close()
                return True
            except:  # pylint: disable=bare-except
                return False
        else:
            return False

    def get_items():
        """Populates existing items for label"""
        progress_ring.visible = True
        tiles.clear()
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
                    products.title AS `title`,
                    `label`.`sku` AS `sku`,
                    left(`label`.`sku`, 3) AS 'L3',
                    right(`label`.`sku`, 3) AS 'R3',
                    `label`.`qty` AS `qty`,
                    `label`.`username` AS `username`,
                    `products`.`short_sku` AS `short_sku`,
                    IFNULL(`upc`.`upc`, '') AS `upc`,
                    CASE
                        WHEN `upc`.`upc` IS NULL THEN 0
                        ELSE 1
                    END AS `has_upc`
                FROM
                    ((`temp__build_label` `label`
                    LEFT JOIN `upc_codes` `upc` ON (`upc`.`sku` = `label`.`sku`))
                    LEFT JOIN products ON products.sku = label.sku OR products.sku = concat(left(label.sku,12),'000'))
                WHERE 1=1
                    AND username = %s
                ORDER BY idtemp__build_label;
            """
            cursor.execute(sql, (page.session.get("username")))
            items = cursor.fetchall()
            global items_list  # pylint: disable=global-statement
            items_list = ""
            for item in items:
                has_upc = bool(item["has_upc"])
                if not has_upc:
                    has_upc = assign_upc(item)
                if has_upc:
                    integrity_icon = ft.Icon(
                        name=ft.icons.CHECK_CIRCLE_ROUNDED, color=ft.colors.GREEN_300
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
