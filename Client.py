import socket
import select
import threading
from Modifier import *

server_address = ("localhost", 33333)
key_map = load_map("map.txt")


def get_server_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect(server_address)
    return server


def read_user(user, server):
    while True:
        try:
            msg = user.recv(4096)
            print(msg)
            # msg = encrypt(msg, key_map)
            server.send(msg)
        except socket.error:
            break
    user.close()
    server.close()


def read_server(user, server):
    while True:
        try:
            msg = server.recv(4096)
            # msg = decrypt(msg, key_map)
            user.send(msg)
        except socket.error:
            break
    user.close()
    server.close()


def handle_user(user):
    server = get_server_socket()
    threading.Thread(target=read_user, args=(user, server))
    threading.Thread(target=read_server, args=(user, server))


a_user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
a_user.bind(("localhost", 22222))
a_user.listen(20)

listen_list = [a_user]

while True:
    read_list, _, _ = select.select(listen_list, [], [])

    for req in read_list:
        user, addr = req.accept()
        handle_user(user)