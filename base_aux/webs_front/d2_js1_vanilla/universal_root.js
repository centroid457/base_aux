// ----------------------------------------------------------------------------------------------------------------
(function bgColorOnLoad() {
    let body_bg_color__old = document.body.style.background;
    document.body.style.background = 'yellow';
    setTimeout(() => document.body.style.background = body_bg_color__old, 100);
})();

// ----------------------------------------------------------------------------------------------------------------
/** НЕ РАБОТАЕТ!!!
 * Добавляет нумерацию к заголовкам (h1-h6) внутри указанного контейнера.
 * @param {string|HTMLElement} container - CSS-селектор или DOM-элемент.
 * @param {Object} options - Настройки.
 * @param {boolean} [options.use_h1=false] - Нумеровать ли h1.
 * @param {string} [options.sep='.'] - Разделитель уровней.
 * @param {boolean} [options.keep_nesting=true] - Показывать полный путь (1.2.3) или только последний номер (3).
 */
function numberHeadings(container, options = {}) {
    const {
        show_h1 = false,
        sep = '.',
        keep_nesting = true
    } = options;

    const root = typeof container === 'string'
        ? document.querySelector(container)
        : container;
    if (!root) {
        console.error(`Контейнер "${container}" не найден`);
        return;
    }

    // Счётчики для уровней 1..6
    const counters = [0, 0, 0, 0, 0, 0];
    let lastLevel = 0;

    const headings = root.querySelectorAll('h1, h2, h3, h4, h5, h6');

    for (const heading of headings) {
        const level = parseInt(heading.tagName[1], 10);
        const idx = level - 1;

        // --- Обновление счётчиков ---
        if (level > lastLevel) {
            // Обнуляем промежуточные уровни
            for (let i = lastLevel; i < level; i++) {
                if (i !== idx) counters[i] = 0;
            }
            counters[idx]++;
        } else {
            counters[idx]++;
            // Обнуляем все более глубокие уровни
            for (let i = idx + 1; i < 6; i++) counters[i] = 0;
        }
        lastLevel = level;

        // --- Формирование номера ---
        let numberParts = [];
        if (keep_nesting) {
            for (let i = 0; i < level; i++) {
                numberParts.push(counters[i] === 0 ? '' : counters[i]);
            }
        } else {
            numberParts.push(counters[idx]);
        }

        let numberStr = numberParts.join(sep);
        numberStr = numberStr.replace(new RegExp(`^${sep}+|${sep}+$`, 'g'), '');

        const showThisNumber = (level === 1) ? show_h1 : true;
        let prefix = '';
        if (showThisNumber && numberStr !== '') {
            prefix = numberStr + sep + ' ';
        }

        // Удаляем старый номер (если есть) – ищем в начале строки цифры, разделители и пробел
        const oldNumberPattern = /^[\d\.]+\s+/;
        let newHTML = heading.innerHTML;
        if (oldNumberPattern.test(newHTML)) {
            newHTML = newHTML.replace(oldNumberPattern, '');
        }
        // Вставляем новый префикс
        heading.innerHTML = prefix + newHTML;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    numberHeadings('#ROOT_MAIN__ID', {
        show_h1: false,
        sep: '.',
        keep_nesting: true
    });
});

