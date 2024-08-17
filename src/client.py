import functools
import select
import sys

from config_handler import Configurations
from network import open_tcp_conn_through_multicast


class ClientConfigurations(Configurations):
    pass


name = input("Your character name: ")
languages = input("Which languages do you speak? (Separate with ,): ") \
    .replace(" ", "").split(',')


def main():
    s = open_tcp_conn_through_multicast()
    s.send(bytes(
        f"{name}:{functools.reduce(lambda a, b: a + ',' + b, languages)}",
        "utf-8"))

    print("lang:message")
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
                    # TODO: Check if player speaks lang
                    # TODO: Check if formatting is correct
                    s.send(bytes(f"{message}", 'utf-8'))
                except:
                    continue


if __name__ == '__main__':
    main()
