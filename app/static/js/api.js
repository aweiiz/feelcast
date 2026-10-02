let deviceId = localStorage.getItem('device_id');
if (!deviceId) {
    deviceId = crypto.randomUUID();
    localStorage.setItem('device_id', deviceId);
}

function getAuthHeaders() {
    const token = localStorage.getItem('jwt_token');
    if (token) return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` };
    return { 'Content-Type': 'application/json', 'X-Device-ID': deviceId };
}

async function authFetch(url, options) {
    const res = await fetch(url, options);
    if (res.status === 401) {
        localStorage.removeItem('jwt_token');
        localStorage.removeItem('user_email');
        localStorage.removeItem('user_nickname');
        showPage('page-login');
    }
    return res;
}

async function apiRequestCode(email) {
    return fetch('/auth/request-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
    });
}

async function apiVerifyCode(email, code) {
    return fetch('/auth/verify-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, code })
    });
}

async function apiOnboarding(data) {
    return authFetch('/onboarding', { method: 'POST', headers: getAuthHeaders(), body: JSON.stringify(data) });
}

async function apiAdvice(city) {
    return authFetch(`/advice/${city}`, { method: 'POST', headers: getAuthHeaders() });
}

async function apiCheckin(city, intensity, comment) {
    return authFetch('/checkin', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ city, intensity, comment: comment || null })
    });
}

async function apiFeed(city) {
    return fetch(`/feed?city=${city}`);
}

async function apiGetMe() {
    return authFetch('/me', { headers: getAuthHeaders() });
}

async function apiUpdateMe(data) {
    return authFetch('/me', { method: 'PATCH', headers: getAuthHeaders(), body: JSON.stringify(data) });
}