// ----------------------------------------------------------------------------------------------------------------
(function generateNavRoot() {
    const navContainer = document.getElementById('ROOT_NAV__ID');
    if (!navContainer) return;
    navContainer.innerHTML = '';

    // ========== КНОПКА "НАВЕРХ" (в начало навигации) ==========
    const topLink = document.createElement('a');
    topLink.href = '#';
    topLink.innerHTML = '⬆️';          // иконка вверх
    topLink.title = 'Наверх страницы';
    topLink.addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    navContainer.appendChild(topLink);

    // ========== ССЫЛКИ НА СЕКЦИИ ==========
    const sections = document.querySelectorAll('section.section__cls[id]');
    sections.forEach(section => {
        const sectionId = section.id;
        if (!sectionId) return;
        let titleText = '';
        const headerH2 = section.querySelector(':scope > h2');
        if (headerH2) titleText = headerH2.innerText.trim();
        if (!titleText) titleText = sectionId;

        const link = document.createElement('a');
        link.href = `#${sectionId}`;
        link.textContent = sectionId;
        link.title = titleText;

        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
        navContainer.appendChild(link);
    });

    // ========== КНОПКА "ВНИЗ" (в конец навигации) ==========
    const bottomLink = document.createElement('a');
    bottomLink.href = '#';
    bottomLink.innerHTML = '⬇️';        // иконка вниз
    bottomLink.title = 'Вниз страницы';
    bottomLink.addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    });
    navContainer.appendChild(bottomLink);
})();

// ----------------------------------------------------------------------------------------------------------------
// LINKS=SCROLL Smooth - ТОЛЬКО ДЛЯ СТАРЫХ БРАУЗЕРОВ!
(function linksSmoothScroll_forOldBrausers() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href && href !== '#') {
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        });
    });
})();

// --------------------------------------------------------------------------------
// Размножитель элемента со стилями (поддержка entries вида "prop:value")
// --------------------------------------------------------------------------------
const CLONE_ATTR_NAME = "data-clone_style_params";

/**
 * Заменяет элемент на список dl с клонами, демонстрирующими разные стили.
 * @param {HTMLElement} original__el - оригинальный элемент.
 * @param {string} defaultProperty - CSS-свойство по умолчанию (для простых значений).
 * @param {string[]} style_values - массив записей: простые значения или строки "свойство:значение".
 */
function _clone_element_with_styles__by_dl(original__el, defaultProperty, style_values) {
    // Если первого элемента нет, добавим маркер "оригинал без изменений"
    style_values.unshift(undefined);
    style_values.unshift("");

    // 1. Создаём контейнер dl с классом для горизонтального отображения
    const dl__el = document.createElement('dl');
    dl__el.className = 'dl_horizontal__cls';

    function addEntry(label_value, clonedElement) {
        let label_str = `${label_value}`;
        if (label_str.length == 0) {
            label_str = '\"\"';
        };

        const dt__el = document.createElement('dt');
        if (typeof label_value !== 'string') {
            dt__el.style.fontStyle = 'italic';
            dt__el.style.textDecoration = 'underline';
        };
        dt__el.textContent = label_str;
        dt__el.style.fontSize = 'xx-small';
        dl__el.appendChild(dt__el);

        const dd = document.createElement('dd');
        dd.appendChild(clonedElement);
        dl__el.appendChild(dd);
    }

    // 2. ITEMS
    for (let i = 0; i < style_values.length; i++) {
        const style_value = style_values[i];
        const clone__el = original__el.cloneNode(true);

        // Проверяем, является ли style_value самостоятельной парой "свойство:значение"
        if (typeof style_value === 'string' && /^[a-z-]+:/i.test(style_value)) {
            const colonPos = style_value.indexOf(':');
            const prop = style_value.substring(0, colonPos).trim();
            let value = style_value.substring(colonPos + 1).trim();
            clone__el.style[prop] = value;
            // console.log(1111, prop, value);
        } else {
            clone__el.style[defaultProperty] = style_value;
            // console.log(2, defaultProperty, style_value);
        }

        addEntry(style_value, clone__el);
    }

    // Оборачиваем в fieldset
    const fieldset__el = document.createElement('fieldset');
    const legend__el = document.createElement('legend');
    legend__el.innerHTML = `<small>${CLONE_ATTR_NAME}</small>[<b>${defaultProperty}</b>]`;
    fieldset__el.appendChild(legend__el);
    fieldset__el.appendChild(dl__el);

    // 4. Заменяем оригинал
    original__el.replaceWith(fieldset__el);
}

