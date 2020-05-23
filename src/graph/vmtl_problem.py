import re

import constraint

from src.graph.graph import Graph
from src.graph.node import Node


class VmtlProblem:

    def __init__(self, graph: Graph):
        self._problem = constraint.Problem()
        self._graph: Graph = graph
        if graph.is_empty():
            return
        self._setup_problem()

    def get_solution(self) -> Graph:
        if self._graph.is_empty():
            return Graph()
        solution: dict = self._problem.getSolution()
        if not solution:
            return Graph()
        return self._solution_to_graph(solution)

    def _setup_problem(self) -> None:
        self._problem = constraint.Problem()
        VmtlProblem._add_k_variable(self._problem, self._graph)
        VmtlProblem._add_graph_to_problem(self._problem, self._graph)
        VmtlProblem._add_vmtl_constraints_to_problem(self._problem, self._graph)

    def _solution_to_graph(self, solution: dict) -> Graph:
        result: Graph = self._graph
        for key in solution:
            if 'k' in key:
                continue
            element_id = int(re.search(r'[0-9]+', key).group())
            if 'n' in key:
                result.set_node_label(element_id, str(solution[key]))
            elif 'e' in key:
                result.set_edge_label(element_id, str(solution[key]))
        result.k = solution['k']
        return result

    @staticmethod
    def _get_k_range(graph: Graph) -> list:
        vertex_count = len(graph.nodes)
        edge_count = len(graph.edges)
        vertex_edge_count = vertex_count + edge_count
        max_edges = graph.max_edges()
        k_max = ((max_edges + 1) * vertex_edge_count - sum(range(1, max_edges + 1))) + 1

        left_side = VmtlProblem._binomial(vertex_edge_count + 1, 2) + VmtlProblem._binomial(edge_count + 1, 2)
        right_side = 2 * VmtlProblem._binomial(vertex_edge_count + 1, 2) + VmtlProblem._binomial(vertex_count + 1, 2)

        return [i for i in range(sum(range(1, max_edges + 1)), k_max) if left_side <= i * vertex_count <= right_side]

    @staticmethod
    def _binomial(n, k) -> int:
        if not 0 <= k <= n:
            return 0
        b = 1
        for t in range(min(k, n - k)):
            b *= n
            b /= t + 1
            n -= 1
        return int(b)

    @staticmethod
    def _add_graph_to_problem(problem: constraint.Problem, graph: Graph) -> None:
        vertex_edge_count = len(graph.edges) + len(graph.nodes)
        colors = [i for i in range(1, vertex_edge_count + 1)]

        for node in graph.nodes.values():
            problem.addVariable('n' + str(node), colors)

        for edge in graph.edges:
            problem.addVariable('e' + str(edge), colors)

    @staticmethod
    def _add_k_variable(problem: constraint.Problem, graph: Graph) -> None:
        if graph.is_cyclic():
            vertex_count = len(graph.nodes)
            known_k = 0
            if vertex_count % 2 == 1:
                known_k = 3 * vertex_count + 1
            elif vertex_count % 4 == 2:
                known_k = 2.5 * vertex_count + 2
            elif vertex_count % 4 == 0:
                known_k = 3 * vertex_count
            possible_k = [known_k]
        else:
            possible_k = VmtlProblem._get_k_range(graph)
            if graph.is_complete():
                possible_k = list(filter(lambda elem: elem % 4 == 0, possible_k))

        problem.addVariable('k', possible_k)

    @staticmethod
    def _add_k_constraint(problem: constraint.Problem, graph: Graph) -> None:
        for node in graph.nodes.values():
            node_edges = ['e' + str(edge) for edge in node.edges]
            problem.addConstraint(lambda v, k, *e: v + sum(e) == k, ['n' + str(node), 'k'] + node_edges)

    @staticmethod
    def _add_vertex_pair_k_constraint(problem: constraint.Problem, node_1: Node, node_2: Node) -> None:
        # k for two vertices is same
        node_1_edges = [str(edge) for edge in node_1.edges]
        node_2_edges = [str(edge) for edge in node_2.edges]

        condition: str = "lambda "

        # Add lambda arguments
        for edge in node_1_edges:
            condition += 'e1_' + edge + ', '
        for edge in node_2_edges:
            condition += 'e2_' + edge + ', '
        condition += 'n' + str(1) + ', '
        condition += 'n' + str(2) + ': '

        # Add lambda body

        # k of first node and it's edges
        for edge in node_1_edges:
            condition += 'e1_' + str(edge) + ' + '
        condition += 'n' + str(1)

        condition += ' == '

        # k of second node and it's edges
        for edge in node_2_edges:
            condition += 'e2_' + edge + ' + '
        condition += 'n' + str(2)

        # Create list of constraint variables
        variables = ['e' + edge for edge in node_1_edges]
        variables += ['e' + edge for edge in node_2_edges]
        variables += ['n' + str(node_1), 'n' + str(node_2)]

        problem.addConstraint(eval(condition), variables)

    @staticmethod
    def _add_vmtl_constraints_to_problem(problem: constraint.Problem, graph: Graph) -> None:
        problem.addConstraint(constraint.AllDifferentConstraint())

        # vertex and it's edge count equals k
        VmtlProblem._add_k_constraint(problem, graph)
        for node_1 in graph.nodes.values():
            for node_2 in graph.nodes.values():
                # Prevents duplicate constraints
                if node_1 == node_2:
                    break

                if not graph.is_cyclic():
                    # k for pair of vertices is the same
                    VmtlProblem._add_vertex_pair_k_constraint(problem, node_1, node_2)
