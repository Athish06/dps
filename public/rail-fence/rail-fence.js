// Rail Fence Cipher JavaScript

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('processBtn').addEventListener('click', process);

    // Input focus select all
    document.querySelectorAll('input[type="text"], input[type="number"]').forEach(input => {
        input.addEventListener('focus', (e) => e.target.select());
    });
});

async function process() {
    const processBtn = document.getElementById('processBtn');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');

    const mode = document.getElementById('operation').value;

    processBtn.disabled = true;
    processBtn.textContent = 'Processing...';

    try {
        const inputText = document.getElementById('inputText').value.toUpperCase().replace(/[^A-Z]/g, '');
        const numRails = parseInt(document.getElementById('numRails').value);

        // Validate
        const errors = [];
        if (inputText.length === 0) {
            errors.push('Input text cannot be empty');
        }
        if (numRails < 2) {
            errors.push('Number of rails must be at least 2');
        }
        if (numRails > inputText.length) {
            errors.push('Number of rails cannot exceed text length');
        }

        if (errors.length > 0) {
            resultsContent.innerHTML = `<div class="error">${errors.join('<br>')}</div>`;
            resultsSection.classList.add('visible');
            return;
        }

        const requestBody = {
            cipher: 'rail_fence',
            mode: mode,
            numRails: numRails
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
        resultsContent.innerHTML = `<div class="error">${data.error || 'Rail Fence operation failed'}</div>`;
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
