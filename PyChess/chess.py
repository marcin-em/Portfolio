import sys

from colorama import init, Fore, Style

from pieces import Blank, Piece, Pawn, Rook, Knight, Bishop, Queen, King

isCheckmate = False
counter = 0
mt_index = 0

blank = Blank()
king = King('W')
b_king = King('B')
queen = Queen('W')
b_queen = Queen('B')
rook1 = Rook('W')
rook2 = Rook('W')
b_rook1 = Rook('B')
b_rook2 = Rook('B')
bishop1 = Bishop('W')
bishop2 = Bishop('W')
knight1 = Knight('W')
knight2 = Knight('W')
b_knight1 = Knight('B')
b_knight2 = Knight('B')
b_bishop1 = Bishop('B')
b_bishop2 = Bishop('B')
pawn1 = Pawn('W')
pawn2 = Pawn('W')
pawn3 = Pawn('W')
pawn4 = Pawn('W')
pawn5 = Pawn('W')
pawn6 = Pawn('W')
pawn7 = Pawn('W')
pawn8 = Pawn('W')
b_pawn1 = Pawn('B')
b_pawn2 = Pawn('B')
b_pawn3 = Pawn('B')
b_pawn4 = Pawn('B')
b_pawn5 = Pawn('B')
b_pawn6 = Pawn('B')
b_pawn7 = Pawn('B')
b_pawn8 = Pawn('B')

start_board = [
    [b_rook1, b_knight1, b_bishop1, b_queen, b_king, b_bishop2, b_knight2, b_rook2],
    [b_pawn1, b_pawn2, b_pawn3, b_pawn4, b_pawn5, b_pawn6, b_pawn7, b_pawn8],
    [blank, blank, blank, blank, blank, blank, blank, blank],
    [blank, blank, blank, blank, blank, blank, blank, blank],
    [blank, blank, blank, blank, blank, blank, blank, blank],
    [blank, blank, blank, blank, blank, blank, blank, blank],
    [pawn1, pawn2, pawn3, pawn4, pawn5, pawn6, pawn7, pawn8],
    [rook1, knight1, bishop1, queen, king, bishop2, knight2, rook2],
]
board = [x[:] for x in start_board]

dictionary = {
    '1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0, # row
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, # column
}

def build_board(board):
    row_num = 8
    print('\n         A   B   C   D   E   F   G   H\n\n')
    for row in board:
        print(f'   {row_num}', end='   ')
        for i in row:
            print(i, end='')
        print(f'    {row_num}\n')
        row_num -= 1
    print('\n         A   B   C   D   E   F   G   H\n')

def move(board, move_code):
    global isCheckmate
    global counter
    start_column = dictionary[move_code[0]]
    start_row = dictionary[move_code[1]]
    end_column = dictionary[move_code[2]]
    end_row = dictionary[move_code[3]]
    
    piece_name = board[start_row][start_column]
    board[start_row][start_column] = blank
    if type(board[end_row][end_column]) == King:
        board[end_row][end_column] = piece_name
        isCheckmate = True
    else:
        board[end_row][end_column] = piece_name
        counter += 1
    if type(piece_name) == Pawn:
        pawn_promotion(board, piece_name, [end_row, end_column])
    piece_name.cls_move_counter(counter)

def check_input(player_input):
    check = [
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
        ['1', '2', '3', '4', '5', '6', '7', '8']
    ]
    if len(player_input) != 4:
        print('Invalid input\n\n')
        return False
    else:
        if player_input[0] in check[0] and player_input[1] in check[1] and\
            player_input[2] in check[0] and player_input[3] in check[1]:
            return True
        else:
            print('Invalid input\n\n')
            return False

