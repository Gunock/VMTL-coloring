from src.graph.node import Node


class Edge:
    def __init__(self, origin: Node, target: Node, edge_id: int):
        self.source: Node = origin
        self.target: Node = target
        self.id: int = edge_id
        self.label: str = ''

    def __eq__(self, other):
        first_condition = self.source.id == other.source.id \
                          and self.target.id == other.target.id
        second_condition = self.source.id == other.target.id \
                           and self.target.id == other.source.id
        return first_condition or second_condition

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    def to_dict(self) -> dict:
        return {
            'id': 'e' + str(self.id),
            'source': 'n' + str(self.source),
            'target': 'n' + str(self.target),
            'label': self.label
        }
