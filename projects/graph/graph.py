"""
Simple graph implementation
"""


from util import Stack, Queue  # These may come in handy


class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("Vertex does not exist!")

    def get_neighbors(self, vertex_id):
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        # create an empty queue and enqueue a starting vertex
        q = Queue()
        q.enqueue(starting_vertex)
        # create a set to store the visited vertices
        visited = set()
        # while the queue is not empty
        while q.size():
            # dequeue the first vertex
            v = q.dequeue()
            if v not in visited:
                # mark the vertex as visited
                visited.add(v)
                # print it for debug
                print(v)
                # add all of it's neighbors to the back of the queue
                for next_vertex in self.get_neighbors(v):
                    q.enqueue(next_vertex)

    def dft(self, starting_vertex):
        # create an empty stack and push a starting vertex
        s = Stack()
        s.push(starting_vertex)
        # create a set to store the visited vertices
        visited = set()
        # while the stack is not empty
        while s.size():
            # pop the first vertex
            v = s.pop()
            # if vertex has not been visited
            if v not in visited:
                # mark the vertex as visited
                visited.add(v)
                # print it for debug
                print(v)
                # add all of it's neighbors to the top of the stack
                for next_vertex in self.get_neighbors(v):
                    s.push(next_vertex)

    def dft_recursive(self, starting_vertex, visited=None):
        # need to add == None so it doesnt add extra child processes when it's called
        if visited is None:
            visited = set()
        visited.add(starting_vertex)
        print(starting_vertex)

        for v in self.get_neighbors(starting_vertex):
            if v not in visited:
                self.dft_recursive(v, visited)

    def bfs(self, starting_vertex, destination_vertex):
        # create an empty queue and enqueue PATH To the Starting Vertex ID
        q = Queue()
        q.enqueue([starting_vertex])
        # create a set to store visited vertices
        visited = set()
        # while queue not empty
        while q.size() > 0:
            # dequeue the first PATH
            path = q.dequeue()
            # get the last vertex from the path
            current_node = path[-1]
            # check if the node hasn't been visited
            if current_node not in visited:
                # is this vertex the target?
                if current_node == destination_vertex:
                    # return the path
                    return path
                # mark it as visited
                visited.add(current_node)
                # add a path to its neighbors to the back of the queue
                for neighbor in self.vertices[current_node]:
                    # copy the path so we don't mutate the original path for different nodes
                    current_path = path.copy()
                    # append the neighbor to the back of the path
                    current_path.append(neighbor)
                    q.enqueue(current_path)

    def dfs(self, starting_vertex_id, target_vertex_id):
        # create an empty stack and push PATH To the Starting Vertex ID
        s = Stack()
        s.push([starting_vertex_id])
        # create a set to store visited vertices
        visited = set()
        # while the stack is not empty
        while s.size() > 0:
            # pop the first PATH
            path = s.pop()
            # grab the last vertex from the Path
            v = path[-1]
            # check if the vertex has not been visited
            if v not in visited:
                # is this vertex the target?
                if v == target_vertex_id:
                    # return the path
                    return path
                # mark it as visited
                visited.add(v)
                # then add A Path to its neighbors to the back of the queue
                for next_v in self.get_neighbors(v):
                    # make a copy of the path
                    path_copy = list(path)
                    # append the neighbor to the end of the path
                    path_copy.append(next_v)
                    # push out new path
                    s.push(path_copy)
        return None

    def dfs_recursive(self, starting_vertex, destination_vertex, visited=set(), path=[]):
        visited.add(starting_vertex)
        # add the node in path
        path = path + [starting_vertex]
        # base case
        # is the node our target?
        if starting_vertex == destination_vertex:
            # if yes, return
            return path
        # for each node's neighbor
        for neighbor in self.get_neighbors(starting_vertex):
            # is the node visited?
            if neighbor not in visited:
                # if no, recurse and get the new path
                new_path = self.dfs_recursive(neighbor, destination_vertex, visited, path)
                # is the new path None?
                if new_path is not None:
                    # if not none, return
                    return new_path


if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
