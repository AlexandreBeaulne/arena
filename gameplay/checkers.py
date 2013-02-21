
from gameplay.game import Game

class Checkers(Game):

    player_mapping = {
        1: 'r',
        2: 'w',
        }

    def __init__(self, board=None, current_player=1):
        self.board = board or self.initial_board()
        self.current_player = current_player
        self.moves_without_capture = 0

    @staticmethod
    def initial_board():
        """
        Initial board state.
        """
        rx = ' r r r rr r r r  r r r r'
        wx = 'w w w w  w w w ww w w w '
        return rx + ' ' * 16 + wx

    def draw_board(self):
        s = ''
        for i in range(0,64,8):
            s += self.board[i:i+8]
            s += '\n'
        s += '=' * 8
        print(s)

    def is_king(self, char):
        return not char.islower()

    def get_direction(self, piece):

        if self.is_king(piece):
            return None
        elif piece == 'r':
            return 1
        elif piece == 'w':
            return -1

    def get_opponent(self, p):
        """
        Returns char symbol for opponent.
        """
        if p in 'Rr':
            return 'w'
        elif p in 'Ww':
            return 'r'
        else:
            return None

    def result(self):

        bl = self.board.lower()

        if 'w' not in bl:
            return 1
        elif 'r' not in bl:
            return 2
        elif self.moves_without_capture >50:
            return -1
        else:
            return 0

    def apply_move(self, initial_board, move):
        """
        Takes the string representation of the board
        and apply the move to it. Return the resulting
        board
        """
        start_p, end_p = move

        distance = abs(start_p - end_p)

        if distance > 9:
            self.moves_without_capture = 0
        else:
            self.moves_without_capture += 1

        board_list = list(self.board)
        board_list[start_p], board_list[end_p] = self.board[end_p], self.board[start_p]    

        if distance > 9:
            jumped_p = int((start_p + end_p) / 2)
            board_list[jumped_p] = ' '

        for position in range(0, 8):
            if board_list[position] == 'w':
                board_list[position] = 'W'

        for position in range(56, 64):
            if board_list[position] == 'r':
                board_list[position] = 'R'

        return ''.join(board_list)
       
    def transition(self, move, _): # No need to use the third argument (player) for checkers

        self.board = self.apply_move(self.board, move)
        self.current_player = 3 - self.current_player # Toggle between 1 and 2.

    def move_legal(self, move):
        """
        Verify that a move is legal.
        """

        # Check for out-of-bounds moves
        if any([pos<0 or pos>63 for pos in move]):
            return false

        start_position, *visited_squares = move

        player = self.player_mapping[self.current_player]

        # Check if starting position is correct player
        if  self.board[start_postion].lower() != player:
            return False

        # Check if all visited squares are empty
        if any([square != ' ' for square in visited_squares]):
            return false

        direction = self.get_direction(player)

        # Check for forced jumps.
        valid_captures = self.captures(player, direction)
        if valid_captures:
            return move in valid_captures
        else:
            return move in self.moves(start_position, direction)

    def captures(self, player):
        """
        Returns all potential capture moves
        """
        start_positions = [i for i, char in enumerate(self.board) if char.lower() == player]
        captures = []
        for pos in start_positions:
            paths = self.captures(pos, self.board)
            yield [pos] + path for path in paths

    def captures(self, start_pos, board): 
        """
        Returns all potential capture moves for a given start position and board
        """
        player = board[start_pos]
        opponent = self.get_opponent(player)
        direction = self.get_direction(player)

        # Handle left and right borders
        if start_pos % 8 in [0,1]:
            end_positions = [start_pos + 18, start_pos - 14]
        elif start_pos % 8 in [6,7]:
            end_positions = [start_pos + 14, start_pos - 18]
        else:
            end_positions = [start_pos + 18, start_pos + 14, start_pos - 14, start_pos - 18]

        # Handle bottom and top borders
        end_positions = [p for p in end_positions if 0 <= e <= 63]

        # Make sure there is a captured pawn
        end_positions = [p for p in end_positions if board[(start_pos+p)//2].lower() == opponent]

        # Handle direction of play
        if direction == 1:
            end_positions = [e for e in moves if e > position]
        elif direction == -1:
            end_positions = [e for e in moves if e < position]

        for end_pos in end_positions:
            paths = self.capture(end_pos, self.apply_move(board, [start_pos,end_pos]))
            yield [end_pos] + path for path in paths
    
    def moves(self, start_position, direction):
        """
        All potential non-capture moves (1 diagonal square away); no collision detection
        """

        # Handle left and right borders
        if start_position % 8 == 0:
            end_positions = [start_position + 9, start_position - 7]
        elif position % 8 == 7:
            end_positions = [start_position + 7, start_position - 9]
        else:
            end_positions = [start_position + 7, start_position + 9, start_position - 7, start_position - 9]

        # Handle bottom and top borders
        end_positions = [p for p in end_positions if 0 <= e <= 63]

        # Handle direction of play
        if direction == 1:
            end_positions = [e for e in moves if e > position]
        elif direction == -1:
            end_positions = [e for e in moves if e < position]
    
        return [[start_position, p] for p in end_positions]

