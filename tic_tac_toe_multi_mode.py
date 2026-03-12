import tkinter as tk
from tkinter import messagebox
import random


# Global Variables
human = "X"
ai = "O"
current_player = human
board = [""] * 9
mode = None  # "HUMAN" or "AI"

win_positions = [
    (0,1,2), (3,4,5), (6,7,8),
    (0,3,6), (1,4,7), (2,5,8),
    (0,4,8), (2,4,6)
]


# Check Winner
def check_winner():
    for a, b, c in win_positions:
        if board[a] == board[b] == board[c] != "":
            return board[a]
    if "" not in board:
        return "Draw"
    return None


# AI Logic
def ai_move():
    # Win
    for i in range(9):
        if board[i] == "":
            board[i] = ai
            if check_winner() == ai:
                buttons[i]["text"] = ai
                return
            board[i] = ""

    # Block
    for i in range(9):
        if board[i] == "":
            board[i] = human
            if check_winner() == human:
                board[i] = ai
                buttons[i]["text"] = ai
                return
            board[i] = ""

    # Center
    if board[4] == "":
        board[4] = ai
        buttons[4]["text"] = ai
        return

    # Random
    empty = [i for i in range(9) if board[i] == ""]
    move = random.choice(empty)
    board[move] = ai
    buttons[move]["text"] = ai


# Button Click
def on_click(index):
    global current_player

    if board[index] != "":
        return

    board[index] = current_player
    buttons[index]["text"] = current_player

    result = check_winner()
    if result:
        end_game(result)
        return

    if mode == "AI" and current_player == human:
        current_player = ai
        window.after(300, ai_turn)
    else:
        current_player = "O" if current_player == "X" else "X"


# AI Turn
def ai_turn():
    global current_player
    ai_move()
    result = check_winner()
    if result:
        end_game(result)
    else:
        current_player = human


# End Game
def end_game(result):
    if result == "Draw":
        messagebox.showinfo("Game Over", "It's a Draw!")
    else:
        winner = "Player X" if result == "X" else "Player O"
        if mode == "AI" and result == ai:
            winner = "Computer"
        messagebox.showinfo("Game Over", f"{winner} Wins!")
    reset_game()


# Reset Game
def reset_game():
    global board, current_player
    board = [""] * 9
    current_player = human
    for btn in buttons:
        btn["text"] = ""


# Mode Selection
def start_game(selected_mode):
    global mode
    mode = selected_mode
    menu.destroy()
    create_game_ui()


# Game UI
def create_game_ui():
    global window, buttons
    window = tk.Tk()
    window.title("Tic-Tac-Toe")

    buttons = []
    for i in range(9):
        btn = tk.Button(
            window,
            text="",
            font=("Arial", 24),
            width=5,
            height=2,
            command=lambda i=i: on_click(i)
        )
        btn.grid(row=i//3, column=i%3)
        buttons.append(btn)

    window.mainloop()


# Main Menu
menu = tk.Tk()
menu.title("Select Game Mode")

tk.Label(menu, text="Tic-Tac-Toe", font=("Arial", 20)).pack(pady=10)

tk.Button(
    menu, text="Human vs Human",
    font=("Arial", 14),
    width=20,
    command=lambda: start_game("HUMAN")
).pack(pady=5)

tk.Button(
    menu, text="Human vs Computer",
    font=("Arial", 14),
    width=20,
    command=lambda: start_game("AI")
).pack(pady=5)

menu.mainloop()
