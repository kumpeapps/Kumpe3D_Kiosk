"""User Model"""


class User:
    """User Class"""

    def __init__(self, **kwargs):
        """User

        Args:
            username (str): User's Username
            password (str): User's Password
        """
        if kwargs["login"]:
            self.username = kwargs["login"]
        else:
            self.username = kwargs["username"]
        self.user_id = kwargs.get("user_id", None)
        self.email = kwargs.get("email", "")
        self.name = kwargs.get("name", "")
        self.__access = kwargs.get("subscriptions", [])
        self.Access.basic = "213" in self.__access
        self.Access.admin = "214" in self.__access
        self.Access.order_filler = "215" in self.__access
        self.Access.production = "218" in self.__access

    def __str__(self):
        return self.username

    def __int__(self):
        return self.user_id

    class Access:
        """Access Permissions"""

        basic = False
        admin = False
        order_filler = False
        cashier = False
        production = False
