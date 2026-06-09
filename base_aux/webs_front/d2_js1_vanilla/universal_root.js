// =====================================================================================================================
// Проверка, загружен ли DOM
//if (document.readyState === 'loading') {
//    console.error('[universal_root] DOM не загружен! Добавьте атрибут defer к тегу <script> или дождитесь события DOMContentLoaded.');
//    // Можно также выбросить исключение
//    throw new Error('Для работы universal_root.js необходимо использовать defer или располагать скрипт перед закрывающим </body>');
//}
/* OTHERWISE WE NEED TO DO SMTH LIKE
(function bgColorOnLoad() {
    function process() {
        //
    }

    // ----------------------------------------------------
    document.addEventListener('DOMContentLoaded', process);
})();
*/


// =====================================================================================================================
const OnLoadRunner = {
    callbacks_queue: [],

    add(fn) {
        if (typeof fn === 'function') {
            this.callbacks_queue.push(fn);
        }
    },

    run_all() {
        this.callbacks_queue.forEach(fn => fn());
    },

    run() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.run_all());
        } else {
            this.run_all();
        }
    }
};


// =====================================================================================================================
function log__ready_state() {
    let msg = "";
    if (document.readyState === 'loading') {
        msg += "PAGE🟡"
    } else {
        msg += "PAGE🟢"
    }

    msg += `document.readyState=${document.readyState}`;
    console.log(msg);
}
log__ready_state();
OnLoadRunner.add(log__ready_state);


// =====================================================================================================================
// UNCACHE -------------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------------
function uncache_loading__all_files_without_cache() {
    // USAGE!
    // ! ПЕРЕЗАПУСКА СЕРВЕРА НЕ ТРЕБУЕТСЯ!!! - сохрани и обнови страницу!!!
    // 1. ПОМЕСТИNM ПРЯМЫМ КОДОМ после подгружаемых скриптов, желательно в HEAD!!!
    //      <script>uncache_loading__all_files_without_cache();</script>
    //      Я ПОМЕСТИЛ В САМУЮ ПЕРВУЮ СТРОКУ HEAD, даже перед всеми загрузками - все работает!!!
    // 2. закинуть в universal_root.js не получится!

    // Генерируем уникальную версию (например, timestamp)
    const version = Date.now();

    // Функция добавления параметра к URL
    function addVersionToUrl(url) {
        if (!url || url.startsWith('data:') || url.startsWith('blob:') || url.startsWith('javascript:')) return url;
        const separator = url.includes('?') ? '&' : '?';
        return url + separator + 'v=' + version;
    }

    // 1. Обрабатываем все link[rel="stylesheet"]
    document.querySelectorAll('link[rel="stylesheet"]').forEach(link => {
        const original = link.getAttribute('href');
        if (original) {
            link.setAttribute('href', addVersionToUrl(original));
        }
    });

    // 2. Обрабатываем все script[src]
    document.querySelectorAll('script[src]').forEach(script => {
        const original = script.getAttribute('src');
        if (original) {
            script.setAttribute('src', addVersionToUrl(original));
        }
    });

    // 3. (Опционально) Обрабатываем изображения
    document.querySelectorAll('img').forEach(img => {
        const original = img.getAttribute('src');
        if (original) {
            img.setAttribute('src', addVersionToUrl(original));
        }
    });

    // 4. (Опционально) Обрабатываем iframe
    document.querySelectorAll('iframe').forEach(iframe => {
        const original = iframe.getAttribute('src');
        if (original) {
            iframe.setAttribute('src', addVersionToUrl(original));
        }
    });

    // 5. (Опционально) Для объектов с фоном в CSS – это сложнее, не требуется в вашем случае.
}


// ---------------------------------------------------------------------------------------------------------------------
// Добавляет кнопку жёсткой перезагрузки (сброс кеша) замещая элемент с атрибутом data-auto__replace_with__btn_hard_reset
function onload__replace_with__btn_hard_reset() {
    const target = document.querySelector('[data-auto__replace_with__btn_hard_reset]');
    if (!target) return;

    // Создаём кнопку
    const btn = document.createElement('button');
    btn.textContent = 'hardReset(unCache)';
    btn.title = 'Перезагрузить страницу и принудительно обновить все ресурсы (CSS, JS)';

    // Добавляем атрибуты для стилизации (если используются ваши классы)
    btn.setAttribute('data-btn_outline', 'yellow');

    // Обработчик клика
    btn.addEventListener('click', () => {
        // Добавляем случайный параметр к URL, чтобы браузер не использовал кеш
        const url = new URL(window.location.href);
        url.searchParams.set('_t', Date.now());
        window.location.href = url.toString();
    });

    target.replaceWith(btn);
}

