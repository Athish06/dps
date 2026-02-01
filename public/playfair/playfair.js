// Playfair Cipher JavaScript

document.addEventListener('DOMContentLoaded', () => {
    // Input focus select all
    document.querySelectorAll('input').forEach(input => {
        input.addEventListener('focus', (e) => e.target.select());
    });

    document.getElementById('encryptBtn').addEventListener('click', encrypt);
});

async function encrypt() {
    const btn = document.getElementById('encryptBtn');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');

    btn.disabled = true;
    btn.textContent = 'Processing...';

    try {
        const plaintext = document.getElementById('plaintext').value;
        const keyword = document.getElementById('keyword').value;

        // Validate
        const errors = [];
        if (!plaintext.trim()) errors.push('Plaintext cannot be empty');
        if (!keyword.trim()) errors.push('Keyword cannot be empty');

        if (errors.length > 0) {
            resultsContent.innerHTML = `<div class="error">${errors.join('<br>')}</div>`;
            resultsSection.classList.add('visible');
            return;
        }

        const response = await fetch('/api/co1', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ cipher: 'playfair', plaintext, keyword })
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

function renderDetailedResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');

    resultsContent.innerHTML = '';

    if (!data.success) {
        resultsContent.innerHTML = `<div class="error">${data.error || 'Playfair cipher operation failed'}</div>`;
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
