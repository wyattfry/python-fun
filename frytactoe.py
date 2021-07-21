#!/usr/bin/env python3

from os import system, name
from random import randint
from time import sleep


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def new_game_board(width = 3, height = 3, unplayed_letter = '-'):
    return [[unplayed_letter for i in range(width)] for j in range(height)]


def get_cell(board, row_index, col_index):
    return board[row_index][col_index]


def set_cell(board, row_index, col_index, value, unplayed_letter):
    current_value = board[row_index][col_index]
    if current_value != unplayed_letter:
        raise RuntimeError('Cannot play a cell that is already played.')
    board[row_index][col_index] = value


def get_free_cell_count(board, unplayed_letter):
    count = 0
    for row in board:
        for col in row:
            count += 1 if col == unplayed_letter else 0
    return count


def parse_move(_unparsed_move):
    column_map = {
        "a": 0,
        "b": 1,
        "c": 2
    }
    column_index = column_map.get(_unparsed_move[0])
    row_index = int(_unparsed_move[1]) - 1
    return row_index, column_index


def print_board(board):
    # clear()
    print("\n\nFry Tac Toe!")
    print('   A B C')
    row_number=1
    for row in board:
        # TODO color code X and O ? for make pretty?
        print(str(row_number) + ' |' + '|'.join(row) + '|')
        row_number += 1


def move_is_valid(board, _move, unplayed_letter):
    current_value = get_cell(board, _move[0], _move[1])
    if current_value != unplayed_letter:
        return False
    return True


def get_winner(board, unplayed_letter):
    # Return X, O, or -
    # Check rows
    for index in (0, 1, 2):
        if board[index][0] == board[index][1] and board[index][1] == board[index][2]:
            return board[index][0]
    # Check columns
    for index in (0, 1, 2):
        if board[0][index] == board[1][index] and board[1][index] == board[2][index]:
            return board[0][index]
    # Check diagonals
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[1][1]
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[1][1]
    return unplayed_letter
    

def get_winning_cell(board, player_letter, unplayed_letter, for_opponent = False):
    """Get first found (row_index, col_index) of cell that would win the game or None"""
    # Check rows
    for ridx, row in enumerate(board):
        player_letter_count = 0
        unplayed_letter_count = 0
        unplayed_letter_idx = -1
        for cidx, col in enumerate(row):
            current_cell = col
            if for_opponent:
                player_letter_count += 1 if current_cell != player_letter and current_cell != unplayed_letter else 0
            else:
                player_letter_count += 1 if current_cell == player_letter else 0
            if current_cell == unplayed_letter:
                unplayed_letter_count += 1
                unplayed_letter_idx = cidx
            if player_letter_count == len(row) - 1 and unplayed_letter_count == 1:
                return (ridx, unplayed_letter_idx) 
    # Check cols
    for cidx, col in enumerate(board[0]):
        player_letter_count = 0
        unplayed_letter_count = 0
        unplayed_letter_idx = -1
        for ridx, row in enumerate(board):
            current_cell = row[cidx]
            if for_opponent:
                player_letter_count += 1 if current_cell != player_letter and current_cell != unplayed_letter else 0
            else:
                player_letter_count += 1 if current_cell == player_letter else 0
            if current_cell == unplayed_letter:
                unplayed_letter_count += 1
                unplayed_letter_idx = ridx
            if player_letter_count == len(row) - 1 and unplayed_letter_count == 1:
                return (unplayed_letter_idx, cidx) 
    # Check diag NW (assumes a square board)
    side_length = len(board)
    player_letter_count = 0
    unplayed_letter_count = 0
    unplayed_letter_idx = -1
    for i in range(side_length):
        current_cell = board[i][i]
        if for_opponent:
            player_letter_count += 1 if current_cell != player_letter and current_cell != unplayed_letter else 0
        else:
            player_letter_count += 1 if current_cell == player_letter else 0
        if current_cell == unplayed_letter:
            unplayed_letter_count += 1
            unplayed_letter_idx = i
        if player_letter_count == len(row) - 1 and unplayed_letter_count == 1:
            return (unplayed_letter_idx, unplayed_letter_idx)
    # Check diag NE (assumes a square board)
    player_letter_count = 0
    unplayed_letter_count = 0
    unplayed_letter_idx = -1
    for i in range(side_length):
        current_cell = board[side_length - 1 - i][i]
        if for_opponent:
            player_letter_count += 1 if current_cell != player_letter and current_cell != unplayed_letter else 0
        else:
            player_letter_count += 1 if current_cell == player_letter else 0
        if current_cell == unplayed_letter:
            unplayed_letter_count += 1
            unplayed_letter_idx = (side_length - 1 - i, i)
        if player_letter_count == len(row) - 1 and unplayed_letter_count == 1:
            return unplayed_letter_idx


