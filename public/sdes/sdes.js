// Default values
const defaults = {
    plaintext: ['1', '0', '1', '1', '1', '1', '0', '1'],
    key: ['1', '0', '1', '0', '0', '0', '0', '0', '1', '0'],
    P10: ['3', '5', '2', '7', '4', '10', '1', '9', '8', '6'],
    P8: ['6', '3', '7', '4', '8', '5', '10', '9'],
    IP: ['2', '6', '3', '1', '4', '8', '5', '7'],
    EP: ['4', '1', '2', '3', '2', '3', '4', '1'],
    P4: ['2', '4', '3', '1'],
    S0: [
        ['01', '00', '11', '10'],
        ['11', '10', '01', '00'],
        ['00', '10', '01', '11'],
        ['11', '01', '11', '10']
    ],
    S1: [
        ['00', '01', '10', '11'],
        ['10', '00', '01', '11'],
        ['11', '00', '01', '00'],
        ['10', '01', '00', '11']
    ]
};

// Theme Management
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeUI(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeUI(newTheme);
}

function updateThemeUI(theme) {
    const sunIcon = document.getElementById('sunIcon');
    const moonIcon = document.getElementById('moonIcon');
    const themeText = document.getElementById('themeText');

    if (theme === 'dark') {
        sunIcon.style.display = 'none';
        moonIcon.style.display = 'block';
        themeText.textContent = 'Light';
    } else {
        sunIcon.style.display = 'block';
        moonIcon.style.display = 'none';
        themeText.textContent = 'Dark';
    }
}

// Create array input boxes
function createArrayBoxes(containerId, values, maxLen = 1) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    values.forEach((val, index) => {
        const input = document.createElement('input');
        input.type = 'text';
        input.className = `array-box${maxLen > 1 ? '' : ' small'}`;
        input.maxLength = maxLen;
        input.value = val;
        input.dataset.index = index;

        // Select all text on focus so typing replaces it
        input.addEventListener('focus', (e) => {
            e.target.select();
        });

        // Auto-focus next input
        input.addEventListener('input', (e) => {
            if (e.target.value.length >= maxLen && index < values.length - 1) {
                const next = container.children[index + 1];
                if (next) next.focus();
            }
        });

        // Handle backspace to go to previous
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && e.target.value === '' && index > 0) {
                const prev = container.children[index - 1];
                if (prev) prev.focus();
            }
        });

        container.appendChild(input);
    });
}

// Create 2D matrix grid for S-boxes
function createMatrixGrid(containerId, matrix) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    matrix.forEach((row, rowIndex) => {
        row.forEach((val, colIndex) => {
            const input = document.createElement('input');
            input.type = 'text';
            input.className = 'matrix-box';
            input.maxLength = 2;
            input.value = val;
            input.dataset.row = rowIndex;
            input.dataset.col = colIndex;

            // Select all text on focus so typing replaces it
            input.addEventListener('focus', (e) => {
                e.target.select();
            });

            container.appendChild(input);
        });
    });
}

// Get values from array boxes
function getArrayValues(containerId) {
    const container = document.getElementById(containerId);
    const inputs = container.querySelectorAll('input');
    return Array.from(inputs).map(input => input.value);
}

// Get values from matrix grid
function getMatrixValues(containerId) {
    const container = document.getElementById(containerId);
    const inputs = container.querySelectorAll('input');
    const matrix = [[], [], [], []];

    inputs.forEach(input => {
        const row = parseInt(input.dataset.row);
        const col = parseInt(input.dataset.col);
        matrix[row][col] = input.value;
    });

    return matrix;
}

// Collect all input data
function collectInputData() {
    return {
        plaintext: getArrayValues('plaintextBoxes').join(''),
        key: getArrayValues('keyBoxes').join(''),
        P10: getArrayValues('p10Boxes').map(v => parseInt(v)),
        P8: getArrayValues('p8Boxes').map(v => parseInt(v)),
        IP: getArrayValues('ipBoxes').map(v => parseInt(v)),
        EP: getArrayValues('epBoxes').map(v => parseInt(v)),
        P4: getArrayValues('p4Boxes').map(v => parseInt(v)),
        S0: getMatrixValues('s0Grid'),
        S1: getMatrixValues('s1Grid')
    };
}

