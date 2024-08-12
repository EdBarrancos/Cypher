import select
import sys

from config_handler import Configurations
from network.helpers import open_tcp_conn_through_multicast


class DirectorConfigurations(Configurations):
    pass


def main():
    s = open_tcp_conn_through_multicast()

    s.send(bytes(f"DIRECTOR", "utf-8"))

    print("character_name:lang:message")

    while True:
        sockets_list = [sys.stdin, s]

        read_sockets, _, _ = select.select(sockets_list, [], [])

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
