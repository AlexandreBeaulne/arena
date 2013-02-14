
from gameplay.game import Game


class TicTacToe(Game):


    def __init__(self, player, board=None):
        self.player = player
        self.board = board or self.initialize()

    
    def transition(self, move, player):
        l = list(self.board)
        l[move] = player
        return ''.join(l)
        
    def move_legal(self, move):
        return self.board[move] == ' '
    
    def winner(self):
        WINCOMBOS = [[0,1,2], [3,4,5], [6,7,8],
                     [0,3,6], [1,4,7], [2,5,8],
                     [0,4,8], [2,4,6]]
        
        for line in WINCOMBOS:
            s = set([self.board[e] for e in line])
            if len(s) == 1 and ' ' not in s:
                winner = s.pop()
                return winner
        return None

    def initialize(self):
        return ' ' * 9        