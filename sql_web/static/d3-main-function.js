d3.xhr("/bakatil/vidfangsefni/", "application/json", function (request) {
    var data = JSON.parse(request.response);
    draw(data.nodes, data.links);
});

function draw(nodes, links) {

    var modifiedLinks = [];
    links.forEach(function (e) {
        // Get the source and target nodes
        var sourceNode = nodes.filter(
            function (n) {
                return n.id === e.source;
            }
        )[0];
        var targetNode = nodes.filter(
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

    var width = 400, height = 400;

    var color = d3.scale.category20();

    var force = d3.layout.force()
        .nodes(nodes)
        .links(links)
        .charge(-120)
        .linkDistance(30)
        .size([width, height]);

    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);

    var link = svg.selectAll(".link")
        .data(modifiedLinks)
        .enter().append("line")
        .attr("class", "link")
        .style("stroke-width", function (d) {
            return Math.sqrt(d.value);
        });

    var node = svg.selectAll(".node")
        .data(nodes)
        .enter().append("circle")
        .attr("class", "node")
        .attr("r", 5)
        .style("fill", function (d) {
            return color(d.group);
        })
        .call(force.drag);

    node.append("title")
        .text(function (d) {
            return d.name;
        });

    var x = 0;
    var tickLim = Infinity; // ToDo decide if this should be less than inf
    force.on("tick", function () {
        if (x < tickLim) {
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

            node.attr("cx", function (d) {
                return d.x;
            })
                .attr("cy", function (d) {
                    return d.y;
                });
            x++;
        }
    });

    force.start();

    d3.selectAll(".node").on("click", function () {
        var selectedNode = d3.select(this);
        window.location = selectedNode[0][0].__data__.location;
    });
}