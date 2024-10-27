"""Server Monitor"""

import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def rw_sql() -> bool:
    """Is mySQL port open for rw.sql.pv

    Returns:
        bool: Server Is Up
    """
    result = sock.connect_ex(("rw.sql.pvt.kumpedns.us", 3306))
    sock.close()
    return result == 0
