import re


class Node:
    def __init__(self, node_id: str, x: float = 0, y: float = 0):
        self.edges: list = []
        self.id: int = int(re.search(r'[0-9]+', node_id).group())
        self.x: float = x
        self.y: float = y
        self.size: int = 10
        self.label: str = ''

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    def to_dict(self, id_as_label: bool) -> dict:
        if id_as_label:
            label = 'n' + str(self.id)
        else:
            label = self.label
        return {
            'id': 'n' + str(self.id),
            'label': label,
            'x': self.x,
            'y': self.y,
            'dX': 0,
            'dY': 0,
            'size': self.size
        }

    def is_connected(self, other):
        for edge in self.edges:
            if edge in other.edges:
                return edge
        return None

    @staticmethod
    def from_dict(node_dict: dict):
        node = Node(node_dict['id'], float(node_dict['x']), float(node_dict['y']))
        node.size = node_dict['size']
        if 'label' in node_dict:
            node.label = node_dict['label']
        return node
