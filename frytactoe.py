#!/usr/bin/env python3

from os import system, name
from random import randint
from time import sleep

board_height = 3
board_width = 3
player1_letter = 'X'
player2_letter = 'O'
unplayed_letter = '-'

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


# TODO prompt for game mode (human vs PC, human vs human, PC vs PC?)
game_board = [[unplayed_letter for i in range(board_width)] for j in range(board_height)]

def get_cell(board, row_index, col_index):
    return board[row_index][col_index]


def set_cell(board, row_index, col_index, value):
    board[row_index][col_index] = value


def get_free_cell_count(board):
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
    clear()
    print("Fry Tac Toe!")
    print('   A B C')
    row_number=1
    for row in board:
        # TODO color code X and O ? for make pretty?
        print(str(row_number) + ' |' + '|'.join(row) + '|')
        row_number += 1


def move_is_valid(board, _move):
    current_value = get_cell(board, _move[0], _move[1])
    if current_value != unplayed_letter:
        return False
    return True


def get_winner(board):
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

def take_human_turn(board, player_letter, player_name):
    # Person's Turn
    prompt_text = player_name + "'s move [" + player_letter + "] (e.g. 'b2'): "
    unparsed_move = input(prompt_text)
    # TODO validate input, case insensitive?
    move = parse_move(unparsed_move)
    while not move_is_valid(game_board, move):
        print('Invalid move, cell already chosen. Try again.')
        unparsed_move = input(prompt_text)
        move = parse_move(unparsed_move)
    set_cell(game_board, move[0], move[1], player_letter)


def take_computer_turn(board, player_letter, player_name):
    # https://www.wikihow.com/Win-at-Tic-Tac-Toe
    sleep(0.5)
    print(player_name + "'s move [" + player_letter + "] (computer)...")
    sleep(1)
    # TODO give more sophisticated behavior, maybe ability to set difficulty?
    # randomly search cells until free cell is found
    total_cell_count = board_height * board_width
    played_cell_count = total_cell_count - get_free_cell_count(board)

    if played_cell_count == 0:
        # empty board, choose random corner
        row = 0 if randint(0, 1) == 0 else board_width - 1
        col = 0 if randint(0, 1) == 0 else board_height - 1
        set_cell(board, row, col, player_letter)

    center_row_index = int((board_width - 1) / 2)
    center_col_index = int((board_height - 1) / 2)
    center_cell_value = get_cell(board, center_row_index, center_col_index)
    if played_cell_count == 1 and center_cell_value != player_letter:
        # center is played, choose random corner
        row = 0 if randint(0, 1) == 0 else board_width - 1
        col = 0 if randint(0, 1) == 0 else board_height - 1
        set_cell(board, row, col, player_letter)

    if played_cell_count == 1 and center_cell_value == unplayed_letter:
        # center is not played, choose center
        set_cell(board, center_row_index, center_col_index, player_letter)

    if played_cell_count == 2 and center_cell_value != player_letter:
        # play opposite corner
        for rc in [(0, 0), (0, board_width - 1), (board_height - 1, board_width - 1), (board_width - 1, 0)]:
            if get_cell(board, rc[0], rc[1]) == player_letter:
                opposite_row = 0 if rc[0] != 0 else board_width - 1
                opposite_col = 0 if rc[1] != 0 else board_height - 1
                set_cell(board, opposite_row, opposite_col, player_letter)

def evaluate_board(board) -> bool:
    """Checks the board after a play for a win condition
    
    :param board: the game board, a 2D list
    :return: bool. whether the game is over
    """
    print_board(game_board)
    winner = get_winner(game_board)
    if winner != unplayed_letter:
        print('#### Game over! The winner is: ' + winner + ' ####')
        return True
    if get_free_cell_count(game_board) == 0:
        print("#### It's a tie! ####")
        return True
    return False

player1 = input("Fry Tac Toe\nPlayer 1 human or computer? [H/c]: ") or 'h'
player2 = input("Player 2 human or computer? [h/C]: ") or 'c'

play_order = [player1, player2]

print_board(game_board)

while True:
    if play_order[0] == 'h':
        take_human_turn(game_board, player1_letter, 'Player 1') 
    else:
        take_computer_turn(game_board, player1_letter, 'Player 1')
    if evaluate_board(game_board):
        break

    if play_order[1] == 'h':
        take_human_turn(game_board, player2_letter, 'Player 2') 
    else:
        take_computer_turn(game_board, player2_letter, 'Player 2')
    if evaluate_board(game_board):
        break

    # TODO Add play again option
