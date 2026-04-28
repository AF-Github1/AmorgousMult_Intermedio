# Reserved for host client. Can play the game, and change the settings
import socket
import information.generic as generic
import pygame
import json
import time
from pygame_calls.game import gameLogic

class Host:

    """
    A class to represent a host. 
    Client user that is able to manipulate the rules and setting of a session
    ...

    Attributes
    ----------
    position : list
        (x,y) position of a given player character
    velocity : float
        Controls the current speed of the player
    connection : object
        Handles the socket for connecting with the server

    """

    def __init__(self, position:list) -> None:
        self.connection = socket.socket()
        self.connection.connect((generic.SERVER_ADDRESS,generic.PORT))
        self.position = position
        self.velocity:float = 7

        data = self.connection.recv(generic.INT_SIZE)
        player_number = int.from_bytes(data, byteorder="big")
        if player_number == 1:
            self.controls = "wasd"
            self.color = (0, 255, 0)
            print("You are Player 1 (WASD)")
        else:
            self.controls = "arrows"
            self.color = (0, 0, 255)
            print("You are Player 2 (Arrows)")

        self.position = position

        self.game_instruct = gameLogic.GameOperations()

    def setPosition(self, newPos):
        self.position = newPos

    def receive_str(self, connect, n_bytes: int) -> str:
        """
        :param n_bytes: The number of bytes to read from the current connection
        :return: The next string read from the current connection
        """
        data = connect.recv(n_bytes)
        return data.decode()

    def send_str(self,connect, value: str) -> None:
        connect.send(value.encode())

    def send_int(self, connect, value: int, n_bytes: int) -> None:
        connect.send(value.to_bytes(n_bytes, byteorder="big", signed=True))     

    def receive_int(self, connect, n_bytes: int) -> int:
        data = connect.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    def send_object(self, connection, obj):
        """1º: envia tamanho, 2º: envia dados."""
        data = json.dumps(obj).encode('utf-8')
        size = len(data)
        self.send_int(connection, size, generic.INT_SIZE)         # Envio do tamanho
        connection.send(data)              		# Envio do objeto

    def receive_object(self, connection):
        """1º: lê tamanho, 2º: lê dados."""
        size = self.receive_int(connection, generic.INT_SIZE)  	# Recebe o tamanho

        #print(f"DEBUG [Object Size Header]: {size} bytes") ##!! Debugging

        data = connection.recv(size)       			# Recebe o objeto
        return json.loads(data.decode('utf-8'))


    def execute(self):
        """
        Starts the client thread when called. Sets up the graphical interface for the user, allows handling of inputs, and draws the player and its partner as circles
        """
        clock = pygame.time.Clock()
        pygame.init()
        ##!! Need to declare screen size, in order to declare positions as % of screen size
        screen = pygame.display.set_mode((800, 600))
        positions = {}

        id = str(self.connection.getsockname())
        try:

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                old_position = self.position[:]
                self.position = self.game_instruct.movement(self.controls, self.position, self.velocity) # Updating position based on key input

                try: # Section for handling if current position should be sent
                    if old_position != self.position:
                        self.send_str(self.connection, generic.MOVE_OP)
                        self.send_object(self.connection, {"pos": self.position})
                        print(f"DEBUG: Current position at {self.position} has been sent")
                except (BrokenPipeError, ConnectionResetError):
                    return

                try: # Section for handling position broadcast
                    
                    opInstruct = self.receive_str(self.connection, generic.COMMAND_SIZE).strip()
                    if opInstruct == "pos":
                        positions = self.receive_object(self.connection)

                except BlockingIOError: #Operation could not be completed
                    pass

                screen.fill("black")
                playerPositions = positions.get("players", {})
                for addr_str, value in playerPositions.items():
                    if addr_str != id:
                        pos = value.get("pos", [0, 0])
                        pygame.draw.circle(screen, (255, 0, 0), (int(pos[0]), int(pos[1])), 10)
                
                ##!! Reserved for enemy positions
                enemyPositions = positions.get("enemies", {})
                for enemyID, value in enemyPositions.items():
                    pos = value.get("pos", [0, 0])
                    pygame.draw.circle(screen, (255, 255, 0), (int(pos[0]), int(pos[1])), 8)
                
                pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), 10)

                pygame.display.flip()
                clock.tick(60)

        except Exception as e:
            print("Error " + str(e))
        finally:
            pygame.quit()
