my_graph = {
    'A101': [('B102', 5), ('C103', 3), ('E105', 11)],
    'B102': [('A101', 5), ('C103', 1), ('F106', 2)],
    'C103': [('A101', 3), ('B102', 1), ('D104', 1), ('E105', 5)],
    'D104': [('C103',1 ), ('E105', 9), ('F106', 3), ('G107', 1)],
    'E105': [('A101', 11), ('C103', 5), ('D104', 9), ('G107', 2)],
    'F106': [('B102', 2), ('D104', 3), ('G107', 8)],
    'G107': [('E105', 2), ('D104', 1), ('F106', 8)]
}


def connect_path(path, start_node, last_node):
    if last_node == start_node:
        # use a set literal { } to avoid breaking the string into characters
        return {start_node}

    wanted_keys = set()
    for key in path:
        key_c = key.split("~")
        if key_c[0] == start_node and key_c[-1] == last_node:
            wanted_keys.add(key)
    return wanted_keys

def lowest_cost_path(path, start_Node, end_Node):
    if end_Node is None:
        print("An end_node has not specified, returning all paths found instead along their costs.")
        return path

    lowest_path_found = None
    lowest_cost_found = float('inf')
    for key in path:
        key_c = key.split("~")
        if key_c[0] == start_Node and key_c[-1] == end_Node:
            if path[key] < lowest_cost_found:
                lowest_path_found = key
                lowest_cost_found = path[key]
    return lowest_path_found, lowest_cost_found

def find_paths(graph, start_node, end_node=None):
    fully_visited = set() # ordering doesn't matter, sets are faster
    paths = {start_node: 0}
    to_visit = {node:1 if node==start_node else 0 for node in graph}

    while len(fully_visited) != len(graph):
        for node in to_visit:
            if to_visit[node]:
                for old_path in connect_path(paths, start_node, node):
                    for connected_node, cost in graph[node]:
                        if connected_node not in old_path:
                            to_visit[connected_node] += 1
                            paths[old_path + "~" + connected_node] = paths[old_path] + cost
            to_visit[node] -= 1
            fully_visited.add(node)

    return lowest_cost_path(paths, start_node, end_node)

# uncomment the next line for testing.
# print(find_paths(my_graph, 'A101', 'G107'))