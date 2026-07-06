// =====================================================================================================================
// FETCH API – ПОЛНЫЙ СПРАВОЧНИК С ПРИМЕРАМИ
// Скопируйте этот файл в консоль браузера или подключите как скрипт.
// Все функции возвращают Promise и логируют результаты в консоль.
// ============================================================

// -------- 0. ВСПОМОГАТЕЛЬНЫЕ УТИЛИТЫ --------

/**
 * Безопасный fetch с проверкой статуса и парсингом JSON
 * @param {string} url
 * @param {object} options – параметры fetch
 * @param {boolean} parseJson – парсить ли ответ как JSON
 * @returns {Promise<any>}
 */
async function safeFetch(url, options = {}, parseJson = true) {
    const response = await fetch(url, options);
    if (!response.ok) {
        let errorMsg = `HTTP ${response.status}: ${response.statusText}`;
        try {
            const errBody = await response.json();
            if (errBody.message) errorMsg += ` – ${errBody.message}`;
        } catch (_) { /* игнорируем, если не JSON */ }
        throw new Error(errorMsg);
    }
    return parseJson ? response.json() : response;
}

/**
 * Логирование с цветом в консоль
 */
function log(title, data) {
    console.log(`%c${title}`, 'font-weight:bold; color:#2c3e50;', data);
}

// -------- 1. БАЗОВЫЙ GET-ЗАПРОС --------

async function getExample(url = 'https://jsonplaceholder.typicode.com/posts/1') {
    try {
        const data = await safeFetch(url);
        log('✅ GET успешно:', data);
        return data;
    } catch (err) {
        console.error('❌ GET ошибка:', err);
    }
}

// -------- 2. POST, PUT, DELETE --------

async function postExample() {
    const newPost = {
        title: 'Новый пост',
        body: 'Содержимое поста',
        userId: 1
    };
    try {
        const data = await safeFetch('https://jsonplaceholder.typicode.com/posts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newPost)
        });
        log('✅ POST успешно:', data);
        return data;
    } catch (err) {
        console.error('❌ POST ошибка:', err);
    }
}

async function putExample(id = 1) {
    const updated = {
        id,
        title: 'Обновлённый заголовок',
        body: 'Новое содержимое',
        userId: 1
    };
    try {
        const data = await safeFetch(`https://jsonplaceholder.typicode.com/posts/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updated)
        });
        log('✅ PUT успешно:', data);
        return data;
    } catch (err) {
        console.error('❌ PUT ошибка:', err);
    }
}

async function deleteExample(id = 1) {
    try {
        const response = await safeFetch(`https://jsonplaceholder.typicode.com/posts/${id}`, {
            method: 'DELETE'
        }, false); // не парсим JSON, т.к. ответ пустой
        if (response.ok) {
            log('✅ DELETE успешно, статус:', response.status);
            return true;
        }
    } catch (err) {
        console.error('❌ DELETE ошибка:', err);
    }
}

// -------- 3. ОБРАБОТКА РАЗНЫХ ТИПОВ ОТВЕТОВ --------

async function textExample() {
    const response = await fetch('https://jsonplaceholder.typicode.com/posts/1');
    const text = await response.text();
    log('📄 Ответ как текст (первые 100 символов):', text.substring(0, 100) + '...');
    return text;
}

async function blobExample() {
    const response = await fetch('https://via.placeholder.com/150');
    const blob = await response.blob();
    log('🖼️ Blob:', { size: blob.size, type: blob.type });
    // Создаём URL для отображения
    const url = URL.createObjectURL(blob);
    console.log('URL изображения:', url);
    return blob;
}

async function formDataExample() {
    // Пример получения FormData (обычно с сервера, но мы сымитируем)
    const response = await fetch('https://httpbin.org/post', {
        method: 'POST',
        body: new URLSearchParams({ key: 'value' })
    });
    const fd = await response.formData();
    log('📋 FormData:', fd);
    return fd;
}

// -------- 4. ЗАПРОСЫ С ПАРАМЕТРАМИ И ЗАГОЛОВКАМИ --------

async function withHeadersExample() {
    const data = await safeFetch('https://jsonplaceholder.typicode.com/posts/1', {
        headers: {
            'Authorization': 'Bearer fake-token',
            'X-Custom-Header': 'my-value'
        }
    });
    log('✅ Заголовки отправлены, ответ:', data);
    return data;
}

async function withQueryParamsExample() {
    const params = new URLSearchParams({
        userId: 1,
        _limit: 3
    });
    const url = `https://jsonplaceholder.typicode.com/posts?${params}`;
    const data = await safeFetch(url);
    log('✅ GET с параметрами:', data);
    return data;
}

// -------- 5. ОТМЕНА ЗАПРОСА (AbortController) --------

let abortController = null;

