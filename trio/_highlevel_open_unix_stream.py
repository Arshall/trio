import trio
from trio._highlevel_open_tcp_stream import close_on_error
from trio.socket import socket, SOCK_STREAM

try:
    from trio.socket import AF_UNIX
    has_unix = True
except ImportError:
    has_unix = False

__all__ = ["open_unix_socket"]


async def open_unix_socket(filename,):
    """Opens a connection to the specified
    `Unix domain socket <https://en.wikipedia.org/wiki/Unix_domain_socket>`__.

    You must have read/write permission on the specified file to connect.

    Args:
      filename (str or bytes): The filename to open the connection to.

    Returns:
      SocketStream: a :class:`~trio.abc.Stream` connected to the given file.

    Raises:
      OSError: If the socket file could not be connected to.
      RuntimeError: If AF_UNIX sockets are not supported.
    """
    if not has_unix:
        raise RuntimeError("Unix sockets are not supported on this platform")

    if filename is None:
        raise ValueError("Filename cannot be None")

    # much more simplified logic vs tcp sockets - one socket type and only one
    # possible location to connect to
    sock = socket(AF_UNIX, SOCK_STREAM)
    with close_on_error(sock):
        await sock.connect(filename)

    return trio.SocketStream(sock)
