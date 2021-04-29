#!/usr/bin/env python3

import sys
import socket
import threading
from tkinter import *
import random
import pickle

PORT = 5555
SERVER = 'localhost'
#SERVER = "192.168.1.175"
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(ADDRESS)
except Exception as e:
    print("Error, exception occured: Couldn't connect with server, terminating!")
    print(e)
    sys.exit()

WIDTH = 30
LENGTH = 30

class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Take Home Assignment")
        self.root.geometry("500x500")
        self.canvas = Canvas(self.root, width=500, heigh=500, bg="grey")
        self.canvas.pack()  

        # create player_list to track other player coordinates
        self.full_player_list = {}
        self.other_labels = {}
        # initialize self.data for send messages
        self.data = ""

        # start the thread
        self.start_thread()
        # start GUI mainloop
        self.root.mainloop()
        # remove all instances of client's rectangle in other client windows
        # still WIP
        self.remove_my_player()

    def add_my_player(self, x, y, number, color):
        self.number = number
        self.color = color
        self.rect = self.canvas.create_rectangle(x, y, x+WIDTH, y+LENGTH, fill="{}".format(color))
        self.set_keys()
        # send data back to server
        self.data = "{}, {}, {}".format(number, x, y)
        self.send_data()
    
    def remove_my_player(self):
        self.data = "DISCONNECTED: Player {}".format(self.number)
        print(self.data)
        self.send_data()

    ### Below are functions to bind keys and move client's rectangle object ###
    def left(self, event):
        self.canvas.move(self.rect, -10, 0)
        # update server with new coords
        coords = self.canvas.coords(self.rect)
        c_x = coords[0]
        c_y = coords[1]
        self.data = (self.number, c_x, c_y, self.color)
        self.send_data()

    def right(self, event):
        self.canvas.move(self.rect, 10, 0)
        coords = self.canvas.coords(self.rect)
        c_x = coords[0]
        c_y = coords[1]
        self.data = (self.number, c_x, c_y, self.color)
        self.send_data()

    def up(self, event):
        self.canvas.move(self.rect, 0, -10)
        coords = self.canvas.coords(self.rect)
        c_x = coords[0]
        c_y = coords[1]
        self.data = (self.number, c_x, c_y, self.color)
        self.send_data()

    def down(self, event):
        self.canvas.move(self.rect, 0, 10)
        coords = self.canvas.coords(self.rect)
        c_x = coords[0]
        c_y = coords[1]
        self.data = (self.number, c_x, c_y, self.color)
        self.send_data()

    def set_keys(self):
        self.root.bind("<Left>", self.left)
        self.root.bind("<Right>", self.right)
        self.root.bind("<Up>", self.up)
        self.root.bind("<Down>", self.down)

    def update_canvas(self):
        # clear other labels that isn't my_player
        for player in self.other_labels:
            self.canvas.delete(self.other_labels[player])
        # creat new labels for updated coordinates of other players
        for player in self.full_player_list:
            if player != self.number:
                # format: dic[player_pos] = "x,y,color"
                p_info = self.full_player_list[player]
                x = int(p_info[0])
                y = int(p_info[1])
                color = p_info[2]
                label = self.canvas.create_rectangle(x, y, x+WIDTH, y+LENGTH, tags="other", fill="{}".format(color))
                self.other_labels[player] = label
        
    # function to start threading process
    def start_thread(self):
        # start receiving threads
        rcv = threading.Thread(target=self.receive_data)
        rcv.start()

    # function to receieve data from server thread
    def receive_data(self):
        # server starts
        # client connects to server
        # server sends client_number
        # client creates player from client_number and sends server player coordinates
        # server receives client data and stores in global player_list
        while True:
            try:
                data = pickle.loads(client.recv(2048))
                if (type(data) == str) and data[:15] == "PLAYER_NUMBER: ":
                    # data will come as "PLAYER_NUMBER: 1,light blue"
                    p_info = data.split(",")
                    p_num = int(p_info[0][-1])
                    p_color = p_info[1]
                    # create player object on canvas
                    p_x = random.randint(10,40) * 10
                    p_y = random.randint(10,40) * 10
                    self.add_my_player(p_x, p_y, p_num, p_color)
                elif (type(data) == str) and data[:12] == "DISCONNECTED":
                    # this part still doesn't work as intended (WIP)
                    del_p_num = int(data[-1])
                    del self.full_player_list[del_p_num]
                    self.update_canvas()
                else:
                    # data will be player lists
                    self.full_player_list[int(data[0])] = [int(data[1]), int(data[2]), data[3]]
                    # update the entire canvas with updated positions
                    self.update_canvas()
            except Exception as e:
                print("An error has occured!")
                print(e)
                client.close()
                break

    def send_data(self):
        while True:
            client.send(pickle.dumps(self.data))
            print("SENDING DATA TO SERVER")
            break

if __name__ == "__main__":
    gui = GUI()