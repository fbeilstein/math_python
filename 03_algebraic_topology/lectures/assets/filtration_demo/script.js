const canvas = document.getElementById('simCanvas');
const ctx = canvas.getContext('2d');
const slider = document.getElementById('radius-slider');
const radiusVal = document.getElementById('radius-val');

let width, height;
let points = [];
let radius = parseInt(slider.value);
let complexType = 'cech';
let draggingPoint = null;

// Styling
const my_green = "rgba(144, 238, 144, 0.4)";
const my_coral = "rgba(240, 128, 128, 0.5)";

function resize() {
    width = canvas.parentElement.clientWidth;
    height = canvas.parentElement.clientHeight;
    canvas.width = width;
    canvas.height = height;
    draw();
}
window.addEventListener('resize', resize);
setTimeout(resize, 100);

// UI Controls
function setComplex(type) {
    complexType = type;
    document.getElementById('btn-cech').classList.toggle('active', type === 'cech');
    document.getElementById('btn-alpha').classList.toggle('active', type === 'alpha');
    document.getElementById('btn-rips').classList.toggle('active', type === 'rips');
    draw();
}

window.setComplex = setComplex;

slider.addEventListener('input', (e) => {
    radius = parseInt(e.target.value);
    radiusVal.innerText = radius;
    draw();
});

// Math Utils
function getDistSq(p1, p2) {
    return (p1.x - p2.x)**2 + (p1.y - p2.y)**2;
}

function getClosestPoint(x, y) {
    let minDist = 15*15;
    let closest = -1;
    for(let i = 0; i < points.length; i++) {
        let d = getDistSq({x, y}, points[i]);
        if (d < minDist) {
            minDist = d;
            closest = i;
        }
    }
    return closest;
}

// Interaction
canvas.addEventListener('contextmenu', (e) => {
    e.preventDefault(); // Prevent default browser context menu
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const pIdx = getClosestPoint(x, y);
    if (pIdx !== -1) {
        points.splice(pIdx, 1);
        draw();
    }
});

canvas.addEventListener('mousedown', (e) => {
    if (e.button !== 0) return; // Only handle left clicks
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    draggingPoint = getClosestPoint(x, y);
    
    // If clicked on empty space, add a point and start dragging it
    if (draggingPoint === -1) {
        points.push({x, y});
        draggingPoint = points.length - 1;
        draw();
    }
});

canvas.addEventListener('mousemove', (e) => {
    if (draggingPoint !== null && draggingPoint !== -1) {
        const rect = canvas.getBoundingClientRect();
        points[draggingPoint].x = e.clientX - rect.left;
        points[draggingPoint].y = e.clientY - rect.top;
        draw();
    }
});

canvas.addEventListener('mouseup', () => {
    draggingPoint = null;
});
canvas.addEventListener('mouseleave', () => {
    draggingPoint = null;
});

// Initial points
function initRandom() {
    points = [];
    for (let i=0; i<15; i++) {
        points.push({
            x: 100 + Math.random() * 400,
            y: 100 + Math.random() * 300
        });
    }
}
initRandom();

// Complex calculations
function getLinesRipsCech() {
    let lines = [];
    for(let i=0; i<points.length; i++) {
        for(let j=i+1; j<points.length; j++) {
            if (Math.sqrt(getDistSq(points[i], points[j])) <= 2 * radius) {
                lines.push([i, j]);
            }
        }
    }
    return lines;
}

function getTrianglesCechRips(type) {
    let triangles = [];
    for(let i=0; i<points.length; i++) {
        for(let j=i+1; j<points.length; j++) {
            for(let k=j+1; k<points.length; k++) {
                let l1 = Math.sqrt(getDistSq(points[i], points[j]));
                let l2 = Math.sqrt(getDistSq(points[j], points[k]));
                let l3 = Math.sqrt(getDistSq(points[i], points[k]));
                
                if (l1 <= 2*radius && l2 <= 2*radius && l3 <= 2*radius) {
                    if (type === 'rips') {
                        triangles.push([i, j, k]);
                    } else if (type === 'cech') {
                        let p = l1 + l2 + l3;
                        let areaDenom = Math.sqrt(p * (p - 2*l1) * (p - 2*l2) * (p - 2*l3));
                        let R = (areaDenom > 0.0001) ? (l1 * l2 * l3 / areaDenom) : Math.max(l1,l2,l3)/2;
                        
                        let f1 = Math.sqrt(getDistSq(points[i], {x: (points[j].x+points[k].x)/2, y: (points[j].y+points[k].y)/2}));
                        let f2 = Math.sqrt(getDistSq(points[j], {x: (points[i].x+points[k].x)/2, y: (points[i].y+points[k].y)/2}));
                        let f3 = Math.sqrt(getDistSq(points[k], {x: (points[i].x+points[j].x)/2, y: (points[i].y+points[j].y)/2}));
                        
                        if (f1 <= radius || f2 <= radius || f3 <= radius || R <= radius) {
                            triangles.push([i, j, k]);
                        }
                    }
                }
            }
        }
    }
    return triangles;
}

