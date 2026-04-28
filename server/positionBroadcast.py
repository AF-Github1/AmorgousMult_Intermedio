##!! To replace   all_positions = self.receive_object(self.connection) ###!! replace with broadcast thread
##!! in line 112, for host.py

import threading
import json
import time

from information import generic
from server import clientList as cl



def receive_str(connect, n_bytes: int) -> str:
	"""
	:param n_bytes: The number of bytes to read from the current connection
	:return: The next string read from the current connection
	"""
	data = connect.recv(n_bytes)
	return data.decode()

def send_str(connect, value: str) -> None:
	connect.send(value.encode())
     
def send_int(connect, value: int, n_bytes: int) -> None:
	connect.send(value.to_bytes(n_bytes, byteorder="big", signed=True))
     
def receive_int(connect, n_bytes: int) -> int:
	data = connect.recv(n_bytes)
	return int.from_bytes(data, byteorder='big', signed=True)

def send_object(connection, obj):
	"""1º: envia tamanho, 2º: envia dados."""
	data = json.dumps(obj).encode('utf-8')
	size = len(data)
	send_int(connection, size, generic.INT_SIZE)         # Envio do tamanho
	connection.send(data)              		# Envio do objeto
     
def receive_object(connection):
    """1º: lê tamanho, 2º: lê dados."""
    size = receive_int(connection, generic.INT_SIZE)  	# Recebe o tamanho

    #print(f"DEBUG [Object Size Header]: {size} bytes") ##!! Debugging

    data = connection.recv(size)       			# Recebe o objeto
    return json.loads(data.decode('utf-8'))


def positionBroadcastThread(clients, game_state): ##!! Clean and refactor in order to handle nested dictionaries (positions from players != positions from enemies)
    """
    Starts the thread for position broadcast thread, in order to inform clients of all current positions in the map 
    """
    print("Initializing server thread")
    server_thread = threading.Thread(target=positionBroadcasting, args=(clients,game_state), daemon=True)
    server_thread.start()
    return server_thread

def positionBroadcasting(clients, game_state): ##!! client_list does not give the actual positions for each of the clients
    """
    
    Logic for the position broadcast thread. Goes through the client list and updates each and every single one with information on the position dictionary (current_positions)
    which handles player and enemy positions ##!! and eventually other information that will need to be shared
    
    """
    while True:
        current_clients = clients.obter_lista()
        current_positions = game_state.get_broadcast_dict()

        for addr, conn in current_clients.items():
            try:
                send_str(conn, generic.POS_OP)
                send_object(conn, current_positions)
                print(f"POSITION BROADCAST THREAD:\nBroadcast sent to all clients at: {current_clients}\nPosition dictionary broadcast: {current_positions}")
            except (BrokenPipeError, ConnectionResetError):
                continue
            except Exception as e:
                print(f"Broadcast Error to {addr}: {e}")

            time.sleep(1/60) #  in order to not overwhelm with requests (60 frames)