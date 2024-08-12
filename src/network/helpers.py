import socket

from .multicast import send_multicast_message


def next_free_port(port=1024, max_port=65535):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while port <= max_port:
        try:
            sock.bind(('', port))
            sock.close()
            return port
        except OSError:
            port += 1
    raise IOError('no free ports')


def get_host():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)


def open_tcp_conn_through_multicast():
    host = get_host()
    port = next_free_port()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))

    sock.listen(100)

    send_multicast_message(f'{host}:{port}')
    conn, addr = sock.accept()
    return conn
