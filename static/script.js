function analyzePassword() {
    const password = document.getElementById('passwordInput').value;

    fetch('/check_password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: password })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('strengthResult').innerText = `Strength: ${data.strength}`;

        const strengthBar = document.getElementById('strengthBar');
        let width = (data.score / 5) * 100;
        strengthBar.style.width = width + "%";

        strengthBar.style.backgroundColor = data.strength === "Weak" ? "#A9DDF4" :
                                             data.strength === "Moderate" ? "#A9DDF4" : "#A9DDF4";

        document.getElementById('tips').innerText = data.tips.length > 0 ? "Tip: " + data.tips.join(' ') :
                                                      "Good job! Your password is strong.";
    });
}

function suggestPassword() {
    const length = document.getElementById('lengthInput').value;

    fetch(`/suggest_password?length=${length}`)
    .then(response => response.json())
    .then(data => {
        document.getElementById('suggestionResult').innerText = `Suggestion: ${data.suggestion}`;
    });
}

function copyPassword() {
    const suggestion = document.getElementById('suggestionResult').innerText.replace('Suggestion: ', '');
    if (suggestion.trim() !== "") {
        navigator.clipboard.writeText(suggestion);
        alert('Password copied to clipboard!');
    } else {
        alert('No password to copy!');
    }
}

function flipCard() {
    document.querySelector(".flip-card").classList.toggle("flipped");
}
