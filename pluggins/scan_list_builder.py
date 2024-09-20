"""Kumpe3D Scan List Builder"""

import pymysql
import pymysql.cursors


def convert_to_list(string: str, delimiter: str) -> list:
    """Convert to List"""
    return list(string.split(delimiter))


def get_scan_translations(cursor: pymysql.cursors.DictCursor) -> list:
    """Get Scan translations List"""
    cursor.execute(
        "SELECT * FROM Web_3dprints.product_scan_translations;"
    )
    translations = cursor.fetchall()
    return translations


def build_k3d_item_dict(
    string: str, translation_type: str = None, cursor: pymysql.cursors.DictCursor = None
) -> list:
    """Build Kumpe3D Item Dict"""
    k3d_dict_list = []
    if translation_type and cursor:
        translations = get_scan_translations(cursor)
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
            qr_id = item_list[2]
        except IndexError:
            qr_id = None
        item_dict = {"qty": qty, "sku": sku, "qr_id": qr_id}
        k3d_dict_list.append(item_dict)
    return k3d_dict_list
