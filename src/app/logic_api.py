import json
import os
from pathlib import Path

from flask import Flask, render_template, send_from_directory, request, Response, jsonify

from src.graph.graph import Graph
from src.graph.vmtl_problem import VmtlProblem

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

graph = Graph()
Path("data").mkdir(parents=True, exist_ok=True)
graph_file_path: str = 'data/graph.json'


def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))


@app.route("/")
def backend_index():
    global graph, graph_file_path

    graph.save_as_json(graph_file_path, id_as_label=True)
    return render_template("backend-graph-editor.html", last_updated=dir_last_updated('data'))


@app.route("/add-node", methods=["POST"])
def backend_add_node():
    global graph, graph_file_path

    graph.create_node(float(request.form['x_pos']), float(request.form['y_pos']))
    graph.save_as_json(graph_file_path, id_as_label=True)
    return render_template("backend-graph-editor.html", last_updated=dir_last_updated('data'))


@app.route("/add-edge", methods=["POST"])
def backend_add_edge():
    global graph, graph_file_path

    graph.create_edge(int(request.form['id_1']), int(request.form['id_2']))
    graph.save_as_json(graph_file_path, id_as_label=True)
    return render_template("backend-graph-editor.html", last_updated=dir_last_updated('data'))


@app.route('/delete-node', methods=["POST"])
def backend_delete_node():
    global graph, graph_file_path
    n = int(request.form['id_del'])
    graph.delete_node(n)
    graph.save_as_json(graph_file_path)
    return render_template("backend-graph-editor.html", last_updated=dir_last_updated('data'))


@app.route('/delete-edge', methods=["POST"])
def backend_delete_edge():
    global graph, graph_file_path
    n = int(request.form['id_edge_del'])
    graph.delete_edge(n)
    graph.save_as_json(graph_file_path)
    return render_template("backend-graph-editor.html", last_updated=dir_last_updated('data'))


@app.route("/clear-graph", methods=["POST"])
def backend_clear_graph():
    global graph, graph_file_path

    graph = Graph()
    graph.save_as_json(graph_file_path)
    return render_template("backend-graph-editor.html", last_updated=dir_last_updated('data'))


@app.route("/solve-vmtl", methods=["GET"])
def backend_solve_vmtl():
    global graph, graph_file_path

    try:
        problem = VmtlProblem(graph)
        graph = problem.get_solution()
        graph.save_as_json(graph_file_path)
    except ValueError:
        pass
    return render_template("backend-graph-editor.html", last_updated=dir_last_updated('data'))


@app.route("/frontend-editor", methods=["GET"])
def frontend_index():
    global graph, graph_file_path

    graph.reset_labels()
    graph.save_as_json(graph_file_path, id_as_label=False)
    return render_template("frontend-graph-editor.html")


@app.route("/frontend-editor/add-node", methods=["POST"])
def frontend_add_node():
    global graph

    node: dict = json.loads(request.data)
    graph.create_node(float(node['x']), float(node['y']))
    return Response(status=201)


@app.route("/frontend-editor/add-edge", methods=["POST"])
def frontend_add_edge():
    global graph

    edge: dict = json.loads(request.data)
    graph.create_edge_from_dict(edge)
    return Response(status=201)


@app.route("/frontend-editor/solve-vmtl", methods=["GET"])
def frontend_solve_vmtl():
    global graph

    solution_graph: dict = {}
    try:
        solution_graph = VmtlProblem(graph).get_solution().to_dict()
    except ValueError:
        pass
    return jsonify(solution_graph)


@app.route("/frontend-editor/clear-graph", methods=["POST"])
def frontend_clear_graph():
    global graph

    graph = Graph()
    return render_template("backend-graph-editor.html", last_updated=dir_last_updated('data'))


@app.route('/data/graph.json')
def data():
    return send_from_directory('data', 'graph.json')


if __name__ == "__main__":
    app.run()
