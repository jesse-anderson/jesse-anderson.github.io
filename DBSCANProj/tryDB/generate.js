// Functions for generating data

// Generate data points from three normal distributions
function threenorm(n) {
    var stDev = 2; //Increase Standard deviation to 2 to create a wider spread
    var rnorm = d3.randomNormal(0, stDev); // Assumes D3.js has been included to provide the random normal distribution function
    var data = new Array(n);
    var mux, muy;

    for (var i = 0; i < n; i++) {
        var j = Math.floor(Math.random() * 3);
        if (j % 3 === 0) {
            mux = -4; // Reduced distance to the center
            muy = -4; // Reduced distance to the center
        } else if (j % 3 === 1) {
            mux = 4; // Reduced distance to the center
            muy = -4; // Reduced distance to the center
        } else {
            mux = 0; // Center remains the same
            muy = 4; // Reduced distance to the center
        }
        data[i] = {x: rnorm() + mux, y: rnorm() + muy, cluster: 0};
    }

    return data;
}

// Generate uniformly distributed data points
function uniform(n) {
    var data = new Array(n);

    for(var i = 0; i < n; i++) {
        data[i] = {x: Math.random() * 20 - 10, y: Math.random() * 20 - 10, cluster: 0};
    }

    return data;
}

function dbscan_rings() {
    var centers = new Array(0);
    var rings = new Array(0);

    var rows = 3;
    var cols = 3;
    for (var row = 0; row < rows; row++) {
        for (var col = 0; col < cols; col++) {
            var MinPoints = row;
            var eps = 1.25 - col * 0.25;

            var x0 = -15 + (30 / (rows + 1)) * (row + 1);
            var y0 = -12 + (24 / (cols + 1)) * (col + 1);

            centers.push({x: x0, y: y0, cluster: 0});
            for (var i = 0; i < MinPoints; i++) {
                var x = x0 + eps * Math.sin(2 * Math.PI * i / MinPoints);
                var y = y0 + eps * Math.cos(2 * Math.PI * i / MinPoints);
                rings.push({x: x, y: y, cluster: 0});
            }
        }
    }

    return {centers: centers, rings: rings};
}

// Returns a smiley face :)
function smiley(n) {
    var data = new Array(n);
    var noiseLevel = 0.75; // Adjust this value to increase or decrease the noise level

    var i = 0;
    while (i < n) {
        var x = Math.random() * 20 - 10;
        var y = Math.random() * 20 - 10;

        // Smiley params
        var a = 6;
        var b = 8;
        var d = 4;
        var c = 0.15;
        var C = (c - a / (b * b));

        // Add random noise
        var noiseX = (Math.random() * 2 - 1) * noiseLevel;
        var noiseY = (Math.random() * 2 - 1) * noiseLevel;

        // The border
        if (x * x + y * y < 100 && x * x + y * y > 81) {
            data[i] = { x: x + noiseX, y: y + noiseY, cluster: 0 };
            i += 1;
        }
        // Left eye
        else if ((x + 4) * (x + 4) + (y - 4) * (y - 4) < 1) {
            data[i] = { x: x + noiseX, y: y + noiseY, cluster: 0 };
            i += 1;
        }
        // Right eye
        else if ((x - 4) * (x - 4) + (y - 4) * (y - 4) < 1) {
            data[i] = { x: x + noiseX, y: y + noiseY, cluster: 0 };
            i += 1;
        }
        // Smile
        else if ((x > -b && x < b) && (y > c * x * x - a) && (y < C * x * x - d)) {
            data[i] = { x: x + noiseX, y: y + noiseY, cluster: 0 };
            i += 1;
        }
    }
    return data;
}




