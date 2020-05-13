;(function () {
    'use strict';

    let s, c, dom, disc, ground, nId = 0, eId = 0, radius = 50, mouseX, mouseY, spaceMode = false, wheelRatio = 1.1,
        nodeRadius = 10, maxDisplacement = 15;


    /**
     * CUSTOM PHYSICS LAYOUT:
     * **********************
     */
    sigma.classes.graph.addMethod('computePhysics', function () {
        let i, l = this.nodesArray.length, s;

        for (i = 0; i < l; i++) {
            s = this.nodesArray[i];
            s.dX = Math.max(Math.min(s.dX, maxDisplacement), -maxDisplacement);
            s.dY = Math.max(Math.min(s.dY, maxDisplacement), -maxDisplacement);
            s.x += s.dX;
            s.y += s.dY;
        }
    });

    /**
     * INITIALIZATION SCRIPT:
     * **********************
     */
    s = new sigma({
        renderer: {
            container: document.getElementById('graph-container'),
            type: 'canvas'
        },
        settings: {
            autoRescale: false,
            mouseEnabled: false,
            touchEnabled: false,
            nodesPowRatio: 1,
            edgesPowRatio: 1,
            defaultEdgeColor: '#333',
            defaultNodeColor: '#333',
            edgeColor: 'default'
        }
    });
    dom = document.querySelector('#graph-container canvas:last-child');
    disc = document.getElementById('disc');
    ground = document.getElementById('ground');
    c = s.camera;

    function frame() {
        s.graph.computePhysics();
        s.refresh();

        if (s.graph.nodes().length) {
            let w = dom.offsetWidth, h = dom.offsetHeight;

            // The "rescale" middleware modifies the position of the nodes, but we
            // need here the camera to deal with this. Here is the code:
            let xMin = Infinity, xMax = -Infinity, yMin = Infinity, yMax = -Infinity, margin = 50, scale;

            s.graph.nodes().forEach(function (n) {
                xMin = Math.min(n.x, xMin);
                xMax = Math.max(n.x, xMax);
                yMin = Math.min(n.y, yMin);
                yMax = Math.max(n.y, yMax);
            });

            xMax += margin;
            xMin -= margin;
            yMax += margin;
            yMin -= margin;

            scale = Math.min(
                w / Math.max(xMax - xMin, 1),
                h / Math.max(yMax - yMin, 1)
            );

            c.goTo({
                x: (xMin + xMax) / 2,
                y: (yMin + yMax) / 2,
                ratio: 1 / scale
            });

            ground.style.top =
                (Math.max(h / 2 - Math.min((yMin + yMax) / 2 * scale, h), 0) + 'px').toString();
            disc.style.borderRadius = (radius * scale).toString();
            disc.style.width = (2 * radius * scale).toString();
            disc.style.height = (2 * radius * scale).toString();
            disc.style.top = (mouseY - radius * scale).toString();
            disc.style.left = (mouseX - radius * scale).toString();
            disc.style.backgroundColor = spaceMode ? '#f99' : '#9cf';
        }
        requestAnimationFrame(frame);
    }

    frame();


    /**
     * EVENTS BINDING:
     * ***************
     */
    dom.addEventListener('click', function (e) {
        // Find neighbors:
        let x, y, p, id, neighbors;

        x = sigma.utils.getX(e) - dom.offsetWidth / 2;
        y = sigma.utils.getY(e) - dom.offsetHeight / 2;

        p = c.cameraPosition(x, y);
        x = p.x;
        y = p.y;

        neighbors = s.graph.nodes().filter(function (n) {
            return (Math.sqrt(
                Math.pow(n.x - x, 2) +
                Math.pow(n.y - y, 2)
            ) - n.size) < radius;
        });

        if (!spaceMode)
            x = x + Math.random() / 10;
            y = y + Math.random() / 10;
            s.graph.addNode({
                id: (id = (++nId) + ''),
                size: nodeRadius,
                x: x,
                y: y,
                dX: 0,
                dY: 0,
                type: 'goo'
            });
            //send node to api
            var xhr_node = new XMLHttpRequest();
            xhr_node.open('POST', 'node', true);
            xhr_node.setRequestHeader('Content-type', 'application/json');
            xhr_node.send(JSON.stringify({"x": x, "y": y}));

        neighbors.forEach(function (n) {
            if (!spaceMode){
                s.graph.addEdge({
                    id: (++eId) + '',
                    source: id,
                    target: n.id,
                    type: 'goo'
                });
                //send edge to api
                var xhr_edge = new XMLHttpRequest();
                xhr_edge.open('POST', 'edge', true);
                xhr_edge.setRequestHeader('Content-type', 'application/json');
                xhr_edge.send(JSON.stringify({"source": id, "target": n.id}));
            }
            else
                s.graph.dropNode(n.id);
        });
    }, false);
    dom.addEventListener('mousemove', function (e) {
        mouseX = sigma.utils.getX(e);
        mouseY = sigma.utils.getY(e);
    }, false);
    dom.addEventListener('DOMMouseScroll', function (e) {
        radius *= sigma.utils.getDelta(e) < 0 ? 1 / wheelRatio : wheelRatio;
    }, false);
    dom.addEventListener('mousewheel', function (e) {
        radius *= sigma.utils.getDelta(e) < 0 ? 1 / wheelRatio : wheelRatio;
    }, false);
    document.addEventListener('keydown', function (e) {
        spaceMode = (e.which === 32) ? true : spaceMode;
    });
    document.addEventListener('keyup', function (e) {
        spaceMode = e.which === 32 ? false : spaceMode;
    });
})();