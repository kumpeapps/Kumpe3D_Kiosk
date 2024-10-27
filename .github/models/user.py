"""User Model"""

class User:
    """User Class"""
    def __init__(self, username: str, password: str):
        """User

        Args:
            username (str): User's Username
            password (str): User's Password
        """        
        self.username = username
        self.password = password
        self.user_id: int
        self.email: str = ""
        self.name: str = ""
    def __setattr__(self, name, value):
         pass
    
    class Access:
            """Access Permissions"""

            basic = False
            admin = False
            order_filler = False
            cashier = False
            production = False