"""Helper Funcs"""
import flet as ft  # type: ignore
import flet_easy as fs  # type: ignore
from flet_toast import flet_toast as toast  # type: ignore
import sounds.beep as beeps

def get_sku_array(sku):
    """Take SKU and seperate it into parts and assign to array"""
    try:
        sku_split = sku.split("-")
        sku_array = {}
        sku_array["design"] = sku_split[0]
        sku_array["product"] = sku_split[1]
        sku_array["options"] = sku_split[2]
        try:
            sku_array["color"] = sku_split[3]
        except IndexError:
            sku_array["color"] = "000"
        sku_array["base_sku"] = "-".join(
            [sku_array["design"], sku_array["product"], sku_array["options"]]
        )
        sku_array["sku"] = "-".join([sku_array["base_sku"], sku_array["color"]])
        sku_array["main_cat"] = sku_array["design"][0]
        sku_array["design_type"] = sku_array["design"][1]
        sku_array["sub_cat"] = sku_array["design"][2]
        sku_array["filament_type"] = sku_array["options"][0]
        sku_array["layer_quality"] = sku_array["options"][1]
        sku_array["size"] = sku_array["options"][2]
        return sku_array
    except IndexError:
        return {"base_sku": sku, "color": "NNN"}

def show_banner_click(
    page: ft.Page,
    message: str,
    toast_type: str = "error",
    beep: bool = True,
    haptic: bool = True,
    position: str = "top_right",
):
    """Show Banner"""
    if toast_type == "success":
        if beep:
            beeps.success(page, haptic)
        toast.sucess(
            page=page,
            message=message,
            position=position,
        )
    elif toast_type == "error":
        if beep:
            beeps.error(page, haptic)
        toast.error(
            page=page,
            message=message,
            position=position,
        )
    else:
        toast.warning(
            page=page,
            message=message,
            position=position,
        )