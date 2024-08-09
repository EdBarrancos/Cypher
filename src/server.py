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
            
            broadcast(player, message.split(':')[0], message.split(':')[1][:-1])
        except:
            continue

def broadcast(sender_player, language, message):
    to_remove = []
    for player in list_of_clients:
        if player == sender_player:
            continue

        try:
            send_message(sender_player, player, language, message)
        except:
            player.conn.close()
            to_remove.append(player)
    
    for p in to_remove:
        remove_player(p)

def send_message(sender, reciver: Player, language, message):
    if reciver.speaks_language(language):
        reciver.conn.send(bytes(
            f"{sender.name}:{language}:{message}",
            'utf-8'))
        return
    reciver.conn.send(bytes(
        f"{sender.name}:{language}:{randomize_message(message)}",
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
    new_player = Player(
        conn, 
        addr, 
        authentication.split(':')[0], 
        authentication.split(':')[1].split(','))

    list_of_clients.append(new_player)

    start_new_thread(handle_client, (new_player,))