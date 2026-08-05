let STEPS = [];
let currentStep = 0;
let rows = 3;
let cols = 3;

// References
const matrixDiv = document.getElementById('matrix');
const msgDiv = document.getElementById('status-msg');
const btnNext = document.getElementById('btn-next');
const btnPrev = document.getElementById('btn-prev');
const setupPanel = document.getElementById('setup-panel');
const playbackControls = document.getElementById('playback-controls');

// ---------------------------------------------------------
// UI & State Management
// ---------------------------------------------------------

function resizeGrid() {
    rows = parseInt(document.getElementById('input-rows').value);
    cols = parseInt(document.getElementById('input-cols').value);
    
    matrixDiv.style.gridTemplateRows = `repeat(${rows}, min(80px, 60vh/${rows}))`;
    matrixDiv.style.gridTemplateColumns = `repeat(${cols}, min(80px, 80vw/${cols}))`;
    
    matrixDiv.innerHTML = '';
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            
            const input = document.createElement('input');
            input.type = 'number';
            input.value = '0';
            input.id = `cell-${r}-${c}`;
            
            // Auto scale font size for large matrices
            const maxDim = Math.max(rows, cols);
            if (maxDim > 5) input.style.fontSize = '1.2rem';
            else if (maxDim > 3) input.style.fontSize = '1.5rem';
            
            cell.appendChild(input);
            matrixDiv.appendChild(cell);
        }
    }
}

function randomizeGrid() {
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            const val = Math.floor(Math.random() * 11) - 5; // -5 to 5
            document.getElementById(`cell-${r}-${c}`).value = val;
        }
    }
}

function loadTriangleD1() {
    document.getElementById('input-rows').value = 3;
    document.getElementById('input-cols').value = 3;
    resizeGrid();
    const d1 = [
        [-1, -1, 0],
        [1, 0, -1],
        [0, 1, 1]
    ];
    for (let r = 0; r < 3; r++) {
        for (let c = 0; c < 3; c++) {
            document.getElementById(`cell-${r}-${c}`).value = d1[r][c];
        }
    }
}

function getMatrixFromUI() {
    let m = [];
    for (let r = 0; r < rows; r++) {
        let row = [];
        for (let c = 0; c < cols; c++) {
            row.push(parseInt(document.getElementById(`cell-${r}-${c}`).value) || 0);
        }
        m.push(row);
    }
    return m;
}

function setMatrixToUI(m) {
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            document.getElementById(`cell-${r}-${c}`).value = m[r][c];
        }
    }
}

// ---------------------------------------------------------
// Playback Logic
// ---------------------------------------------------------

function updateGrid(stepIndex) {
    const step = STEPS[stepIndex];
    msgDiv.textContent = step.msg;

    // Remove all highlights/animations
    document.querySelectorAll('.cell').forEach(cell => {
        cell.classList.remove('highlight-row', 'highlight-col', 'pivot', 'value-changed');
    });

    // Update numbers and add changed animation
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            const cellDiv = document.getElementById(`cell-${r}-${c}`).parentElement;
            const input = document.getElementById(`cell-${r}-${c}`);
            
            if (step.changed) {
                const isChanged = step.changed.some(pair => pair[0] === r && pair[1] === c);
                if (isChanged) {
                    setTimeout(() => cellDiv.classList.add('value-changed'), 10);
                }
            }
            input.value = step.matrix[r][c];
        }
    }

    // Apply highlights
    step.highlights.forEach(h => {
        if (h.type === 'row') {
            for (let c = 0; c < cols; c++) {
                const cell = document.getElementById(`cell-${h.idx}-${c}`).parentElement;
                cell.classList.add('highlight-row');
                if (h.pivot === c) cell.classList.add('pivot');
            }
        } else if (h.type === 'col') {
            for (let r = 0; r < rows; r++) {
                const cell = document.getElementById(`cell-${r}-${h.idx}`).parentElement;
                cell.classList.add('highlight-col');
                if (h.pivot === r) cell.classList.add('pivot');
            }
        }
    });

    btnNext.disabled = (currentStep === STEPS.length - 1);
    btnPrev.disabled = (currentStep === 0);
}

function nextStep() {
    if (currentStep < STEPS.length - 1) {
        currentStep++;
        updateGrid(currentStep);
    }
}

function prevStep() {
    if (currentStep > 0) {
        currentStep--;
        updateGrid(currentStep);
    }
}

