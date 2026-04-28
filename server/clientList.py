import threading
from typing import Dict, Tuple
import socket

class ClientList:
    """
    This class handles all the users that are currently connected to the server
    Client user that is able to manipulate the rules and setting of a session
    ...

    Attributes
    ----------
    clients : dict
        Dict[Tuple[str, int], obj], representing the tuple that contains the host address and port, and the object associated with the socket
    client_total: int
        Number of clients currently present on the list
    lock: Synchronization primitive
        Handles locking of data in order to prevent concurrent access
    """
    def __init__(self):
        self._clients: Dict[Tuple[str, int], socket.socket] = {}
        self._lock = threading.Lock()
        self.client_total = 0



    def adicionar(self, address: Tuple[str, int], connection: socket.socket) -> None:
        """
        This function adds the address and socket information of the client to the dictionary, and increments client_total by 1

        Parameters:
            address: Tuple
                Tuple containing the address and port number information for the client
            
            connection: Obj
                Object representing the socket used for the connection

        """
        with self._lock:
            self._clients[address] = connection
            self.client_total += 1
            # Test
            print("Client ", address," added to dictionary")
            print("Nr. de clientes:",self.client_total)

    def remover(self, addr: Tuple[str, int]) -> None:
        """
        This function removes the specified address from the dictionary, and decrements the client_total

        Parameters:
            address: Tuple
                Tuple containing the address and port number information of the client to be removed

        """
        with self._lock:
            if addr in self._clients:
                del self._clients[addr]
                self.client_total -= 1

    def obter_lista(self) -> Dict[Tuple[str, int], socket.socket]:
        """
        This functions returns a shallow copy of the client list
        """
        with self._lock:
            return self._clients.copy()

    def obterclient_total(self) -> int:
        """
        This functions returns the current client total
        """
        return self.client_total

