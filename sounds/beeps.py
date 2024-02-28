import flet as ft


def play_error(page: ft.Page):
    error_file = ft.Audio(src="error.wav")
    page.overlay.append(error_file)
    error_file.play()

def play_success(page: ft.Page):
    success_file = ft.Audio(src="success.wav")
    page.overlay.append(success_file)
    success_file.play()
