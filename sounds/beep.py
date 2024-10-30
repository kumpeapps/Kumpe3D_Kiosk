"""Beep Functions"""

import flet as ft  # type: ignore

hf = ft.HapticFeedback()

def error(page: ft.Page):
    """Play Error Beep"""
    hf.heavy_impact()
    error_file = ft.Audio(
        src="/audio/error.wav",  # pylint: disable=line-too-long
        autoplay=True,
    )
    page.overlay.append(error_file)
    page.update()


def success(page: ft.Page):
    """Play Success Beep"""
    page.overlay.append(hf)
    hf.light_impact()
    success_file = ft.Audio(
        src="/audio/success.wav",  # pylint: disable=line-too-long
        autoplay=True,
    )
    page.overlay.append(success_file)
    page.update()


def login(page: ft.Page):
    """Play Success Beep"""
    success_file = ft.Audio(
        src="/audio/login.aiff",  # pylint: disable=line-too-long
        autoplay=True,
    )
    page.overlay.append(success_file)
    page.update()
