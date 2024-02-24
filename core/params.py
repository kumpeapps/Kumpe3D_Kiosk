"""Parameters file for Kumpe3D-Python"""

import os
from dotenv import load_dotenv
from infisical_api import infisical_api


load_dotenv()
service_token = os.getenv("SERVICE_TOKEN")
app_env = os.getenv("APP_ENV")
creds = infisical_api(
    service_token=service_token, infisical_url="https://creds.kumpeapps.com"
)


class Params:
    """Parameters"""

    class SHIPPO:
        """Shippo Parameters"""

        base_url = "https://api.goshippo.com"
        api_key = creds.get_secret(  # pylint: disable=no-member
            secret_name="APIKEY", environment="dev", path="/SHIPPO/"
        ).secretValue

    class SQL:
        """SQL Parameters for Web_3d User"""

        username = creds.get_secret(  # pylint: disable=no-member
            secret_name="USERNAME", environment=app_env, path="/MYSQL/"
        ).secretValue
        password = creds.get_secret(  # pylint: disable=no-member
            secret_name="PASSWORD", environment=app_env, path="/MYSQL/"
        ).secretValue
        server = creds.get_secret(  # pylint: disable=no-member
            secret_name="SERVER", environment=app_env, path="/MYSQL/"
        ).secretValue
        port = creds.get_secret(  # pylint: disable=no-member
            secret_name="PORT", environment=app_env, path="/MYSQL/"
        ).secretValue
        database = creds.get_secret(  # pylint: disable=no-member
            secret_name="DATABASE", environment=app_env, path="/MYSQL/"
        ).secretValue

        @staticmethod
        def dict():
            """returns as dictionary"""
            return {
                "username": Params.SQL.username,
                "password": Params.SQL.password,
                "server": Params.SQL.server,
                "port": Params.SQL.port,
                "database": Params.SQL.database,
            }

    class KumpeApps:
        """KumpeApps Params"""

        api_url = creds.get_secret(  # pylint: disable=no-member
            secret_name="KA_API_URL", environment=app_env, path="/KUMPEAPPS/"
        ).secretValue
        api_key = creds.get_secret(  # pylint: disable=no-member
            secret_name="KA_SSO_APIKEY", environment=app_env, path="/KUMPEAPPS/"
        ).secretValue

    class Access:
        """Access Permissions"""

        access_level = "unauthenticated"
        user_id = ""
        username = ""
        email = ""
        name = ""
        basic = False
        production = False
        orders = False
        product_stock = False
        print_labels = False
        filament_stock = False
        admin = False

        @staticmethod
        def refresh():
            """Refresh Permissions"""
            if Params.Access.access_level == "unauthenticated":
                Params.Access.basic = False
                Params.Access.production = False
                Params.Access.orders = False
                Params.Access.product_stock = False
                Params.Access.print_labels = False
                Params.Access.filament_stock = False
                Params.Access.admin = False
                Params.Access.user_id = ""
                Params.Access.username = ""
                Params.Access.name = ""
                Params.Access.email = ""
            elif Params.Access.access_level == "basic":
                Params.Access.basic = True
                Params.Access.production = True
                Params.Access.orders = False
                Params.Access.product_stock = True
                Params.Access.print_labels = True
                Params.Access.filament_stock = True
                Params.Access.admin = False
            elif Params.Access.access_level == "limited":
                Params.Access.basic = True
                Params.Access.production = True
                Params.Access.orders = False
                Params.Access.product_stock = False
                Params.Access.print_labels = False
                Params.Access.filament_stock = True
                Params.Access.admin = False
            elif Params.Access.access_level == "admin":
                Params.Access.basic = True
                Params.Access.production = True
                Params.Access.orders = True
                Params.Access.product_stock = True
                Params.Access.print_labels = True
                Params.Access.filament_stock = True
                Params.Access.admin = True
            elif Params.Access.access_level == "order_filler":
                Params.Access.basic = True
                Params.Access.production = False
                Params.Access.orders = True
                Params.Access.product_stock = True
                Params.Access.print_labels = True
                Params.Access.filament_stock = False
                Params.Access.admin = False

        @staticmethod
        def set_access_level(
            access_level: str,
        ):
            """set access level and refresh"""
            Params.Access.access_level = access_level
            Params.Access.refresh()
