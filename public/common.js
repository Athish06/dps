// Common JavaScript for all cipher pages

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

    if (!sunIcon || !moonIcon || !themeText) return;

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

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initTheme();

    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
});