function getAlphaComplex() {
    if (points.length < 3) return {lines: getLinesRipsCech(), triangles: []};
    
    let coords = [];
    points.forEach(p => { coords.push(p.x, p.y); });
    const delaunay = new Delaunator(coords);
    
    let lines = [];
    let triangles = [];
    let edgesAdded = new Set();
    
    for (let idx = 0; idx < delaunay.triangles.length; idx += 3) {
        let i = delaunay.triangles[idx];
        let j = delaunay.triangles[idx + 1];
        let k = delaunay.triangles[idx + 2];
        
        let l1 = Math.sqrt(getDistSq(points[i], points[j]));
        let l2 = Math.sqrt(getDistSq(points[j], points[k]));
        let l3 = Math.sqrt(getDistSq(points[i], points[k]));
        
        // Add edges if they satisfy cech distance
        let edges = [[i,j, l1], [j,k, l2], [i,k, l3]];
        for (let e of edges) {
            let key = Math.min(e[0], e[1]) + "-" + Math.max(e[0], e[1]);
            if (e[2] <= 2 * radius && !edgesAdded.has(key)) {
                lines.push([e[0], e[1]]);
                edgesAdded.add(key);
            }
        }
        
        // Cech triangle condition for alpha
        let p = l1 + l2 + l3;
        let areaDenom = Math.sqrt(p * (p - 2*l1) * (p - 2*l2) * (p - 2*l3));
        let R = (areaDenom > 0.0001) ? (l1 * l2 * l3 / areaDenom) : Math.max(l1,l2,l3)/2;
        
        let f1 = Math.sqrt(getDistSq(points[i], {x: (points[j].x+points[k].x)/2, y: (points[j].y+points[k].y)/2}));
        let f2 = Math.sqrt(getDistSq(points[j], {x: (points[i].x+points[k].x)/2, y: (points[i].y+points[k].y)/2}));
        let f3 = Math.sqrt(getDistSq(points[k], {x: (points[i].x+points[j].x)/2, y: (points[i].y+points[j].y)/2}));
        
        let r_critical = Math.max(Math.min(R, f1, f2, f3), l1/2, l2/2, l3/2);
        if (r_critical <= radius) {
            triangles.push([i, j, k]);
        }
    }
    return {lines, triangles};
}

// Draw loop
function draw() {
    if (!ctx) return;
    ctx.clearRect(0, 0, width, height);

    // Draw balls
    for (let p of points) {
        ctx.beginPath();
        ctx.fillStyle = my_green;
        ctx.arc(p.x, p.y, radius, 0, 2 * Math.PI);
        ctx.fill();
        
        ctx.strokeStyle = "rgba(100, 100, 100, 0.3)";
        ctx.lineWidth = 1;
        ctx.stroke();
    }

    let lines = [];
    let triangles = [];

    if (complexType === 'alpha') {
        let alpha = getAlphaComplex();
        lines = alpha.lines;
        triangles = alpha.triangles;
    } else {
        lines = getLinesRipsCech();
        triangles = getTrianglesCechRips(complexType);
    }

    // Draw triangles
    ctx.fillStyle = my_coral;
    for (let t of triangles) {
        ctx.beginPath();
        ctx.moveTo(points[t[0]].x, points[t[0]].y);
        ctx.lineTo(points[t[1]].x, points[t[1]].y);
        ctx.lineTo(points[t[2]].x, points[t[2]].y);
        ctx.fill();
    }

    // Draw edges
    ctx.strokeStyle = "#555";
    ctx.lineWidth = 1.5;
    for (let l of lines) {
        ctx.beginPath();
        ctx.moveTo(points[l[0]].x, points[l[0]].y);
        ctx.lineTo(points[l[1]].x, points[l[1]].y);
        ctx.stroke();
    }

    // Draw points
    ctx.fillStyle = "#333";
    for (let p of points) {
        ctx.beginPath();
        ctx.arc(p.x, p.y, 4, 0, 2 * Math.PI);
        ctx.fill();
    }
}
