// Keyed Columnar Cipher JavaScript

document.addEventListener('DOMContentLoaded', () => {
    // Initialize column order boxes from keyword
    updateColumnOrderBoxes();

    document.getElementById('processBtn').addEventListener('click', process);

    // Only regenerate boxes when keyword length changes (not on every input)
    let lastKeywordLength = document.getElementById('keyword').value.length;
    document.getElementById('keyword').addEventListener('input', () => {
        const newLength = document.getElementById('keyword').value.replace(/[^A-Za-z]/g, '').length;
        if (newLength !== lastKeywordLength) {
            lastKeywordLength = newLength;
            updateColumnOrderBoxes();
        }
    });

    // Input focus select all
    document.querySelectorAll('input[type="text"]').forEach(input => {
        input.addEventListener('focus', (e) => e.target.select());
    });
});

function calculateKeyOrder(keyword) {
    // Calculate alphabetical ranking with left-to-right tie-breaker
    const indexed = keyword.toUpperCase().split('').map((char, idx) => ({ char, idx }));
    const sorted = [...indexed].sort((a, b) => {
        if (a.char !== b.char) return a.char.localeCompare(b.char);
        return a.idx - b.idx; // Left-to-right for ties
    });

    // Create order array: order[originalIndex] = readPosition (1-indexed)
    const order = new Array(keyword.length);
    sorted.forEach((item, sortedIdx) => {
        order[item.idx] = sortedIdx + 1; // 1-indexed
    });

    return order;
}

function updateColumnOrderBoxes() {
    const keyword = document.getElementById('keyword').value.toUpperCase().replace(/[^A-Z]/g, '');
    const container = document.getElementById('columnOrderBoxes');
    container.innerHTML = '';

    if (keyword.length === 0) {
        container.innerHTML = '<span style="opacity: 0.6;">Enter a keyword to generate column order</span>';
        return;
    }

    const order = calculateKeyOrder(keyword);

    order.forEach((rank, idx) => {
        const box = document.createElement('input');
        box.type = 'number';
        box.className = 'array-box';
        box.value = rank;
        box.min = 1;
        box.max = keyword.length;
        box.dataset.index = idx;
        box.title = `Column ${idx + 1} (${keyword[idx]}) - Read order: ${rank}`;
        container.appendChild(box);
    });
}

function getColumnOrder() {
    const boxes = document.querySelectorAll('#columnOrderBoxes .array-box');
    const order = [];
    boxes.forEach(box => {
        order.push(parseInt(box.value) || 1);
    });
    return order;
}

async function process() {
    const processBtn = document.getElementById('processBtn');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');

    const mode = document.getElementById('operation').value;

    processBtn.disabled = true;
    processBtn.textContent = 'Processing...';

    try {
        const inputText = document.getElementById('inputText').value.toUpperCase().replace(/[^A-Z]/g, '');
        const keyword = document.getElementById('keyword').value.toUpperCase().replace(/[^A-Z]/g, '');
        const columnOrder = getColumnOrder();

        // Validate
        const errors = [];
        if (inputText.length === 0) {
            errors.push('Input text cannot be empty');
        }
        if (keyword.length === 0) {
            errors.push('Keyword cannot be empty');
        }
        if (columnOrder.length === 0) {
            errors.push('Column order not set');
        }

        if (errors.length > 0) {
            resultsContent.innerHTML = `<div class="error">${errors.join('<br>')}</div>`;
            resultsSection.classList.add('visible');
            processBtn.disabled = false;
            processBtn.textContent = 'Process';
            return;
        }

        const requestBody = {
            cipher: 'keyed',
            mode: mode,
            keyword: keyword,
            columnOrder: columnOrder
        };

        if (mode === 'encrypt') {
            requestBody.plaintext = inputText;
        } else {
            requestBody.ciphertext = inputText;
        }

        const response = await fetch('/api/co1', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody)
        });

        const result = await response.json();
        renderDetailedResults(result);

    } catch (error) {
        resultsContent.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        resultsSection.classList.add('visible');
    } finally {
        processBtn.disabled = false;
        processBtn.textContent = 'Process';
    }
}

function renderDetailedResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');

    resultsContent.innerHTML = '';

    if (!data.success) {
        resultsContent.innerHTML = `<div class="error">${data.error || 'Keyed cipher operation failed'}</div>`;
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
