// Monoalphabetic Cipher JavaScript

document.addEventListener('DOMContentLoaded', () => {
    // Input focus select all
    document.querySelectorAll('input').forEach(input => {
        input.addEventListener('focus', (e) => e.target.select());
    });

    // Mode change handler
    const modeSelect = document.getElementById('cipherMode');
    modeSelect.addEventListener('change', updateModeUI);
    updateModeUI();

    document.getElementById('encryptBtn').addEventListener('click', process);
});

function updateModeUI() {
    const mode = document.getElementById('cipherMode').value;
    const keyKGroup = document.getElementById('keyKGroup');
    const keyAGroup = document.getElementById('keyAGroup');
    const keyBGroup = document.getElementById('keyBGroup');
    const modeInfo = document.getElementById('modeInfo');

    if (mode === 'additive') {
        keyKGroup.style.display = 'block';
        keyAGroup.style.display = 'none';
        keyBGroup.style.display = 'none';
        modeInfo.innerHTML = `
            <strong>Additive Cipher (Caesar):</strong>
            <p>E(x) = (x + k) mod 26 &nbsp;|&nbsp; D(x) = (x - k) mod 26</p>
        `;
    } else if (mode === 'multiplicative') {
        keyKGroup.style.display = 'block';
        keyAGroup.style.display = 'none';
        keyBGroup.style.display = 'none';
        modeInfo.innerHTML = `
            <strong>Multiplicative Cipher:</strong>
            <p>E(x) = (x × k) mod 26 &nbsp;|&nbsp; D(x) = (x × k⁻¹) mod 26</p>
            <p><em>k must be coprime with 26: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25</em></p>
        `;
    } else { // affine
        keyKGroup.style.display = 'none';
        keyAGroup.style.display = 'block';
        keyBGroup.style.display = 'block';
        modeInfo.innerHTML = `
            <strong>Affine Cipher:</strong>
            <p>E(x) = (a×x + b) mod 26 &nbsp;|&nbsp; D(x) = a⁻¹×(x - b) mod 26</p>
            <p><em>a must be coprime with 26: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25</em></p>
        `;
    }
}

async function process() {
    const btn = document.getElementById('encryptBtn');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');

    btn.disabled = true;
    btn.textContent = 'Processing...';

    try {
        const plaintext = document.getElementById('plaintext').value;
        const mode = document.getElementById('cipherMode').value;
        const operation = document.getElementById('operation').value;
        const key_k = parseInt(document.getElementById('keyK').value);
        const key_a = parseInt(document.getElementById('keyA').value);
        const key_b = parseInt(document.getElementById('keyB').value);

        // Validate
        const errors = [];
        if (!plaintext.trim()) errors.push('Plaintext cannot be empty');

        if (errors.length > 0) {
            resultsContent.innerHTML = `<div class="error">${errors.join('<br>')}</div>`;
            resultsSection.classList.add('visible');
            return;
        }

        const response = await fetch('/api/co1', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cipher: 'monoalphabetic', plaintext, mode, operation, key_k, key_a, key_b })
        });

        const result = await response.json();
        renderDetailedResults(result);

    } catch (error) {
        resultsContent.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        resultsSection.classList.add('visible');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Process';
    }
}

function renderDetailedResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');

    resultsContent.innerHTML = '';

    if (!data.success) {
        resultsContent.innerHTML = `<div class="error">${data.error || 'Monoalphabetic cipher operation failed'}</div>`;
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
