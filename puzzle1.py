from collections import deque


class PuzzleState:
    def __init__(self, board, goal, cost=0, previous=None, move=None, zero_moves=0):
        self.board = board
        self.goal = goal
        self.cost = cost
        self.previous = previous
        self.move = move
        self.zero_moves = zero_moves

    def is_goal(self):
        return self.board == self.goal

    def neighbors(self):
        neighbors = []
        x, y = self.find_blank()
        moves = [(1, 0, 'up'), (-1, 0, 'down'), (0, 1, 'left'), (0, -1, 'right')]
        for dx, dy, move in moves:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_board = [row[:] for row in self.board]
                new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]
                zero_moves = self.zero_moves + 1 if new_board[new_x][new_y] == 0 else self.zero_moves
                neighbor = PuzzleState(new_board, self.goal, self.cost + 1, self, move, zero_moves)
                neighbors.append((move, neighbor))
        return neighbors

    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j


def is_solvable(board):
    inversions = 0
    blank_row = 0
    for i in range(9):
        for j in range(i + 1, 9):
            if board[j // 3][j % 3] and board[j // 3][j % 3] < board[i // 3][i % 3]:
                inversions += 1
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                blank_row = i
                break
    if blank_row % 2 == 0:
        solvable = inversions % 2 == 0
    else:
        solvable = inversions % 2 == 1

    return solvable, (blank_row, inversions)


def solve_puzzle(initial_state, goal_state):
    solvable, node = is_solvable(initial_state)
    if not solvable:
        return None, node

    initial_state = PuzzleState(initial_state, goal_state)
    queue = deque()
    queue.append(initial_state)
    visited = set()

    while queue:
        current_state = queue.popleft()
        if current_state.is_goal():
            moves = []
            while current_state.previous:
                moves.append((current_state.previous.board, current_state.previous.cost, current_state.move, current_state.previous.zero_moves))
                current_state = current_state.previous
            moves.reverse()
            return moves, node

        visited.add(str(current_state.board))

        for move, neighbor in current_state.neighbors():
            if str(neighbor.board) not in visited:
                queue.append(neighbor)

    return None, node


def print_solution(moves):
    zero_moves_total = 0
    for i, move in enumerate(moves):
        board, cost, move_name, zero_moves = move
        zero_moves_total += zero_moves
        print(f"Step {i + 1}: Move '{move_name}' at cost {cost} (Node numbers: {zero_moves_total})")
        print_board(board)
        print()

    print("Puzzle solved!")


def print_board(board):
    for row in board:
        print(' '.join(str(cell) for cell in row))
    print()


def get_input_state():
    board = []
    print("Enter the initial state (separate the numbers by spaces):")
    for _ in range(3):
        row = input().strip().split()
        board.append([int(cell) for cell in row])
    return board


def get_goal_state():
    board = []
    print("Enter the goal state (separate the numbers by spaces):")
    for _ in range(3):
        row = input().strip().split()
        board.append([int(cell) for cell in row])
    return board


def main():
    print("Welcome to 8-Puzzle Solver!")
    print("Enter the initial and goal states using numbers 0-8.")
    print("0 represents the blank space.")
    print()
    initial_state = get_input_state()
    goal_state = get_goal_state()

    moves, node = solve_puzzle(initial_state, goal_state)
    if not moves:
        print("The initial state is unsolvable.")
        print(f"Unsolvable node: Row {node[0] + 1}, Inversions {node[1]}")
        return

    print("Solving the puzzle...")
    print_solution(moves)


if __name__ == '__main__':
    main()
