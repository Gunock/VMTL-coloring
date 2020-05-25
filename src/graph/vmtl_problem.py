from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import IntVar

from src.graph.graph import Graph


class VmtlProblem:

    def __init__(self, graph: Graph):
        self._n_vars: dict = {}
        self._e_vars: dict = {}
        self._k_var: IntVar
        self._model = cp_model.CpModel()
        self._graph: Graph = graph
        if graph.is_empty():
            return
        self._setup_problem()

    def get_solution(self) -> Graph:
        if self._graph.is_empty():
            return Graph()
        solver = cp_model.CpSolver()
        status = solver.Solve(self._model)
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            return self._solution_to_graph(solver)
        else:
            return Graph()

    def _setup_problem(self) -> None:
        self._add__k_variable()
        self._add_graph_to_problem()
        self._add_vmtl_constraints_to_problem()

    def _solution_to_graph(self, solver: cp_model.CpSolver) -> Graph:
        result: Graph = self._graph
        for key in self._n_vars:
            result.set_node_label(key, str(solver.Value(self._n_vars[key])))
        for key in self._e_vars:
            result.set_edge_label(key, str(solver.Value(self._e_vars[key])))
        return result

    def _add_graph_to_problem(self) -> None:
        vertex_edge_count = len(self._graph.edges) + len(self._graph.nodes)
        colors = [i for i in range(1, vertex_edge_count + 1)]

        for node in self._graph.nodes.values():
            n = self._model.NewIntVar(min(colors), max(colors), 'n' + str(node))
            self._n_vars['n' + str(node)] = n

        for edge in self._graph.edges:
            e = self._model.NewIntVar(min(colors), max(colors), 'e' + str(edge))
            self._e_vars['e' + str(edge)] = e

    def _add__k_variable(self) -> None:
        possible_k = VmtlProblem._get_k_range(self._graph)
        if self._graph.is_complete():
            possible_k = list(filter(lambda elem: elem % 4 == 0, possible_k))

        self._k_var = self._model.NewIntVar(min(possible_k), max(possible_k), 'k')

    def _add_vmtl_constraints_to_problem(self) -> None:
        self._model.AddAllDifferent(list(self._n_vars.values()) + list(self._e_vars.values()) + [self._k_var])

        # vertex and it's edge count equals k
        for node in self._graph.nodes.values():
            node_edges = ['e' + str(edge) for edge in node.edges]
            constraint: str = 'self._n_vars["{}"]'.format('n' + str(node))
            for edge in node_edges:
                constraint += ' + self._e_vars["{}"]'.format(edge)
            constraint += ' == self._k_var'
            self._model.Add(eval(constraint))

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
