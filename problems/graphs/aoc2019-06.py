"""
Starter code for Advent of Code 2019 Day #6

You must implement functions part1 and part2
"""

import sys
import os


#### Part 1 ####

def count_orbiters(orbits: dict[str, str], orbited: str) -> int:
    """
    Recursive helper function for counting number of orbits. 

    Parameters:
    - orbits: a dictionary mapping an object name (e.g., "B")
              to the name of the object it orbits (e.g., "COM")
    - orbited: the name of the orbited object

    Returns an integer
    """

    if orbited not in orbits:
        return 1
    else:
        return 1 + count_orbiters(orbits, orbits[orbited])


def part1(orbits: dict[str, str]) -> int:
    """
    Solves Part 1 (see problem statement for more details)

    Parameter:
    - orbits: a dictionary mapping an object name (e.g., "B")
              to the name of the object it orbits (e.g., "COM")

    Returns an integer
    """

    d = {}
    for orbiter in orbits:
        orbited = orbits[orbiter]
        d[orbiter] = count_orbiters(orbits, orbited)
    
    return sum(d.values())


#### Part 2 ####

class Vertex:
    '''
    Vertex class to represent an orbit.

    Attributes:
        name [str]: name of the current orbit
        edges_to [set]: set of orbits that the current orbit
                            orbits around
    '''
    name: str
    edges_to: set['Vertex']
    
    def __init__(self, name: str):
        self.name = name
        self.edges_to = set()

    def add_edge_to(self, dest: 'Vertex') -> None:
        self.edges_to.add(dest)

    def has_edge_to(self, dest: 'Vertex') -> bool:
        return dest in self.edges_to


class Graph:
    '''
    Graph class to represent the map of orbits.

    Attributes:
        vertices [dict]: a dictionary mapping an object name (e.g., "B")
              to the name of the object it orbits (e.g., "COM")
    '''
    vertices: dict[str, Vertex]

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex: Vertex) -> None:
        self.vertices[vertex.name] = vertex
    
    def get_vertex(self, name: str) -> Vertex|None: 
        return self.vertices.get(name)


def make_graph(orbits: dict[str, str]) -> Graph:
    '''
    Helper function for converting orbits dictionary
    into a graph

    Parameter:
    - orbits: a dictionary mapping an object name (e.g., "B")
              to the name of the object it orbits (e.g., "COM")

    Returns an undirected, unweighted graph
    '''
    g = Graph()

    for orbiter in orbits:
        if not g.get_vertex(orbiter):
            v = Vertex(orbiter)
            g.add_vertex(v)
        else:
            v = g.get_vertex(orbiter)

        if not g.get_vertex(orbits[orbiter]):
            o = Vertex(orbits[orbiter])
            g.add_vertex(o)
        else:
            o = g.get_vertex(orbits[orbiter])

        v.add_edge_to(o)
        o.add_edge_to(v)
        
    return g


def bfs(graph: Graph, start: str, dest: str) -> int:
    '''
    Helper function for returning length of shorted path
    between two objects using BFS

    Parameter:
    - graph: undirected, unweighted graph object representing
            the map of orbits
    - start: starting node of the BFS
    - dest: end node of the BFS

    Returns the shortest distance
    '''
    queue: list[str] = [start]
    visited: set[str] = {start}
    dist: dict[str, int] = {start: 0}
    
    while queue:
        name = queue.pop()
        v = graph.get_vertex(name)

        for neighbor in v.edges_to:
            if neighbor.name == dest:
                return dist[name] - 1
            
            if neighbor.name not in visited: 
                visited.add(neighbor.name)
                queue.append(neighbor.name)
                dist[neighbor.name] = dist[name] + 1


def part2(orbits: dict[str, str]):
    """
    Solves Part 2 (see problem statement for more details)

    Parameter:
    - orbits: a dictionary mapping an object name (e.g., "B")
              to the name of the object it orbits (e.g., "COM")

    Returns an integer
    """
    graph = make_graph(orbits)
    return bfs(graph, 'YOU', 'SAN')



############################################
###                                      ###
###      Do not modify the code below    ###
###                EXCEPT                ###
###    to comment/uncomment the calls    ###
###        to the functions above        ###
###                                      ###
############################################


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"USAGE: python3 {os.path.basename(sys.argv[0])} <INPUT FILE>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"ERROR: No such file: {input_file}")
        sys.exit(1)

    with open(input_file) as f:
        lines = f.read().strip().split("\n")
        objs = [line.split(")") for line in lines]
        orbits = {}
        for p1, p2 in objs:
            orbits[p2] = p1

    print(f"Part 1:", part1(orbits))
    
    # Uncomment the following line when you're ready to work on Part 2
    print(f"Part 2:", part2(orbits))
