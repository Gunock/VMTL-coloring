import json
import os
import re
from pathlib import Path

from flask import Flask, render_template, send_from_directory, request, Response, flash, redirect, url_for
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

from src.graph.graph import Graph
from src.graph.vmtl_problem import VmtlProblem

app = Flask(__name__)
app.secret_key = b'blablabla'
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


@app.route("/backend-editor")
def backend_index_redirect():
    return redirect(url_for('backend_index'))


@app.route("/add-node", methods=["POST"])
def backend_add_node():
    global graph, graph_file_path

    try:
        if graph.create_node(float(request.form['x_pos']), float(request.form['y_pos'])):
            graph.save_as_json(graph_file_path, id_as_label=True)
        else:
            flash('Given coordinates already used by other node')
    except (ValueError, AttributeError):
        flash('Incorrect input')
    return render_template("backend-graph-editor.html", last_updated=dir_last_updated('data'))


@app.route("/add-edge", methods=["POST"])
def backend_add_edge():
    global graph, graph_file_path

    try:
        node_id_1: str = re.match(r'n([0-9]+)|([0-9]+)', request.form['id_1']).group()
        node_id_2: str = re.match(r'n([0-9]+)|([0-9]+)', request.form['id_2']).group()
        assert not node_id_1 == node_id_2
        print(node_id_1)
        print(node_id_2)
        if graph.create_edge(node_id_1, node_id_2):
            graph.save_as_json(graph_file_path, id_as_label=True)
        else:
            flash('One of given nodes does not exist')
    except (ValueError, AttributeError):
        flash('Incorrect input')
    except AssertionError:
        flash('Node IDs should be different')
    return render_template("backend-graph-editor.html", last_updated=dir_last_updated('data'))


@app.route('/delete-node', methods=["POST"])
def backend_delete_node():
    global graph, graph_file_path

    try:
        node_id: str = str(re.match(r'n([0-9]+)|([0-9]+)', request.form['id_del']).group())
        if graph.delete_node(node_id):
            graph.save_as_json(graph_file_path, id_as_label=True)
    except (ValueError, AttributeError):
        flash('Incorrect input')
    return render_template("backend-graph-editor.html", last_updated=dir_last_updated('data'))


@app.route('/delete-edge', methods=["POST"])
def backend_delete_edge():
    global graph, graph_file_path

    try:
        edge_id: str = re.match(r'e([0-9]+)|([0-9]+)', request.form['id_edge_del']).group()
        if graph.delete_edge(edge_id):
            graph.save_as_json(graph_file_path, id_as_label=True)
    except (ValueError, AttributeError):
        flash('Incorrect input')
    return render_template("backend-graph-editor.html", last_updated=dir_last_updated('data'))


@app.route("/hide-labels", methods=["GET"])
def backend_hide_labels():
    global graph, graph_file_path

    graph.reset_labels()
    graph.save_as_json(graph_file_path, id_as_label=False)
    flash('labels-hidden')
    return render_template("backend-graph-editor.html", last_updated=dir_last_updated('data'))


@app.route("/clear-graph", methods=["GET"])
def backend_clear_graph():
    global graph, graph_file_path

    graph = Graph()
    graph.save_as_json(graph_file_path)
    return render_template("backend-graph-editor.html", last_updated=dir_last_updated('data'))


@app.route("/solve-vmtl", methods=["GET"])
def backend_solve_vmtl():
    global graph, graph_file_path

    solution_graph = VmtlProblem(graph).get_solution()
    if not solution_graph.is_empty():
        graph = solution_graph
        graph.save_as_json(graph_file_path)
        flash('labels-vmtl')
    else:
        flash("VMTL coloring not found")
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


@app.route("/frontend-editor/clear-graph", methods=["POST"])
def frontend_clear_graph():
    global graph

    graph = Graph()
    return Response(status=200)


@app.route('/data/graph.json')
def data():
    return send_from_directory('data', 'graph.json')


if __name__ == "__main__":
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()
