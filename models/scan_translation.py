"""Scan Translation Model"""

from typing import Optional


class ScanTranslation:
    """Scan Translation Class"""

    def __init__(self, **kwargs) -> None:
        """
        Initialize a Scan Translation object.

        Args:
            **kwargs: Arbitrary keyword arguments for scan translation attributes.
        """
        if kwargs.get("scanned", "") == "":
            raise ValueError("Scanned value is required.")
        self.scanned: str = kwargs.get("scanned", "")
        self.to_stock_translation: Optional[str] = kwargs.get(
            "to_stock_translation", None
        )
        self.to_order_translation: Optional[str] = kwargs.get(
            "to_order_translation", None
        )
        self.company_use_translation: Optional[str] = kwargs.get(
            "company_use_translation", None
        )
        self.defective_translation: Optional[str] = kwargs.get(
            "defective_translation", None
        )
        self.empty_translation: Optional[str] = kwargs.get("empty_translation", None)
        self.company_use_method: str = kwargs.get("company_use_method", "order")
        self.recieving_translation: Optional[str] = kwargs.get(
            "recieving_translation", None
        )

    def __str__(self) -> str:
        """
        Get the scanned value of the scan translation.

        Returns:
            str: Scanned value of the scan translation.
        """
        return self.scanned

    def to_dict(self) -> dict:
        """
        Return a dictionary representation of the ScanTranslation instance.

        Returns:
            dict: A dictionary containing the scan translation's attributes.
        """
        return {
            "scanned": self.scanned,
            "to_stock_translation": self.to_stock_translation,
            "to_order_translation": self.to_order_translation,
            "company_use_translation": self.company_use_translation,
            "defective_translation": self.defective_translation,
            "empty_translation": self.empty_translation,
            "company_use_method": self.company_use_method,
            "recieving_translation": self.recieving_translation,
        }


class ScanTranslations:
    """Scan Translations Class"""

    def __init__(self, translations: list) -> None:
        """
        Initialize a Scan Translations object.

        Args:
            translations (list): A list of ScanTranslation objects.
        """
        self.translations: list = []
        for translation in translations:
            if not isinstance(translation, ScanTranslation):
                self.translations.append(ScanTranslation(**translation))
            else:
                self.translations.append(translation)

    def to_dict(self) -> list:
        """
        Return a dictionary representation of the ScanTranslations instance.

        Returns:
            dict: A dictionary containing the scan translations' attributes.
        """
        return [translation.to_dict() for translation in self.translations]

    def __list__(self) -> list:
        return self.translations

    def __iter__(self):
        return iter([translation.to_dict() for translation in self.translations])
