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


@home.page(route="/.well-known/assetlinks.json", title="Android Links", protected_route=False)
def assetlinks(data: fs.Datasy):
    """Android Asset Links"""
    return [{
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "com.kumpe3d.kiosk",
      "sha256_cert_fingerprints":
      ["98:0D:71:8C:CB:0A:53:82:FC:71:E7:48:3F:C1:3F:0B:9B:4D:1F:58:C7:2D:8E:AD:72:39:E5:84:B4:EF:29:8A"]
    }
  }]