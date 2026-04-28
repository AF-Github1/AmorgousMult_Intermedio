import threading
import pygame

class GameOperations:

    """
    A class to handle actions related to the game (movement and attacks of player characters) through pygame
    ...

    Attributes
    ----------
    instanced_clientlist : Object
        Contains the same object used 

    lock: Synchronization primitive
        Handles locking of data in order to prevent concurrent access 

    """
    def __init__(self, instanced_clientlist=None):
        self._lock = threading.Lock()
        self.client_list = instanced_clientlist


    def movement(self, controls:str, position:float, velocity:float) -> float:
        """
        This method handles player movement, using pygame specific functions to handle keypress events, and update events.
        Depending on the keypress, the player will move a distance in a given direction, by the value of its own velocity
        ...
    
        Parameters
        ----------
        controls : str
            Defines if the player will be using wasd or arrows keys to move their character
        position: float
            Current position of the player character
        velocity: float
            Current velocity of the player character
        Return
        ----------
            position : float
              The new updated position of the player character

        """
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if controls == "wasd":
            if keys[pygame.K_w]: position[1] -= velocity
            if keys[pygame.K_s]: position[1] += velocity
            if keys[pygame.K_a]: position[0] -= velocity
            if keys[pygame.K_d]: position[0] += velocity
        else: # arrows
            if keys[pygame.K_UP]:    position[1] -= velocity
            if keys[pygame.K_DOWN]:  position[1] += velocity
            if keys[pygame.K_LEFT]:  position[0] -= velocity
            if keys[pygame.K_RIGHT]: position[0] += velocity
        return position
    
    def mouse_movement(self, controls:str, position:float, velocity:float) -> float:
        """
        Reserved for cursor based movement scheme
        """
        pass


    def attack(self, controls:str, position:float) -> None:
        """
        Reserved for character attack logic (the attack will come from the character itself, so position is necessary, control scheme might not be necessary)
        """

        pass
