import time

from src.graph.graph import Graph
from src.graph.vmtl_problem import VmtlProblem


def benchmark_complete_graph(n: int):
    print()
    print('graph vertex count = ' + str(n))
    graph = Graph.generate_complete(n)

    time_start = time.time()
    solution: Graph = VmtlProblem(graph).get_solution()
    print('time: ' + str(round(time.time() - time_start, 3)) + 's')
    print('time: ' + str(round(time.time() - time_start, 5) * 1000) + 'ms')


def main():
    benchmark_complete_graph(4)
    benchmark_complete_graph(5)
    benchmark_complete_graph(6)


if __name__ == '__main__':
    main()
