import os
from pathlib import Path

from flask import Flask, render_template, request, send_from_directory

from src.graph.graph import Graph
from src.graph.node import Node
from src.graph.vmtl_problem import VmtlProblem

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

graph = Graph()


def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))


@app.route("/")
def index():
    Path("data").mkdir(parents=True, exist_ok=True)
    open('data/graph.json', 'w').close()
    return render_template("index.html", last_updated=dir_last_updated('data'))


@app.route("/addNode", methods=["POST"])
def add_node():
    n = Node(int(request.form['v_id']), float(request.form['x_pos']), float(request.form['y_pos']))
    graph.add_node(n)
    graph.save_as_json()
    return render_template("index.html", last_updated=dir_last_updated('data'))


@app.route("/addEdge", methods=["POST"])
def add_edge():
    graph.create_edge(int(request.form['id_1']), int(request.form['id_2']))
    graph.save_as_json()
    return render_template("index.html", last_updated=dir_last_updated('data'))


@app.route("/clearGraph", methods=["POST"])
def clear_graph():
    open('data/graph.json', 'w').close()
    return render_template("index.html", last_updated=dir_last_updated('data'))


@app.route("/solveVmtl", methods=["GET"])
def solve_vmtl():
    problem = VmtlProblem(graph)
    temp_graph = problem.get_solution()
    temp_graph.save_as_json()
    return render_template("index.html", last_updated=dir_last_updated('data'))


@app.route('/data/graph.json')
def data():
    return send_from_directory('data', 'graph.json')


if __name__ == "__main__":
    app.run()