def is_move_valid(move_code, board):
    start_column = dictionary[move_code[0]]
    start_row = dictionary[move_code[1]]
    next_column = dictionary[move_code[2]]
    next_row = dictionary[move_code[3]]
    piece_name = board[start_row][start_column]
    piece_destination = board[next_row][next_column]
    if isinstance(piece_name, Piece):                           # czy zostala zaznaczona bierka            
        if (counter % 2 == 0 and piece_name.color == 'B') or \
            (counter % 2 != 0 and piece_name.color == 'W'):         # czy zostala zaznaczona bierka
                print('Your cannot move your opponents pieces')     # odpowiedniego koloru
                return False
        if type(piece_destination) == Blank:                    # czy miejsce jest puste
            
            # Sprawdzenie roszady
            if type(piece_name) == King and piece_name.first_move == True:
                if next_column == start_column + 2 or next_column == start_column - 2:
                    castling_dir = 1 if next_column > start_column else -1
                    rooks_column = 7 if next_column > start_column else 0
                    rooks_row = 7 if piece_name.color == 'W' else 0
                    if type(board[rooks_row][rooks_column]) == Rook:
                        temp_rook = board[rooks_row][rooks_column]
                        if piece_name.color == board[rooks_row][rooks_column].color and\
                            board[rooks_row][rooks_column].first_move == True:
                            if castling(piece_name.color, castling_dir) == True and\
                                piece_name.rules(move_code, board):
                                # Ustawienie wiezy
                                board[rooks_row][next_column - castling_dir] = temp_rook
                                temp_rook.first_move = False
                                board[rooks_row][rooks_column] = blank
                                return True
                            else:
                                return False
                        else:
                            print('Castling not possible')
                            return False
                    else:
                        print('Castling not possible')
                        return False

            if piece_name.rules(move_code, board):
                if type(piece_name) == Pawn and piece_name.en_passantable == True:      # ustawia pionek ze jest do zbicia
                    piece_name.pawn_move_counter = counter + 2                          # w przelocie w tej turze
                if type(piece_name) == Pawn and piece_name.en_passant_move == True and\
                    type(board[next_row + piece_name.en_passant_row_dir][next_column]) == Pawn and\
                        board[next_row + piece_name.en_passant_row_dir][next_column].en_passantable == True:
                            if board[next_row + piece_name.en_passant_row_dir][next_column].pawn_move_counter >\
                                board[next_row + piece_name.en_passant_row_dir][next_column].global_counter:
                                    board[next_row + piece_name.en_passant_row_dir][next_column] = blank
                                    piece_name.en_passant_move = False
                                    return True
                            else:
                                print('En passant not available')
                                return False
                return True

            else:
                print('Your move is against the rules')
                return False
        else:
            if piece_name.color != piece_destination.color:     # czy pionek docelowy jest innego koloru
                if piece_name.rules(move_code, board):
                    return True
                else:
                    print('Your move is against the rules')
                    return False
            else:
                print('Can\'t move on your own piece')
    else:
        print('Piece not selected')
        return False

def pawn_promotion(board, piece, row):
    if piece.color == 'W' and row[0] == 0 or\
        piece.color == 'B' and row[0] == 7:
        while True:
            promotion_input = input('You can promote the pawn to a Queen(q), Rook(r), Bishop(b) or Knight(n). Please select: ')
            if promotion_input == 'q':
                board[row[0]][row[1]] = Queen(piece.color)
                break
            elif promotion_input == 'r':
                board[row[0]][row[1]] = Rook(piece.color)
                break
            elif promotion_input == 'b':
                board[row[0]][row[1]] = Bishop(piece.color)
                break
            elif promotion_input == 'n':
                board[row[0]][row[1]] = Knight(piece.color)
                break
            else:
                print('Type \'q\', \'r\', \'b\' or \'n\'')

