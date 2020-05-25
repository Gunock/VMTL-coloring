import json
import re
from typing import List, Dict

from src.graph.edge import Edge
from src.graph.node import Node


class Graph:
    def __init__(self):
        self.edges: Dict[int, Edge] = {}
        self.nodes: Dict[int, Node] = {}
        self.k: int = -1

    def __repr__(self):
        return str(self.to_dict())

    def to_dict(self, id_as_label: bool = False) -> dict:
        return {
            "nodes": [node.to_dict(id_as_label) for node in self.nodes.values()],
            "edges": [edge.to_dict(id_as_label) for edge in self.edges.values()]
        }

    def save_as_json(self, path: str = 'data/graph.json', id_as_label: bool = False) -> None:
        with open(path, "w+") as f:
            f.write(json.dumps(self.to_dict(id_as_label)))

    def create_edge_from_dict(self, edge_dict: dict) -> None:
        source_id = edge_dict['source']
        target_id = edge_dict['target']
        self.create_edge(source_id, target_id)
        if 'label' in edge_dict:
            self.set_edge_label(len(self.edges), edge_dict['label'])

    def create_edge(self, node_1_id: str, node_2_id: str) -> bool:
        node_1_id = int(re.search(r'[0-9]+', node_1_id).group())
        node_2_id = int(re.search(r'[0-9]+', node_2_id).group())
        if node_1_id not in self.nodes or node_2_id not in self.nodes:
            return False
        node_1 = self.nodes[node_1_id]
        node_2 = self.nodes[node_2_id]

        # Check if nodes are already in graph
        if node_1 not in self.nodes.values():
            self.nodes[node_1.id] = node_1
        if node_2 not in self.nodes.values():
            self.nodes[node_2.id] = node_2

        edge_1 = Edge(node_1, node_2, len(self.edges) + 1)
        edge_2 = Edge(node_2, node_1, len(self.edges) + 1)

        # check if edge is already in graph
        if edge_1 not in self.edges.values():
            self.edges[edge_1.id] = edge_1

        # check if edge is already in connected nodes
        if edge_1 not in self.nodes[node_1.id].edges:
            self.nodes[node_1.id].edges.append(edge_1)

        # check if edge is already in connected nodes
        if edge_2 not in self.nodes[node_2.id].edges:
            self.nodes[node_2.id].edges.append(edge_2)
        return True

    def create_node(self, x_pos: float, y_pos: float) -> None:
        node = Node(len(self.nodes) + 1, x_pos, y_pos)
        self.add_node(node)

    def add_node(self, node: Node) -> None:
        if node not in self.nodes.values():
            self.nodes[node.id] = node
        else:
            self.nodes[node.id].x = node.x
            self.nodes[node.id].y = node.y

    def delete_node(self, node_id: str) -> bool:
        node_id = int(re.search(r'[0-9]+', node_id).group())
        if node_id not in self.nodes:
            return False

        while len(self.nodes[node_id].edges) > 0:
            self.delete_edge(str(self.nodes[node_id].edges[0]))
        del self.nodes[node_id]
        self.reset_ids()
        return True

    def delete_edge(self, edge_id: str) -> bool:
        edge_id = int(re.search(r'[0-9]+', edge_id).group())
        if edge_id not in self.edges:
            return False
        edge = self.edges[edge_id]
        self.nodes[edge.source.id].edges.remove(edge)
        self.nodes[edge.target.id].edges.remove(edge)
        del self.edges[edge_id]
        self.reset_ids()
        return True

    def set_node_label(self, node_id: int, label: str) -> None:
        if node_id in self.nodes:
            self.nodes[node_id].label = label

    def set_edge_label(self, edge_id: int, label: str) -> None:
        if edge_id not in self.edges:
            return

        self.edges[edge_id].label = label
        for i in range(0, len(self.nodes[self.edges[edge_id].source.id].edges)):
            if self.nodes[self.edges[edge_id].source.id].edges[i].id == edge_id:
                self.nodes[self.edges[edge_id].source.id].edges[i].label = label
        for i in range(0, len(self.nodes[self.edges[edge_id].target.id].edges)):
            if self.nodes[self.edges[edge_id].target.id].edges[i].id == edge_id:
                self.nodes[self.edges[edge_id].target.id].edges[i].label = label

    def max_edges(self) -> int:
        result: int = 0
        for node in self.nodes.values():
            if len(node.edges) > result:
                result = len(node.edges)
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

    def is_path(self) -> bool:
        if len(self.edges) != len(self.nodes) - 1:
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

        return True

    def is_complete(self) -> bool:
        matrix: List[list] = self._to_reduced_matrix()
        for row in matrix:
            for cell in row:
                if cell != 1:
                    return False
        return True

    def is_vmtl(self) -> bool:
        previous_k = None
        for node in self.nodes.values():
            current_k = sum([int(node.label)] + [int(edge.label) for edge in node.edges])
            if current_k != previous_k and previous_k is not None:
                return False
        return True

    def is_empty(self) -> bool:
        return len(self.nodes) == 0

    def reset_labels(self) -> None:
        for node_key in self.nodes:
            self.nodes[node_key].label = ''
        for edge_key in self.edges:
            self.edges[edge_key].label = ''

    def reset_ids(self) -> None:
        graph_new = Graph()
        node_ids_map = {}
        for key in self.nodes:
            node = self.nodes[key]
            graph_new.create_node(node.x, node.y)
            node_id_new = graph_new.nodes[list(graph_new.nodes.keys())[-1]].id
            node_ids_map[key] = str(node_id_new)
        for key in self.edges:
            edge = self.edges[key]
            graph_new.create_edge(node_ids_map[edge.source.id], node_ids_map[edge.target.id])
        self.nodes = graph_new.nodes
        self.edges = graph_new.edges

    def _to_dict(self) -> dict:
        matrix_dict: dict = {}
        for node_1 in self.nodes.values():
            matrix_dict[node_1.id] = {}
            for node_2 in self.nodes.values():
                matrix_dict[node_1.id][node_2.id] = 0

        for edge in self.edges.values():
            matrix_dict[edge.source.id][edge.target.id] = 1
            matrix_dict[edge.target.id][edge.source.id] = 1
        return matrix_dict

    def _to_matrix(self) -> list:
        matrix_dict = self._to_dict()

        result: list = []
        for key_1 in matrix_dict:
            result.append([1])
            for key_2 in matrix_dict[key_1]:
                result[len(result) - 1].append(matrix_dict[key_1][key_2])
        return result

    def _to_reduced_matrix(self) -> list:
        result = self._to_matrix()
        i: int = 0
        while i < len(result):
            j: int = i + 1
            while j < len(result[i]):
                del result[i][j]
            i += 1
        return result

    @staticmethod
    def from_dict(input_data: dict):
        graph: Graph = Graph()
        for node_dict in input_data['nodes']:
            node: Node = Node.from_dict(node_dict)
            graph.add_node(node)
        if 'edges' in input_data:
            for edge_dict in input_data['edges']:
                graph.create_edge_from_dict(edge_dict)
        return graph

    @staticmethod
    def load_from_json(path: str = 'data/graph.json'):
        with open(path, "r") as f:
            file_content = f.read()
        if file_content is None:
            file_content = '{}'
        return Graph.from_dict(json.loads(file_content))

    @staticmethod
    def generate_cyclic(n: int):
        graph = Graph()
        for i in range(1, n + 1):
            graph.add_node(Node(i))
        for i in range(1, n + 1):
            graph.create_edge(str(i), str(i % n + 1))
        return graph

    @staticmethod
    def generate_path(n: int):
        graph = Graph()
        for i in range(1, n + 1):
            graph.add_node(Node(i))
        for i in range(1, n):
            graph.create_edge(str(i), str(i + 1))
        return graph

    @staticmethod
    def generate_complete(n: int):
        graph = Graph()
        for i in range(1, n + 1):
            graph.add_node(Node(i))
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if i == j:
                    break
                graph.create_edge(str(i), str(j))
        return graph