OnLoadRunner.add(onload__replace_with__btn_hard_reset);


// =====================================================================================================================
function onload__bg_color() {
    let body_bg_color__old = document.body.style.background;
    document.body.style.background = 'yellow';
    setTimeout(() => document.body.style.background = body_bg_color__old, 100);
}
OnLoadRunner.add(onload__bg_color);


// =====================================================================================================================
function page_reload_force(msg) {
    console.warn("[page_reload_force]🟡", msg);
    location.reload();
//    history.go(0);
}


function onload__ws_ping() {
    // Настройки
    const ATTR_NAME__PING_MONITOR = 'data-auto__ping_lost';
    const VALUE__PING_LOST = '1';
    const VALUE__PING_OK = '';
    const TIMEOUT_RECONNECT = 3000;

    // Функция обновления всех целевых элементов
    function updateElements(isConnected) {
        const value_new = isConnected ? VALUE__PING_OK : VALUE__PING_LOST;
        document.querySelectorAll(`[${ATTR_NAME__PING_MONITOR}]`).forEach(el => {
            el.setAttribute(ATTR_NAME__PING_MONITOR, value_new);
        });
    }

    // Переменные для WebSocket и переподключения
    let ping__enabled = null;

    let ws_ping = null;
    let timer__ping_reconnect = null;   // object used reconnection

    let currentServerId = null;

    function ws_ping__init() {
        // Уже открыт или пытается открыться? → выходим
        if (ws_ping && (ws_ping.readyState === WebSocket.OPEN || ws_ping.readyState === WebSocket.CONNECTING)) {
            return;
        }

        // Очищаем старый таймер (если есть) — чтобы не было двойного переподключения
        if (timer__ping_reconnect) {
            clearTimeout(timer__ping_reconnect);
            timer__ping_reconnect = null;
        }

        // если не было инициализации успешной
        if (ping__enabled === false) {
            return;
        }

        const ws_protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host;
        const ws_url = `${ws_protocol}//${host}/ws/ping`;

        // ОБЯЗАТЕЛЬНО СОЗДАЕМ КАЖДЫЙ РАЗ НОВЫЙ сокет!!!
        // После закрытия WebSocket его нельзя «переоткрыть» — только создать новый. Это особенность протокола.
        ws_ping = new WebSocket(ws_url);

        ws_ping.onopen = () => {
            if (ping__enabled === null) {
                ping__enabled = true;
                console.log("[ws_ping.ping__enabled]🟢MONITORING is ON");
            }

            if (timer__ping_reconnect) clearTimeout(timer__ping_reconnect);
            updateElements(true);   // связь есть > атрибут = "0"
            console.log("[ws_ping.onopen]🟢connected");
        };

        ws_ping.onclose = () => {
            updateElements(false);  // связь потеряна > атрибут = "1"
            if (ping__enabled) console.warn(`[ws_ping.onclose]🔴closed (code:${event.code})`);
            // Запускаем переподключение, только если оно не было инициировано вручную (например, при выгрузке страницы)
            if (timer__ping_reconnect === null) {
                timer__ping_reconnect = setTimeout(ws_ping__init, TIMEOUT_RECONNECT);
            }
        };

        ws_ping.onerror = () => {
            if (ping__enabled === null) {
                ping__enabled = false;
                console.log("[ws_ping.ping__enabled]🟡MONITORING is OFF");
            } else {
                console.warn(`[ws_ping.onerror]🟡error (code:${event.code})`);
            }

            ws_ping.close();   // инициируем закрытие, вызовется onclose
        };

        ws_ping.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                if (data.event === 'server_id') {
                    const newServerId = data.id;
                    console.log(`[ws_ping.onmessage.server_id](currentServerId=${currentServerId}/newServerId=${newServerId})`);
                    if (currentServerId === null) {
                        // Первое подключение, сохраняем ID
                        currentServerId = newServerId;
                        console.log(`[ws_ping.onmessage.server_id]NEW=${currentServerId}`);
                    } else if (currentServerId !== newServerId) {
                        // ID не совпадает, значит сервер был перезапущен и возможны изменения
                        console.warn(`[ws_ping.onmessage.server_id]🟡changed=(currentServerId=${currentServerId}/newServerId=${newServerId})`);
                        page_reload_force("ServerId changed");
                    }
                }
            } catch (error) {
                console.warn('[ws_ping.onmessage]🟡Ошибка при обработке сообщения:', error);
                page_reload_force("ServerId check error");
            }
        };
    }

    // Чистое завершение (например, при beforeunload)
    window.addEventListener('beforeunload', () => {
        if (timer__ping_reconnect) {
            clearTimeout(timer__ping_reconnect);
            timer__ping_reconnect = null;
        }
        if (ws_ping && ws_ping.readyState === WebSocket.OPEN) {
            ws_ping.close();
        }
    });

    // Запуск при загрузке
    ws_ping__init();

    // Опционально: если элементы добавляются динамически после загрузки,
    // можно перевызвать updateElements при изменении DOM.
    // Но для простоты оставим так. Если нужно – раскомментируйте:
    /*
    new MutationObserver(() => {
        if (ws_ping && ws_ping.readyState === WebSocket.OPEN) updateElements(true);
        else updateElements(false);
    }).observe(document.body, { childList: true, subtree: true });
    */
}
OnLoadRunner.add(onload__ws_ping);


