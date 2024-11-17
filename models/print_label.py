"""Kumpe 3D label printer model."""

from typing import Optional


class K3DPrintLabel:  # type: ignore
    """Kumpes 3D label model."""

    def __init__(self, items: list) -> None:
        """
        Initialize a K3DPrintLabel object.

        Args:
            items (list): A list of K3DPrintLabelItem objects.
        """
        self.items: list = []
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
        qty: int,
        username: str,
        id: Optional[int] = None,
        title: Optional[str] = None,
    ) -> None:
        """
        Initialize a K3DPrintLabelItem instance.

        Args:
            id (int): The unique identifier for the label item.
            sku (str): The stock keeping unit for the label item.
            qty (int): The quantity of the label item.
            username (str): The username associated with the label item.
        """
        self.id: Optional[int] = id
        self.sku: str = sku
        self.qty: int = qty
        self.username: str = username
        self.title = title if title else sku

    def to_dict(self):
        """
        Return a dictionary representation of the K3DLabelPrinter instance.

        Returns:
            dict: A dictionary containing the label printer's attributes.
        """
        return {
            "id": self.id,
            "sku": self.sku,
            "qty": self.qty,
            "username": self.username,
            "title": self.title,
        }

    def __str__(self):
        return f"K3DPrintLabelItem({self.sku}, {self.qty}, {self.username})"
