import time

from src.graph.graph import Graph
from src.vmtl_problem import VmtlProblem


def main():
    graph = Graph()
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(5, 6)
    graph.add_edge(6, 1)

    vmtl_problem = VmtlProblem(graph)

    time_start = time.time()
    solution: dict = vmtl_problem.get_solution()
    print('time: ' + str(round(time.time() - time_start, 3)) + 's')
    print('time: ' + str(round(time.time() - time_start, 5) * 1000) + 'ms')
    print(dict(sorted(solution.items())))


if __name__ == '__main__':
    main()