function resetDemo() {
    setupPanel.style.display = 'flex';
    playbackControls.style.display = 'none';
    msgDiv.textContent = "Enter a matrix or load an example, then click Compute.";
    
    // Enable inputs
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            document.getElementById(`cell-${r}-${c}`).disabled = false;
        }
    }
    
    if (STEPS.length > 0) {
        setMatrixToUI(STEPS[0].matrix);
    }
}

function startSolve() {
    let m = getMatrixFromUI();
    
    // Disable inputs
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            document.getElementById(`cell-${r}-${c}`).disabled = true;
        }
    }
    
    setupPanel.style.display = 'none';
    playbackControls.style.display = 'flex';
    
    STEPS = [];
    current_matrix = JSON.parse(JSON.stringify(m)); // Deep copy
    
    recordStep("Initial Matrix", []);
    
    // Run the algorithm to populate STEPS
    try {
        invariant_factors_algo(current_matrix, 0, 0);
        // Final cleanup: make all diagonal entries positive
        let changed = [];
        let highlights = [];
        let r1s = [];
        for (let i = 0; i < Math.min(rows, cols); i++) {
            if (current_matrix[i][i] < 0) {
                current_matrix[i][i] = -current_matrix[i][i];
                changed.push([i,i]);
                highlights.push({type: 'row', idx: i});
                r1s.push(`R${i+1}`);
            }
        }
        if (changed.length > 0) {
            recordStep(`${r1s.join(', ')} ← -(${r1s.join(', ')})`, highlights, changed);
        }
        recordStep("Done! SNF form reached.", []);
    } catch (e) {
        console.error(e);
        recordStep(e.stack || e.message || "Error", []);
    }
    
    currentStep = 0;
    updateGrid(currentStep);
}


// ---------------------------------------------------------
// Smith Normal Form Algorithm (Ported from implementation_tasks.py)
// ---------------------------------------------------------

let current_matrix = [];

function recordStep(msg, highlights, changed) {
    STEPS.push({
        matrix: JSON.parse(JSON.stringify(current_matrix)),
        msg: msg,
        highlights: highlights || [],
        changed: changed || []
    });
}

function z_div(a, b) {
    let q = Math.trunc(a / b);
    let r = a % b;
    // To match Python's divmod:
    if (r !== 0 && ((a < 0) !== (b < 0))) {
        q -= 1;
        r += b;
    }
    return [q, r];
}

function z_gcdex(a, b) {
    if (a === 0 && b === 0) return [0, 1, 0];
    if (a === 0) return [0, Math.sign(b) || 1, Math.abs(b)];
    if (b === 0) return [Math.sign(a) || 1, 0, Math.abs(a)];

    let x_sign = a < 0 ? -1 : 1;
    let y_sign = b < 0 ? -1 : 1;
    a = Math.abs(a); b = Math.abs(b);

    let x = 1, y = 0, r = 0, s = 1;
    while (b !== 0) {
        let c = a % b;
        let q = Math.floor(a / b);
        let new_r = x - q * r;
        let new_s = y - q * s;
        a = b; b = c;
        x = r; y = s;
        r = new_r; s = new_s;
    }
    return [x * x_sign, y * y_sign, a];
}

function add_columns(m, i, j, a, b, c, d, offset_r, offset_c) {
    let changed = [];
    for (let k = offset_r; k < rows; k++) {
        let e = m[k][i];
        m[k][i] = a * e + b * m[k][j];
        m[k][j] = c * e + d * m[k][j];
        changed.push([k, i]);
        changed.push([k, j]);
    }
    let msg = `C${j+1} ← ${c}·C${i+1} + ${d}·C${j+1}`;
    recordStep(msg, [{type: 'col', idx: i, pivot: offset_r}, {type: 'col', idx: j}], changed);
}

function add_rows(m, i, j, a, b, c, d, offset_r, offset_c) {
    let changed = [];
    for (let k = offset_c; k < cols; k++) {
        let e = m[i][k];
        m[i][k] = a * e + b * m[j][k];
        m[j][k] = c * e + d * m[j][k];
        changed.push([i, k]);
        changed.push([j, k]);
    }
    let msg = `R${j+1} ← ${c}·R${i+1} + ${d}·R${j+1}`;
    recordStep(msg, [{type: 'row', idx: i, pivot: offset_c}, {type: 'row', idx: j}], changed);
}

