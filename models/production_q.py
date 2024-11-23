"""Production Q model."""

import flet as ft  # type: ignore


class ProductionQItem:
    """Represents an item in the production queue."""

    def __init__(
        self,
        sku: str = "",
        swatch_id: str = "",
        name: str = "",
        qty: int = 0,
        priority: int = 0,
        title: str = "",
        **_,
    ) -> None:
        """
        Initialize a new ProductionQItem.

        Args:
            sku (str): The SKU of the item.
            swatch_id (str): The swatch ID of the item.
            name (str): The name of the item.
            qty (int): The quantity of the item.
            priority (int): The priority of the item.
            title (str): The title of the item.
        """
        self.sku: str = sku
        self.swatch_id: str = swatch_id
        self.name: str = name
        self.qty: int = qty
        self.priority: int = priority
        self.title: str = title

    def __str__(self) -> str:
        """
        Return a string representation of the ProductionQItem.

        Returns:
            str: A string in the format "sku - title - qty".
        """
        return f"{self.sku} - {self.title} - {self.qty}"

    def __repr__(self) -> str:
        """
        Return a detailed string representation of the ProductionQItem.

        Returns:
            str: A string in the format "ProductionQItem(sku, swatch_id, name, qty, priority, title)".
        """
        return f"ProductionQItem({self.sku}, {self.swatch_id}, {self.name}, {self.qty}, {self.priority}, {self.title})"


class ProductionQ:
    """Represents the production queue."""

    def __init__(self, items: list) -> None:
        """
        Initialize a new ProductionQ.

        Args:
            items (List[ProductionQItem]): The items in the production queue.
        """
        self.items: list = []
        if isinstance(items, list):
            self.items = [ProductionQItem(**item) for item in items]
        elif isinstance(items, ProductionQItem):
            self.items = [items]

    def __str__(self) -> str:
        """
        Return a string representation of the ProductionQ.

        Returns:
            str: A string containing the string representation of each item in the production queue.
        """
        return "\n".join(str(item) for item in self.items)

    def __repr__(self) -> str:
        """
        Return a detailed string representation of the ProductionQ.

        Returns:
            str: A string containing the detailed string representation of each item in the production queue.
        """
        return "\n".join(repr(item) for item in self.items)

    @property
    def data_rows(self) -> list:
        """
        Return a list of data rows for the production queue.

        Returns:
            list: A list of data rows for the production queue.
        """
        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(item.qty)),
                    ft.DataCell(ft.Text(item.sku)),
                    ft.DataCell(ft.Text(item.title)),
                ],
            )
            for item in self.items
        ]
