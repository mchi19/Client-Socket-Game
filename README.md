# Client-Socket-GUI-Game
README
#####################################################################
This is a simple multi client-server network game, where up to 4 
players can connect to a screen and move objects around using arrow 
keys. GUI created using python Tkinter and python socket programming.

#####################################################################
Follow these instructions before running the bash scripts
- download and unzip file.
- pull extracted folder to a directory of your choice and cd to it.
- first run ./run_server.sh to start server.
- from another terminal or machine that is on  the same network, 
    run ./run_client.sh to run client, (server can connect with up 
    to 4 clients, any more than 4 is not currently supported).
- to quit from client, close window, then use CTRL-C from terminal.
- to quit from server, use CTRL-C. (Make sure all other client terminals
    are closed first before closing server and attempting to run the 
    server script again, this will prevent server being unavailable).

#####################################################################
Possible Future Improvements
- Adding bounds to the window so objects cannot leave field of view.
- Making disconnecting remove rectangle from other client's windows (WIP).
- Increasing support to more than 4 clients to connect to server.
- Include User Interface to manually monitor Server start and shutdown.
- Find alternative to close applications instead of using CTRL-C.
- More ideas are welcome...
