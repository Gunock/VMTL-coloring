import constraint

from src.graph.graph import Graph
from src.graph.node import Node


class VmtlProblem:
    _problem = constraint.Problem()

    def __init__(self, graph: Graph):
        self._setup_problem(graph)

    @staticmethod
    def _add_graph_to_problem(problem: constraint.Problem, graph: Graph) -> None:
        variable_names = []
        vertex_edge_count = len(graph.edges) + len(graph.nodes)
        colors = [i for i in range(1, vertex_edge_count + 1)]
        for node in graph.nodes.values():
            variable_names.append('v' + str(node))
            problem.addVariable('v' + str(node), colors)

        for edge in graph.edges:
            variable_names.append('e' + str(edge))
            problem.addVariable('e' + str(edge), colors)

    @staticmethod
    def _add_k_constraint(problem: constraint.Problem, node_1: Node, node_2: Node) -> None:
        # k for two vertices is same
        node_1_edges = [str(edge) for edge in node_1.edges]
        node_2_edges = [str(edge) for edge in node_2.edges]

        condition: str = "lambda "

        # Add lambda arguments
        for edge in node_1_edges:
            condition += 'e1_' + edge + ', '
        for edge in node_2_edges:
            condition += 'e2_' + edge + ', '
        condition += 'v' + str(1) + ', '
        condition += 'v' + str(2) + ': '

        # Add lambda body

        # k of first node and it's edges
        for edge in node_1_edges:
            condition += 'e1_' + str(edge) + ' + '
        condition += 'v' + str(1)

        condition += ' == '

        # k of second node and it's edges
        for edge in node_2_edges:
            condition += 'e2_' + edge + ' + '
        condition += 'v' + str(2)

        # Create list of constraint variables
        variables = ['e' + edge for edge in node_1_edges]
        variables += ['e' + edge for edge in node_2_edges]
        variables += ['v' + str(node_1), 'v' + str(node_2)]

        problem.addConstraint(eval(condition), variables)

    @staticmethod
    def _add_vmtl_constraints_to_problem(problem: constraint.Problem, graph: Graph) -> None:

        for edge_1 in graph.edges:
            for edge_2 in graph.edges:
                # Prevents duplicate constraints
                if edge_1 == edge_2:
                    break

                # Pair of edges have different labels
                problem.addConstraint(lambda e_1, e_2: e_1 != e_2, ['e' + str(edge_1), 'e' + str(edge_2)])

        for node_1 in graph.nodes.values():
            for edge in graph.edges:
                problem.addConstraint(lambda v, e: v != e, ['v' + str(node_1), 'e' + str(edge)])

            for node_2 in graph.nodes.values():
                # Prevents duplicate constraints
                if node_1 == node_2:
                    break

                # Pair of vertices have different labels
                problem.addConstraint(lambda v_1, v_2: v_1 != v_2, ['v' + str(node_1), 'v' + str(node_2)])

                # k for pair of vertices is the same
                VmtlProblem._add_k_constraint(problem, node_1, node_2)

    def _setup_problem(self, graph: Graph) -> None:
        self._problem = constraint.Problem()

        VmtlProblem._add_graph_to_problem(self._problem, graph)
        VmtlProblem._add_vmtl_constraints_to_problem(self._problem, graph)

    def get_solution(self) -> dict:
        solution: dict = self._problem.getSolution()
        return solution

    def get_solutions(self) -> dict:
        solution: dict = self._problem.getSolutions()
        return solution
