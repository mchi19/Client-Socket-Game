#!/usr/bin/env python3

import socket
import sys
import threading
import pickle

#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = 'localhost'
PORT = 5555
ADDRESS = (SERVER, PORT)

# list of all clients that connect to server
clients = []
# list of clients positions
player_list = {}
# list of unique colors, only 4 for now
colors = ["light blue", "light salmon", "yellow", "black"]
# number of clients
client_number = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind(ADDRESS)
except socket.error as e:
    print(str(e))

def start_server():
    print("[INFO] Server is starting")
    # limits to 4 clients can connect
    server.listen(4)
    while True:
        conn, addr = server.accept()
        # send client player_number 
        message = "PLAYER_NUMBER: " + str(client_number) + "," + colors[client_number]
        conn.send(pickle.dumps(message))
        
        # receive client's player_position
        # issue where data is not received from connected port
        data = pickle.loads(conn.recv(2048))
        d_list = data.split(",")
        p_num, p_x, p_y = d_list[0], d_list[1], d_list[2]

        # update the positions and clients lists
        # player_pos in "x,y,color" format
        player_list[p_num] = [p_x, p_y, colors[int(p_num)]]
        clients.append(conn)

        # sending all clients the list of player_positions
        broadcast(player_list)
        print("[INFO] Connection successful!")
        # start handling thread
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()

        print("[INFO] active connections: {}".format(threading.activeCount()-1))

def handle_client(conn, addr):
    print("[INFO] New Connection {}".format(addr))
    # increases for each client added
    global client_number
    client_number += 1
    connected = True
    while connected:
        try:
            # recieve data for player position
            # check if see conn.recv is empty
            if conn.recv(2048) != b'':
            # this below is not receiving anything
                data = pickle.loads(conn.recv(2048))
                if type(data) == str and data[:12] == "DISCONNECTED":
                    del player_list[int(data[-1])]
                    del clients[conn]
                # broadcast data
                broadcast(data)
            else:
                continue
        except:
            connected = False
            break
    # close connection and decrease client_number count
    client_number -= 1
    conn.close()

def broadcast(data):
    # change format on how data is broadcast
    # make sure data is in string format
    print("broadcasting to other clients!!!")
    for client in clients:
        if type(data) == dict:
            for key in data:
                msg = [key] + data[key]
                client.send(pickle.dumps(msg))
        else:
            client.send(pickle.dumps(data))
    print("Done broadcasting...")

if __name__ == "__main__":
    start_server()
    close()
