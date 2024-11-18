"""User Model"""

from typing import List, Dict, Any


class User:
    """User Class"""

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize a User object.

        Args:
            **kwargs: Arbitrary keyword arguments for user attributes.
        """
        self.username: str = kwargs.get("username", "")
        self.user_id: int = kwargs.get("id", None)
        self.email: str = kwargs.get("email", "")
        self.first_name: str = kwargs.get("first_name", "")
        self.last_name: str = kwargs.get("last_name", "")
        self.company: str = kwargs.get("company_name", "")
        self.is_locked: bool = kwargs.get("is_locked", False)
        self.master_id: int = kwargs.get("master_id", 0)
        self.phone: str = kwargs.get("phone", "")
        self.status: int = kwargs.get("status", 1)
        self.street_address: Dict[str, str] = {
            "street": kwargs.get("street", ""),
            "street2": kwargs.get("street2", ""),
            "city": kwargs.get("city", ""),
            "state": kwargs.get("state", ""),
            "zip": kwargs.get("zip", ""),
            "country": kwargs.get("country", ""),
        }
        self.__access: List[int] = kwargs.get("access_list", [])
        self.Access.basic = 213 in self.__access
        self.Access.admin = 214 in self.__access
        self.Access.order_filler = 215 in self.__access
        self.Access.production = 218 in self.__access

    @property
    def name(self) -> str:
        """
        Get the full name of the user.

        Returns:
            str: Full name of the user.
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        """
        Get the username of the user.

        Returns:
            str: Username of the user.
        """
        return self.username

    def __int__(self) -> int:
        """
        Get the user ID.

        Returns:
            int: User ID.
        """
        return self.user_id

    class Access:
        """Access Permissions"""

        basic: bool = False
        admin: bool = False
        order_filler: bool = False
        cashier: bool = False
        production: bool = False
