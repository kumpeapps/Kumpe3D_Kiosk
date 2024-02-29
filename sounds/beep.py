"""Beep Functions"""

import flet as ft


def error(page: ft.Page):
    """Play Error Beep"""
    error_file = ft.Audio(
        src="https://github.com/kumpeapps/Kumpe3D_Kiosk/blob/632ea64ec087451cb44447d62c84a153b7edd1fa/sounds/error.wav?raw=true",  # pylint: disable=line-too-long
        autoplay=True,
    )
    page.overlay.append(error_file)


def success(page: ft.Page):
    """Play Success Beep"""
    success_file = ft.Audio(
        src="https://github.com/kumpeapps/Kumpe3D_Kiosk/blob/632ea64ec087451cb44447d62c84a153b7edd1fa/sounds/success.wav?raw=true",  # pylint: disable=line-too-long
        autoplay=True,
    )
    page.overlay.append(success_file)
