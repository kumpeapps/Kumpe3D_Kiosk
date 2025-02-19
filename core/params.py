"""Parameters file for Kumpe3D-Python"""

import os
import sys
from dotenv import load_dotenv
import loguru


load_dotenv(override=True)
app_env = os.getenv("APP_ENV", "prod")
is_mobile = os.getenv("is_mobile", "0")
log_level = os.getenv("LOG_LEVEL", "INFO")
logger = loguru.logger
logger.remove()
logger.add(sys.stderr, level=log_level)
logger.add("flet-kumpe3dkiosk.log", retention="2 days")


class Params:
    """Parameters"""

    mobile = bool(int(is_mobile))  # type: ignore

    class SHIPPO:
        """Shippo Parameters"""

        base_url = ""
        api_key = ""

    class SQL:
        """SQL Parameters for Web_3d User"""

        username = "Web_3d"
        password = os.getenv("MYSQL_PASSWORD", "")
        server = "rw.sql.pvt.kumpedns.us"
        port = "3306"
        database = "Web_3dprints"
        ro_server = "ro.sql.pvt.kumpedns.us"

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

        api_url = "https://www.kumpeapps.com/api"
        api_key = os.getenv("KA_SSO_APIKEY", "")

    class API:
        """API Params"""

        url = "https://api.kumpeapps.us"
        client_id = os.getenv("API_CLIENT_ID", "")
        client_secret = os.getenv("API_CLIENT_SECRET", "")
