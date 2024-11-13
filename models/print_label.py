"""Kumpe 3D label printer model."""


class K3DPrintLabel:  # type: ignore
    """Kumpes 3D label model."""

    def __init__(self, items: list) -> None:
        """
        Initialize a K3DPrintLabel object.

        Args:
            items (list): A list of K3DPrintLabelItem objects.
        """
        self.items: list
        for item in items:
            if not isinstance(item, K3DPrintLabelItem):
                self.items.append(K3DPrintLabelItem(**item))
            else:
                self.items.append(item)

    def to_dict(self):
        """
        Return a dictionary representation of the K3DPrintLabel instance.

        Returns:
            dict: A dictionary containing the label printer's attributes.
        """
        return {[item.to_dict() for item in self.items]}

    def __str__(self):
        return f"K3DPrintLabel({self.items})"

    def __repr__(self):
        return f"K3DPrintLabel({self.items})"

    def __list__(self):
        return self.items


class K3DPrintLabelItem:  # type: ignore
    """Kumpe 3D label item model."""

    def __init__(
        self,
        sku: str,
        qr_data: str,
        label_type: str,
        qty: int = 1,
        enable_print: bool = True,
    ) -> None:
        """
        Initialize a K3DPrintLabel object.

        Args:
            sku (str): The stock keeping unit for the label.
            qr_data (str): The QR code data for the label.
            label_type (str): The type of the label.
            qty (int, optional): The quantity of labels to print. Defaults to 1.
            enable_print (bool, optional): Flag to enable or disable printing. Defaults to True.
        """

        self.sku: str = sku
        self.qr_data: str = qr_data
        self.label_type: str = label_type
        self.distributor_id: int = 0
        self.qty: int = qty
        self.enable_print: bool = enable_print

    def to_dict(self):
        """
        Return a dictionary representation of the K3DLabelPrinter instance.

        Returns:
            dict: A dictionary containing the label printer's attributes.
        """
        return {
            "sku": self.sku,
            "qr_data": self.qr_data,
            "label_type": self.label_type,
            "distributor_id": self.distributor_id,
            "qty": self.qty,
            "enable_print": self.enable_print,
        }
