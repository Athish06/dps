// ADFGVX Cipher JavaScript

const API_BASE = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : '';

document.getElementById('encryptBtn').addEventListener('click', () => process('encrypt'));
document.getElementById('decryptBtn').addEventListener('click', () => process('decrypt'));

// Enter key triggers encryption
document.querySelectorAll('.text-input').forEach(input => {
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') process('encrypt');
    });
});

async function process(mode) {
    const inputText = document.getElementById('inputText').value.trim();
    const polyKey = document.getElementById('polyKey').value.trim();
    const transKey = document.getElementById('transKey').value.trim();

    if (!inputText || !polyKey || !transKey) {
        alert('Please fill in all fields');
        return;
    }

    const encryptBtn = document.getElementById('encryptBtn');
    const decryptBtn = document.getElementById('decryptBtn');
    encryptBtn.disabled = true;
    decryptBtn.disabled = true;

    const activeBtn = mode === 'encrypt' ? encryptBtn : decryptBtn;
    const originalText = activeBtn.textContent;
    activeBtn.textContent = 'Processing...';

    try {
        const body = {
            mode: mode,
            polyKey: polyKey,
            transKey: transKey
        };

        if (mode === 'encrypt') {
            body.plaintext = inputText;
        } else {
            body.ciphertext = inputText;
        }

        const response = await fetch(`${API_BASE}/api/adfgvx`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
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
        encryptBtn.disabled = false;
        decryptBtn.disabled = false;
        activeBtn.textContent = originalText;
    }
}

function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');

    resultsSection.style.display = 'block';
    resultsContent.innerHTML = '';

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