def castling(piece_color, cast_dir):
    short_castling = [[7,4],[7,5],[7,6],[7,7]] if piece_color == 'W' else [[0,4],[0,5],[0,6],[0,7]]
    long_castling = [[7,0],[7,1],[7,2],[7,3],[7,4]] if piece_color == 'W' else [[0,0],[0,1],[0,2],[0,3],[0,4]]
    between_short_castling = short_castling[1:-1]
    between_long_castling = long_castling[1:-1]

    # reversed translation
    dict_row = {
        '1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0
    }
    dict_column = {
        'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7
    }

    for row in board:
        for piece in row:
            piece_row = list(dict_row.keys())[list(dict_row.values()).index(board.index(row))]
            piece_column = list(dict_column.keys())[list(dict_column.values()).index(row.index(piece))]
            piece_pos = piece_column + piece_row
            if isinstance(piece,Piece):
                if piece_color != piece.color:
                    if cast_dir > 0:
                        for pos in short_castling:
                            piece_dest_row = list(dict_row.keys())[list(dict_row.values()).index(pos[0])]
                            piece_dest_column = list(dict_column.keys())[list(dict_column.values()).index(pos[1])]
                            piece_dest_pos = piece_dest_column + piece_dest_row
                            if pos in between_short_castling:
                                if type(board[pos[0]][pos[1]]) == Blank:
                                    if piece.rules(piece_pos + piece_dest_pos, board) == True:
                                        print('Castling not possible - position not safe')
                                        return False
                                    pass
                                else:
                                    print('Castling not possible - no free space between King and Rook')
                                    return False
                    else:
                        for pos in long_castling:
                            piece_dest_row = list(dict_row.keys())[list(dict_row.values()).index(pos[0])]
                            piece_dest_column = list(dict_column.keys())[list(dict_column.values()).index(pos[1])]
                            piece_dest_pos = piece_dest_column + piece_dest_row
                            if pos in between_long_castling:
                                if type(board[pos[0]][pos[1]]) == Blank:
                                    if piece.rules(piece_pos + piece_dest_pos, board) == True:
                                        print('Castling not possible - position not safe')
                                        return False
                                    pass
                                else:
                                    print('Castling not possible - no free space between King and Rook')
                                    return False
    return True

if __name__ == "__main__":
    init()
    build_board(board)
    print('Type your move (e.g. c2c3 - this moves white pawn from c2 to c3)')

    # ----------- IMPORT MOVES ------------- #
    # with open('your_file.txt', 'r', encoding="utf-8") as f:
    #     all_moves = f.readlines()
    #     move_test = all_moves[15]
    #     move_test = move_test.replace('\n',' ').split()

    while True:
        if counter % 2 == 0:
            print('White player')
        else:
            print(Style.RESET_ALL + Fore. RED + 'Red player' + Style.RESET_ALL)

        # ----------- PLAYER VS PLAYER ------------- #
        player_input = input('Your move: ')
        # ------------------------------------------ #
        
        # ---------------- TESTY ------------------- #
        # player_input = move_test[mt_index]
        # if player_input == '0-0':
        #     if counter % 2 == 0:
        #         player_input = 'e1g1'
        #     else:
        #         player_input = 'e8g8'
        # if player_input == '0-0-0':
        #     if counter % 2 == 0:
        #         player_input = 'e1c1'
        #     else:
        #         player_input = 'e8c8'
        # ------------------------------------------ #

        if not check_input(player_input):
            continue
        
        if is_move_valid(player_input, board):
            move(board, player_input)
        else:
            pass

        if isCheckmate:
            while True:
                build_board(board)
                print('Counter: ' + str(counter) + ' moves')
                play_again = input('Checkmate\nPlay again?(y/n): ')
                if play_again == 'n':
                    sys.exit()
                elif play_again == 'y':
                    board = [x[:] for x in start_board]
                    isCheckmate = False
                    counter = 0
                    break
                else:
                    print('Type \'y\' or \'n\'')


        build_board(board)
        print(f'\n{player_input[0].upper()}{player_input[1]} => {player_input[2].upper()}{player_input[3]}\n')

        # ---------------- TESTY ------------------- #
        # if mt_index < len(move_test) - 1:
        #     mt_index += 1
        # else:
        #     print('Finished')
        #     break