function clear_column(m, r_start, c_start) {
    if (m[r_start][c_start] === 0) return m;
    let pivot = m[r_start][c_start];
    for (let j = r_start + 1; j < rows; j++) {
        if (m[j][c_start] === 0) continue;
        let [q, r] = z_div(m[j][c_start], pivot);
        if (r === 0) {
            add_rows(m, r_start, j, 1, 0, -q, 1, r_start, c_start);
        } else {
            let [a, b, g] = z_gcdex(pivot, m[j][c_start]);
            let d_0 = z_div(m[j][c_start], g)[0];
            let d_j = z_div(pivot, g)[0];
            add_rows(m, r_start, j, a, b, d_0, -d_j, r_start, c_start);
            pivot = g;
        }
    }
    return m;
}

function clear_row(m, r_start, c_start) {
    if (m[r_start][c_start] === 0) return m;
    let pivot = m[r_start][c_start];
    for (let j = c_start + 1; j < cols; j++) {
        if (m[r_start][j] === 0) continue;
        let [q, r] = z_div(m[r_start][j], pivot);
        if (r === 0) {
            add_columns(m, c_start, j, 1, 0, -q, 1, r_start, c_start);
        } else {
            let [a, b, g] = z_gcdex(pivot, m[r_start][j]);
            let d_0 = z_div(m[r_start][j], g)[0];
            let d_j = z_div(pivot, g)[0];
            add_columns(m, c_start, j, a, b, d_0, -d_j, r_start, c_start);
            pivot = g;
        }
    }
    return m;
}

function invariant_factors_algo(m, r_start, c_start) {
    if (r_start >= rows || c_start >= cols) return;
    
    // 1. Bring a non-zero element to [r_start][c_start]
    let found_r = -1;
    let found_c = -1;
    for (let i = r_start; i < rows; i++) {
        for (let j = c_start; j < cols; j++) {
            if (m[i][j] !== 0) {
                found_r = i;
                found_c = j;
                break;
            }
        }
        if (found_r !== -1) break;
    }

    // If entire submatrix is zero, we are done!
    if (found_r === -1) return;

    // Swap row if needed
    if (found_r !== r_start) {
        for (let k = c_start; k < cols; k++) {
            let temp = m[r_start][k];
            m[r_start][k] = m[found_r][k];
            m[found_r][k] = temp;
        }
        let changed = [];
        for(let k=c_start; k<cols; k++) { changed.push([r_start, k]); changed.push([found_r, k]); }
        recordStep(`Swap Row ${r_start+1} and Row ${found_r+1}`, [{type: 'row', idx: r_start}, {type: 'row', idx: found_r}], changed);
    }
    
    // Swap col if needed
    if (found_c !== c_start) {
        for (let k = r_start; k < rows; k++) {
            let temp = m[k][r_start];
            m[k][r_start] = m[k][found_c];
            m[k][found_c] = temp;
        }
        let changed = [];
        for(let k=r_start; k<rows; k++) { changed.push([k, r_start]); changed.push([k, found_c]); }
        recordStep(`Swap Col ${c_start+1} and Col ${found_c+1}`, [{type: 'col', idx: r_start}, {type: 'col', idx: found_c}], changed);
    }

    // 2. Iteratively clear row and column
    while (true) {
        let has_non_zero = false;
        for (let i = c_start + 1; i < cols; i++) if (m[r_start][i] !== 0) has_non_zero = true;
        for (let i = r_start + 1; i < rows; i++) if (m[i][c_start] !== 0) has_non_zero = true;
            
        if (!has_non_zero) break;
        
        clear_column(m, r_start, c_start);
        clear_row(m, r_start, c_start);
    }

    // 3. Recursion
    invariant_factors_algo(m, r_start + 1, c_start + 1);

    // 4. Divisibility condition a_i | a_{i+1}
    // We can do this in a simple sweep at the end if needed, but for visual pedagogy, 
    // the core diagonal form is usually enough. For completeness, we enforce it:
    if (m[r_start][c_start] !== 0 && r_start+1 < rows && c_start+1 < cols) {
        if (m[r_start+1][c_start+1] !== 0) {
            let [q, r] = z_div(m[r_start+1][c_start+1], m[r_start][c_start]);
            if (r !== 0) {
                // Add next row to this row so the non-divisible element is in the same col
                add_rows(m, r_start+1, r_start, 1, 0, 1, 1, r_start, c_start);
                // Now restart clearing on this submatrix
                invariant_factors_algo(m, r_start, c_start);
            }
        }
    }
}

// ---------------------------------------------------------
// Theme & Init
// ---------------------------------------------------------

resizeGrid();

window.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'theme-change') {
        if (event.data.theme === 'light') {
            document.body.classList.add('light-theme');
        } else {
            document.body.classList.remove('light-theme');
        }
    }
});
window.parent.postMessage({ type: 'get-theme' }, '*');
