"""Kumpe3D Scan List Builder"""


def convert_to_list(string: str, delimiter: str) -> list:
    """Convert to List"""
    return list(string.split(delimiter))


def build_k3d_item_dict(string: str) -> list:
    """Build Kumpe3D Item Dict"""
    k3d_dict_list = []
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
