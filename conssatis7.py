import tkinter as tk
from tkinter import messagebox
import itertools

def correct_vals(p, puzzle):
    op1, op, op2, e, r = break_puzzle(puzzle.translate(p))
    return eval(op1 + op + op2 + "==" + r)

def break_puzzle(puzzle):
    return tuple(puzzle.upper().split())

def get_unique_letters(puzzle):
    return [i for i in set(''.join(break_puzzle(puzzle))) if i.isalpha()]

def get_starting_letters(puzzle, letters):
    return [i for i in range(len(letters)) if letters[i] == break_puzzle(puzzle)[0][0] or letters[i] == break_puzzle(puzzle)[2][0] or letters[i] == break_puzzle(puzzle)[4][0]]

def get_valid_permutations(puzzle):
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    letters = get_unique_letters(puzzle)
    critical_indices = get_starting_letters(puzzle, letters)
    poss_perms = []
    for perm in itertools.permutations(digits, len(letters)):
        flag = 0
        for i in critical_indices:
            if perm[i] == '0':
                flag = 1
                break
        if flag == 0:
            poss_perms.append(perm)
    return poss_perms

def solve_puzzle():
    user_puzzle = entry_puzzle.get()
    letters = get_unique_letters(user_puzzle)
    if len(letters) > 10:
        messagebox.showerror("Error", "Invalid equation: More than one letter maps to the same digit")
        return

    solutions = []

    for poss in get_valid_permutations(user_puzzle):
        p = str.maketrans(''.join(letters), ''.join(poss))
        if correct_vals(p, user_puzzle):
            answer = dict(zip(letters, poss))
            solutions.append(answer)

    if not solutions:
        messagebox.showinfo("Solution", "No solution found.")
        return

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Possible solutions:\n")
    
    for i, answer in enumerate(solutions, start=1):
        result_text.insert(tk.END, f"Solution {i}:\n")
        result_text.insert(tk.END, "Letter Values:\n")
        for letter, value in answer.items():
            result_text.insert(tk.END, f"{letter} = {value}\n")
        
        result_text.insert(tk.END, "Equation:\n")
        for step in user_puzzle.split(' + '):
            for c in step:
                result_text.insert(tk.END, answer.get(c, c))
            result_text.insert(tk.END, " + ")
        result_text.insert(tk.END, "= ")
        for c in user_puzzle.split(' = ')[1]:
            result_text.insert(tk.END, answer.get(c, c))
        result_text.insert(tk.END, "\n\n")

# Create the main window
root = tk.Tk()
root.title("Alphametic Puzzle Solver")

# Create and pack widgets
label_instruction = tk.Label(root, text="Enter your alphametic puzzle:")
label_instruction.pack()

entry_puzzle = tk.Entry(root)
entry_puzzle.pack()

button_solve = tk.Button(root, text="Solve", command=solve_puzzle)
button_solve.pack()

result_text = tk.Text(root, height=15, width=50)
result_text.pack()

# Start the GUI main loop
root.mainloop()
