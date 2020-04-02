from typing import List, Dict

from src.graph.edge import Edge
from src.graph.node import Node


class Graph:
    edges: List[Edge]
    nodes: Dict[int, Node]

    def __init__(self):
        self.edges = []
        self.nodes = {}

    def add_edge(self, node_1_id: int, node_2_id: int):
        node_1 = Node(node_1_id)
        node_2 = Node(node_2_id)

        # Check if nodes are already in graph
        if node_1 not in self.nodes.values():
            self.nodes[node_1.id] = node_1
        if node_2 not in self.nodes.values():
            self.nodes[node_2.id] = node_2

        edge_1 = Edge(node_1, node_2, len(self.edges) + 1)
        edge_2 = Edge(node_2, node_1, len(self.edges) + 1)

        # check if edge is already in graph
        if edge_1 not in self.edges:
            self.edges.append(edge_1)

        # check if edge is already in connected nodes
        if edge_1 not in self.nodes[node_1.id].edges:
            self.nodes[node_1.id].edges.append(edge_1)
        if edge_2 not in self.nodes[node_2.id].edges:
            self.nodes[node_2.id].edges.append(edge_2)

    def _to_dict(self):
        matrix_dict: dict = {}
        for node_1 in self.nodes.values():
            matrix_dict[node_1.id] = {}
            for node_2 in self.nodes.values():
                matrix_dict[node_1.id][node_2.id] = 0

        for edge in self.edges:
            matrix_dict[edge.origin.id][edge.target.id] = 1
            matrix_dict[edge.target.id][edge.origin.id] = 1
        return matrix_dict

    def _to_matrix(self):
        matrix_dict = self._to_dict()

        result: list = []
        for key_1 in matrix_dict:
            result.append([1])
            for key_2 in matrix_dict[key_1]:
                result[len(result) - 1].append(matrix_dict[key_1][key_2])
        return result

    def _to_reduced_matrix(self):
        result = self._to_matrix()
        i: int = 0
        while i < len(result):
            j: int = i + 1
            while j < len(result[i]):
                del result[i][j]
            i += 1
        return result

    def is_cyclic(self) -> bool:
        if len(self.nodes) != len(self.edges):
            return False

        matrix: List[list] = self._to_reduced_matrix()

        # cut first column
        matrix.pop(0)
        for row in matrix:
            del row[0]

        # check axis
        i: int = 0
        while i < len(matrix):
            if matrix[i][i] == 0:
                return False
            i += 1

        # check left lower corner
        if matrix[i - 1][0] == 0:
            return False

        return True
