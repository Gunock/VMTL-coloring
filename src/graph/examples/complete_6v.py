import time

from src.graph.graph import Graph
from src.graph.vmtl_problem import VmtlProblem


def main():
    graph = Graph.generate_complete(6)

    time_start = time.time()
    solution: Graph = VmtlProblem(graph).get_solution()
    print('time: ' + str(round(time.time() - time_start, 3)) + 's')
    print('time: ' + str(round(time.time() - time_start, 5) * 1000) + 'ms')
    print(solution)


if __name__ == '__main__':
    main()
