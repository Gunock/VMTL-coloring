import constraint
import numpy as np

from src.graph.graph import Graph
from src.graph.node import Node


class VmtlSolver:
    problem = constraint.Problem()

    @staticmethod
    def _add_graph_to_problem(problem: constraint.Problem, graph: Graph) -> list:
        variable_names = []
        vertex_edge_count = len(graph.edges) + len(graph.nodes)
        colors = [i for i in range(1, vertex_edge_count + 1)]
        for node in graph.nodes.values():
            variable_names.append('v' + str(node))
            problem.addVariable('v' + str(node), colors)

        for edge in graph.edges:
            variable_names.append('e' + str(edge))
            problem.addVariable('e' + str(edge), colors)
        return variable_names

    @staticmethod
    def _add_k_constraint(problem: constraint.Problem, node_1: Node, node_2: Node):
        # k for two vertices is same
        node_1_edges = [str(edge) for edge in node_1.edges]
        node_2_edges = [str(edge) for edge in node_2.edges]

        condition = "lambda "

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
    def _add_vmtl_constraints_to_problem(problem: constraint.Problem, graph: Graph):
        for node_1 in graph.nodes.values():
            for node_2 in graph.nodes.values():
                if node_1 == node_2:
                    # Edges for all vertices are unique
                    node_1_edges = ['e' + str(edge) for edge in node_1.edges]
                    problem.addConstraint(lambda *x: np.unique(x).size == len(x), node_1_edges)
                    continue

                shared_edge = node_1.is_connected(node_2)
                if not shared_edge:
                    continue

                # Adjacent vertices are different
                problem.addConstraint(lambda v_1, v_2: v_1 != v_2, ['v' + str(node_1), 'v' + str(node_2)])

                # k for two vertices is the same
                VmtlSolver._add_k_constraint(problem, node_1, node_2)

    @staticmethod
    def find_first_vmtl_labeling(graph: Graph) -> dict:
        problem = constraint.Problem()

        variable_names = VmtlSolver._add_graph_to_problem(problem, graph)

        # Every label is different
        problem.addConstraint(lambda *x: np.unique(x).size == len(x), variable_names)
        VmtlSolver._add_vmtl_constraints_to_problem(problem, graph)

        solution: dict = problem.getSolution()

        # Resets problem solver
        VmtlSolver.problem = constraint.Problem()
        return solution
