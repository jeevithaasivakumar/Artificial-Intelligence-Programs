class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name, heuristic):
        self.nodes[name] = {'heuristic': heuristic, 'neighbors': {}}

    def add_edge(self, node1, node2, cost):
        if node1 not in self.nodes or node2 not in self.nodes:
            raise ValueError("Node not in graph.")
        self.nodes[node1]['neighbors'][node2] = cost
        self.nodes[node2]['neighbors'][node1] = cost

    def get_neighbors(self, node):
        return self.nodes[node]['neighbors']

    def heuristic_cost(self, node):
        return self.nodes[node]['heuristic']


def find_all_paths(graph, start, goal):
    stack = [(start, [start], 0)]  # (current, path, total_cost)
    all_paths = []

    while stack:
        current, path, total_cost = stack.pop()

        if current == goal:
            all_paths.append((path, total_cost))
        else:
            for neighbor, cost in graph.get_neighbors(current).items():
                if neighbor not in path:
                    new_cost = total_cost + cost
                    stack.append((neighbor, path + [neighbor], new_cost))

    return all_paths


def a_star(graph, start, goal):
    open_list = [(0, start, [])]  # (f = g + h, node, path)
    closed_set = set()

    while open_list:
        _, current, path = min(open_list)
        open_list = [item for item in open_list if item[1] != current]
        closed_set.add(current)

        if current == goal:
            return path + [current]

        for neighbor, cost in graph.get_neighbors(current).items():
            if neighbor not in closed_set:
                g = len(path) + cost
                h = graph.heuristic_cost(neighbor)
                f = g + h
                open_list.append((f, neighbor, path + [current]))

    return None  # No path found


def parse_input_node_data(input_string):
    node_data = input_string.split()
    nodes = node_data[::2]   #DATASETS
    heuristics = [int(heuristic) for heuristic in node_data[1::2]]
    return nodes, heuristics


if __name__ == "__main__":
    graph = Graph()

    # Taking input for the graph nodes and their heuristic values
    nodes_input = input("Enter node names and their heuristic values: ")
    nodes, heuristics = parse_input_node_data(nodes_input)

    for node, heuristic in zip(nodes, heuristics):
        graph.add_node(node, heuristic)

    num_edges = int(input("Enter the number of edges: "))
    for i in range(num_edges):
        edge_input = input(f"Enter nodes connected by edge {i + 1} and the cost : ")
        node1, node2, cost = edge_input.split()
        cost = int(cost)
        graph.add_edge(node1, node2, cost)

    start_node = input("Enter the start node: ")
    goal_node = input("Enter the goal node: ")

    # Finding all possible paths using DFS approach
    all_paths = find_all_paths(graph, start_node, goal_node)

    # Displaying all possible paths and their heuristic costs
    print("\nAll possible paths and their heuristic costs:")
    for path, total_cost in all_paths:
        path_str = " -> ".join(path)
        print(f"{path_str}, Heuristic Cost: {total_cost}")

    # Finding the shortest path using A* algorithm
    shortest_path = a_star(graph, start_node, goal_node)

    if shortest_path:
        print("\nShortest path:", " -> ".join(shortest_path))
    else:
        print("\nNo path found.")