async function abortableFetch(url = 'https://jsonplaceholder.typicode.com/posts/1', timeout = 3000) {
    // Создаём новый контроллер для каждого вызова
    abortController = new AbortController();
    const signal = abortController.signal;

    // Таймаут для автоматической отмены
    const timeoutId = setTimeout(() => {
        abortController.abort();
        console.warn('⏰ Запрос отменён по таймауту');
    }, timeout);

    try {
        const response = await fetch(url, { signal });
        clearTimeout(timeoutId);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        log('✅ Запрос выполнен:', data);
        return data;
    } catch (err) {
        if (err.name === 'AbortError') {
            console.warn('🚫 Запрос был отменён пользователем или таймаутом');
        } else {
            console.error('❌ Ошибка:', err);
        }
    } finally {
        abortController = null;
    }
}

// Функция для ручной отмены
function cancelFetch() {
    if (abortController) {
        abortController.abort();
        console.log('🛑 Отмена запроса инициирована');
    } else {
        console.warn('Нет активного запроса для отмены');
    }
}

// -------- 6. ТАЙМАУТ (универсальный) --------

async function fetchWithTimeout(url, options = {}, timeout = 5000) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);
    try {
        const response = await fetch(url, { ...options, signal: controller.signal });
        clearTimeout(timeoutId);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
    } catch (err) {
        if (err.name === 'AbortError') {
            throw new Error('Запрос превысил таймаут');
        }
        throw err;
    }
}

// -------- 7. ПАРАЛЛЕЛЬНЫЕ ЗАПРОСЫ --------

async function parallelRequestsExample() {
    const urls = [
        'https://jsonplaceholder.typicode.com/posts/1',
        'https://jsonplaceholder.typicode.com/posts/2',
        'https://jsonplaceholder.typicode.com/posts/3'
    ];
    try {
        const results = await Promise.all(urls.map(url => safeFetch(url)));
        log('✅ Параллельные GET (Promise.all):', results);
        return results;
    } catch (err) {
        console.error('❌ Один из запросов упал:', err);
    }
}

async function parallelSettledExample() {
    const urls = [
        'https://jsonplaceholder.typicode.com/posts/1',
        'https://jsonplaceholder.typicode.com/posts/2',
        'https://invalid-url.fail' // этот запрос упадёт
    ];
    const results = await Promise.allSettled(urls.map(async url => {
        try {
            return await safeFetch(url);
        } catch (e) {
            return { error: e.message };
        }
    }));
    log('✅ Promise.allSettled (все результаты):', results);
    return results;
}

// -------- 8. ПОВТОРНЫЕ ЗАПРОСЫ (RETRY) --------

async function fetchWithRetry(url, options = {}, retries = 3, delay = 1000) {
    let lastError;
    for (let attempt = 1; attempt <= retries; attempt++) {
        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                // Если 5xx – пробуем снова
                if (response.status >= 500 && attempt < retries) {
                    console.warn(`🔄 Попытка ${attempt}/${retries} (${response.status}), повтор через ${delay}ms...`);
                    await new Promise(r => setTimeout(r, delay));
                    continue;
                }
                throw new Error(`HTTP ${response.status}`);
            }
            return response.json();
        } catch (err) {
            lastError = err;
            if (attempt < retries) {
                console.warn(`🔄 Попытка ${attempt}/${retries} упала: ${err.message}, повтор...`);
                await new Promise(r => setTimeout(r, delay));
            }
        }
    }
    throw new Error(`Не удалось выполнить запрос после ${retries} попыток: ${lastError?.message}`);
}

// -------- 9. ЗАГРУЗКА ФАЙЛА (скачивание) --------

async function downloadFile(url, filename = 'downloaded-file') {
    try {
        const response = await fetch(url);
        const blob = await response.blob();
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(link.href);
        log(`✅ Файл "${filename}" скачан`, { size: blob.size, type: blob.type });
        return true;
    } catch (err) {
        console.error('❌ Ошибка скачивания:', err);
    }
}

// -------- 10. ПРОГРЕСС ЗАГРУЗКИ (потоковое чтение) --------

async function fetchWithProgress(url, onProgress) {
    const response = await fetch(url);
    const contentLength = +response.headers.get('Content-Length');
    const reader = response.body.getReader();
    let received = 0;
    const chunks = [];

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        chunks.push(value);
        received += value.length;
        if (onProgress && contentLength) {
            const percent = Math.round((received / contentLength) * 100);
            onProgress(percent);
        }
    }

    const blob = new Blob(chunks);
    return blob;
}

// Пример использования с логом
async function downloadWithProgressExample(url = 'https://via.placeholder.com/150') {
    const blob = await fetchWithProgress(url, percent => {
        console.log(`⏳ Прогресс: ${percent}%`);
    });
    log('✅ Файл загружен, размер:', blob.size);
    return blob;
}

// -------- 11. КЕШИРОВАНИЕ (ручное) --------

const fetchCache = new Map();

async function cachedFetch(url, options = {}, ttl = 60000) {
    const key = url + JSON.stringify(options);
    if (fetchCache.has(key)) {
        const entry = fetchCache.get(key);
        if (Date.now() - entry.timestamp < ttl) {
            log(`💾 Кеш (${key})`, entry.data);
            return entry.data;
        } else {
            fetchCache.delete(key);
        }
    }

    const data = await safeFetch(url, options);
    fetchCache.set(key, { data, timestamp: Date.now() });
    log('📡 Запрос выполнен, сохранён в кеш', data);
    return data;
}

