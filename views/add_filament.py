"""Add to Stock"""

import pymysql
import flet as ft  # type: ignore
import flet_easy as fs  # type: ignore
from core.params import Params as params
from core.params import logger
import sounds.beep as beep

add_filament = fs.AddPagesy()


@add_filament.page(route="/add_filament", protected_route=True)
def add_filament_page(data: fs.Datasy):
    """Add new filament"""
    logger.trace("add_filament_page")
    page = data.page
    view = data.view
    pr = ft.ProgressRing(width=16, height=16, stroke_width=2, visible=False)

    page.title = "Add New Filament"
    if params.SQL.username == "":
        params.SQL.get_values()
    sql_params = params.SQL

    def show_drawer(_):
        view.drawer.open = True
        page.update()

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

    def add_filament_to_database(_):
        updating()
        db = pymysql.connect(
            db=sql_params.database,
            user=sql_params.username,
            passwd=sql_params.password,
            host=sql_params.server,
            port=3306,
        )
        cursor = db.cursor(pymysql.cursors.DictCursor)

        filament_sql = """
            INSERT INTO `Web_3dprints`.`filament`
            (`swatch_id`,
            `sku`,
            `name`,
            `type`,
            `color_name`,
            `brand`,
            `cost_per_g`,
            `manufacture_barcode`,
            `instock`,
            `coming_soon`)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, 1, 0);
        """

        filament_values = (
            color_id.value,
            f"{manufacture_abbv.value}-FIL-{color_id.value[0]}1K-{color_id.value}",
            filament_name.value,
            filament_type.value,
            color_name.value,
            manufacture.value,
            cost_per_g.value,
            barcode.value,
        )

        product_sql = """
            INSERT INTO `Web_3dprints`.`products`
            (`base_sku`,
            `sku`,
            `short_sku`,
            `title`,
            `description`,
            `price`,
            `filament_usage`,
            `default_photo`)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s);
        """

        product_values = (
            f"{manufacture_abbv.value}-FIL-{color_id.value[0]}1K",
            f"{manufacture_abbv.value}-FIL-{color_id.value[0]}1K-{color_id.value}",
            "",
            f"{color_name.value} {filament_type.value}",
            f"{color_name.value} {filament_type.value}",
            0,
            0,
            image.value,
        )

        product_values_part = (
            f"{manufacture_abbv.value}-FIL-PRT",
            f"{manufacture_abbv.value}-FIL-PRT-{color_id.value}",
            "",
            f"{color_name.value} {filament_type.value} Partial Roll",
            f"{color_name.value} {filament_type.value} Partial Roll",
            0,
            0,
            image.value,
        )

        scan_translation_sql = """
            INSERT INTO `Web_3dprints`.`product_scan_translations`
            (`scanned`,
            `to_stock_translation`,
            `to_order_translation`,
            `company_use_translation`,
            `defective_translation`,
            `empty_translation`,
            `company_use_method`,
            `recieving_translation`)
            VALUES
            (%s, %s, %s, %s, null, null, %s, %s);
        """

        scan_translation_values = (
            barcode.value,
            f"1;;{manufacture_abbv.value}-FIL-{color_id.value[0]}1K-{color_id.value}",
            f"1;;{manufacture_abbv.value}-FIL-{color_id.value[0]}1K-{color_id.value}",
            f"1;;{manufacture_abbv.value}-FIL-{color_id.value[0]}1K-{color_id.value}|-1;;{manufacture_abbv.value}-FIL-PRT-{color_id.value}",
            "order",
            f"1;;{manufacture_abbv.value}-FIL-{color_id.value[0]}1K-{color_id.value}",
        )

        scan_translation_values_sku = (
            f"{manufacture_abbv.value}-FIL-{color_id.value[0]}1K-{color_id.value}",
            f"1;;{manufacture_abbv.value}-FIL-{color_id.value[0]}1K-{color_id.value}",
            f"1;;{manufacture_abbv.value}-FIL-{color_id.value[0]}1K-{color_id.value}",
            f"1;;{manufacture_abbv.value}-FIL-{color_id.value[0]}1K-{color_id.value}|-1;;{manufacture_abbv.value}-FIL-PRT-{color_id.value}",
            "order",
            f"1;;{manufacture_abbv.value}-FIL-{color_id.value[0]}1K-{color_id.value}",
        )

        try:
            cursor.execute(filament_sql, filament_values)
            cursor.execute(product_sql, product_values)
            cursor.execute(product_sql, product_values_part)
            cursor.execute(scan_translation_sql, scan_translation_values)
            cursor.execute(scan_translation_sql, scan_translation_values_sku)
        except (KeyError, pymysql.IntegrityError):
            beep.error(page)
            show_banner_click("Error")
            updating(False)
        else:
            db.commit()
            updating(False)
            beep.success(page)
        finally:
            cursor.close()
            db.close()

    text = ft.Container(
        content=ft.Text("Generate new Filament", text_align=ft.TextAlign.CENTER),
        alignment=ft.alignment.center,
    )
    manufacture = ft.TextField(
        label="manufacture",
        autofocus=True,
        autocorrect=False,
        enable_suggestions=False,
        on_submit=None,
        text_align=ft.TextAlign.CENTER,
    )
    manufacture_abbv = ft.TextField(
        label="manufacture_abbv",
        autofocus=True,
        autocorrect=False,
        enable_suggestions=False,
        on_submit=None,
        max_length=3,
        text_align=ft.TextAlign.CENTER,
    )
    filament_type = ft.TextField(
        label="filament type",
        autofocus=True,
        autocorrect=False,
        enable_suggestions=False,
        on_submit=None,
        text_align=ft.TextAlign.CENTER,
    )
    color_name = ft.TextField(
        label="color name",
        autofocus=True,
        autocorrect=False,
        enable_suggestions=False,
        on_submit=None,
        text_align=ft.TextAlign.CENTER,
    )
    filament_name = ft.TextField(
        label="filament name",
        autofocus=True,
        autocorrect=False,
        enable_suggestions=False,
        on_submit=None,
        text_align=ft.TextAlign.CENTER,
    )
    color_id = ft.TextField(
        label="color id",
        autofocus=True,
        autocorrect=False,
        enable_suggestions=False,
        on_submit=None,
        max_length=3,
        text_align=ft.TextAlign.CENTER,
    )
    cost_per_g = ft.TextField(
        label="cost per g",
        autofocus=True,
        autocorrect=False,
        enable_suggestions=False,
        on_submit=None,
        text_align=ft.TextAlign.CENTER,
    )
    image = ft.TextField(
        label="image url",
        autofocus=True,
        autocorrect=False,
        enable_suggestions=False,
        on_submit=None,
        text_align=ft.TextAlign.CENTER,
    )
    barcode = ft.TextField(
        label="manufacture barcode",
        autofocus=True,
        autocorrect=False,
        enable_suggestions=False,
        prefix_icon=ft.icons.BARCODE_READER,
        on_submit=add_filament_to_database,
        text_align=ft.TextAlign.CENTER,
    )
    submit_container = ft.Container(
        content=ft.ElevatedButton(text="Submit", on_click=add_filament),
        alignment=ft.alignment.center,
    )

    menu_button = ft.Container(
        content=ft.IconButton(icon=ft.icons.MENU, on_click=show_drawer),
        alignment=ft.alignment.top_left,
        disabled=False,
    )

    progress_ring = ft.Container(
        content=pr,
        alignment=ft.alignment.center,
    )

    def updating(updating: bool = True):
        barcode.disabled = updating
        submit_container.disabled = updating
        progress_ring.visible = updating
        if not updating:
            barcode.value = ""
        page.update()
        barcode.focus()

    return ft.View(
        route="/add_filament5",
        controls=[
            ft.SafeArea(menu_button, bottom=False),
            text,
            manufacture,
            manufacture_abbv,
            filament_type,
            color_name,
            filament_name,
            color_id,
            cost_per_g,
            image,
            barcode,
            submit_container,
            progress_ring,
        ],
        drawer=view.drawer,
    )
