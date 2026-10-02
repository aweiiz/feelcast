// ── Навигация ──────────────────────────────────────────────────────────────

const ALL_PAGES = [
    'page-login', 'page-verify', 'page-onboarding',
    'page-advice', 'page-checkin', 'page-feed', 'page-profile'
];

const NAV_PAGES = ['page-advice', 'page-checkin', 'page-feed', 'page-profile'];

function showPage(id) {
    ALL_PAGES.forEach(p => {
        const el = document.getElementById(p);
        if (el) el.classList.remove('active');
    });
    const target = document.getElementById(id);
    if (target) target.classList.add('active');

    const withNav = NAV_PAGES.includes(id);
    document.getElementById('topnav').style.display = withNav ? 'flex' : 'none';
    document.getElementById('bottom-nav').style.display = withNav ? 'block' : 'none';

    // Подсветка активного пункта навигации
    document.querySelectorAll('.nav-link, .bottom-nav-item').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.page === id);
    });

    if (id === 'page-profile') loadProfile();
    if (id === 'page-advice') setAdviceDate();
}

function setAdviceDate() {
    const el = document.getElementById('advice-date');
    if (!el) return;
    const now = new Date();
    const days = ['Воскресенье','Понедельник','Вторник','Среда','Четверг','Пятница','Суббота'];
    const months = ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря'];
    el.textContent = `${days[now.getDay()]}, ${now.getDate()} ${months[now.getMonth()]}`;
}

// ── Онбординг (пошаговый) ──────────────────────────────────────────────────

const OB_STEPS = 4;
let obCurrentStep = 1;
const obAnswers = {};

function obNext(step) {
    if (!obAnswers[_obFieldForStep(step)]) {
        alert('Выбери вариант, чтобы продолжить');
        return;
    }
    document.getElementById(`ob-step-${step}`).style.display = 'none';
    obCurrentStep = step + 1;
    document.getElementById(`ob-step-${obCurrentStep}`).style.display = 'block';
    _obUpdateProgress();
}

function obFinish() {
    if (!obAnswers[_obFieldForStep(4)]) {
        alert('Выбери вариант, чтобы продолжить');
        return;
    }
    submitOnboarding();
}

function _obFieldForStep(step) {
    return ['cold_sensitivity','climate','activity','rain_sensitivity'][step - 1];
}

function _obUpdateProgress() {
    const segs = document.querySelectorAll('#ob-progress .progress-seg');
    segs.forEach((seg, i) => {
        seg.classList.toggle('done', i < obCurrentStep);
    });
    const label = document.getElementById('ob-step-label');
    if (label) label.textContent = `Вопрос ${obCurrentStep} из ${OB_STEPS}`;
}

function selectOption(btn, field, value) {
    // Снимаем выбор со всех кнопок в той же группе (в том же option-list)
    const list = btn.closest('.option-list');
    list.querySelectorAll('.option-btn').forEach(b => b.classList.remove('selected'));
    btn.classList.add('selected');
    obAnswers[field] = value;
}

// ── Чекин ─────────────────────────────────────────────────────────────────

let selectedCheckinIntensity = null;

function selectCheckin(btn, intensity) {
    const list = btn.closest('.option-list');
    list.querySelectorAll('.option-btn').forEach(b => b.classList.remove('selected'));
    btn.classList.add('selected');
    selectedCheckinIntensity = intensity;
}

// ── Онбординг submit ───────────────────────────────────────────────────────

async function submitOnboarding() {
    const data = {
        cold_sensitivity: obAnswers.cold_sensitivity || 'нормально',
        climate:          obAnswers.climate          || 'умеренный',
        activity:         obAnswers.activity         || 'обычная ходьба',
        rain_sensitivity: obAnswers.rain_sensitivity || 'не важно',
        gender: null
    };
    const res = await apiOnboarding(data);
    if (res.ok) {
        localStorage.setItem('onboarding_done', '1');
        showPage('page-advice');
    } else {
        alert('Ошибка: ' + await res.text());
    }
}

// ── Совет ──────────────────────────────────────────────────────────────────