// -------- 12. ИНТЕРЦЕПТОРЫ (обёртка) --------

function createApiClient(baseURL = 'https://jsonplaceholder.typicode.com') {
    async function request(endpoint, options = {}) {
        const defaultHeaders = {
            'Content-Type': 'application/json',
        };
        // Можно добавить авторизацию из localStorage
        const token = localStorage.getItem('token');
        if (token) {
            defaultHeaders['Authorization'] = `Bearer ${token}`;
        }

        const url = baseURL + endpoint;
        const fullOptions = {
            ...options,
            headers: {
                ...defaultHeaders,
                ...options.headers
            }
        };

        // Логируем запрос
        console.log(`📤 ${fullOptions.method || 'GET'} ${url}`, fullOptions.body);

        const response = await fetch(url, fullOptions);
        if (!response.ok) {
            // Обработка ошибок: если 401 – перенаправление на логин
            if (response.status === 401) {
                console.warn('🔐 Неавторизован, перенаправление на логин');
                // window.location.href = '/login';
            }
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        const data = await response.json();
        console.log(`📥 Ответ от ${endpoint}`, data);
        return data;
    }

    return {
        get: (endpoint, options) => request(endpoint, { ...options, method: 'GET' }),
        post: (endpoint, body, options) => request(endpoint, { ...options, method: 'POST', body: JSON.stringify(body) }),
        put: (endpoint, body, options) => request(endpoint, { ...options, method: 'PUT', body: JSON.stringify(body) }),
        delete: (endpoint, options) => request(endpoint, { ...options, method: 'DELETE' }),
        // можно добавить другие методы
    };
}

// -------- 13. РАБОТА С ЗАГОЛОВКАМИ ОТВЕТА --------

async function inspectHeaders(url = 'https://jsonplaceholder.typicode.com/posts/1') {
    const response = await fetch(url);
    log('📋 Заголовки ответа:');
    for (const [key, value] of response.headers) {
        console.log(`  ${key}: ${value}`);
    }
    // Получить конкретный заголовок
    const contentType = response.headers.get('content-type');
    console.log('Content-Type:', contentType);
    return response;
}

// -------- 14. ЗАГРУЗКА ФАЙЛОВ НА СЕРВЕР (пример) --------

async function uploadFileExample(fileInputElement) {
    if (!fileInputElement || !fileInputElement.files.length) {
        console.warn('Выберите файл в input[type="file"]');
        return;
    }
    const file = fileInputElement.files[0];
    const formData = new FormData();
    formData.append('file', file);
    formData.append('description', 'Мой файл');

    try {
        const response = await fetch('https://httpbin.org/post', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        log('✅ Файл загружен, ответ:', data);
        return data;
    } catch (err) {
        console.error('❌ Ошибка загрузки:', err);
    }
}

// -------- 15. ПОТОКОВОЕ ЧТЕНИЕ JSON (JSON Lines) --------

async function streamJsonLines(url) {
    const response = await fetch(url);
    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';
    let chunkCount = 0;

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop(); // оставляем неполную строку
        for (const line of lines) {
            if (line.trim()) {
                try {
                    const obj = JSON.parse(line);
                    chunkCount++;
                    console.log(`📦 Объект #${chunkCount}:`, obj);
                } catch (e) {
                    console.warn('Некорректный JSON:', line);
                }
            }
        }
    }
    console.log(`✅ Поток завершён, обработано ${chunkCount} объектов`);
}

// -------- АВТОЗАПУСК ДЕМОНСТРАЦИИ (при загрузке в консоли) --------

if (typeof window !== 'undefined') {
    console.log('%c📡 FETCH API – Справочник с примерами', 'font-size:16px; font-weight:bold; color:#2980b9;');
    console.log('Доступные функции:');
    const funcs = [
        'getExample()', 'postExample()', 'putExample()', 'deleteExample()',
        'textExample()', 'blobExample()', 'formDataExample()',
        'withHeadersExample()', 'withQueryParamsExample()',
        'abortableFetch()', 'cancelFetch()', 'fetchWithTimeout()',
        'parallelRequestsExample()', 'parallelSettledExample()',
        'fetchWithRetry()', 'downloadFile()', 'downloadWithProgressExample()',
        'cachedFetch()', 'createApiClient()', 'inspectHeaders()',
        'uploadFileExample()', 'streamJsonLines()'
    ];
    funcs.forEach(name => {
        console.log(`  ${name}`);
    });
    console.log('Пример: await getExample()');
}

// ============================================================
// ЭКСПОРТ (для модулей, если нужно)
// ============================================================

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        safeFetch,
        getExample,
        postExample,
        putExample,
        deleteExample,
        textExample,
        blobExample,
        formDataExample,
        withHeadersExample,
        withQueryParamsExample,
        abortableFetch,
        cancelFetch,
        fetchWithTimeout,
        parallelRequestsExample,
        parallelSettledExample,
        fetchWithRetry,
        downloadFile,
        downloadWithProgressExample,
        cachedFetch,
        createApiClient,
        inspectHeaders,
        uploadFileExample,
        streamJsonLines
    };
}


// =====================================================================================================================
