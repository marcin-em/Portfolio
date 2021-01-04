from colorama import Fore, Style

dictionary = {
    '1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0, # row
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, # column
}

class Blank:
    def __str__(self):
        return '  . '

class Piece:

    global_counter = 0

    def __init__(self, color):
        self.color = color
        self.current_column = 0
        self.current_row = 0
        self.next_column = 0
        self.next_row = 0

    def cls_move_counter(self, counter):
        Piece.global_counter = counter
    
    def translate(self, cur_loc):
        self.current_column = dictionary[cur_loc[0]]
        self.current_row = dictionary[cur_loc[1]]
        self.next_column = dictionary[cur_loc[2]]
        self.next_row = dictionary[cur_loc[3]]

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)

        self.first_move = True
        self.pawn_move_counter = 1000
        self.end_en_passable = True if self.pawn_move_counter < self.global_counter else False
        self.en_passantable = False
        self.en_passant_move = False
        self.en_passant_row_dir = 1 if self.color == 'W' else -1

        if self.color == 'W':
            self.moves = [[-2, 0], [-1, 0]]
            self.captures = [[-1, -1], [-1, 1]]
        else:
            self.moves = [[2, 0], [1, 0]]
            self.captures = [[1, -1], [1, 1]]

    def __str__(self):
        if self.color == 'W':
            return '  \u265F '
        else:
            return Style.RESET_ALL + Fore. RED + '  \u265F ' + Style.RESET_ALL

    def rules(self, current_loc, board):
        self.translate(current_loc)
        
        next_move = [self.next_row, self.next_column]
        valid_moves = []
        en_pass_moves = []

        for move in self.moves:
            temp_current_row = self.current_row
            temp_current_column = self.current_column
            pos = []
            temp_current_row += move[0]
            temp_current_column += move[1]
            
            if temp_current_row < 0 or temp_current_row > 7 or\
                temp_current_column < 0 or temp_current_column > 7:
                continue
            else:
                if type(board[temp_current_row][temp_current_column]) == Blank:
                    pos.append(temp_current_row)
                    pos.append(temp_current_column)
                    valid_moves.append(pos)
                else:
                    continue
        for capture in self.captures:
            temp_current_row = self.current_row
            temp_current_column = self.current_column
            pos = []
            temp_current_row += capture[0]
            temp_current_column += capture[1]

            if temp_current_row < 0 or temp_current_row > 7 or\
                temp_current_column < 0 or temp_current_column > 7:
                continue
            else:
                side_pos = board[temp_current_row + self.en_passant_row_dir][temp_current_column]
                if isinstance(board[temp_current_row][temp_current_column], Piece) and\
                    board[temp_current_row][temp_current_column].color != self.color:
                        pos.append(temp_current_row)
                        pos.append(temp_current_column)
                        valid_moves.append(pos)
                elif isinstance(board[temp_current_row][temp_current_column], Blank) and\
                    isinstance(side_pos, Pawn) and side_pos.en_passantable == True and\
                        side_pos.end_en_passable == False and side_pos.color != self.color:
                            pos.append(temp_current_row)
                            pos.append(temp_current_column)
                            valid_moves.append(pos)
                            en_pass_moves.append(pos)
                else:
                    continue

        if next_move in valid_moves:
            if next_move in en_pass_moves:
                self.en_passant_move = True
            if next_move[0] == self.current_row + self.moves[0][0] and self.first_move:
                self.en_passantable = True 
            # usuwa poczatkowy ruch 2 do przodu
            if self.first_move:
                self.moves.remove(self.moves[0])
                self.first_move = False
            return True
        else:
            return False

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
    
        self.directions = [[-1, 0], [1, 0], [0, -1], [0, 1], ]
        self.first_move = True

    def __str__(self):
        if self.color == 'W':
            return '  \u265C '
        else:
            return Style.RESET_ALL + Fore. RED + '  \u265C ' + Style.RESET_ALL  

    def rules(self, current_loc, board):
        self.translate(current_loc)
        
        next_move = [self.next_row, self.next_column]
        valid_moves = []

        for direction in self.directions:
            temp_current_row = self.current_row
            temp_current_column = self.current_column
            while temp_current_row >= 0 and temp_current_row <= 7 and\
                temp_current_column >= 0 and temp_current_column <= 7:
                pos = []
                temp_current_row += direction[0]
                temp_current_column += direction[1]
                
                if temp_current_row < 0 or temp_current_row > 7 or\
                    temp_current_column < 0 or temp_current_column > 7:
                    continue
                else:
                    if type(board[temp_current_row][temp_current_column]) == Blank:
                        pos.append(temp_current_row)
                        pos.append(temp_current_column)
                        valid_moves.append(pos)
                    elif isinstance(board[temp_current_row][temp_current_column], Piece) and\
                        board[temp_current_row][temp_current_column].color != self.color:
                        pos.append(temp_current_row)
                        pos.append(temp_current_column)
                        valid_moves.append(pos)
                        break
                    else:
                        break

        if next_move in valid_moves:
            if self.first_move:
                self.first_move = False
            return True
        else:
            return False

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)

        self.moves = [
            [-2, 1], [-1, 2], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], 
        ]
    
    def __str__(self):
        if self.color == 'W':
            return '  \u265E '
        else:
            return Style.RESET_ALL + Fore. RED + '  \u265E ' + Style.RESET_ALL  

    def rules(self, current_loc, board):
        self.translate(current_loc)

        next_move = [self.next_row, self.next_column]

        valid_moves = []
        
        for move in self.moves:
            temp_current_row = self.current_row
            temp_current_column = self.current_column
            temp_current_row += move[0]
            temp_current_column += move[1]
            pos = []
            if temp_current_row < 0 or temp_current_row > 7 or\
                temp_current_column < 0 or temp_current_column > 7:
                continue
            else:
                if type(board[temp_current_row][temp_current_column]) == Blank:
                    pos.append(temp_current_row)
                    pos.append(temp_current_column)
                    valid_moves.append(pos)
                elif isinstance(board[temp_current_row][temp_current_column], Piece) and\
                    board[temp_current_row][temp_current_column].color != self.color:
                    pos.append(temp_current_row)
                    pos.append(temp_current_column)
                    valid_moves.append(pos)
                    continue
                else:
                    continue

        if next_move in valid_moves:
            return True
        else:
            return False