// =====================================================================================================================
// COUNTERS ------------------------------------------------------------------------------------------------------------
// ---------------------------------------------------------------------------------------------------------------------
/**
 * Добавляет порядковые номера во все элементы, соответствующие селектору.
 * @param {string} selector - CSS-селектор элементов для нумерации.
 * @param {Object} options - настройки (необязательно)
 * @param {number} options.startIndex - номер первого элемента (по умолчанию 1)
 * @param {string} options.attrName - для стилизации
 */
function onload__count_elements(selector, options = {}) {
    const {
        startIndex = 1,
        attrName = 'data-counter_index',
        attr_skip = 'data-skip',
    } = options;

    const elements = document.querySelectorAll(selector);
    if (!elements.length) return;

    // Удаляем старые счетчики, если нужно
    elements.forEach(el => {
        const oldSpan = el.querySelector(`span[${attrName}]`);
        if (oldSpan) oldSpan.remove();
    });

    let counter_index = startIndex;

    // Проставляем новые номера
    elements.forEach(el => {
        if (el.hasAttribute(attr_skip)) return;
        const span = document.createElement('span');
        span.setAttribute(attrName, "");
        span.textContent = counter_index;
        el.prepend(span);
        counter_index += 1;
    });
}

OnLoadRunner.add(
    function() {
        onload__count_elements('.section__cls h2' );
    }
);


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
OnLoadRunner.add(
    function() {
        numberHeadings('body > main', {
            show_h1: false,
            sep: '.',
            keep_nesting: true
        });
});

// ---------------------------------------------------------------------------------------------------------------------
function onload__generateNavRoot() {
    const navContainer = document.querySelector('body > nav');
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
}
OnLoadRunner.add(onload__generateNavRoot);


// ---------------------------------------------------------------------------------------------------------------------
// LINKS=SCROLL Smooth - ТОЛЬКО ДЛЯ СТАРЫХ БРАУЗЕРОВ!
function onload__linksSmoothScroll_forOldBrausers() {
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
}
OnLoadRunner.add(onload__linksSmoothScroll_forOldBrausers);


// =====================================================================================================================
// ERROR
// ---------------------------------------------------------------------------------------------------------------------
/**
 * Пользовательская ошибка для скриптов разметки (клонеры, парсеры и т.п.)
 * @param {Object} options - параметры ошибки
 * @param {string} options.node - имя функции, где произошла ошибка
 * @param {*} options.source - исходные данные (строка, DOM-элемент, что угодно)
 * @param {string} options.message - сообщение об ошибке
 * @param {*} [options.params] - дополнительные параметры (объект, примитив)
 * @param {...*} [options.rest] - любые другие пользовательские атрибуты
 */
