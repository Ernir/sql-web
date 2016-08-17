var drawGraph = function (data, subject) {
    /*
    Creates one subject connectivity graph.
    Heavily based on this graph: http://bl.ocks.org/mbostock/1153292
     */
    var links = data.links;
    var nodes = data.nodes;

    // Update the links with the full data
    // ToDo: Just initialize them properly
    links.forEach(function (link) {
        link.source = nodes[link.source] || (nodes[link.source] = {name: link.source});
        link.target = nodes[link.target] || (nodes[link.target] = {name: link.target});
    });

    var width = 400;
    var height = 300;

    var force = d3.layout.force()
        .nodes(d3.values(nodes))
        .links(links)
        .size([width, height])
        .linkDistance(80)
        .charge(-300)
        .on("tick", tick)
        .start();

    var containerId = "#svg-container-" + subject;
    var svg = d3.select(containerId).insert("svg")
        .attr("width", width)
        .attr("height", height);

    svg.append("defs").append("marker")
        .attr("id", "arrow")
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 15)
        .attr("refY", -1.5)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,-5L10,0L0,5");

    var path = svg.append("g").selectAll("path")
        .data(force.links())
        .enter().append("path")
        .attr("class", "link")
        .attr("marker-end", "url(#arrow)");

    var circle = svg.append("g").selectAll("circle")
        .data(force.nodes())
        .enter().append("circle")
        .attr("r", 6)
        .style("fill-opacity", function (d) {
            if (d.read) {
                return 0.2;
            } else {
                return 1;
            }
        })
        .call(force.drag);

    var text = svg.append("g").selectAll("text")
        .data(force.nodes())
        .enter().append("text")
        .attr("x", 8)
        .attr("y", ".31em")
        .text(function (d) {
            return d.name;
        });

    circle.on("mouseover", function () {
        this.style.cursor = "pointer";
    });

    // Use elliptical arc path segments to doubly-encode directionality.
    function tick() {
        path.attr("d", linkArc);
        circle.attr("transform", transform);
        text.attr("transform", transform);
    }

    function linkArc(d) {
        var dx = d.target.x - d.source.x,
            dy = d.target.y - d.source.y,
            dr = Math.sqrt(dx * dx + dy * dy);
        return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
    }

    function transform(d) {
        return "translate(" + d.x + "," + d.y + ")";
    }
};

window.onload = function () {
    var subjects = document.getElementsByClassName("subject");
    for (var i = 0; i < subjects.length; i++) {
        var subjectNumber = parseInt(subjects[i].id.replace(/[^0-9]/g, ''));
        d3.xhr("/bakatil/vidfangsefni/" + subjectNumber + "/", "application/json", function (request) {
            var data = JSON.parse(request.response);
            drawGraph(data, data.subject);
        });
    }
};