// парсинг параметризации - Поддерживаемые форматы:
// 1. "color:#c0392b;#2c3e50;#16a085"               --->; as separator
// 2. "color-other:[#c0392b; #2c3e50; #16a085]"     --->[] brackets available
// 3. "background:[rgba(0,0,0,0.1);linear-gradient(135deg, #667eea, #764ba2)]"  ---> sophisticated values available!
function parse_style_parametrisation(source) {
    // Ищем первую двоеточие
    const colonIndex = source.indexOf(':');
    if (colonIndex === -1) {
        console.error('Неверный формат: отсутствует двоеточие', source);
        return null;
    }
    const property = source.substring(0, colonIndex).trim();
    let valuesStr = source.substring(colonIndex + 1).trim();

    // Удаляем квадратные скобки, если они есть
    if (valuesStr.startsWith('[') && valuesStr.endsWith(']')) {
        valuesStr = valuesStr.slice(1, -1);
    }
    // Разбиваем варианты и чистим пробелы
    let values = valuesStr.split(';').map(v => v.trim()).filter(v => v);
    if (values.length === 0) {
        console.error('Не найдено значений', source);
        return null;
    }
    return { property, values };
}

// Автоматическое клонирование
// Поддерживаемые форматы:
// 1. data-clone_style_params="color:#c0392b;#2c3e50;#16a085"
// 2. data-clone_style_params="color-other:[#c0392b; #2c3e50; #16a085]"
(function clone_elements__parametrisation() {
    const elements = document.querySelectorAll(`[${CLONE_ATTR_NAME}]`);
    elements.forEach(el => {
        const paramLine = el.getAttribute(CLONE_ATTR_NAME);
        const parsed = parse_style_parametrisation(paramLine);
        if (!parsed) return;
        const { property, values } = parsed;
        _clone_element_with_styles__by_dl(el, property, values);
    });
})();

// ----------------------------------------------------------------------------------------------------------------
// ========== УПРАВЛЕНИЕ СЕКЦИЯМИ (data-collapsed) ==========
(function() {
    const sections = document.querySelectorAll('section.section__cls');
    if (!sections.length) return;

    // Функция: скрыть все секции (добавить атрибут data-collapsed)
    function collapseAll() {
        sections.forEach(section => {
            section.setAttribute('data-collapsed', '');
        });
    }

    // Функция: раскрыть все секции (удалить атрибут data-collapsed)
    function expandAll() {
        sections.forEach(section => {
            section.removeAttribute('data-collapsed');
        });
    }

    // Обработчики кликов по заголовкам секций
    sections.forEach(section => {
        const header = section.querySelector(':scope > h2');
        if (!header) return;

        header.addEventListener('click', (e) => {
            // Если клик на ссылку внутри заголовка — не сворачиваем (чтобы не мешать якорям)
            if (e.target.closest('a')) return;

            if (section.hasAttribute('data-collapsed')) {
                section.removeAttribute('data-collapsed');
            } else {
                section.setAttribute('data-collapsed', '');
            }
        });
    });

    // Кнопки управления (находим по ID)
    const collapseBtn = document.getElementById('collapseAllBtn');
    const expandBtn = document.getElementById('expandAllBtn');

    if (collapseBtn) {
        collapseBtn.addEventListener('click', collapseAll);
    }
    if (expandBtn) {
        expandBtn.addEventListener('click', expandAll);
    }

    // Обработка якорей: если перешли по ссылке #sectionId, раскрываем секцию
    function handleHash() {
        const hash = window.location.hash.substring(1);
        if (hash) {
            const targetSection = document.getElementById(hash);
            if (targetSection && targetSection.classList.contains('section__cls')) {
                targetSection.removeAttribute('data-collapsed');
            }
        }
    }
    window.addEventListener('hashchange', handleHash);
    handleHash();
})();
// ----------------------------------------------------------------------------------------------------------------
