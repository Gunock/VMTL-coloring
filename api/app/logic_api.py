from flask import Flask, render_template, request, send_from_directory
import time
import os

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

    def addnode(self, n):
        self.nodes.append(n)

    def addedge(self, e):
        self.edges.append(e)

    def saveasjson(self):
        jsonGraph = '{'
        jsonGraph += '"nodes": ['
        for x in range(len(self.nodes)):
            jsonGraph += '{'
            jsonGraph += '"id": ' + '"n' + str(x) + '",'
            jsonGraph += '"label": ' + '"Node ' + str(x) + '",'
            jsonGraph += '"x": ' + self.nodes[x].x_pos + ","
            jsonGraph += '"y": ' + self.nodes[x].y_pos + ","
            jsonGraph += '"size": ' + str(2)
            if(x == len(self.nodes)-1):
                jsonGraph += '}'
            else:
                jsonGraph += '},'
        jsonGraph += '],'
        jsonGraph += '"edges": ['
        for x in range(len(self.edges)):
            jsonGraph += '{'
            jsonGraph += '"id": ' + '"e' + str(x) + '",'
            jsonGraph += '"source": ' + '"n' + self.edges[x].id_1 + '",'
            jsonGraph += '"target": ' + '"n' + self.edges[x].id_2 + '"'
            if (x == len(self.edges) - 1):
                jsonGraph += '}'
            else:
                jsonGraph += '},'
        jsonGraph += ']'
        jsonGraph += '}'
        f = open('data/graph.json', "w")
        f.write(jsonGraph)
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
def addN():
    n = Node(request.form['x_pos'], request.form['y_pos'])
    graph.addnode(n)
    graph.saveasjson()
    return render_template("index.html", last_updated=dir_last_updated('data'))


@app.route("/addEdge", methods=["POST"])
def addE():
    e = Edge(request.form['id_1'], request.form['id_2'])
    graph.addedge(e)
    graph.saveasjson()
    return render_template("index.html", last_updated=dir_last_updated('data'))


@app.route('/data/graph.json')
def data():
    return send_from_directory('data', 'graph.json')


if __name__ == "__main__":
    app.run()
