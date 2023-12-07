
def parse_input_node_data(input_string):
    node_data = input_string.split()
    nodes = node_data[::2]
    heuristics = [int(heuristic) for heuristic in node_data[1::2]]
    return nodes, heuristics

def Cost(H, condition, weight=1):
    cost = {}
    if 'AND' in condition:
        AND_nodes = condition['AND']
        Path_A = ' AND '.join(AND_nodes)
        PathA = sum(H[node] + weight for node in AND_nodes if node in H)
        cost[Path_A] = PathA

    if 'OR' in condition:
        OR_nodes = condition['OR']
        Path_B = ' OR '.join(OR_nodes)
        PathB = min(H[node] + weight for node in OR_nodes if node in H)
        cost[Path_B] = PathB
    return cost

def update_cost(H, Conditions, weight=1):
    Main_nodes = list(Conditions.keys())
    Main_nodes.reverse()
    least_cost = {}
    for key in Main_nodes:
        condition = Conditions[key]
        print(f"Node {key}: {Conditions[key]} <-- {Cost(H, condition, weight)}")
        c = Cost(H, condition, weight)
        H[key] = min(c.values())
        least_cost[key] = Cost(H, condition, weight)
    return least_cost
def shortest_path(Start, Updated_cost, H, exploring=None):
    if exploring is None:
        exploring = []

    Path = Start
    while Start in Updated_cost.keys():
        Min_cost = min(Updated_cost[Start].values())
        key = list(Updated_cost[Start].keys())
        values = list(Updated_cost[Start].values())
        Index = values.index(Min_cost)

        # FIND MINIMUM PATH KEY
        Next = key[Index].split()
        # ADD TO PATH FOR OR PATH
        if len(Next) == 1:
            Start = Next[0]
            if Start not in exploring:  # Check if the node has already been explored
                exploring.append(Start)
                Path += ' <-- ' + Start
        # ADD TO PATH FOR AND PATH
        else:
            Path += ' <-- (' + key[Index] + ') '
            for node in Next:
                if node not in exploring:  # Check if the node has already been explored
                    exploring.append(node)
                    Path += '[' + node + ' + '

            # Remove the trailing ' + ' and close the parentheses
            Path = Path[:-3]
            Path += ']'
 
    return Path

# Rest of your code remains the same


# Rest of your code remains the same

if __name__ == "__main__":
    H = {}
    Conditions = {}

    nodes_input = input("Enter node names and their heuristic values: ")
    nodes, heuristics = parse_input_node_data(nodes_input)

    for node, heuristic in zip(nodes, heuristics):
        H[node] = heuristic

    num_conditions = int(input("Enter the number of conditions: "))
    for _ in range(num_conditions):
        node = input("Enter node name: ")
        condition_type = input(f"Does node {node} have an AND or OR condition? (Type 'AND' or 'OR'): ").upper()
        if condition_type == 'AND':
            condition_nodes = input(f"Enter nodes separated by space for AND condition: ").split()
            Conditions[node] = {'AND': condition_nodes}
        elif condition_type == 'OR':
            condition_nodes = input(f"Enter nodes separated by space for OR condition: ").split()
            Conditions[node] = {'OR': condition_nodes}
        else:
            print("Invalid input. Please enter 'AND' or 'OR'.")

    weight = int(input("Enter weight for calculation: "))   # WEIGHT FOR THAT CALCULATION

    print("\nInitial Cost (H):")
    for node, cost in H.items():
        print(f"{node}: {cost}")

    print("\nUpdated Cost:")
    Updated_cost = update_cost(H, Conditions, weight)
    for node, cost in H.items():
        print(f"{node}: {cost}")

    print("--" * 75)
    print("Shortest Path:\n", shortest_path('A', Updated_cost, H))