class Bishop(Rook):
    def __init__(self, color):
        super().__init__(color)

        self.directions = [[-1, 1], [1, 1], [1, -1], [-1, -1], ]

    def __str__(self):
        if self.color == 'W':
            return '  \u265D '
        else:
            return Style.RESET_ALL + Fore. RED + '  \u265D ' + Style.RESET_ALL  

class Queen(Rook):
    def __init__(self, color):
        super().__init__(color)

        self.directions = [
            [-1, 0], [1, 0], [0, -1], [0, 1], 
            [-1, 1], [1, 1], [1, -1], [-1, -1],
        ]
    
    def __str__(self):
        if self.color == 'W':
            return '  \u265B '
        else:
            return Style.RESET_ALL + Fore. RED + '  \u265B ' + Style.RESET_ALL

class King(Piece):
    def __init__(self, color):
        super().__init__(color)

        self.moves = [
            [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1],
            [0, 2], [0, -2]
        ]
        self.first_move = True

    def __str__(self):
        if self.color == 'W':
            return '  \u265A '
        else:
            return Style.RESET_ALL + Fore. RED + '  \u265A ' + Style.RESET_ALL  

    def rules(self, current_loc, board):
        self.translate(current_loc)

        next_move = [self.next_row, self.next_column]

        valid_moves = []

        for move in self.moves:
            temp_current_row = self.current_row
            temp_current_column = self.current_column
            temp_current_row += move[0]
            temp_current_column += move[1]
            pos = []
            if temp_current_row < 0 or temp_current_row > 7 or\
                temp_current_column < 0 or temp_current_column > 7:
                continue
            else:
                if type(board[temp_current_row][temp_current_column]) == Blank:
                    pos.append(temp_current_row)
                    pos.append(temp_current_column)
                    valid_moves.append(pos)
                elif isinstance(board[temp_current_row][temp_current_column], Piece) and\
                    board[temp_current_row][temp_current_column].color != self.color:
                    pos.append(temp_current_row)
                    pos.append(temp_current_column)
                    valid_moves.append(pos)
                    continue
                else:
                    continue

        if next_move in valid_moves:
            if self.first_move:
                del self.moves[-2:]
                self.first_move = False
            return True
        else:
            return False

        