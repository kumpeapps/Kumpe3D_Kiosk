"""Home/Login Page"""

import flet as ft  # type: ignore
import flet_easy as fs  # type: ignore
import assets.logo as logo  # pylint: disable=import-error

home = fs.AddPagesy()


@home.page(route="/home", title="Home", protected_route=True)
def home_page(data: fs.Datasy):
    """Login Page"""
    page = data.page
    view = data.view
    print(page.padding)

    def show_drawer(_):
        view.drawer.open = True
        page.update()

    img_container = ft.Container(
        content=ft.Image(src_base64=logo.logo_base64, height=page.height / 5),
        alignment=ft.alignment.top_center,
    )

    menu_button = ft.Container(
        content=ft.IconButton(icon=ft.icons.MENU, on_click=show_drawer),
        alignment=ft.alignment.top_left,
        disabled=False,
    )

    return ft.View(
        controls=[
            ft.SafeArea(menu_button, bottom=False),
            img_container,
        ],
        drawer=view.drawer,
    )

@home.page(route="/json", title="JSON Response", protected_route=False)
def json_page(data: fs.Datasy):
    """JSON Response Page"""
    page = data.page

    def return_json(_):
        page.response = ft.Response(
            status_code=200,
            headers={"Content-Type": "application/json"},
            body='{"message": "Hello, World!"}'
        )
        page.update()

    return_json(None)

# Run the app
if __name__ == "__main__":
    home.run()