class ErrorUser extends Error {
  constructor({ node, source, message, params, ...rest }) {
    super(message);
    //this.name = 'ErrorUser';
    this.node = node;
    this.source = source;
    this.params = params;

    // Все дополнительные поля (например, line, column, rawAttr и т.д.)
    Object.assign(this, rest);

    // Сохраняем стек вызовов без лишних фреймов этого конструктора
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, ErrorUser);
    }
  }

  // Сериализация в плоский объект (для JSON, копирования в буфер обмена)
  // @returns {Object}
  toJSON() {
    // Безопасно сериализуем source (строку, число, объект – что угодно)
    let safeSource = this.source;
    if (typeof this.source === 'object' && this.source !== null) {
      try {
        // пытаемся превратить в строку, но не проваливаемся
        safeSource = JSON.stringify(this.source);
      } catch {
        safeSource = String(this.source);
      }
    }

    return {
      name: this.name,
      node: this.node,
      source: safeSource,
      message: this.message,
      params: this.params,
      // дополнительные поля (исключаем стандартные, чтобы не дублировать)
      ...Object.fromEntries(
        Object.entries(this).filter(([key]) =>
          !['name', 'node', 'source', 'message', 'params', 'stack'].includes(key)
        )
      ),
      stack: this.stack,
    };
  }

  //Краткое строковое представление для консоли
  toString() {
    return `[${this.name}/${this.node}]: ${this.message}`;
  }
}

/* Пример использования
try {
  throw new ErrorUser({
    node: '_parse_css_style',
    source: 'color:red;; background:blue',   // строка с ошибкой (двойной ;; )
    message: 'Некорректный формат CSS-объявления',
    params: { separator: ';', expectedPairs: true },
    customField: 'доп. данные',    // произвольное поле – попадёт в rest
  });
} catch (err) {
  console.error(err.toString());                  // ErrorUser: Некорректный формат CSS-объявления [_parse_css_style]
  console.log(JSON.stringify(err.toJSON(), null, 2));
  // Теперь можно скопировать этот JSON для анализа
  // Или скопировать err.message и err.stack
}
*/

// =====================================================================================================================
// STRING
// ---------------------------------------------------------------------------------------------------------------------
function toString_Map(source) {
    if (!(source instanceof Map)) {
        return String(source);  // FIXME: return null???
    }

    const entries = [];
    for (const [k, v] of source) {
        entries.push(`${k}:${v}`);
    }
    return `Map(${entries.join('; ')})`;
}


// ---------------------------------------------------------------------------------------------------------------------
/**
 * Возвращает строковое описание DOM-элемента: тег, ключевые атрибуты, инлайн-стили.
 * @param {Element} source - целевой элемент
 * @returns {string} описание в формате "Element(tagname:...; attrs:{...}; style:{...})"
 */
function toString_Element(source) {     // TODO: ref!!! its just the beginning!
    if (!(source instanceof Element)) {
        return String(source);  // FIXME: return null???
    }

    const tag = source.tagName.toLowerCase();

    // Список атрибутов, которые считаем «важными» для отображения
    const importantAttrs = [
        'id', 'class', 'type', 'href', 'src', 'name', 'value',
        'disabled', 'checked', 'readonly', 'target', 'rel',
        'alt', 'title', 'role', 'aria-label', 'data-group'
    ];

    const attrs = {};
    for (const attr of importantAttrs) {
        const val = source.getAttribute(attr);
        if (val !== null && val !== '') {
            attrs[attr] = val;
        }
    }

    // Инлайн-стили (то, что в атрибуте style)
    const inlineStyle = source.style.cssText.trim();

    // Формируем строку
    let result = `Element(tagname:${tag}`;

    if (Object.keys(attrs).length) {
        const attrsStr = Object.entries(attrs)
            .map(([k, v]) => `${k}:${v}`)
            .join('; ');
        result += `; attrs:{${attrsStr}}`;
    }

    if (inlineStyle) {
        result += `; style:{${inlineStyle}}`;
    }

    result += ')';
    return result;
}
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


