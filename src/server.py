import socket
from dataclasses import dataclass

from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# TODO: Multicast IP
# TODO: Ability to narrate

IP = "127.0.0.1"
PORT = 65432

server.bind((IP, PORT))

server.listen(100)

@dataclass
class Player:
    conn: socket
    addr: any
    name: str
    languages: list

    def speaks_language(self, language):
        return language in self.languages

list_of_clients = []
director = None

print("Server Up and Running")

def handle_client(player: Player):
    print(f"{player.name} Logged in")
    
    while True:
        try:
            message = player.conn.recv(2048)
            if not message:
                remove_player(player)
                return
            
            message = message.decode('utf-8')
            # language:message
            
            print(f"< {player.name},{message.split(':')[0]} > " +
                    f"{message.split(':')[1][:-1]}")
            
            broadcast(player.name, message.split(':')[0], message.split(':')[1][:-1])
        except:
            continue

def handle_director(conn: socket):
    print(f"Director Logged in")

    while True:
        try:
            message = conn.recv(2048)
            if not message:
                return
            
            message = message.decode('utf-8')
            # character:language:message
            
            print(f"< DIRECTOR,{message.split(':')[0]},{message.split(':')[1]} > " +
                    f"{message.split(':')[2][:-1]}")
            
            broadcast(message.split(':')[0], message.split(':')[1], message.split(':')[2][:-1])
        except:
            continue


def broadcast(sender_name, language, message):
    # TODO: Make this more uniform so it works well on player and dm
    to_remove = []
    is_director = True
    for player in list_of_clients:
        if player.name == sender_name:
            is_director = False
            continue

        try:
            send_message(sender_name, player, language, message)
        except:
            player.conn.close()
            to_remove.append(player)
    
    for p in to_remove:
        remove_player(p)

    if not is_director:
        send_message_director(sender_name, director, language, message)

def send_message_director(sender_name, conn: socket, language, message):
    conn.send(bytes(
        f"{sender_name}:{language}:{message}",
        'utf-8'))

def send_message(sender_name, reciver: Player, language, message):
    if reciver.speaks_language(language):
        reciver.conn.send(bytes(
            f"{sender_name}:{language}:{message}",
            'utf-8'))
        return
    reciver.conn.send(bytes(
        f"{sender_name}:{language}:{randomize_message(message)}",
        'utf-8'))

def remove_player(player):
    if player in list_of_clients:
        list_of_clients.remove(player) 

def randomize_message(message: str):
    return "".join(map(lambda a: ' ' if a == ' ' else '?', message))

while True:
    conn, addr = server.accept()
    print(f"Connected by {addr}")
    # name:lang1,lang2...
    authentication = conn.recv(2048).decode("utf-8")
    if authentication == "DIRECTOR":
        director = conn
        start_new_thread(handle_director, (conn,))
        continue
    new_player = Player(
        conn, 
        addr, 
        authentication.split(':')[0], 
        authentication.split(':')[1].split(','))

    list_of_clients.append(new_player)

    start_new_thread(handle_client, (new_player,))