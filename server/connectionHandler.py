import threading
import json
from information import generic
from server import clientList as cl
from server.gameState import GameState
import socket

class ThreadConnection(threading.Thread):
    """
    A class that handles the connection thread, which handles the connection from clients to the server.
    ...

    Attributes
    ----------
    s : object
        Instance of the socket class, in the socket module, that handles connections from clients
        
    running : bool
        Defines current state of the server

    clientList : object
        Instance of ClientList class that controls the full list of currently connected users
    """
    def __init__(self):
        super().__init__(daemon=True)
        self.s = socket.socket()
        self.s.bind(('', generic.PORT))
        self.s.listen(35000)
        self.running = True
        self.clientList = cl.ClientList()

        self.game_state = GameState(self.clientList)
    #-----
    def send_int(self,connection, value: int, n_bytes: int) -> None:
        """
        Sends size of message through connection
        """
        connection.send(value.to_bytes(n_bytes, byteorder="big", signed=True))

    def send_object(self, connection, obj):
        """
        Sends serialized object through connection
        """
        data = json.dumps(obj).encode('utf-8')
        size = len(data)
        self.send_int(connection,size, generic.INT_SIZE)
        connection.send(data)


    def run(self):
        """
        Called by threading.Thread. Acepts connections and calls clientList methods in other to update the client list. Gives a number to each player to identify control scheme
        """

        print("The server has started listening")
        while self.running:
            try:
                connection, address = self.s.accept()
                player_num = self.clientList.obterclient_total() + 1
                connection.send(player_num.to_bytes(generic.INT_SIZE, byteorder="big"))
                self.clientList.adicionar(address, connection)
                print("New player has connected with address : " + str(address))
            except Exception as e:
                print(f"Erro: {e}")
                continue
