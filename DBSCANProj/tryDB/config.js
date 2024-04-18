// Define margins, width, and height
const margin = {top: 20, right: 20, bottom: 30, left: 40};
const width = 960 - margin.left - margin.right;
const height = 500 - margin.top - margin.bottom;

// Create linear scales for x and y
const x = d3.scaleLinear()
    .range([0, width]);

const y = d3.scaleLinear()
    .range([height, 0]);

// Set domain for y and x
y.domain([-10, 10]);
const xlim = 10 * width / height;
x.domain([-xlim, xlim]);

// Define color array and color function
const clr = ["white", "red", "blue", "green", "yellow", "black", "purple", "grey", "brown", "orange", "pink"];
function color(i) {
    if(i === 0) {
        return clr[0];
    } else {
        return clr[1 + (i - 1) % (clr.length - 1)];
    }
}

// Create x and y axis
const xAxis = d3.axisBottom(x);
const yAxis = d3.axisLeft(y);

// Define distance function
function dist(w, z) {
    return Math.sqrt(Math.pow(w.x - z.x, 2) + Math.pow(w.y - z.y, 2));
}

function setup() {
    // Ensure that width and margin are defined
    if (typeof width === 'undefined' || typeof margin === 'undefined') {
        console.error('width and margin must be defined before calling setup()');
        return;
    }

    // Remove any existing SVG element
    d3.select("svg").remove();

    // Initialize the SVG element
     svg = d3.select("#svg_area")
        .append("svg")
        .attr("width", "100%")
        .attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
        .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);

    // Insert a white rectangle as the first child of the SVG element
    svg.insert("rect", ":first-child")
        .attr("x", 0)
        .attr("y", 0)
        .attr("width", "100%")
        .attr("height", "100%")
        .style("fill", "white");

    // Remove any existing buttons
    d3.select("#button_area").selectAll("input").remove();

    // Initialize the Restart button
    d3.select("#button_area")
        .append("input")
        .attr("class", "restart_button")
        .attr("name", "restart_button")
        .attr("type", "button")
        .attr("value", "Restart")
        .on("click", restart);  // Make sure the restart function is defined
}

function draw(data) {
    var points = svg.selectAll(".dot")
      .data(data)
    .enter().append("circle")
      .attr("class", "dot")
      .attr("r", 3.5)
      .attr("cx", function(d, i) { return x(30 * Math.cos(i / 5)); })
      .attr("cy", function(d, i) { return y(30 * Math.sin(i / 5)); })
      .style("fill", function(d) { return color(d.cluster); })
      .style("stroke", "black")
      .style("stroke-width", "1px");

    points.transition()
    .duration(500)
    .attr("cx", function(d) { return x(d.x); })
    .attr("cy", function(d) { return y(d.y); });
}

function choose_data(callback) {
    algo = choice;

    var Smiley_Face = function() { return smiley(500); };
    var Uniform_Points  = function() { return uniform(250); };
    var Gaussian_Mix = function() { return threenorm(400); };
    var Spiral = function() { return generateSpirals(100); };
    var Circles = function() { return circle_pack(500); };
    var Anisotropic = function() { return anisotropicBlobs(500); };
    var Rings = function() { return rings1(); };
    ////////////////////
    var Infinity_Symbol = function() { return generateInfinitySignData(300); };
    var Cross = function() { return generateCrossData(200)};
    
    var choices = [
        {name: "Uniform Points", choice: Uniform_Points, txtpos_x: -14.0},
        {name: "Gaussian Mixture", choice: Gaussian_Mix, txtpos_x: -4.5},
        {name: "Smiley Face", choice: Smiley_Face, txtpos_x: 6.6},
        {name: "Anisotropic", choice: Anisotropic, txtpos_x: -13.4},
        {name: "Packed Circles", choice: Circles, txtpos_x: -3.9},
        {name: "Spirals", choice: Spiral, txtpos_x: 7.5},
        {name: "Rings", choice: Rings, txtpos_x: -12.4},
        {name: "Infinity", choice: Infinity_Symbol, txtpos_x: -2.6},
        {name: "Cross", choice: Cross, txtpos_x: 8.0}
    ];

    var title = {text: "Choose your Distribution.", x: -14, y: 9};

    display_choice(choices, title, callback);
}