// Validate inputs
function validateInputs(data) {
    const errors = [];

    if (!/^[01]{8}$/.test(data.plaintext)) {
        errors.push('Plaintext must be exactly 8 binary digits (0 or 1)');
    }

    if (!/^[01]{10}$/.test(data.key)) {
        errors.push('Key must be exactly 10 binary digits (0 or 1)');
    }

    if (data.P10.some(v => isNaN(v) || v < 1 || v > 10)) {
        errors.push('P10 values must be numbers from 1 to 10');
    }

    if (data.P8.some(v => isNaN(v) || v < 1 || v > 10)) {
        errors.push('P8 values must be numbers from 1 to 10');
    }

    if (data.IP.some(v => isNaN(v) || v < 1 || v > 8)) {
        errors.push('IP values must be numbers from 1 to 8');
    }

    if (data.EP.some(v => isNaN(v) || v < 1 || v > 4)) {
        errors.push('EP values must be numbers from 1 to 4');
    }

    if (data.P4.some(v => isNaN(v) || v < 1 || v > 4)) {
        errors.push('P4 values must be numbers from 1 to 4');
    }

    // Validate S-boxes
    const sboxPattern = /^[01]{2}$/;
    data.S0.flat().forEach((val, i) => {
        if (!sboxPattern.test(val)) {
            errors.push(`S0 box values must be 2-bit binary (e.g., 00, 01, 10, 11)`);
        }
    });

    data.S1.flat().forEach((val, i) => {
        if (!sboxPattern.test(val)) {
            errors.push(`S1 box values must be 2-bit binary (e.g., 00, 01, 10, 11)`);
        }
    });

    // Remove duplicates
    return [...new Set(errors)];
}

// Render detailed results
function renderDetailedResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');

    resultsContent.innerHTML = '';

    if (!data.success) {
        resultsContent.innerHTML = `<div class="error">${data.error || 'Encryption failed'}</div>`;
        resultsSection.classList.add('visible');
        return;
    }

    // Render each section
    if (!data.sections || !Array.isArray(data.sections)) {
        resultsContent.innerHTML = `<div class="error">Invalid response format. Please restart the server with: python dev_server.py</div>`;
        resultsSection.classList.add('visible');
        return;
    }

    data.sections.forEach((section, sectionIndex) => {
        const sectionDiv = document.createElement('div');
        sectionDiv.className = 'result-section';

        // Section header
        const sectionHeader = document.createElement('h3');
        sectionHeader.className = 'section-header';
        sectionHeader.innerHTML = `<span class="section-number">${sectionIndex + 1}</span>${section.section}`;
        sectionDiv.appendChild(sectionHeader);

        // Subsections
        section.subsections.forEach((subsection, subIndex) => {
            const subsectionDiv = document.createElement('div');
            subsectionDiv.className = 'subsection';

            const subsectionTitle = document.createElement('h4');
            subsectionTitle.className = 'subsection-title';
            subsectionTitle.textContent = subsection.title;
            subsectionDiv.appendChild(subsectionTitle);

            const contentPre = document.createElement('pre');
            contentPre.className = 'step-content';
            contentPre.textContent = subsection.content;
            subsectionDiv.appendChild(contentPre);

            sectionDiv.appendChild(subsectionDiv);
        });

        resultsContent.appendChild(sectionDiv);
    });

    resultsSection.classList.add('visible');
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Perform encryption
async function encrypt() {
    const btn = document.getElementById('encryptBtn');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');

    btn.disabled = true;
    btn.textContent = 'Encrypting...';

    try {
        const data = collectInputData();

        // Validate
        const errors = validateInputs(data);
        if (errors.length > 0) {
            resultsContent.innerHTML = `<div class="error">${errors.join('<br>')}</div>`;
            resultsSection.classList.add('visible');
            return;
        }

        // Send to API
        const response = await fetch('/api/sdes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        renderDetailedResults(result);

    } catch (error) {
        resultsContent.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        resultsSection.classList.add('visible');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Encrypt';
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initTheme();

    // Create input boxes with default values
    createArrayBoxes('plaintextBoxes', defaults.plaintext, 1);
    createArrayBoxes('keyBoxes', defaults.key, 1);
    createArrayBoxes('p10Boxes', defaults.P10, 2);
    createArrayBoxes('p8Boxes', defaults.P8, 2);
    createArrayBoxes('ipBoxes', defaults.IP, 1);
    createArrayBoxes('epBoxes', defaults.EP, 1);
    createArrayBoxes('p4Boxes', defaults.P4, 1);
    createMatrixGrid('s0Grid', defaults.S0);
    createMatrixGrid('s1Grid', defaults.S1);

    // Event listeners
    document.getElementById('themeToggle').addEventListener('click', toggleTheme);
    document.getElementById('encryptBtn').addEventListener('click', encrypt);
});
