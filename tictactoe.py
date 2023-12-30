import random
import threading

class Player():
    def __init__(self):
        pass

    def play(playable: list) -> int:
        return 0
    
class HumanPlayer(Player):
    def play(self, playable: list, state) -> int:
        while True:
            print(f'Choose a number in {", ".join(playable)}')
            n = input()
            if n in playable:
                break
        return n

class BotPlayer(Player):
    learned = dict()
    learning_rate = 0.01

    def __init__(self, decision=False):
        self.reward = 0
        self.actions = []
        self.decision = decision

    def play(self, playable: list, state) -> int:
        if not self.decision: 
            return random.choice(playable)
        
        # choose best from learned
        best = -1
        best_value = 0
        for moove in playable:
            future = state[:moove] + '1' + state[moove+1:]
            future_v = BotPlayer.learned[future] if future in BotPlayer.learned else 0
            if best == -1 or future_v > best_value:
                best = moove
                best_value = future_v
        return best

    def giveReward(self, reward):
        self.reward = reward

    def add_action(self, state):
        self.actions.append(state)

    def learn(self):
        prev = self.reward
        for k, action in enumerate(reversed(self.actions)):
            a_v = BotPlayer.learned[action] if action in BotPlayer.learned else 0
            BotPlayer.learned[action] = a_v + BotPlayer.learning_rate * (prev - a_v)
            prev = BotPlayer.learned[action]

class tictactoe():
    def __init__(self):
        self.plate = [
            0, 0, 0,
            0, 0, 0,
            0, 0, 0
        ]

    def player_input(self, player: int, place: int) -> bool:
        if self.plate[place] != 0: return False
        self.plate[place] = player
        return True
    
    def finished(self) -> int:
        sequences = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [6, 4, 2]
        ]

        # check for player wins
        for s in sequences:
            n = self.plate[s[0]]
            if self.plate[s[1]] == n and self.plate[s[2]] == n and n != 0:
                return n
        
        if 0 not in self.plate:
            # game finished
            return -1

        # no wins but can still play
        return 0
    
    def playable(self):
        return [k for k, v in enumerate(self.plate) if v == 0]
    
    def state(self, player):
        if player == 1:
            return ''.join([str(x if player == 1 else 2) for x in self.plate])
        else:
            return ''.join([str(2 if x == 1 else (1 if x == 2 else 0)) for x in self.plate])


    def __str__(self) -> str:
        return '\n'.join([f"{self.plate[i]} {self.plate[i+1]} {self.plate[i+2]}" for i in range(0, len(self.plate), 3)])
    
def play(p1, p2, game, train=False):
    players = [p1, p2]

    is_finished = game.finished()
    player_turn = random.randint(0, 1)
    while is_finished == 0:
        c_player = players[player_turn]

        game.player_input(player_turn + 1, c_player.play(game.playable(), game.state(player_turn+1)))

        if train:
            c_player.add_action(game.state(player_turn + 1))

        is_finished = game.finished()
        player_turn = 0 if player_turn == 1 else 1
    
    return is_finished

def learn_game():
    for _ in range(1000):
        p1, p2 = BotPlayer(), BotPlayer()
        game = tictactoe()
        result = play(p1, p2, game, train=True)
        if result == 1:
            p1.giveReward(1)
            p2.giveReward(-1)
        elif result == 2:
            p1.giveReward(-1)
            p2.giveReward(1)
        
        p1.learn()
        p2.learn()

if __name__ =='__main__':
    threads = []
    for _ in range(200):
        t = threading.Thread(target=learn_game)
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
            

    print(list(sorted(BotPlayer.learned.items(), key=lambda x: x[1]))[-3:])

    nb_games = 1000
    count = dict({'p1': 0, 'p2': 0, 'draw': 0})
    for _ in range(nb_games):
        game = tictactoe()
        r = play(BotPlayer(decision=True), BotPlayer(), game)
        if r == 1:
            count['p1'] += 1
        if r == 2:
            count['p2'] += 1
        if r == -1:
            count['draw'] += 1

    print(f"{100 * count['p1'] / nb_games}% Player1")
    print(f"{100 * count['p2'] / nb_games}% Player2")
    print(f"{100 * count['draw'] / nb_games}% draws")
    print()

    nb_games = 1000
    count = dict({'p1': 0, 'p2': 0, 'draw': 0})
    for _ in range(nb_games):
        game = tictactoe()
        r = play(BotPlayer(decision=True), BotPlayer(decision=True), game)
        if r == 1:
            count['p1'] += 1
        if r == 2:
            count['p2'] += 1
        if r == -1:
            count['draw'] += 1

    print(f"{100 * count['p1'] / nb_games}% Player1")
    print(f"{100 * count['p2'] / nb_games}% Player2")
    print(f"{100 * count['draw'] / nb_games}% draws")
        
