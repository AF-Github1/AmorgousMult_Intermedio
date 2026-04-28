from information import generic
import json
import time
import threading

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


def serverToClientThread(clients, game_state):
    """
    Starts the thread for server, in order to handle multiple clients separatly
    """
    print("Initializing server thread")
    server_thread = threading.Thread(target=instructionHandler, args=(clients, game_state), daemon=True)
    server_thread.start()
    return server_thread


def instructionHandler(clients, game_state) -> None:
    """
    Main loop for the serverLogic. Gets and iterates through the list of connected clients, broadcasting their position to all other clients on the same list

    """
    positions = {}
    
    while True:
        current_clients = clients.obter_lista()
        for addr, conn in current_clients.items():
            addr_str = str(addr)
            if addr_str not in positions: ##!! This section needs to be changed, initial position needs to be set by players
                positions[addr_str] = [960, 540]
            try:
                conn.setblocking(False) # Set blocking used to prevent freezing clients in case one of them crashes. Does add latency

                opInstruct = receive_str(conn, generic.COMMAND_SIZE).strip()
                if opInstruct == "move": ##!! updatePosition here
                        conn.setblocking(True)
                        pos_dict = receive_object(conn)
                        if pos_dict:
                            game_state.update_player_position(addr_str, pos_dict["pos"])
                            #print(f"[RECV] From {addr_str}: {msg['pos']}")
                        
                elif opInstruct == "atk":
                    pass

                conn.setblocking(False)

            except BlockingIOError: # Operação não conseguiu ser realizada
                continue

            except (BrokenPipeError, ConnectionResetError): # Ligação fechada ou client encerrou
                clients.remover(addr)
                if addr_str in positions:
                    del positions[addr_str]
                print(addr_str + " removed")


        time.sleep(1/60) # lockde framerate to 60fps
