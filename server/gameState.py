import threading

class GameState:

    """
    A class to represent the state of the game (if it has started) and handle actions related to the game (movement and attacks of player characters)
    ...

    Attributes
    ----------
    instanced_clientlist : Object
        Contains the same object used 

    game_active : bool
        Defines is the game is currently running or not

    lock: Synchronization primitive
        Handles locking of data in order to prevent concurrent access 

    """
    def __init__(self, instanced_clientlist=None):
        self.game_active = False
        self._lock = threading.Lock()
        self.client_list = instanced_clientlist
        self.full_state = {
            "players": {},
            "enemies": {}
        }


    def startFlag(self) -> bool:
        """
        Checks if theres a connected client and if the game has yet to start
        """
        with self._lock:
            if self.client_list.obterclient_total() > 0 and not self.game_active:
                self.game_active = True
                return True
            return False
        
    def resetFlag(self):
        """
        Resets the game state
        """
        with self._lock:
            self.game_active = False


    def update_player_position(self, addr_str: str, pos: list):
        with self._lock:
            if addr_str not in self.full_state["players"]:
                self.full_state["players"][addr_str] = {}
            self.full_state["players"][addr_str]["pos"] = pos

    def remove_player(self, addr_str: str):
        with self._lock:
            if addr_str in self.full_state["players"]:
                del self.full_state["players"][addr_str]

    def get_broadcast_dict(self) -> dict:
        with self._lock:
            return {
                "players": self.full_state["players"].copy(),
                "enemies": self.full_state["enemies"].copy()
            }