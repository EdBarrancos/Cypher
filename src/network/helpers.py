import socket


def next_free_port(port: int = 1024, max_port: int = 65535) -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while port <= max_port:
        try:
            sock.bind(('', port))
            sock.close()
            return port
        except OSError:
            port += 1
    raise IOError('no free ports')


def get_host() -> str:
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

