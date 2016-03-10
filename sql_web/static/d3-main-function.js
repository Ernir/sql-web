d3.xhr("/bakatil/vidfangsefni/", "application/json", function (request) {
    var data = JSON.parse(request.response);
    drawGraph(data);
});

var drawGraph = function (graph) {

    var modifiedLinks = [];
    graph.links.forEach(function (e) {
        // Get the source and target nodes
        var sourceNode = graph.nodes.filter(
            function (n) {
                return n.id === e.source;
            }
        )[0];
        var targetNode = graph.nodes.filter(
            function (n) {
                return n.id === e.target;
            }
        )[0];
        // Add the edge to the array
        modifiedLinks.push({
            source: sourceNode,
            target: targetNode,
            value: e.value
        });
    });

    var width = 900;
    var height = 500;

    var color = d3.scale.category20();

    var force = d3.layout.force()
        .charge(-200)
        .linkDistance(300)
        .size([width, height]);

    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);

    force
        .nodes(graph.nodes)
        .links(graph.links)
        .start();

    var link = svg.selectAll(".link")
        .data(modifiedLinks)
        .enter().append("line")
        .attr("class", "link");

    var gnodes = svg.selectAll('g.gnode')
        .data(graph.nodes)
        .enter()
        .append('g')
        .classed('gnode', true);

    var node = gnodes.append("circle")
        .attr("class", "node")
        .attr("r", 10)
        .style("fill", function (d) {
            return color(d.group);
        })
        .style("fill-opacity", function (d) {
            if (d.read) {
                return 0.2;
            } else {
                return 1;
            }
        })
        .call(force.drag);

    var labels = gnodes.append("text")
        .text(function (d) {
            return d.name;
        })
        .style("fill", function (d) {
            if (d.read) {
                return "purple";
            } else {
                return "blue";
            }
        })
        .style("text-decoration", "underline");

    force.on("tick", function () {
        link.attr("x1", function (d) {
            return d.source.x;
        })
            .attr("y1", function (d) {
                return d.source.y;
            })
            .attr("x2", function (d) {
                return d.target.x;
            })
            .attr("y2", function (d) {
                return d.target.y;
            });

        gnodes.attr("transform", function (d) {
            return 'translate(' + [d.x, d.y] + ')';
        });
    });

    gnodes.on("click", function () {
        var selectedNode = d3.select(this);
        window.location = selectedNode[0][0].__data__.location;
    });

    gnodes.on("mouseover", function () {
        this.style.cursor = "pointer";
    })
};

function presentNodes(groupId) {
    // Hides all nodes not belonging to the given group.

    var gnodes = d3.selectAll('g.gnode');
    var links = d3.selectAll(".link");
    if (!groupId) {
        gnodes.style("visibility", "visible");
        links.style("stroke-width", function (d) {
            return Math.sqrt(d.value)
        });
        return;
    }

    gnodes.style("visibility", function (d) {
        if (d.group === groupId) {
            return "visible";
        } else {
            return "hidden";
        }
    });

    links.style("stroke-width", function (d) {
        if (d.target.group === groupId || d.source.group === groupId) {
            return Math.sqrt(d.value);
        } else {
            return 0;
        }
    });
}

window.onload = function () {
    var subjects = document.getElementsByClassName("subject");
    for (var i = 0; i < subjects.length; i++) {
        var subject = subjects[i];
        subject.onmouseover = function () {
            var groupNumber = parseInt(this.id.slice(8));
            presentNodes(groupNumber);
        };
        subject.onmouseout = function () {
            presentNodes();
        }
    }
};