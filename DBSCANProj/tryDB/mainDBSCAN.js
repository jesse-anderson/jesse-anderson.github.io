// Some global variables
let svg;
let data;
let dbscan_state;
let algo_delay;
let process = null; // For setInterval

function twodecs(x) {
    return parseFloat(Math.round(x*100)/100).toFixed(2);
}

function go() {
    dbscan_state.phase = "inprogress";
    d3.selectAll(".choose_eps_ball").remove()
    
    d3.select("#next_button").remove();

    process = setInterval(function() {
        dbscan_iter(data);
        svg.selectAll(".dot")
        .transition()
        .style("fill", function(d) { return color(d.cluster); });
    }, algo_delay);

    d3.select("#button_area").append("input")
    .attr("id", "pause")
    .attr("name", "pause_button")
    .attr("type", "button")
    .attr("value", "Pause")
    .on("click", function() {
        d3.select("#pause").remove();

        clearInterval(process);

        d3.select("#button_area").append("input")
        .attr("id", "next_button")
        .attr("name", "updateButton")
        .attr("type", "button")
        .attr("value", "   GO!   ")
        .on("click", go);
    });
    d3.select("#eps_select").remove();
    d3.select("#minPoints_select").remove();
    d3.select('#speed_select').remove();
}

function restart() {
    // Reset global variables
    data = [];
    dbscan_state = {eps: 1.0, minPoints: 4, cluster: 0, index: 0, neigh: [], phase: "choose"};
    algo_delay = 125; //default 125
    clearInterval(process);
    process = null;
    
    // Call the setup function to initialize the SVG and buttons
    setup();

    // Append a group element with class 'own_region' and set its opacity
    const svgGroup = svg.append("g")
        .attr("class", "own_region")
        .attr("opacity", 0.5);

    // Choose data and proceed with further operations
    choose_data(function() {
        dbscan_state.phase = "postchoose";
        data = choice();
        draw(data);

        // Append text elements for displaying epsilon and minPoints values
        // svg.append("text")
        //     .attr("id", "Distribution")
        //     .attr("x", x(-20))
        //     .attr("y", y(-6.5))
        //     .text(`Distribution = ${choice.name}`);

        svg.append("text")
            .attr("id", "eps_value")
            .attr("x", x(-20))
            .attr("y", y(-7.5))
            .text(`epsilon = ${twodecs(dbscan_state.eps)}`);

        svg.append("text")
            .attr("id", "minPoints_value")
            .attr("x", x(-20))
            .attr("y", y(-8.5))
            .text(`minPoints = ${dbscan_state.minPoints}`);

        svg.append("text")
            .attr("id", "speed_value")
            .attr("x", x(-20))
            .attr("y", y(-9.5))
            .text(`Speed = ${1/(algo_delay/125)}`);

        // Append input elements for adjusting epsilon and minPoints values
        d3.select("#button_area").append("input")
            .attr("id", "eps_select")
            .attr("name", "eps_select")
            .attr("type", "range")
            .attr("min", 0.102920)
            .attr("max", 2.0)
            .attr("step", 0.02)
            .attr("value", dbscan_state.eps)
            .style("width", "20%")
            .on("change", function() { update_eps(parseFloat(this.value)); })
            .on("input", function() { update_eps(parseFloat(this.value)); });

        d3.select("#button_area").append("input")
            .attr("id", "minPoints_select")
            .attr("name", "minPoints_select")
            .attr("type", "range")
            .attr("min", 1)
            .attr("max", 20)
            .attr("step", 1)
            .attr("value", dbscan_state.minPoints)
            .style("width", "20%")
            .on("change", function() { update_minPoints(parseInt(this.value)); })
            .on("input", function() { update_minPoints(parseInt(this.value)); });

        d3.select("#button_area").append("input")
            .attr("id", "speed_select")
            .attr("name", "speed_select")
            .attr("type", "range")
            .attr("min", 10)
            .attr("max", 250)
            .attr("step", 1)
            .attr("value", (algo_delay))
            .style("width", "20%")
            .on("change", function() { updateSpeed(parseInt(this.value)); })
            .on("input", function() { updateSpeed(parseInt(this.value)); });
        
        // Append a button for triggering the 'go' function
        d3.select("#button_area").append("input")
            .attr("id", "next_button")
            .attr("name", "updateButton")
            .attr("type", "button")
            .attr("value", "   GO!   ")
            .on("click", go);

        // Call the draw_eps_balls function after a delay
        setTimeout(draw_eps_balls, 500);
    });
}
