// ---------------------------------------------------------------------------------------------------------------------
(function bgColorOnLoad() {
    let body_bg_color__old = document.body.style.background;
    document.body.style.background = 'yellow';
    setTimeout(() => document.body.style.background = body_bg_color__old, 100);
})();

// ---------------------------------------------------------------------------------------------------------------------
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

// ---------------------------------------------------------------------------------------------------------------------
(function generateNavRoot() {
    const navContainer = document.getElementById('ROOT_NAV__ID');
    if (!navContainer) return;
    //navContainer.innerHTML = '';

    // ========== КНОПКА "НАВЕРХ" (в начало навигации) ==========
    const topLink = document.createElement('a');
    topLink.href = '#';
    topLink.innerHTML = '⬆️';
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

// ---------------------------------------------------------------------------------------------------------------------
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

// =====================================================================================================================
// CLONES
// ---------------------------------------------------------------------------------------------------------------------
function isIconChar(ch) {
    const code = ch.codePointAt(0);
    return (
        // Специальные символы пунктуации (…, •, — и т.д.)
        (code === 0x2026) || // …
        (code === 0x2022) || // •
        (code === 0x2014) || // —
        (code === 0x2013) || // –

        (code >= 0x2190 && code <= 0x21FF) || // стрелки (←↑→↓↔↕↖↗↘↙)
        (code >= 0x2300 && code <= 0x23FF) || // технические
        (code >= 0x24EA && code <= 0x24FF) || // Числовые символы в кружках
        (code >= 0x25A0 && code <= 0x25FF) || // геометрические фигуры
        (code >= 0x2600 && code <= 0x26FF) || // разное (погода, звёзды)
        (code >= 0x2700 && code <= 0x27BF) || // Дингбаты (галочки, крестики, лампочки)
        (code >= 0x2B00 && code <= 0x2BFF) || // стрелки дополнительные
        (code >= 0x1F300 && code <= 0x1F9FF) || // эмодзи основные
        (code >= 0x1F900 && code <= 0x1FADF) || // эмодзи дополнительные

        // Отдельные иконки
        code === 0x24D8 || code === 0x2139 || code === 0x00A9 || code === 0x00AE || code === 0x2122
    );
}

(function _icons_show_code() {
    function processTextNode(node) {
        const text = node.nodeValue;
        if (!text) return;
        const chars = Array.from(text);
        let resultNodes = [];
        let currentPlain = '';
        for (const ch of chars) {
            if (isIconChar(ch)) {
                if (currentPlain) {
                    resultNodes.push(document.createTextNode(currentPlain));
                    currentPlain = '';
                }
                const codePoint = ch.codePointAt(0);
                const hex = codePoint.toString(16).toUpperCase();

                const span = document.createElement('span');
                span.setAttribute("data-border", "")
                span.setAttribute("data-radius05rem", "")
                span.innerHTML = `${ch} <code>&amp;#x${hex};</code>`;
                resultNodes.push(span);
            } else {
                currentPlain += ch;
            }
        }
        if (currentPlain) resultNodes.push(document.createTextNode(currentPlain));
        if (resultNodes.length) {
            const parent = node.parentNode;
            const next = node.nextSibling;
            for (const newNode of resultNodes) parent.insertBefore(newNode, next);
            parent.removeChild(node);
        }
    }

    function processElements(element) {
        const walker = document.createTreeWalker(
            element,
            NodeFilter.SHOW_TEXT,
            {
                acceptNode: (node) => {
                    if (node.parentNode && node.parentNode.classList && node.parentNode.classList.contains('icon-unicode-item')) {
                        return NodeFilter.FILTER_REJECT;
                    }
                    return NodeFilter.FILTER_ACCEPT;
                }
            }
        );
        const textNodes = [];
        let node;
        while (node = walker.nextNode()) textNodes.push(node);
        textNodes.forEach(processTextNode);
    }

    const elements = document.querySelectorAll('[data-icons__show_unicode_values]');
    elements.forEach(element => {
        processElements(element);
    });
})();

// ---------------------------------------------------------------------------------------------------------------------
const ATTR_NAME__CLONE_CSS_DL = "data-clone_element__with_css__by_dl";

/**
 * Заменяет элемент на список dl с клонами, демонстрирующими разные стили.
 * @param {HTMLElement} original__el - оригинальный элемент.
 * @param {string} def_property_name - CSS-свойство по умолчанию (для простых значений).
 * @param {string[]} value_items - массив записей: простые значения или строки "свойство:значение".
 */
function _clone_element__with_css__by_dl(original__el, def_property_name, value_items) {
    value_items.unshift(undefined);
    value_items.unshift("WRONG_VAL");
    if (!value_items.includes("none")) {value_items.unshift("none");}
    value_items.unshift("revert");
    value_items.unshift("");

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
        dd.setAttribute("data-border", "")
        //dd.setAttribute("data-bg_grey_eee", "")
        dd.appendChild(clonedElement);
        dl__el.appendChild(dd);
    }

    // 2. ITEMS
    for (const style_value of value_items) {
        const clone__el = original__el.cloneNode(true);

        // если style_value - MAP!
        if (typeof style_value === 'string') {
            clone__el.style[def_property_name] = style_value;
            // console.log(2, def_property_name, style_value);
        } else if (style_value instanceof Map) {
            // несколько свойств из Map
            for (const [name, val] of style_value) {
                clone__el.style[name] = val;
            }
        }

        addEntry(style_value, clone__el);
    }

    // Оборачиваем в fieldset
    const fieldset__el = document.createElement('fieldset');
    const legend__el = document.createElement('legend');
    legend__el.innerHTML = `<small>${ATTR_NAME__CLONE_CSS_DL}</small>[<b data-mouse_select_all>${def_property_name}</b>]`;
    fieldset__el.appendChild(legend__el);
    fieldset__el.appendChild(dl__el);

    // 4. Заменяем оригинал
    original__el.replaceWith(fieldset__el);
}

// parse string like in STiLE tag into Map
// n1:v1;n2:v2;; => Map([n1,v1], [n2,v2])
function _parse__css_style(source) {
    const result = new Map();

    // Разбиваем по ';', удаляем лишние пробелы по краям, отбрасываем пустые элементы
    const pairs = source.split(';').map(v => v.trim()).filter(v => v);

    for (const pair of pairs) {
        // Ищем ПЕРВОЕ двоеточие (ключ:значение)
        // теоретически может быть двоеточие (например, content:"::before"), поэтому важно брать первое вхождение.
        const colonIndex = pair.indexOf(':');
        if (colonIndex !== -1) {
            const key = pair.slice(0, colonIndex).trim();
            const value = pair.slice(colonIndex + 1).trim();
            // Добавляем только если ключ не пуст
            if (key) result.set(key, value);
        }
    };
    return result;
}

// парсинг строки параметризации
// 1. "color:[#c0392b  ; #2c3e50; #16a085 ]"  --->; as separator and [] brackets always! and Space available
// 2. "background:[rgba(0,0,0,0.1);linear-gradient(135deg, #667eea, #764ba2)]" ---> sophisticated values available!
// 3. nameDef:[v1; {n21:v21;n22:v22}; v3;]
function _parse__parametrisation(source) {
    const result = [];
    source = source.trim();

    // 1=parse default_param_name
    const colonIndex = source.indexOf(':');
    if (colonIndex === -1) {
        console.error('Неверный формат: отсутствует двоеточие - ', source);
        return null;
    }

    const default_param_name = source.slice(0, colonIndex).trim();

    // 2=get all values_str
    let values_str = source.slice(colonIndex + 1).trim();
    if (values_str.startsWith('[') && values_str.endsWith(']')) {
        values_str = values_str.slice(1, -1);
        values_str = values_str.trim();
    } else {
        console.error('Неверный формат: скобки отсутствуют [] - ', source);
        return null;
    }

    // 3=parse variants
    let data_rest = values_str;
    while (data_rest.length != 0) {
        let step_result;
        let _data_first;

        if (data_rest.startsWith('{')) {
            const _index = data_rest.indexOf('}');
            if (_index !== -1) {
                _data_first = data_rest.slice(0+1, _index).trim();
                data_rest = data_rest.slice(_index + 1).trim();

                if (_data_first) {
                    step_result = _parse__css_style(_data_first)
                }

            } else {
                console.error('Неверный формат: скобки - нет завершающей } - ', data_rest);
                return null;
            }
        } else {
            const _index = data_rest.indexOf(';');
            if (_index !== -1) {
                _data_first = data_rest.slice(0, _index).trim();
                data_rest = data_rest.slice(_index + 1).trim();
            } else {
                _data_first = data_rest;
                data_rest = "";
            }

            if (_data_first) {
                step_result = _data_first;
            }
        }

        result.push(step_result)
    }

    return [ default_param_name, result ];
}

// клонирование - применение
(function clone_element__with_css__by_dl() {
    const elements = document.querySelectorAll(`[${ATTR_NAME__CLONE_CSS_DL}]`);
    elements.forEach(el => {
        const params_source = el.getAttribute(ATTR_NAME__CLONE_CSS_DL);
        const [ def_property_name, params_parsed ] = _parse__parametrisation(params_source);
        if (!params_parsed) return;
        _clone_element__with_css__by_dl(el, def_property_name, params_parsed);
    });
})();

// =====================================================================================================================
// ---------------------------------------------------------------------------------------------------------------------
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
        const hash = window.location.hash.slice(1);
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

// =====================================================================================================================
