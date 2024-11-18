"""Server Monitor"""

import socket
from core.params import app_env

def rw_sql() -> bool:
    """Is mySQL port open for rw.sql.pvt.kumpedns.us

    Returns:
        bool: Server Is Up
    """
    if app_env == "dev":
        return True
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("rw.sql.pvt.kumpedns.us", 3306))
    sock.close()
    return result == 0
