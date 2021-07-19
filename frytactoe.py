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


# TODO prompt for game mode (human vs PC, human vs human, PC vs PC?)
game_board = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]


def get_cell(board, row_index, col_index):
    return board[row_index][col_index]


def set_cell(board, row_index, col_index, value):
    board[row_index][col_index] = value


def get_free_cell_count(board):
    count = 0
    for row in board:
        for col in row:
            count += 1 if col == '-' else 0
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
    if current_value != '-':
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
    return '-'


def take_computer_turn(board):
    # TODO give more sophisticated behavior, maybe ability to set difficulty?
    # randomly search cells until free cell is found
    computers_move = randint(0, 2), randint(0, 2)
    while not move_is_valid(board, computers_move):
        computers_move = randint(0, 2), randint(0, 2)
    set_cell(board, computers_move[0], computers_move[1], 'O')


print_board(game_board)

while True:
    # Person's Turn
    unparsed_move = input("Your move (e.g. 'b2'): ")
    # TODO validate input, case insensitive?
    move = parse_move(unparsed_move)
    while not move_is_valid(game_board, move):
        print('Invalid move, cell already chosen. Try again.')
        unparsed_move = input("Your move (e.g. 'b2'): ")
        move = parse_move(unparsed_move)
    set_cell(game_board, move[0], move[1], 'X')
    # TODO refactor out duplicated code below
    print_board(game_board)
    winner = get_winner(game_board)
    if winner != '-':
        print('#### Game over! The winner is: ' + winner + ' ####')
        break
    if get_free_cell_count(game_board) == 0:
        print("#### It's a tie! ####")
        break

    # Computer's Turn
    sleep(1)
    print("Computer's turn...")
    sleep(2)
    take_computer_turn(game_board)
    # TODO refactor out duplicated code below
    print_board(game_board)
    winner = get_winner(game_board)
    if winner != '-':
        print('#### Game over! The winner is: ' + winner + ' ####')
        break
    if get_free_cell_count(game_board) == 0:
        print("#### It's a tie! ####")
        break

    # TODO Add play again option
