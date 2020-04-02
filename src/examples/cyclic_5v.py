import time

from src.graph.graph import Graph
from src.vmtl_solver import VmtlSolver


def main():
    graph = Graph()
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(5, 1)

    time_start = time.time()
    solution: dict = VmtlSolver.find_first_vmtl_labeling(graph)
    print('time: ' + str(time.time() - time_start))
    print(dict(sorted(solution.items())))


if __name__ == '__main__':
    main()
