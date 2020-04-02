from src.graph.node import Node


class Edge:
    origin: Node
    target: Node
    id: int

    def __init__(self, origin: Node, target: Node, edge_id: int):
        self.origin = origin
        self.target = target
        self.id = edge_id

    def __eq__(self, other):
        first_condition = self.origin.id == other.origin.id \
                          and self.target.id == other.target.id
        second_condition = self.origin.id == other.target.id \
                           and self.target.id == other.origin.id
        return first_condition or second_condition

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)
