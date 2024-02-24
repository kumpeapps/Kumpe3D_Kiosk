"""Print Product Label"""

import os

try:
    from beepy import beep
except ImportError:
    pass
import flet as ft
import flet_easy as fs
from pyhtml2pdf import converter
import core.params as params

printproductlabel = fs.AddPagesy()


@printproductlabel.page(route="/print_product_label", protected_route=True)
def printproductlabel_page(data: fs.Datasy):
    """Main Function for Add Roll"""
    page = data.page
    view = data.view

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

    def print_product_label(_):
        """Prints Product Label"""
        try:
            generate_label(sku)
            print_label()
            try:
                beep(1)
            except NameError:
                pass
        except KeyError:
            try:
                beep(3)
            except NameError:
                pass
            show_banner_click(f"Invalid SKU {sku.value}")

    text = ft.Container(
        content=ft.Text(
            "Scan/Enter Product SKU to Print Product Label",
            text_align=ft.TextAlign.CENTER,
        ),
        alignment=ft.alignment.center,
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
        content=ft.FilledButton("Menu", on_click=show_drawer),
        alignment=ft.alignment.top_right,
    )

    return ft.View(
        route="/print_product_label",
        controls=[menu_button, text, sku, submit_container],
        drawer=view.drawer,
    )
