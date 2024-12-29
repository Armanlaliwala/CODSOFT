import streamlit as st
import numpy as np

# Initialize the game board
def initialize_board():
    return np.full((3, 3), " ")

# Check for winner
def check_winner(board):
    # Check rows
    for row in board:
        if len(set(row)) == 1 and row[0] != " ":
            return row[0]
    # Check columns
    for col in board.T:
        if len(set(col)) == 1 and col[0] != " ":
            return col[0]
    # Check diagonals
    if len(set([board[i, i] for i in range(3)])) == 1 and board[0, 0] != " ":
        return board[0, 0]
    if len(set([board[i, 2 - i] for i in range(3)])) == 1 and board[0, 2] != " ":
        return board[0, 2]
    return None

# Check if the board is full
def is_full(board):
    return " " not in board

# Evaluate the board for Minimax (1 = AI win, -1 = player win, 0 = draw)
def evaluate(board):
    winner = check_winner(board)
    if winner == "X":
        return 1  # AI win
    elif winner == "O":
        return -1  # Player win
    else:
        return 0  # Draw

# Minimax Algorithm
def minimax(board, depth, is_maximizing):
    score = evaluate(board)
    if score != 0:  # If the game is over, return the score
        return score

    if is_full(board):
        return 0  # Draw

    if is_maximizing:
        best = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i, j] == " ":
                    board[i, j] = "X"
                    best = max(best, minimax(board, depth + 1, False))
                    board[i, j] = " "
        return best
    else:
        best = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i, j] == " ":
                    board[i, j] = "O"
                    best = min(best, minimax(board, depth + 1, True))
                    board[i, j] = " "
        return best

# AI move using Minimax
def ai_move(board):
    best_val = -float("inf")
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i, j] == " ":
                board[i, j] = "X"
                move_val = minimax(board, 0, False)
                board[i, j] = " "
                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)

    return best_move

# Streamlit App
st.title("Tic-Tac-Toe")
st.write("You are 'O' and the AI is 'X'. Try to beat the AI!")

# Add custom styles for better visuals
st.markdown(
    """
    <style>
    .stButton>button {
        height: 50px;
        width: 50px;
        font-size: 20px;
        margin: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state variables if they are not already initialized
if "board" not in st.session_state:
    st.session_state.board = initialize_board()
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "winner" not in st.session_state:
    st.session_state.winner = None
if "turn" not in st.session_state:
    st.session_state.turn = "O"  # Player's turn starts first

# Display the game board
def display_board():
    board = st.session_state.board
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            key = f"{i}-{j}"  # Unique key for each button
            if board[i, j] == " " and not st.session_state.game_over:
                if st.session_state.turn == "O":  # Human player's turn
                    if cols[j].button(" ", key=key):
                        board[i, j] = "O"
                        winner = check_winner(board)
                        if winner:
                            st.session_state.winner = winner
                            st.session_state.game_over = True
                        elif is_full(board):
                            st.session_state.winner = "Draw"
                            st.session_state.game_over = True
                        else:
                            st.session_state.turn = "X"  # Switch to AI's turn
                else:  # AI's turn
                    cols[j].button(" ", key=key, disabled=True)  # Disable button during AI's move
            else:
                # Display existing marks (O, X, or empty)
                cols[j].button(board[i, j], key=key, disabled=True)

    # If AI's turn, let it make a move
    if st.session_state.turn == "X" and not st.session_state.game_over:
        with st.spinner("AI is thinking..."):  # Show spinner while AI calculates
            move = ai_move(board)
        if move != (-1, -1):  # Safeguard in case no valid move is found
            board[move] = "X"
            winner = check_winner(board)
            if winner:
                st.session_state.winner = winner
                st.session_state.game_over = True
            elif is_full(board):
                st.session_state.winner = "Draw"
                st.session_state.game_over = True
            else:
                st.session_state.turn = "O"  # Switch to player's turn

display_board()

# Show the result
if st.session_state.game_over:
    if st.session_state.winner == "Draw":
        st.success("It's a draw!")
    else:
        st.success(f"The winner is {st.session_state.winner}!")
    
    # Restart button
    if st.button("Restart"):
        # Reset the board and game state properly
        st.session_state.board = initialize_board()
        st.session_state.game_over = False
        st.session_state.winner = None
        st.session_state.turn = "O"  # Reset to player's turn