// Returns packed circles
function circle_pack(n) {
    // Initialize constants and data array
    var r = 3;
    var root3 = Math.sqrt(3);
    var data = new Array(n);

    // Define circle centers
    var circles = [
        {x: -2 * r, y: 0},
        {x: 0, y: 0},
        {x: 2 * r, y: 0},
        {x: -r, y: root3 * r},
        {x: r, y: root3 * r},
        {x: -r, y: -root3 * r},
        {x: r, y: -root3 * r}
    ];

    // Generate a unique random density factor for each circle
    var densityFactors = circles.map(() => Math.random() * (1.2 - 0.8) + 0.8);

    var i = 0;
    while (i < n) {
        // Randomly choose a circle for each point based on the density factor
        var circleIndex = Math.floor(Math.random() * circles.length);
        var densityFactor = densityFactors[circleIndex];
        var effectiveRadius = r * densityFactor;

        // Generate random x and y coordinates within the bounds of the circle
        var angle = Math.random() * 2 * Math.PI;
        var distance = Math.random() * effectiveRadius;
        var x = circles[circleIndex].x + distance * Math.cos(angle);
        var y = circles[circleIndex].y + distance * Math.sin(angle);

        data[i] = { x: x, y: y, cluster: 0 };
        i += 1;
    }

    return data;
}




function anisotropicBlobs(n) {
    // Initialize the data array
    var data = new Array(n);

    // D3's random normal function
    var randomNormal = d3.randomNormal;

    // Define the number of blobs
    var numBlobs = 3;
    // Define the standard deviations and rotation for each blob
    var stdDevs = [2, 1, 2];
    var rotations = [Math.PI / 4, -Math.PI / 4, Math.PI / 8]; // Rotation angles for each blob

    for (var i = 0; i < n; i++) {
        var blobIndex = Math.floor(numBlobs * Math.random());
        var stdDevX = stdDevs[blobIndex];
        var stdDevY = stdDevX / 4; // Make y deviation smaller to create elongation
        var rotation = rotations[blobIndex];

        // Create random normal variables for x and y
        var x = randomNormal(0, stdDevX)();
        var y = randomNormal(0, stdDevY)();

        // Rotate the points to create the elongation effect in different directions
        var xRotated = x * Math.cos(rotation) - y * Math.sin(rotation);
        var yRotated = x * Math.sin(rotation) + y * Math.cos(rotation);

        // Define the center for each blob
        var centers = [
            { x: -5, y: 0 },
            { x: 0, y: 1 },
            { x: 5, y: 5 }
        ];
        var center = centers[blobIndex];

        // Offset the points by the blob's center
        var xOffset = center.x;
        var yOffset = center.y;

        data[i] = { x: xRotated + xOffset, y: yRotated + yOffset, cluster: 0 };
    }

    return data;
}

function rings1() {
    // Initialize centers and rings arrays
    var centers = [];
    var rings = [];
    var data = [];
    var rows = 9;
    var cols = 3;

    for (var row = 0; row < rows; row++) {
        for (var col = 0; col < cols; col++) {
            var MinPoints = row;
            var eps = 1.25 - col * 0.25;

            var x0 = -15 + (30 / (rows + 1)) * (row + 1);
            var y0 = -12 + (24 / (cols + 1)) * (col + 1);

            centers.push({ x: x0, y: y0, cluster: 0 });

            for (var i = 0; i < MinPoints; i++) {
                var x = x0 + eps * Math.sin(2 * Math.PI * i / MinPoints);
                var y = y0 + eps * Math.cos(2 * Math.PI * i / MinPoints);
                rings.push({ x: x, y: y, cluster: 0 });
            }
        }
    }
    data = [centers, rings]
    data = centers.concat(rings)
    return data ;
}

////////////////
function generateInfinitySignData(numPoints, gapProbability = 0.1, offsetRange = 2) {
    const a = 10;  // Scale factor to adjust the size of the infinity sign
    const data = [];
    for (let i = 0; i < numPoints; i++) {
        // Randomly decide whether to skip this point to create gaps
        if (Math.random() > gapProbability) {
            const t = (2 * Math.PI * i) / numPoints;
            // Calculate the base x and y without any offsets
            const baseX = a * Math.cos(t) / (1 + Math.sin(t) ** 2);
            const baseY = a * Math.sin(t) * Math.cos(t) / (1 + Math.sin(t) ** 2);
            
            // Apply a random offset to x and y coordinates
            const angle = Math.random() * 2 * Math.PI; // Random angle for offset direction
            const offset = Math.random() * offsetRange; // Random magnitude for the offset
            const offsetX = offset * Math.cos(angle);  // Calculate offset x based on the random angle and magnitude
            const offsetY = offset * Math.sin(angle);  // Calculate offset y based on the random angle and magnitude

            // Add the offset to the base coordinates
            const x = baseX + offsetX;
            const y = baseY + offsetY;
            
            data.push({ x: x, y: y, cluster: 0 });
        }
    }
    return data;
}

