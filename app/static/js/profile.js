async function loadProfile() {
    const res = await apiGetMe();
    if (!res.ok) return;
    const d = await res.json();

    const name = d.nickname || d.email || '?';
    document.getElementById('profile-avatar').textContent = name[0].toUpperCase();
    document.getElementById('profile-name').textContent = d.nickname || 'Без имени';
    document.getElementById('profile-email').textContent = d.email || 'Гость';
    document.getElementById('profile-nickname-input').value = d.nickname || '';

    document.getElementById('stat-checkins').textContent = d.checkin_count ?? '—';
    document.getElementById('stat-cities').textContent = d.top_cities?.length ?? '—';

    const citiesEl = document.getElementById('profile-cities');
    if (!d.top_cities || d.top_cities.length === 0) {
        citiesEl.innerHTML = '<div style="color:#9e9790;font-size:14px;padding:12px 0">Пока нет чекинов</div>';
    } else {
        citiesEl.innerHTML = d.top_cities.map(c => `
            <div class="city-item">
                <span>📍 ${c.city}</span>
                <span class="city-cnt">${c.count} чекин${c.count === 1 ? '' : c.count < 5 ? 'а' : 'ов'}</span>
            </div>
        `).join('');
    }

    const a = d.answers || {};
    if (a.cold_sensitivity) setSelectVal('profile-cold_sensitivity', a.cold_sensitivity);
    if (a.climate)          setSelectVal('profile-climate', a.climate);
    if (a.activity)         setSelectVal('profile-activity', a.activity);
    if (a.rain_sensitivity) setSelectVal('profile-rain_sensitivity', a.rain_sensitivity);
}

function setSelectVal(id, value) {
    const el = document.getElementById(id);
    if (!el) return;
    for (const opt of el.options) {
        if (opt.value === value) { el.value = value; break; }
    }
}

async function saveNickname() {
    const nickname = document.getElementById('profile-nickname-input').value.trim();
    if (!nickname) return alert('Введи имя');
    const res = await apiUpdateMe({ nickname });
    if (res.ok) {
        localStorage.setItem('user_nickname', nickname);
        document.getElementById('profile-name').textContent = nickname;
        document.getElementById('profile-avatar').textContent = nickname[0].toUpperCase();
    } else {
        alert('Ошибка сохранения');
    }
}

async function saveProfileSettings() {
    const data = {
        cold_sensitivity: document.getElementById('profile-cold_sensitivity').value,
        climate:          document.getElementById('profile-climate').value,
        activity:         document.getElementById('profile-activity').value,
        rain_sensitivity: document.getElementById('profile-rain_sensitivity').value,
        gender: null
    };
    const res = await apiOnboarding(data);
    if (res.ok) {
        alert('Настройки сохранены');
    } else {
        alert('Ошибка: ' + await res.text());
    }
}