// ---------------------------------------------------------------------------------------------------------------------
function get_num__direct_or_by_id(source, defaultValue = null) {
    if (typeof source === 'number') return source;
    if (typeof source === 'string') {
        let trimmed = source.trim();
        // Нормализуем десятичный разделитель (заменяем первую запятую на точку)
        let normalized = trimmed.replace(',', '.');
        // Проверяем, что после нормализации строка является валидным числом (целым или десятичным)
        // Допустимы: цифры, одна точка, знак минус в начале
        const validNumberPattern = /^-?\d+(\.\d+)?$/;
        if (validNumberPattern.test(normalized)) {
            let num = parseFloat(normalized);
            if (!isNaN(num)) return num;
        }
        // Если не число, пробуем найти элемент с таким ID
        const el = document.getElementById(source);
        if (el) {
            let rawValue = (el.value !== undefined) ? el.value : (el.textContent || el.innerText);
            if (rawValue != null) {
                let rawNorm = String(rawValue).trim();
                if (validNumberPattern.test(rawNorm)) {
                    let num = parseFloat(rawNorm);
                    if (!isNaN(num)) return num;
                }
            }
        }
    }
    console.warn(`[get_value__direct_or_by_id] Не удалось получить число из "${source}", используем значение по умолчанию: ${defaultValue}`);
    return defaultValue;
}

// =====================================================================================================================
// CLONES
// ---------------------------------------------------------------------------------------------------------------------
function onload__icons_show_code() {
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
}
OnLoadRunner.add(onload__icons_show_code);


// =====================================================================================================================
const ATTR_NAME__CLONE_EL__PARAMS = "data-clone_element__params";
const ATTR_NAME__CLONE_EL__W_ATTRS = "data-clone_element__w_attrs"; // css(def)/attrs
const ATTR_NAME__CLONE_EL__BY_DIRECT = "data-clone_element__by_direct"; //dl(def)/direct
const ATTR_NAME__DELETE_ON_PROCESS = "data-attr__delete_on_process";

// ---------------------------------------------------------------------------------------------------------------------
/**
 * Заменяет элемент на список dl с клонами, демонстрирующими разные стили.
 * @param {HTMLElement} original__el - оригинальный элемент.
 * @param {string} def_property_name - CSS-свойство по умолчанию (для простых значений).
 * @param {string[]} variants - массив записей: простые значения или строки "свойство:значение".
 */
function _clone_element(original__el, def_property_name, variants, with_attrs=false, by_direct=false) {
    // 0=append irrational values
    variants.unshift(undefined);
    variants.unshift(new Map());
    //variants.unshift("WRONG_VAL"); //NOT NEEDED!!!
    if (!variants.includes("none")) {variants.unshift("none");}
    variants.unshift("revert");
    variants.unshift("");

    // 1=make all clones ---------------------------------------
    const clones_map = new Map();

    for (const variant of variants) {
        const clone__el = original__el.cloneNode(true);

        let params_map;

        // define final item_map
        if (variant instanceof Map) {
            params_map = variant;
        } else if (typeof variant === 'string' || variant === undefined) {
            // Специальный случай: пустое имя свойства → режим атрибутов
            if (def_property_name === '') {
                // Строка – это имя булевого атрибута (значение пусто)
                params_map = new Map().set(variant, '');
            } else {
                // Обычный CSS‑стиль
                params_map = new Map().set(def_property_name, variant);
            }
        } else {
            // fallback (не должно случаться)
            params_map = new Map();
        }

        // apply params
        for (const [name, val] of params_map) {
            if (def_property_name === '' || with_attrs) {
                // Для булевых атрибутов или если явно запрошены атрибуты
                clone__el.setAttribute(name, val);
            } else {
                clone__el.style[name] = val;
            }
        }

        if (clone__el.hasAttribute(ATTR_NAME__DELETE_ON_PROCESS)) clone__el.removeAttribute(ATTR_NAME__DELETE_ON_PROCESS);

        clones_map.set(variant, clone__el);
    }

    // 2=APPLY-1=DIRECT ------------------------------------------
    if (by_direct) {
        const clonesArray = Array.from(clones_map.values());
        original__el.replaceWith(...clonesArray);
        return;
    }

    // 2=APPLY-2=DL -----------------------------------------------
    const fieldset__el = document.createElement('fieldset');
    const legend__el = document.createElement('legend');
    // Если имя свойства пусто, показываем [attributes]
    const displayName = def_property_name === '' ? 'attributes' : def_property_name;
    legend__el.innerHTML = `<small>${ATTR_NAME__CLONE_EL__PARAMS}</small>[<b data-mouse_select__all>${displayName}</b>]`;
    fieldset__el.appendChild(legend__el);

    const dl__el = document.createElement('dl');
    dl__el.className = 'dl_horizontal__cls';
    fieldset__el.appendChild(dl__el);

    function addEntryDl(label_value, cloned_el) {
        // 1=resolve label_str
        let label_str;

        if (label_value instanceof Map) {
            label_str = toString_Map(label_value);
        } else {
            label_str = String(label_value);
        }

        if (label_str.length === 0) label_str = '""';

        //2=WORK
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
        //dd.setAttribute("data-bg_a5", "")
        dd.appendChild(cloned_el);
        dl__el.appendChild(dd);
    }

    for (const [_value, _cloned_el] of clones_map) {
        addEntryDl(_value, _cloned_el);
    }

    // 4. Заменяем оригинал
    original__el.replaceWith(fieldset__el);
}