function generateCrossData(numPoints, gapProbability = 0.1, offsetRange = 1) {
    const a = 10;  // Scale factor to adjust the size of the infinity sign
    const data = [];

    for (let i = 0; i < numPoints; i++) {
        // Randomly decide whether to skip this point to create gaps
        if (Math.random() > gapProbability) {
            const t = (2 * Math.PI * i) / numPoints;
            
            // Calculate the base x and y for the horizontal infinity sign
            const baseXHorizontal = a * Math.cos(t) / (1 + Math.sin(t) ** 2);
            const baseYHorizontal = a * Math.sin(t) * Math.cos(t) / (1 + Math.sin(t) ** 2);

            // Apply a random offset to x and y coordinates for the horizontal infinity sign
            const angleHorizontal = Math.random() * 2 * Math.PI; // Random angle for offset direction
            const offsetHorizontal = Math.random() * offsetRange; // Random magnitude for the offset
            const offsetXHorizontal = offsetHorizontal * Math.cos(angleHorizontal);  // Calculate offset x based on the random angle and magnitude
            const offsetYHorizontal = offsetHorizontal * Math.sin(angleHorizontal);  // Calculate offset y based on the random angle and magnitude

            // Add the offset to the base coordinates for the horizontal infinity sign
            const xHorizontal = baseXHorizontal + offsetXHorizontal;
            const yHorizontal = baseYHorizontal + offsetYHorizontal;

            data.push({ x: xHorizontal, y: yHorizontal, cluster: 0 });

            // Calculate the base x and y for the vertical infinity sign by swapping the base calculations
            const baseXVertical = baseYHorizontal;
            const baseYVertical = baseXHorizontal;

            // Apply a random offset to x and y coordinates for the vertical infinity sign
            const angleVertical = Math.random() * 2 * Math.PI; // Random angle for offset direction
            const offsetVertical = Math.random() * offsetRange; // Random magnitude for the offset
            const offsetXVertical = offsetVertical * Math.cos(angleVertical);  // Calculate offset x based on the random angle and magnitude
            const offsetYVertical = offsetVertical * Math.sin(angleVertical);  // Calculate offset y based on the random angle and magnitude

            // Add the offset to the base coordinates for the vertical infinity sign
            const xVertical = baseXVertical + offsetXVertical;
            const yVertical = baseYVertical + offsetYVertical;

            data.push({ x: xVertical, y: yVertical, cluster: 0 });
        }
    }
    return data;
}

function generateSpirals(n, turns = 1, noiseLevel = 0.3) {
    var data = [];

    // Define the scale to fit the spiral within the [-10, 10] range
    var scale = 10 / (turns * 2 * Math.PI);

    // Function to generate a single spiral arm
    function generateSpiral(centerX, centerY, deltaTheta) {
        for (var i = 0; i < n; i++) {
            var theta = (i / n) * (2 * Math.PI) * turns; // Angle for the spiral
            var radius = theta * scale; // Linearly increasing radius

            // Calculate the x and y coordinates based on the spiral equation
            var x = centerX + radius * Math.cos(theta + deltaTheta);
            var y = centerY + radius * Math.sin(theta + deltaTheta);

            // Add random noise within the noise level
            x += (Math.random() - 0.5) * noiseLevel;
            y += (Math.random() - 0.5) * noiseLevel;

            // Ensure the points are within the [-10, 10] bounds after adding noise
            x = Math.max(-10, Math.min(10, x));
            y = Math.max(-10, Math.min(10, y));

            data.push({ x: x, y: y, cluster: 0 });
        }
    }

    // Generate the three spirals with different phase shifts
    generateSpiral(0.3, 0, 0); // No phase shift for the first spiral
    generateSpiral(-0.3, 0, 2 * Math.PI / 3); // 120 degrees phase shift for the second spiral
    // generateSpiral(0, 0, 4 * Math.PI / 3); // 240 degrees phase shift for the third spiral

    return data;
}