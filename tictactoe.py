class Player():
    def __init__():
        ""

    def play() -> int:
        return 0
    
class tictactoe():
    def __init__(self):
        self.plate = [
            0, 0, 0,
            0, 0, 0,
            0, 0, 0
        ]

    def player_input(self, player, place) -> bool:
        if self.plate[place] != 0: return False
        self.plate[place] = player
        return True