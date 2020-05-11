import time

from src.graph.graph import Graph
from src.graph.vmtl_problem import VmtlProblem


def main():
    graph = Graph()
    vertex_count: int = 6
    for i in range(1, vertex_count + 1):
        for j in range(1, vertex_count + 1):
            if i == j:
                break
            graph.add_edge(i, j)

    vmtl_problem = VmtlProblem(graph)

    time_start = time.time()
    solution: dict = vmtl_problem.get_solution()
    print('time: ' + str(round(time.time() - time_start, 3)) + 's')
    print('time: ' + str(round(time.time() - time_start, 5) * 1000) + 'ms')
    print(dict(sorted(solution.items())))


if __name__ == '__main__':
    main()
