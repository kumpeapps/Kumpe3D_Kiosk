"""Beep Functions"""

import flet as ft  # type: ignore
from flet_audio import Audio  # type: ignore


def error(page: ft.Page, hf: ft.HapticFeedback = None):
    """Play Error Beep"""
    if hf:
        try:
            hf.heavy_impact()
            page.update()
            hf.heavy_impact()
            page.update()
            hf.heavy_impact()
            page.update()
        except AttributeError:
            pass
    error_file = Audio(
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
            page.update()
            hf.heavy_impact()
            page.update()
        except AttributeError:
            pass
    success_file = Audio(
        src="/audio/success.wav",  # pylint: disable=line-too-long
        autoplay=True,
    )
    page.overlay.append(success_file)
    page.update()


def login(page: ft.Page):
    """Play Success Beep"""
    success_file = Audio(
        src="/audio/login.aiff",  # pylint: disable=line-too-long
        autoplay=True,
    )
    page.overlay.append(success_file)
    page.update()
