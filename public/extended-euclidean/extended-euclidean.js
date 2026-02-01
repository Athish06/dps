// Extended Euclidean Algorithm JavaScript

const API_BASE = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : '';

document.getElementById('calculateBtn').addEventListener('click', calculate);

// Enter key triggers calculation
document.querySelectorAll('.number-input').forEach(input => {
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') calculate();
    });
});

async function calculate() {
    const a = parseInt(document.getElementById('inputA').value);
    const m = parseInt(document.getElementById('inputM').value);

    if (isNaN(a) || isNaN(m) || a < 1 || m < 1) {
        alert('Please enter valid positive integers for a and m');
        return;
    }

    const btn = document.getElementById('calculateBtn');
    btn.disabled = true;
    btn.textContent = 'Calculating...';

    try {
        const response = await fetch(`${API_BASE}/api/math-ops`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ operation: 'extended-euclidean', a, m })
        });

        const data = await response.json();

        if (data.success) {
            displayResults(data);
        } else {
            alert('Error: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error connecting to server. Make sure the server is running.');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Calculate';
    }
}

function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');

    resultsSection.style.display = 'block';
    resultsContent.innerHTML = '';

    // Create collapsible sections
    data.sections.forEach(section => {
        const sectionDiv = document.createElement('div');
        sectionDiv.className = 'result-section';

        const header = document.createElement('div');
        header.className = 'section-header';
        header.innerHTML = `
            <span>${section.section}</span>
            <span class="toggle-icon">▼</span>
        `;
        header.onclick = () => {
            sectionDiv.classList.toggle('collapsed');
        };

        const content = document.createElement('div');
        content.className = 'section-content';

        section.subsections.forEach(sub => {
            const subDiv = document.createElement('div');
            subDiv.className = 'subsection';
            subDiv.innerHTML = `
                <div class="subsection-title">${sub.title}</div>
                <pre class="step-content">${sub.content}</pre>
            `;
            content.appendChild(subDiv);
        });

        sectionDiv.appendChild(header);
        sectionDiv.appendChild(content);
        resultsContent.appendChild(sectionDiv);
    });
}
