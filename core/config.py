"""Core Class"""

import flet as ft
import flet_easy as fs # pylint: disable=import-error
from core.params import Params as params


class ConfigApp:
    """Define Core App"""

    def __init__(self, app: fs.FletEasy):
        """Core init"""
        self.app = app
        self.start()

    def start(self):
        """Core Start"""

        @self.app.view
        def view_config(page: ft.Page):
            def addroll_go(_):
                page.page.session.set("selected_page", "addroll")
                page.go("/add_roll")

            def home_go(_):
                page.page.session.set("selected_page", "home")
                page.go("/login")

            def logout(_):
                params.Access.set_access_level("unauthenticated")
                page.page.client_storage.clear()
                page.page.session.set("selected_page", "home")
                page.go("/login")

            def addstock_go(_):
                page.page.session.set("selected_page", "addstock")
                page.go("/add_stock")

            def openroll_go(_):
                page.page.session.set("selected_page", "openroll")
                page.go("/open_roll")

            def emptyroll_go(_):
                page.page.session.set("selected_page", "emptyroll")
                page.go("/empty_roll")

            def productionq_go(_):
                page.page.session.set("selected_page", "productionq")
                page.go("/production_queue")

            # def addstockandprint_go(_):
            #     page.go("/add_stock_and_print_label")

            def productlabel_go(_):
                page.page.session.set("selected_page", "productlabel")
                page.go("/print_product_label")

            def pendingorders_go(_):
                page.page.session.set("selected_page", "pendingorders")
                page.go("/pending_orders")

            # def filamentcolorscard_go(_):
            #     page.go("/print_filament_colors_card")

            return fs.Viewsy(
                drawer=ft.NavigationDrawer(
                    controls=[
                        ft.Container(height=12),
                        ft.Column(
                            controls=[
                                ft.Text("Navigation", size=25),
                                ft.Divider(thickness=2),
                                ft.FilledButton(
                                    text="Home",
                                    on_click=home_go,
                                ),
                                ft.FilledButton(
                                    text="Add to Stock",
                                    on_click=addstock_go,
                                ),
                                ft.FilledButton(
                                    text="Add Filament Roll",
                                    on_click=addroll_go,
                                ),
                                ft.FilledButton(
                                    text="Open Filament Roll",
                                    on_click=openroll_go,
                                ),
                                ft.FilledButton(
                                    text="Empty Filament Roll",
                                    on_click=emptyroll_go,
                                ),
                                ft.FilledButton(
                                    text="Production Queue",
                                    on_click=productionq_go,
                                ),
                                ft.FilledButton(
                                    text="Print Product Label",
                                    on_click=productlabel_go,
                                ),
                                ft.FilledButton(
                                    text="Pending Orders",
                                    on_click=pendingorders_go
                                ),
                                ft.FilledButton(
                                    text="Logout",
                                    on_click=logout,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                )
            )

        @self.app.config
        def page_config(page: ft.Page):
            theme = ft.Theme()
            platforms = ["android", "ios", "macos", "linux", "windows"]
            for platform in platforms:  # Removing animation on route change.
                setattr(theme.page_transitions, platform, ft.PageTransitionTheme.CUPERTINO)
            page.theme = theme
