class Spectator:
    """
    ##!! Reserved for the spectator class. Capable of witnessing game, capable to being promoted to player in lobby, unable to play the game if game starts, can only watch
    """

    def __init__(self, idSpectator: str, ipSpectator: tuple) -> None:

        self.idSpectator = idSpectator
        self.ipSpectator = ipSpectator