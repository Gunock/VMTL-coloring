import os
import json
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


class Node:
    def __init__(self, x, y):
        self.x_pos = x
        self.y_pos = y


class Edge:
    def __init__(self, id1, id2):
        self.id_1 = id1
        self.id_2 = id2


class Graph:
    nodes = []
    edges = []

    def add_node(self, n):
        self.nodes.append(n)

    def add_edge(self, e):
        self.edges.append(e)

    def save_as_json(self):
        dictionary = {
            "nodes": [],
            "edges": []
        }
        for x in range(len(self.nodes)):
            new_node = {
                "id": "n"+str(x),
                "label": "Node"+str(x),
                "x": int(self.nodes[x].x_pos),
                "y": int(self.nodes[x].y_pos),
                "size": 2
            }
            dictionary["nodes"].append(new_node)
        for x in range(len(self.edges)):
            new_edge = {
                "id": "e"+str(x),
                "source": self.edges[x].id_1,
                "target": self.edges[x].id_2
            }
            dictionary["edges"].append(new_edge)
        f = open('data/graph.json', "w")
        f.write(json.dumps(dictionary))
        f.close()


graph = Graph()


def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))


@app.route("/")
def index():
    open('data/graph.json', 'w').close()
    return render_template("index.html", last_updated=dir_last_updated('data'))


@app.route("/addNode", methods=["POST"])
def add_node():
    n = Node(request.form['x_pos'], request.form['y_pos'])
    graph.add_node(n)
    graph.save_as_json()
    return render_template("index.html", last_updated=dir_last_updated('data'))


@app.route("/addEdge", methods=["POST"])
def add_edge():
    e = Edge(request.form['id_1'], request.form['id_2'])
    graph.add_edge(e)
    graph.save_as_json()
    return render_template("index.html", last_updated=dir_last_updated('data'))


@app.route('/data/graph.json')
def data():
    return send_from_directory('data', 'graph.json')


if __name__ == "__main__":
    app.run()
