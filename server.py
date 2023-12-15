import socket
import pickle
import sys
from _thread import *
from board import Board


server = "192.168.1.61"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


boards = [Board(23, 10, -400), Board(23, 10, 400)]

def threaded_client(conn, player):
    conn.send(pickle.dumps(boards[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            boards[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = boards[0]
                else:
                    reply = boards[1]
                
                reply.set_offset(400)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1