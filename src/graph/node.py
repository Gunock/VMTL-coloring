class Node:
    id: int
    edges: list

    def __init__(self, node_id):
        self.edges = []
        self.id = node_id

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    def is_connected(self, other):
        for edge in self.edges:
            if edge in other.edges:
                return edge
        return None