async function getAdvice() {
    const city = document.getElementById('city').value.trim();
    if (!city) return alert('Введи город');

    document.getElementById('advice-empty').style.display = 'none';
    document.getElementById('advice-result').style.display = 'none';

    const res = await apiAdvice(city);
    if (!res.ok) {
        alert('Ошибка получения совета');
        return;
    }
    const data = await res.json();

    document.getElementById('advice-city-name').textContent = city;
    document.getElementById('advice-main-text').textContent = data.advice || '';
    document.getElementById('advice-profile-note').textContent = '';

    // Заполняем погодные карточки если есть данные
    document.getElementById('wc-wind').textContent = data.wind ? `${data.wind} м/с` : '—';
    document.getElementById('wc-rain').textContent = data.rain !== undefined ? `${data.rain}%` : '—';
    document.getElementById('wc-humidity').textContent = data.humidity ? `${data.humidity}%` : '—';
    document.getElementById('advice-temp').textContent = data.temp ? `${data.temp > 0 ? '+' : ''}${data.temp}°` : '';
    document.getElementById('advice-feels').textContent = data.feels_like ? `ощущается как ${data.feels_like > 0 ? '+' : ''}${data.feels_like}°` : '';

    document.getElementById('advice-result').style.display = 'block';

    // Подставляем город в чекин и ленту
    document.getElementById('checkin-city').value = city;
    document.getElementById('feed-city').value = city;
}

// ── Чекин submit ──────────────────────────────────────────────────────────

async function submitCheckin() {
    const city = document.getElementById('checkin-city').value.trim();
    if (!city) return alert('Введи город');
    if (selectedCheckinIntensity === null) return alert('Выбери ощущение');

    const comment = document.getElementById('checkin-comment').value.trim();
    const res = await apiCheckin(city, selectedCheckinIntensity, comment || null);
    if (res.ok) {
        // Сбрасываем форму
        document.querySelectorAll('#page-checkin .option-btn').forEach(b => b.classList.remove('selected'));
        document.getElementById('checkin-comment').value = '';
        selectedCheckinIntensity = null;
        showPage('page-advice');
        alert('Отзыв сохранён, спасибо!');
    } else {
        alert('Ошибка: ' + await res.text());
    }
}

// ── Лента ──────────────────────────────────────────────────────────────────

async function loadFeed() {
    const city = document.getElementById('feed-city').value.trim();
    if (!city) return alert('Введи город');

    const res = await apiFeed(city);
    const data = await res.json();
    const list = document.getElementById('feed-list');

    const labels = {
        '-2': ['Холоднее, чем кажется', 'badge-cold'],
        '-1': ['Прохладно',             'badge-cold'],
        '0':  ['В самый раз',           'badge-ok'],
        '1':  ['Теплее, чем кажется',   'badge-hot'],
        '2':  ['Очень жарко',           'badge-hot'],
    };

    if (!data.length) {
        list.innerHTML = '<div class="feed-empty">Отзывов за последние 3 часа нет</div>';
        return;
    }

    list.innerHTML = data.map(r => {
        const [label, cls] = labels[String(r.intensity)] || [r.intensity, 'badge-ok'];
        const ts = r.created_at ? _relativeTime(r.created_at) : '';
        return `<div class="feed-card">
            <div class="feed-card-top">
                <span class="feed-badge ${cls}">${label}</span>
                <span class="feed-ts">${ts}</span>
            </div>
            ${r.comment
                ? `<div class="feed-comment">${r.comment}</div>`
                : `<div class="feed-no-comment">Без комментария</div>`}
        </div>`;
    }).join('');
}

function _relativeTime(isoStr) {
    const diff = Math.floor((Date.now() - new Date(isoStr)) / 60000);
    if (diff < 1) return 'только что';
    if (diff < 60) return `${diff} мин назад`;
    const h = Math.floor(diff / 60);
    return `${h} ч назад`;
}

// ── Инициализация ──────────────────────────────────────────────────────────

function init() {
    const token = localStorage.getItem('jwt_token');
    const email = localStorage.getItem('user_email');

    if (token && email) {
        showPage(localStorage.getItem('onboarding_done') ? 'page-advice' : 'page-onboarding');
    } else {
        showPage('page-login');
    }
}

init();
