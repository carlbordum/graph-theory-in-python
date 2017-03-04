"""
    graphs
    ~~~~~~

    You are supposed to use the classes DirectedGraph and UndirectedGraph.
    This file is just my implementation after learning basic graph theory.

    Example:
        >>> edges = [('a', 'b'), ('a', 'c'), ('c', 'c')]
        >>> graph = UndirectedGraph(edges)  # you don't have to give it anything
        >>> print(graph)
        b: ['a']
        a: ['b', 'c']
        c: ['a', 'c']
        >>> graph.isolated_nodes()
        []
        >>> graph.add_node('d')
        >>> graph.isolated_nodes()
        ['d']
        >>> graph.depth_first_search('b', 'c')
        ['b', 'a', 'c']
        >>> graph.distance('a', 'b')
        1
        >>> graph.diameter()
        2

    A <class 'Graph'> object g exposes the following methods:
        isolated_nodes() -- a list with all isolated nodes
        add_node(node) -- node has to be hashable
        add_edge(n1, n2) -- add edge between n1 and n2
        depth_first_search(n1, n2) -- shortest path from n1 to n2
        node_degree(node) -- number of adjacent nodes
        delta() -- smallest node_degree in graph
        min_degree() -- alias for delta
        Delta() -- largest node_degree in graph
        max_degree() -- alias for Delta
        is_connected() -- True if all nodes are reachable
        distance(n1, n2) -- distance between two nodes
        diameter() -- distance between most distanced nodes
    And has the following properties...
        nodes -- list with all nodes
        edges -- list with all edges
    And overrides the magic methods...
        len(g) -- number of nodes
        str(g) -- return a pretty representation
        print(g) -- prints str(g)
    Furthermore a <class 'UndirectedGraph'> object has the method:
        degree_sequence() -- the degree sequence as a tuple


    :author: Carl Bordum Hansen
"""

from collections import defaultdict
from itertools import starmap, combinations


class Graph:
    """A graph consisting of nodes and edges."""
    def __init__(self, edges=None):
        self._graph = defaultdict(list)
        if edges:
            for edge in edges:
                self.add_edge(edge)

    def __str__(self):
        """
        a: ['b', 'c']
        b: ['a']
        c: ['a', 'c']
        """
        return '\n'.join(['%s: %s' % (str(k), str(v)) for k, v in self._graph.items()])

    def __len__(self):
        """Return the number of nodes."""
        return len(self._graph)

    @property
    def nodes(self):
        """Return a list of all nodes in the graph."""
        return list(self._graph)

    @property
    def edges(self):
        """Return a list of two element tuples of the connected nodes.

        [('a', 'b')] is one edge between node a and b."""
        edge_pairs = []
        for node, edges in self._graph.items():
            for edge in edges:
                edge_pairs.append((node, edge))
        return edge_pairs

    def add_node(self, node):
        """Add new node to graph. Nodes are automatically added, when you add an
        edge to a new node."""
        self._graph[node]

    def isolated_nodes(self):
        """Return a list with all isolated nodes."""
        nodes = []
        for node, edges in self._graph.items():
            if len(edges) == 0:
                for edge in self._graph.values():
                    if node in edge:
                        break
                else:
                    nodes.append(node)
        return nodes

    def depth_first_search(self, start_node, end_node, path=None):
        """Perform a depth first search to find the shortest path from *start_node*
        to *end_node*."""
        if path is None:
            path = []
        path.append(start_node)
        if start_node == end_node:
            return path
        if start_node not in self._graph:
            return None
        for node in self._graph[start_node]:
            if node not in path:
                return self.depth_first_search(node, end_node, path)

    def node_degree(self, node):
        """Return the number of adjacent nodes i.e. the number of edges connecting
        to *node* with loops counted twice."""
        return len(self._graph[node]) + self._graph[node].count(node)

    def delta(self):
        """Return the smallest degree of all nodes in the graph."""
        return min(map(self.node_degree, self._graph))

    min_degree = delta

    def Delta(self):
        """Return the biggest degree of all nodes in the graph."""
        return max(map(self.node_degree, self._graph))

    max_degree = Delta

    def is_connected(self):
        """Return True if you can reach all nodes from any node in the graph."""
        return len(self.isolated_nodes()) == 0

    def distance(self, start_node, end_node):
        """Return the distance between two nodes. -1 if no path is found."""
        dist = self.depth_first_search(start_node, end_node)
        if dist is None:
            return -1
        return len(dist) - 1

    def diameter(self):
        """Return the length between the most distanced nodes."""
        return max(starmap(self.distance, combinations(self._graph, 2)))


class UndirectedGraph(Graph):
    """In an undirected graph, edges are two-way."""
    def add_edge(self, edge):
        """Connect edge[0] with edge[1] and the other way."""
        edge = set(edge)
        node1 = edge.pop()
        if edge:
            node2 = edge.pop()
            self._graph[node1].append(node2)
            self._graph[node2].append(node1)
        else:
            self._graph[node1].append(node1)

    def degree_sequence(self):
        """Returns the degree sequence as a tuple. The degree sequence of an
        undirected graph is its node degrees in decending order."""
        return tuple(sorted(map(self.node_degree, self._graph), reverse=True))


class DirectedGraph(Graph):
    """In a directed graph, edges are one-way."""
    def add_edge(self, edge):
        """Connect edge[0] with edge[1]"""
        self.add_node(edge[1])  # so it is registered as a node
        self._graph[edge[0]].append(edge[1])
