import socket
import select
import sys

from config_handler import Configutations
from network.helpers import get_host, next_free_port
from network.multicast import send_multicast_message


class DirectorConfigurations(Configutations):
    pass


def open_tcp_conn():
    host = get_host()
    port = next_free_port()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))

    sock.listen(100)

    send_multicast_message(f'CLI:{host}:{port}')
    conn, addr = sock.accept()
    return conn


def main():
    s = open_tcp_conn()

    s.send(bytes(f"DIRECTOR", "utf-8"))

    print("character_name:lang:message")

    while True:
        sockets_list = [sys.stdin, s]

        read_sockets, write_socket, error_socket = select.select(
            sockets_list, [], [])

        for sock in read_sockets:
            if sock == s:
                message = s.recv(2048).decode('utf-8')
                print(message)
            else:
                try:
                    message = sys.stdin.readline()
                    if message == "exit":
                        s.close()
                        break
                    s.send(bytes(f"{message}", 'utf-8'))
                except:
                    continue


if __name__ == "__main__":
    main()
