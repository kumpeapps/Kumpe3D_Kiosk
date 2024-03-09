"""Print Product Label"""

import os
import flet as ft
import flet_easy as fs # pylint: disable=import-error
import core.params as params
try:
    from pyhtml2pdf import converter
except ImportError:
    pass
import sounds.beep as beep

printproductlabel = fs.AddPagesy()


@printproductlabel.page(route="/print_product_label", protected_route=True)
def printproductlabel_page(data: fs.Datasy):
    """Main Function for Add Roll"""
    page = data.page
    view = data.view
    pr = ft.ProgressRing(width=16, height=16, stroke_width=2, visible=False)

    def show_drawer(_):
        view.drawer.open = True
        page.update()

    page.title = "Print Product Label"

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

    def generate_pdf(url, pdf_path):
        """Generate PDF from URL"""
        print(url)
        converter.convert(
            url,
            pdf_path,
            print_options={
                "marginBotton": 0,
                "marginTop": 0,
                "marginLeft": 0,
                "marginRight": 0,
                "paperHeight": 1.97,
                "paperWidth": 3.15,
            },
        )
        print_label()

    # Run the function
    def generate_label(sku: str):
        """Generate PDF Product Label"""
        generate_pdf(
            "https://www.kumpe3d.com/product_labels.php?sku=" + sku,
            "label.pdf",
        )

    def print_label():
        """Print Product Label PDF to Printer"""
        # Only print in production environment
        if params.app_env == "prod":
            os.system(
                "lp -d Product_Label_Printer -o media=50x80mm -o orientation-requested=4 label.pdf"
            )
        else:
            print(printer_selection.value)
        updating(False)

    def print_product_label(_):
        """Prints Product Label"""
        try:
            print(sku.value)
            updating()
            generate_label(sku.value)
            page.update()
            beep.success(page)
        except KeyError:
            beep.error(page)
            show_banner_click(f"Invalid SKU {sku.value}")
            sku.disabled = False
            submit_container.disabled = False
            page.update()

    def updating(updating: bool = True):
        pr.visible = updating
        sku.disabled = updating
        submit_container.disabled = updating
        if not updating:
            sku.value = ""
        page.update()
        sku.focus()

    text = ft.Container(
        content=ft.Text(
            "Scan/Enter Product SKU to Print Product Label",
            text_align=ft.TextAlign.CENTER,
        ),
        alignment=ft.alignment.center,
    )

    printer_selection = ft.Dropdown(
        label="Label Printer",
        options=[
            ft.dropdown.Option(
                "Product_Label_Printer",
                text="Product Label Printer (50x80mm)",
            ),
            ft.dropdown.Option(
                "Barcode_Label_Printer",
                text="Barcode Label Printer (40x30mm)",
                disabled=True,
            ),
            ft.dropdown.Option(
                "Shipping_Label_Printer",
                text="Shipping Label Printer (4x6in)",
                disabled=True,
            ),
        ],
        value="Product_Label_Printer",
        prefix_icon=ft.icons.PRINT_ROUNDED,
    )

    sku = ft.TextField(
        label="sku",
        autofocus=True,
        autocorrect=False,
        enable_suggestions=False,
        prefix_icon=ft.icons.BARCODE_READER,
        on_submit=print_product_label,
        text_align=ft.TextAlign.CENTER,
    )
    submit_container = ft.Container(
        content=ft.ElevatedButton(text="Submit", on_click=print_product_label),
        alignment=ft.alignment.center,
    )

    menu_button = ft.Container(
        content=ft.IconButton(icon=ft.icons.MENU, on_click=show_drawer),
        alignment=ft.alignment.top_left,
    )

    progress_ring = ft.Container(
        content=pr,
        alignment=ft.alignment.center,
    )

    return ft.View(
        route="/print_product_label",
        controls=[
            menu_button,
            text,
            printer_selection,
            sku,
            submit_container,
            progress_ring,
        ],
        drawer=view.drawer,
    )
