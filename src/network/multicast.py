import logging
import socket
import struct
from typing import Callable, Iterator

from .helpers import get_host, next_free_port

logger = logging.Logger("multicast", 0)


def start_multicast_receiver(
        multicast_group: str = '224.3.29.71',
        server_address: tuple[str, int] = ('', 10000),
        response_builder: Callable[[], str] = lambda: "ACK") -> Iterator[str]:
    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind to the server address
    sock.bind(server_address)
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    while True:
        logger.debug('waiting to receive message')
        data, address = sock.recvfrom(1024)

        logger.debug('received %s bytes from %s' % (len(data), address))
        logger.debug(data)
        yield data.decode('utf-8')

        logger.debug('sending acknowledgement to', address)
        sock.sendto(response_builder().encode('utf-8'), address)


def send_multicast_message(message: str, multicast_group: tuple[str, int] = ('224.3.29.71', 10000)) -> None:
    # Create the datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout so the socket does not block indefinitely when trying
    # to receive data.
    sock.settimeout(0.2)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    try:

        # Send data to the multicast group
        logger.debug('sending "%s"' % message)
        message_data = message.encode('utf-8')
        sock.sendto(message_data, multicast_group)

    finally:
        logger.debug('closing socket')
        sock.close()


def open_tcp_conn_through_multicast() -> socket:
    host = get_host()
    port = next_free_port()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))

    sock.listen(100)

    send_multicast_message(f'{host}:{port}')
    conn, _ = sock.accept()
    return conn
