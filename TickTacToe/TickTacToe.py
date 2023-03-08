import random
from flask import Flask, render_template, request
import random

app = Flask(__name__)

def print_board(board):
    print(board[0] + " | " + board[1] + " | " + board[2])
    print("--|---|--")
    print(board[3] + " | " + board[4] + " | " + board[5])
    print("--|---|--")
    print(board[6] + " | " + board[7] + " | " + board[8])

def is_winner(board, player):
    # Check all the winning combinations
    return ((board[0] == player and board[1] == player and board[2] == player) or
            (board[3] == player and board[4] == player and board[5] == player) or
            (board[6] == player and board[7] == player and board[8] == player) or
            (board[0] == player and board[3] == player and board[6] == player) or
            (board[1] == player and board[4] == player and board[7] == player) or
            (board[2] == player and board[5] == player and board[8] == player) or
            (board[0] == player and board[4] == player and board[8] == player) or
            (board[2] == player and board[4] == player and board[6] == player))

def get_player_move(board):
    while True:
        move = input("Enter your move (0-8): ")
        if move.isnumeric():
            move = int(move)
            if move >= 0 and move <= 8 and board[move] == " ":
                return move
        print("Invalid move. Try again.")

def get_computer_move(board, computer_player):
    # Check if the computer can win on the next move
    for i in range(9):
        if board[i] == " ":
            board[i] = computer_player
            if is_winner(board, computer_player):
                return i
            else:
                board[i] = " "

    # Check if the player could win on their next move, and block them.
    for i in range(9):
        if board[i] == " ":
            board[i] = "X" if computer_player == "O" else "O"
            if is_winner(board, "X" if computer_player == "O" else "O"):
                board[i] = computer_player
                return i
            else:
                board[i] = " "

    # Try to take one of the corners
    corners = [0, 2, 6, 8]
    random.shuffle(corners)
    for corner in corners:
        if board[corner] == " ":
            return corner

    # Try to take the center
    if board[4] == " ":
        return 4

    # Take any empty square
    for i in range(9):
        if board[i] == " ":
            return i

def play_game():
    print("Welcome to Tic Tac Toe!")
    while True:
        board = [" "] * 9
        players = ["X", "O"]
        random.shuffle(players)
        computer_player = players[0]
        print("You are playing against the computer, which is " + computer_player)
        print_board(board)
        while True:
            # Player's turn
            player_move = get_player_move(board)
            board[player_move] = players[1]
            print_board(board)

            if is_winner(board, players[1]):
                print("Congratulations! You won!")
                break

            if " " not in board:
                print("It's a tie!")
                break

            # Computer's turn
            print("Computer's turn...")
            computer_move = get_computer_move(board, computer_player)
            board[computer_move] = computer_player

            print_board(board)

            if is_winner(board, computer_player):
                print("Sorry, you lost. Better luck next time!")
                break

            if " " not in board:
                print("It's a tie!")
                break

        play_again = input("Do you want to play again? (y/n) ")
        if play_again.lower() != "y":
            break

play_game()