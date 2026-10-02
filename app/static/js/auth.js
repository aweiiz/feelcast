async function requestCode() {
    const email = document.getElementById('login-email').value.trim();
    if (!email) return alert('Введи email');

    const res = await apiRequestCode(email);
    if (!res.ok) return alert('Ошибка: ' + await res.text());

    const data = await res.json();
    document.getElementById('verify-email-label').textContent = email;
    if (data.debug_code) {
        document.getElementById('debug-code-box').style.display = 'block';
        document.getElementById('debug-code').textContent = data.debug_code;
    }
    showPage('page-verify');
}

async function verifyCode() {
    const email = document.getElementById('login-email').value.trim();
    const code = document.getElementById('verify-code').value.trim();
    if (!code) return alert('Введи код');

    const res = await apiVerifyCode(email, code);
    if (!res.ok) return alert('Неверный или истёкший код');

    const data = await res.json();
    localStorage.setItem('jwt_token', data.access_token);
    localStorage.setItem('user_email', email);

    showPage(localStorage.getItem('onboarding_done') ? 'page-advice' : 'page-onboarding');
}

function continueAsGuest() {
    showPage(localStorage.getItem('onboarding_done') ? 'page-advice' : 'page-onboarding');
}

function logout() {
    localStorage.removeItem('jwt_token');
    localStorage.removeItem('user_email');
    localStorage.removeItem('user_nickname');
    showPage('page-login');
}
