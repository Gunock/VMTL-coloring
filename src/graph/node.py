class Node:
    def __init__(self, node_id: int, x: float = 0, y: float = 0):
        self.edges: list = []
        self.id: int = node_id
        self.x: float = x
        self.y: float = y
        self.label: str = ''

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    def to_dict(self) -> dict:
        return {
            'id': 'n' + str(self.id),
            'label': self.label,
            'x': self.x,
            'y': self.y,
            'size': 10
        }

    def is_connected(self, other):
        for edge in self.edges:
            if edge in other.edges:
                return edge
        return None