// ---------------------------------------------------------------------------------------------------------------------
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
        let key;
        let value;
        if (colonIndex !== -1) {
            key = pair.slice(0, colonIndex).trim();
            value = pair.slice(colonIndex + 1).trim();
        } else {
            // Нет двоеточия – значит это булевый атрибут (значение – пустая строка)
            key = pair;
            value = '';
        }

        // Добавляем только если ключ не пуст
        if (key) {
            result.set(key, value);
        } else {
            console.error(`_parse__css_style: нет ключа[pair=${pair}/source=${source}]`);
        }

    };
    return result;
}

// ---------------------------------------------------------------------------------------------------------------------
// парсинг строки параметризации
// 1. "color:[#c0392b  ; #2c3e50; #16a085 ]"  --->; as separator and [] brackets always! and Space available
// 2. "background:[rgba(0,0,0,0.1);linear-gradient(135deg, #667eea, #764ba2)]" ---> sophisticated values available!
// 3. RETURN =
//      GOOD = Array[ defName, Array[variants] ] ---> [ nameDef, [v1; {n21:v21;n22:v22}; v3;] ]
//      BAD1 = level 1 - full error             ---> Error{}
//      BAD2 = level 2 - inner element error ---> [ nameDef, [Error{}; {n21:v21;n22:v22}; v3;] ]
function _parse__parametrisation(source) {
    const result = [];
    source = source.trim();

    // 1=parse default_param_name
    const colonIndex = source.indexOf(':');
    if (colonIndex === -1) {
        console.error(`_parse__parametrisation: отсутствует двоеточие [source=${source}]`);
        return null;
    }

    const default_param_name = source.slice(0, colonIndex).trim();

    // 2=get all values_str
    let values_str = source.slice(colonIndex + 1).trim();
    if (values_str.startsWith('[') && values_str.endsWith(']')) {
        values_str = values_str.slice(1, -1);
        values_str = values_str.trim();
    } else {
        console.error(`_parse__parametrisation: отсутствуют скобки []=[source=${source}]`);
        return null;
    }

    // 3=parse variants
    let data_rest = values_str;
    while (data_rest.length != 0) {
        let step_result;
        let _data_first;

        if (data_rest.startsWith('{')) {
            // 1=first=get MAP
            const _index = data_rest.indexOf('}');
            if (_index !== -1) {
                _data_first = data_rest.slice(0+1, _index).trim();
                data_rest = data_rest.slice(_index + 1).trim();

                if (_data_first) {
                    step_result = _parse__css_style(_data_first);
                } else {
                    step_result = new Map();
                }

            } else {
                console.error(`_parse__parametrisation: скобки - нет завершающей } =[data_rest=${data_rest}]`);
                return null;
            }

        } else {
            // 2=next=get separated values
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

// ---------------------------------------------------------------------------------------------------------------------
function onload__clone_elements() {
    const elements = document.querySelectorAll(`[${ATTR_NAME__CLONE_EL__PARAMS}]`);
    elements.forEach(el => {
        try {
            const params_source = el.getAttribute(ATTR_NAME__CLONE_EL__PARAMS);
            const with_attrs = el.hasAttribute(ATTR_NAME__CLONE_EL__W_ATTRS);
            const by_direct = el.hasAttribute(ATTR_NAME__CLONE_EL__BY_DIRECT);

            const parsed_object = _parse__parametrisation(params_source);
            if (!(parsed_object instanceof Array)) return;

            const [ def_property_name, params_parsed ] = parsed_object;
            if (!params_parsed) return;

            _clone_element(el, def_property_name, params_parsed, with_attrs, by_direct);
        } catch (err) {
            const msg = `el=${el}/err=${err}`
            console.error(msg);
        };

    });
}
OnLoadRunner.add(onload__clone_elements);


// =====================================================================================================================
const ATTR_NAME__AUTO__CONNECT_VALUES = "data-auto__connect_values";
const ATTR_NAME__GROUP = "data-group";

// ---------------------------------------------------------------------------------------------------------------------
// connect all elements like INPUT/OUTPUT/OUTPUT/PROGRESS/METER [${ATTR_NAME__GROUP}="${group_name}"] with updating values
// APPLY CALLING with param in page!!!
function _connect_values_in_group(group_name) {
    const schemaStable = true;

    function updateGroup(value) {
        let v = parseFloat(value);
        if (isNaN(v)) v = value;

        if (!schemaStable) {
            // Ограничиваем 0..1 для единообразия (хотя у некоторых max может отличаться)
            v = Math.min(1, Math.max(0, v));
        }

        // Обновляем все элементы с нужным name
        const elements = document.querySelectorAll(`[${ATTR_NAME__GROUP}="${group_name}"]`);
        elements.forEach(el => {
            if (el.value == v) return;

            if (el.tagName === 'PROGRESS' || el.tagName === 'METER' || el.tagName === 'INPUT' || el.tagName === 'OUTPUT') {
                if (schemaStable) {
                    el.value = v;
                } else {
                    // Учитываем возможный max (по умолчанию 1)
                    const max = parseFloat(el.getAttribute('max')) || 1;
                    let scaledValue = v * max;
                    scaledValue = Math.min(max, Math.max(0, scaledValue));
                    el.value = scaledValue;
                };
            }
        });
        // Синхронизируем управляющие элементы
        //_rangeInput.value = v;
        //_numberInput.value = v;
    }

    // События для задающих элементов
    const elements_input = document.querySelectorAll(`input[${ATTR_NAME__GROUP}="${group_name}"]`);
    elements_input.forEach(el => {
        el.addEventListener('input', (e) => updateGroup(e.target.value));
    });

    // Установим начальное состояние (из значения ползунка)
    //updateGroup(rangeInput.value);
}
// ---------------------------------------------------------------------------------------------------------------------
function onload__connect_values() {
    // PLACE ATTR_NAME__AUTO__CONNECT_VALUES ONLY IN INPUT!!! and its enough for only ONE!!!
    const groups_processed = new Set();

    const elements = document.querySelectorAll(`input[${ATTR_NAME__AUTO__CONNECT_VALUES}]`);
    for (let el of elements) {
        let group_name = el.getAttribute(ATTR_NAME__GROUP);
        if (!group_name || groups_processed.has(group_name)) continue;
        groups_processed.add(group_name);
        _connect_values_in_group(group_name);
    }
}
OnLoadRunner.add(onload__connect_values);


// =====================================================================================================================
// ---------------------------------------------------------------------------------------------------------------------
// ========== УПРАВЛЕНИЕ СЕКЦИЯМИ (data-collapsed) ==========
function onload__sections_collapse_init() {
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
}
OnLoadRunner.add(onload__sections_collapse_init);


// =====================================================================================================================
/**
 * Генерирует палитру цветов с равномерным делением шкалы 0..255.
 * @param {string} containerId - ID элемента, куда вставить таблицу.
 * @param {number} intervals - количество интервалов (делений) на шкале 0..255. (>=1)
 * @param {boolean} showHexValue - показывать ли шестнадцатеричный код (true) или только цвет.
 * @param {string} outputId - ID элемента <output> для отображения выбранного цвета (опционально).
 */
function generateColorPalette(containerId, intervals, showHexValue = false, outputId = null) {
    const DIVISIONS_DEF = 3;
    const container = document.getElementById(containerId);
    if (!container) {
        console.log(`Элемент с id "${containerId}" не найден`);
        return;
    }

    // Получаем массив значений от 0 до 255 с равномерным делением
    const values = [];
    intervals = get_num__direct_or_by_id(intervals);
    if (intervals === null) intervals = DIVISIONS_DEF;
    for (let i = 0; i <= intervals; i++) {
        let v = Math.round(255 * i / intervals);
        if (i === intervals) v = 255;
        values.push(v);
    }
    const uniqueValues = [...new Set(values)];

    // Преобразуем в hex-строки (2 символа)
    const hexValues = uniqueValues.map(v => v.toString(16).padStart(2, '0').toUpperCase());

    // Создаём таблицу
    const table = document.createElement('table');
    table.style.borderCollapse = 'collapse';
    table.style.width = '100%';
    table.style.margin = '1rem 0';
    table.style.fontFamily = 'monospace';
    table.style.fontSize = '0.8rem';

    // Заголовок: пустая ячейка, затем сочетания (зелёный, синий)
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    headerRow.appendChild(document.createElement('th')); // пустая
    for (const g of hexValues) {
        for (const b of hexValues) {
            const th = document.createElement('th');
            th.textContent = `${g}${b}`;
            th.style.padding = '4px';
            th.style.border = '1px solid #ccc';
            th.style.backgroundColor = '#f0f0f0';
            headerRow.appendChild(th);
        }
    }
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Тело таблицы: строки для каждого красного, внутри ячейки для каждой пары (g,b)
    const tbody = document.createElement('tbody');
    for (const r of hexValues) {
        const row = document.createElement('tr');
        // Ячейка с красным компонентом
        const thRow = document.createElement('th');
        thRow.textContent = r;
        thRow.style.border = '1px solid #ccc';
        thRow.style.backgroundColor = '#f0f0f0';
        thRow.style.padding = '4px';
        row.appendChild(thRow);

        // Ячейки для всех комбинаций g,b
        for (const g of hexValues) {
            for (const b of hexValues) {
                const hex = `#${r}${g}${b}`;
                const cell = document.createElement('td');
                cell.style.border = '1px solid #ccc';
                cell.style.padding = '8px';
                cell.style.backgroundColor = hex;
                cell.style.textAlign = 'center';
                cell.style.color = (parseInt(r, 16) * 0.299 + parseInt(g, 16) * 0.587 + parseInt(b, 16) * 0.114) > 128 ? '#000' : '#fff';
                if (showHexValue) {
                    cell.textContent = hex;
                }
                // Добавляем обработчик клика, если указан outputId
                if (outputId) {
                    cell.addEventListener('click', (function(color) {
                        return function() {
                            const output = document.getElementById(outputId);
                            if (output) {
                                // Устанавливаем значение output
                                if ('value' in output) {
                                    output.value = color;
                                } else {
                                    output.textContent = color;
                                };
                                output.dispatchEvent(new Event('input', { bubbles: false }));
                            }
                        };
                    })(hex));
                    cell.style.cursor = 'pointer';
                }
                row.appendChild(cell);
            }
        }
        tbody.appendChild(row);
    }
    table.appendChild(tbody);

    // Очищаем контейнер и вставляем таблицу
    container.innerHTML = '';
    container.appendChild(table);
}

OnLoadRunner.add(() => generateColorPalette('palette__id', null, false, "output_palette__id"));

// =====================================================================================================================
// ============================================================
// Изменение font-size при Ctrl + Wheel на элементах с атрибутом data-auto__scroll__font_size
// ============================================================
function onload__apply_wheel_textsize() {
    // TODO: use event on CTRL??? not wheel! cause of many calls???
    if (true) { return };

    const STEP = 2;
    const MIN = 8;
    const MAX = 48;

    function changeFontSize(el, delta) {
        let current = parseFloat(getComputedStyle(el).fontSize);
        let newSize = current + delta;
        if (newSize < MIN) newSize = MIN;
        if (newSize > MAX) newSize = MAX;
        el.style.fontSize = newSize + 'px';
    }

    document.addEventListener('wheel', function(e) {
        if (!e.ctrlKey) return;
        let target = e.target.closest('[data-auto__scroll__font_size]');
        if (!target) return;
        e.preventDefault();
        let delta = e.deltaY > 0 ? -STEP : STEP;
        changeFontSize(target, delta);
    });
}
OnLoadRunner.add(onload__apply_wheel_textsize);


// =====================================================================================================================
// FINISH
// ---------------------------------------------------------------------------------------------------------------------
OnLoadRunner.run();


// =====================================================================================================================
