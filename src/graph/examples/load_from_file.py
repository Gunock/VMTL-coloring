from src.graph.graph import Graph


def main():
    graph: Graph = Graph.load_from_json()
    print(graph)


if __name__ == '__main__':
    main()
