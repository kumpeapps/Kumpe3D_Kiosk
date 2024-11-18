"""Beep Functions"""

import flet as ft  # type: ignore


def error(page: ft.Page, hf: ft.HapticFeedback = None):
    """Play Error Beep"""
    if hf:
        try:
            hf.heavy_impact()
            hf.heavy_impact()
            hf.heavy_impact()
        except AttributeError:
            pass
    error_file = ft.Audio(
        src="/audio/error.wav",  # pylint: disable=line-too-long
        autoplay=True,
    )
    page.overlay.append(error_file)
    page.update()


def success(page: ft.Page, hf: ft.HapticFeedback = None):
    """Play Success Beep"""
    if hf:
        try:
            hf = ft.HapticFeedback()
            page.overlay.append(hf)
            hf.light_impact()
            hf.heavy_impact()
        except AttributeError:
            pass
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