def take_human_turn(board, player_letter, player_name, unplayed_letter):
    # Person's Turn
    prompt_text = player_name + "'s move [" + player_letter + "] (e.g. 'b2'): "
    unparsed_move = input(prompt_text)
    # TODO validate input, case insensitive?
    move = parse_move(unparsed_move)
    while not move_is_valid(board, move, unplayed_letter):
        print('Invalid move, cell already chosen. Try again.')
        unparsed_move = input(prompt_text)
        move = parse_move(unparsed_move)
    set_cell(board, move[0], move[1], player_letter, unplayed_letter)


def take_computer_turn(board, player_letter, player_name, unplayed_letter):
    board_width = len(board[0])
    board_height = len(board)
    # https://www.wikihow.com/Win-at-Tic-Tac-Toe
    sleep(0.5)
    print(player_name + "'s move [" + player_letter + "] (computer)...")
    sleep(1)

    # check for 1-move away from wins, first for self, then for opponent
    for b in [False, True]:
        cell_for_win = get_winning_cell(board, player_letter, unplayed_letter, for_opponent=b)
        if cell_for_win:
            set_cell(board, cell_for_win[0], cell_for_win[1], player_letter, unplayed_letter)
            return

    total_cell_count = board_height * board_width
    played_cell_count = total_cell_count - get_free_cell_count(board, unplayed_letter)

    if played_cell_count == 0:
        # empty board, choose random corner
        row = 0 if randint(0, 1) == 0 else board_width - 1
        col = 0 if randint(0, 1) == 0 else board_height - 1
        set_cell(board, row, col, player_letter, unplayed_letter)
        return

    center_row_index = int((board_width - 1) / 2)
    center_col_index = int((board_height - 1) / 2)
    center_cell_value = get_cell(board, center_row_index, center_col_index)
    if played_cell_count == 1 and center_cell_value != player_letter and center_cell_value != unplayed_letter:
        # center is played, choose random corner
        row = 0 if randint(0, 1) == 0 else board_width - 1
        col = 0 if randint(0, 1) == 0 else board_height - 1
        set_cell(board, row, col, player_letter, unplayed_letter)
        return

    if played_cell_count == 1 and center_cell_value == unplayed_letter:
        # center is not played, choose center
        set_cell(board, center_row_index, center_col_index, player_letter, unplayed_letter)
        return

    if played_cell_count == 2 and center_cell_value != player_letter:
        # play opposite corner
        for rc in [(0, 0), (0, board_width - 1), (board_height - 1, board_width - 1), (board_width - 1, 0)]:
            if get_cell(board, rc[0], rc[1]) == player_letter:
                opposite_row = 0 if rc[0] != 0 else board_width - 1
                opposite_col = 0 if rc[1] != 0 else board_height - 1
                set_cell(board, opposite_row, opposite_col, player_letter, unplayed_letter)
                return

    # if all else fails, make random move
    rand_row = randint(0, board_height - 1)
    rand_col = randint(0, board_width - 1)
    while not move_is_valid(board, (rand_row, rand_col), unplayed_letter):
        rand_row = randint(0, board_height - 1)
        rand_col = randint(0, board_width - 1)
    print('Default move, random. r/c: ', rand_row, rand_col)
    set_cell(board, rand_row, rand_col, player_letter, unplayed_letter)
    return

def evaluate_board(board, unplayed_letter) -> bool:
    """Checks the board after a play for a win condition
    
    :param board: the game board, a 2D list
    :return: bool. whether the game is over
    """
    print_board(board)
    winner = get_winner(board, unplayed_letter)
    if winner != unplayed_letter:
        print('#### Game over! The winner is: ' + winner + ' ####')
        return True
    if get_free_cell_count(board, unplayed_letter) == 0:
        print("#### It's a tie! ####")
        return True
    return False

def main():
    board_height = 3
    board_width = 3
    player1_letter = 'X'
    player2_letter = 'O'
    unplayed_letter = '-'
    player1=''
    player2=''
    print('Fry Tac Toe')
    valid_input = ['h', 'c']
    while player1 not in valid_input:
        player1 = input("Player 1 human (default) or computer? [H/c]: ").lower() or 'h'
    while player2 not in valid_input:
        player2 = input("Player 2 human or computer (default)? [h/C]: ").lower() or 'c'

    play_order = [player1, player2]

    game_board = new_game_board(board_width, board_height, unplayed_letter)
    print_board(game_board)

    while True:
        if play_order[0] == 'h':
            take_human_turn(game_board, player1_letter, 'Player 1', unplayed_letter) 
        else:
            take_computer_turn(game_board, player1_letter, 'Player 1', unplayed_letter)
        if evaluate_board(game_board, unplayed_letter):
            break

        if play_order[1] == 'h':
            take_human_turn(game_board, player2_letter, 'Player 2', unplayed_letter) 
        else:
            take_computer_turn(game_board, player2_letter, 'Player 2', unplayed_letter)
        if evaluate_board(game_board, unplayed_letter):
            break

        # TODO Add play again option

if __name__ == '__main__':
    main()