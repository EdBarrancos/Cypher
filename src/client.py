import functools
import select
import sys
import threading
from typing import Callable

from config_handler import Configurations
from network import open_tcp_conn_through_multicast
from interactive_cli.player_cli import PlayerCli


class ClientConfigurations(Configurations):
    pass


def _read_thread(socket, callable: Callable[[], bool]):
    while callable():
        socket.setblocking(0)

        ready = select.select([socket], [], [], 0.5)
        if ready[0]:
            message = socket.recv(2048).decode('utf-8')
            print(message)


def main():
    s = open_tcp_conn_through_multicast()
    running = True
    thread = threading.Thread(target=lambda: _read_thread(s, lambda: running))
    thread.start()
    cli = PlayerCli(lambda message: s.send(bytes(f"{message}", 'utf-8')), prompt=True)
    cli.start_cli()
    running = False
    thread.join()


if __name__ == '__main__':
    main()
