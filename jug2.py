class State:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.action = None

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


def solve_water_jug_problem(x_cap, y_cap, target_x, target_y):
    visited = set()
    stack = []
    initial_state = State(0, 0)
    stack.append(initial_state)

    while stack:
        current_state = stack.pop()

        if current_state in visited:
            continue

        visited.add(current_state)

        if current_state.x == target_x and current_state.y == target_y:
            return current_state

        # Fill jug X
        if current_state.x < x_cap:
            new_state = State(x_cap, current_state.y)
            new_state.parent = current_state
            new_state.action = "Fill X"
            stack.append(new_state)

        # Fill jug Y
        if current_state.y < y_cap:
            new_state = State(current_state.x, y_cap)
            new_state.parent = current_state
            new_state.action = "Fill Y"
            stack.append(new_state)

        # Empty jug X
        if current_state.x > 0:
            new_state = State(0, current_state.y)
            new_state.parent = current_state
            new_state.action = "Empty X"
            stack.append(new_state)

        # Empty jug Y
        if current_state.y > 0:
            new_state = State(current_state.x, 0)
            new_state.parent = current_state
            new_state.action = "Empty Y"
            stack.append(new_state)

        # Transfer from X to Y
        if current_state.x > 0 and current_state.y < y_cap:
            transfer_amount = min(current_state.x, y_cap - current_state.y)
            new_state = State(current_state.x - transfer_amount, current_state.y + transfer_amount)
            new_state.parent = current_state
            new_state.action = f"Transfer X to Y ({transfer_amount})"
            stack.append(new_state)

        # Transfer from Y to X
        if current_state.y > 0 and current_state.x < x_cap:
            transfer_amount = min(current_state.y, x_cap - current_state.x)
            new_state = State(current_state.x + transfer_amount, current_state.y - transfer_amount)
            new_state.parent = current_state
            new_state.action = f"Transfer Y to X ({transfer_amount})"
            stack.append(new_state)

    return None


def print_solution(final_state):
    if final_state is None:
        print("No solution found. The target amount is not reachable from the initial state")
        return

    steps = []
    current_state = final_state
    while current_state.parent:
        steps.append((current_state.action, current_state))
        current_state = current_state.parent

    steps.reverse()
    print(f"Solution steps ({len(steps)} steps):")
    for i, (action, state) in enumerate(steps):
        print(f"Step {i + 1}: {action}. Jug status: {state}")

    print("Puzzle solved!")


def main():
    print("Welcome to the Water Jug problem solver!")
    x_cap = int(input("Enter the capacity of Jug X: "))
    y_cap = int(input("Enter the capacity of Jug Y: "))
    target_x = int(input("Enter the target amount for Jug X: "))
    target_y = int(input("Enter the target amount for Jug Y: "))

    final_state = solve_water_jug_problem(x_cap, y_cap, target_x, target_y)
    print_solution(final_state)


if __name__ == '__main__':
    main()
