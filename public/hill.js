// Hill Cipher JavaScript

const defaultMatrix3x3 = [
    [6, 24, 1],
    [13, 16, 10],
    [20, 17, 15]
];

let currentMatrixSize = 3;

document.addEventListener('DOMContentLoaded', () => {
    initMatrix(3);

    document.getElementById('updateMatrixBtn').addEventListener('click', () => {
        const size = parseInt(document.getElementById('matrixSize').value);
        if (size >= 2 && size <= 5) {
            initMatrix(size);
        }
    });

    document.getElementById('encryptBtn').addEventListener('click', encrypt);

    // Input focus select all
    document.querySelectorAll('input[type="number"], input[type="text"]').forEach(input => {
        input.addEventListener('focus', (e) => e.target.select());
    });
});

function initMatrix(size) {
    currentMatrixSize = size;
    const container = document.getElementById('keyMatrix');
    container.innerHTML = '';
    container.style.gridTemplateColumns = `repeat(${size}, 50px)`;

    document.getElementById('matrixSizeLabel').textContent = size;
    document.getElementById('matrixSizeLabel2').textContent = size;

    for (let i = 0; i < size; i++) {
        for (let j = 0; j < size; j++) {
            const input = document.createElement('input');
            input.type = 'number';
            input.className = 'matrix-input';
            input.min = 0;
            input.max = 25;
            input.dataset.row = i;
            input.dataset.col = j;

            // Use default values for 3x3, otherwise 0
            if (size === 3 && defaultMatrix3x3[i] && defaultMatrix3x3[i][j] !== undefined) {
                input.value = defaultMatrix3x3[i][j];
            } else {
                input.value = i === j ? 1 : 0; // Identity-ish matrix for others
            }

            input.addEventListener('focus', (e) => e.target.select());
            container.appendChild(input);
        }
    }
}

function getMatrixValues() {
    const container = document.getElementById('keyMatrix');
    const inputs = container.querySelectorAll('input');
    const matrix = [];

    for (let i = 0; i < currentMatrixSize; i++) {
        matrix.push([]);
    }

    inputs.forEach(input => {
        const row = parseInt(input.dataset.row);
        const col = parseInt(input.dataset.col);
        matrix[row][col] = parseInt(input.value) || 0;
    });

    return matrix;
}

async function encrypt() {
    const btn = document.getElementById('encryptBtn');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');

    btn.disabled = true;
    btn.textContent = 'Processing...';

    try {
        const plaintext = document.getElementById('plaintext').value.toUpperCase().replace(/[^A-Z]/g, '');
        const keyMatrix = getMatrixValues();
        const m = currentMatrixSize;

        // Validate
        const errors = [];
        if (plaintext.length === 0) {
            errors.push('Plaintext cannot be empty');
        }
        if (plaintext.length % m !== 0) {
            errors.push(`Plaintext length must be a multiple of ${m}. Current length: ${plaintext.length}`);
        }

        if (errors.length > 0) {
            resultsContent.innerHTML = `<div class="error">${errors.join('<br>')}</div>`;
            resultsSection.classList.add('visible');
            return;
        }

        const response = await fetch('/api/hill', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ plaintext, keyMatrix, m })
        });

        const result = await response.json();
        renderDetailedResults(result);

    } catch (error) {
        resultsContent.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        resultsSection.classList.add('visible');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Encrypt & Decrypt';
    }
}

function renderDetailedResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');

    resultsContent.innerHTML = '';

    if (!data.success) {
        resultsContent.innerHTML = `<div class="error">${data.error || 'Hill cipher operation failed'}</div>`;
        resultsSection.classList.add('visible');
        return;
    }

    if (!data.sections || !Array.isArray(data.sections)) {
        resultsContent.innerHTML = `<div class="error">Invalid response format</div>`;
        resultsSection.classList.add('visible');
        return;
    }

    data.sections.forEach((section, sectionIndex) => {
        const sectionDiv = document.createElement('div');
        sectionDiv.className = 'result-section';

        const sectionHeader = document.createElement('h3');
        sectionHeader.className = 'section-header';
        sectionHeader.innerHTML = `<span class="section-number">${sectionIndex + 1}</span>${section.section}`;
        sectionDiv.appendChild(sectionHeader);

        section.subsections.forEach((subsection) => {
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
