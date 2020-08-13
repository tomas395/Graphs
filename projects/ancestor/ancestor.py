class Graph:
    def __init__(self):
        self.vertices = {}
        # add an adjacency list

    def add_vertex(self, vertex_id):
        if vertex_id not in self.vertices:  # in case we have a grandparent in the set, we wouldnt want to override it, so we add an if
            self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("Vertex does not exist!")

    def get_neighbors(self, vertex_id):
        return self.vertices[vertex_id]


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)

# Implement the graph and the stack from util or you can just use get_neighbors
# Nodes = people
# Edges = when a child has a parent
# If you wanted to go with either BFS or DFS. For DFS, you can use a Stack, but for BFS you can use a Queue
# The longest path will be our earliest ancestor/eldest
# Build a path like we did earlier in search
# But we dont know when to stop until we've seen everyone
# I should have gone BFS in hindsight.


def build_graph(ancestors):
    graph = Graph()
    for parent, child in ancestors:  # tuple unpacking
        graph.add_vertex(parent)
        graph.add_vertex(child)
        graph.add_edge(child, parent)
        # add an edge connecting every child to the parent if they have one
    return graph


def earliest_ancestor(ancestors, starting_node):
    graph = build_graph(ancestors)
    s = Stack()
    visited = set()
    s.push([starting_node])
    longest_path = 1
    elder = -1

    # start the DFS
    while s.size() > 0:
        path = s.pop()
        vertex = path[-1]
    # keep track of the longest length to find our earliest ancestor/eldest
    # if the path is longer or is == but the value is smaller
        if len(path) > longest_path or (len(path) == longest_path and vertex < elder):
            longest_path = len(path)
            elder = vertex

        if vertex not in visited:
            visited.add(vertex)
            parents = graph.get_neighbors(vertex)

            for parent in parents:
                new_path = path + [parent]
                s.push(new_path)
    return elder








# BFS Version
# def earliest_ancestor(ancestors, starting_node):
#     graph = Graph()
#     for pair in ancestors:
#         graph.add_vertex(pair[0])
#         graph.add_vertex(pair[1])
#         graph.add_edge(pair[0], pair[1])

#     # Do a BFS Storing the path

#     q = Queue()
#     q.enqueue([starting_node])
#     max_path_length = 1
#     earliest_anc = -1

#     while q.size() > 0:
#         path = q.dequeue()
#         v = path[-1]
#         if (len(path) >= max_path_length and v < earliest_anc) or (len(path) > max_path_length):
#             earliest_anc = v
#             max_path_length = len(path)
#             for neighbor in graph.vertices[v]:
#                 path_copy = list(path)
#                 path_copy.append(neighbor)
#                 q.enqueue(path_copy)
#     return earliest_anc
