"""Kumpe3D Scan List Builder"""

import flet as ft # type: ignore
import api.get
from models.scan_translation import ScanTranslations

def convert_to_list(string: str, delimiter: str) -> list:
    """Convert to List"""
    return list(string.split(delimiter))


def get_scan_translations(page: ft.Page) -> ScanTranslations:
    """Get Scan translations List"""
    translations: ScanTranslations = api.get.get_scan_translations(page).data
    return translations


def build_k3d_item_dict(
    string: str,
    translation_type: str = None,  # type: ignore
    page: ft.Page = None,  # type: ignore
) -> list:
    """Build Kumpe3D Item Dict"""
    k3d_dict_list = []
    if translation_type and page:
        translations = get_scan_translations(page)
        for translation in translations:
            if translation["scanned"] == string and translation[translation_type]:
                string = translation[translation_type]
    k3d_list = convert_to_list(string, "|")
    for item in k3d_list:
        item_list = convert_to_list(item, ";;")
        try:
            qty = int(item_list[0])
            sku = str(item_list[1])
        except (IndexError, ValueError):
            qty = 1
            sku = str(item_list[0])
        try:
            width = item_list[4]
        except IndexError:
            width = None
        try:
            length = item_list[5]
        except IndexError:
            length = None
        try:
            height = item_list[6]
        except IndexError:
            height = None
        try:
            lb = item_list[2]
        except IndexError:
            lb = None
        try:
            oz = item_list[3]
        except IndexError:
            oz = None
        try:
            order_id = item_list[7]
        except IndexError:
            order_id = None
        item_dict = {
            "qty": qty,
            "sku": sku,
            "width": width,
            "length": length,
            "height": height,
            "lb": lb,
            "oz": oz,
            "order_id": order_id,
        }
        k3d_dict_list.append(item_dict)
    return k3d_dict_list
