"""Parameters file for Kumpe3D-Python"""

import os
import sys
from dotenv import load_dotenv
from infisical_api import infisical_api  # type: ignore
import loguru


load_dotenv(override=True)
service_token = os.getenv("SERVICE_TOKEN")
app_env = os.getenv("APP_ENV")
creds = infisical_api(
    service_token=service_token, infisical_url="https://creds.kumpeapps.com"
)
is_mobile = os.getenv("is_mobile")
log_level = os.getenv("LOG_LEVEL", "INFO")
logger = loguru.logger
logger.remove()
logger.add(sys.stderr, level=log_level)

class Params:
    """Parameters"""

    mobile = bool(int(is_mobile))  # type: ignore

    class SHIPPO:
        """Shippo Parameters"""

        base_url = ""
        api_key = ""

        @staticmethod
        def get_values():
            """Get Values"""
            Params.SHIPPO.base_url = "https://api.goshippo.com"
            Params.SHIPPO.api_key = creds.get_secret(  # pylint: disable=no-member
                secret_name="APIKEY", environment="dev", path="/SHIPPO/"
            ).secretValue

    class SQL:
        """SQL Parameters for Web_3d User"""

        username = ""
        password = ""
        server = ""
        port = ""
        database = ""
        ro_server = ""

        @staticmethod
        def get_values():
            """Get Values"""
            Params.SQL.username = creds.get_secret(  # pylint: disable=no-member
                secret_name="USERNAME", environment=app_env, path="/MYSQL/"
            ).secretValue
            Params.SQL.password = creds.get_secret(  # pylint: disable=no-member
                secret_name="PASSWORD", environment=app_env, path="/MYSQL/"
            ).secretValue
            Params.SQL.server = creds.get_secret(  # pylint: disable=no-member
                secret_name="SERVER", environment=app_env, path="/MYSQL/"
            ).secretValue
            Params.SQL.port = creds.get_secret(  # pylint: disable=no-member
                secret_name="PORT", environment=app_env, path="/MYSQL/"
            ).secretValue
            Params.SQL.database = creds.get_secret(  # pylint: disable=no-member
                secret_name="DATABASE", environment=app_env, path="/MYSQL/"
            ).secretValue
            Params.SQL.ro_server = creds.get_secret(  # pylint: disable=no-member
                secret_name="RO_SERVER", environment=app_env, path="/MYSQL/"
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

        api_url = ""
        api_key = ""

        @staticmethod
        def get_values():
            """Get Values"""
            Params.KumpeApps.api_url = creds.get_secret(  # pylint: disable=no-member
                secret_name="KA_API_URL", environment=app_env, path="/KUMPEAPPS/"
            ).secretValue
            Params.KumpeApps.api_key = creds.get_secret(  # pylint: disable=no-member
                secret_name="KA_SSO_APIKEY", environment=app_env, path="/KUMPEAPPS/"
            ).secretValue
