class Enemy:

    def __init__(self, idEnemy: str, position: list) -> None:

        self.idEnemy = idEnemy
        self.position = position
        self.velocity:float = 3
        self.size = 0


    def tag(self): ##!! Reserved for checking contact from current positions and sending it back to server
        pass

    def move(self): ##!! Reserved for handling enemy movement
        pass
