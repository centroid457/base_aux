(function() {
    // Встроенные стили (можно вынести в отдельный CSS, но для автономности оставим здесь)
    const txt_styles_new = `
        .info-bar {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            background-color: #333;
            color: #fff;
            padding: 4px 8px;
            gap: 12px;
            font-size: 13px;
            font-family: Arial, sans-serif;
            position: relative;
            z-index: 1000;
        }
        .info-item {
            display: flex;
            align-items: center;
            gap: 3px;
            white-space: nowrap;
        }
        .label {
            font-weight: bold;
            color: #aaa;
        }
        .value {
            color: #fff;
        }
        .info-toggle {
            background: none;
            border: none;
            color: #fff;
            font-size: 20px;
            cursor: pointer;
            margin-left: auto;
            padding: 0 4px;
            line-height: 1;
            text-decoration: none;
        }
        .info-toggle:hover {
            color: #0af;
        }
    `;

    const txt_header = `
        <div class="info-item">
            <span class="label">Сервис:</span>
            <span class="value" id="id__service_name">Загрузка...</span>
        </div>
        <div class="info-item">
            <span class="label">Описание:</span>
            <span class="value" id="id__service_description">Загрузка...</span>
        </div>
        <div class="info-item">
            <span class="label">Ваш IP:</span>
            <span class="value" id="id__client_ip">...</span>
        </div>
        <div class="info-item">
            <span class="label">URL:</span>
            <span class="value" id="id__current_url>...</span>
        </div>
        <div class="info-item">
            <span class="label">Серверное время:</span>
            <span class="value" id="id__server_clock">...</span>
        </div>
        <a href="/service_details" class="info-toggle" title="Подробная информация">ⓘ</a>
    `;


    // Добавляем стили в head
    const el_styles_new = document.createElement('style');
    el_styles_new.textContent = txt_styles_new;
    document.head.appendChild(el_styles_new);

    // Создаём хедер
    const el_header = document.createElement('header');
    el_header.className = 'info-bar';
    el_header.innerHTML = txt_header

    // Вставляем хедер в самое начало body
    document.body.insertBefore(el_header, document.body.firstChild);

    // Получаем ссылки на элементы
    const el__service_name = document.getElementById('id__service_name');
    const el__service_description = document.getElementById('id__service_description');
    const el__client_ip = document.getElementById('id__client_ip');
    const el__current_url = document.getElementById('id__current_url');
    const el__server_clock = document.getElementById('id__server_clock');

    // Устанавливаем текущий URL
    el__current_url.textContent = window.location.href;

    // Функция загрузки данных с сервера
    async function fetchHeaderInfo() {
        try {
            const response = await fetch('/api/info');
            const data = await response.json();
            el__service_name.textContent = data.SERVICE.name;
            el__service_description.textContent = data.SERVICE.description;
            el__client_ip.textContent = data.NETWORK.client_ip;
        } catch (error) {
            console.error('Ошибка загрузки данных хедера:', error);
            el__service_name.textContent = 'Ошибка';
            el__service_description.textContent = 'Ошибка';
            el__client_ip.textContent = 'Ошибка';
        }
    }

    // Функция обновления часов
    async function updateClock() {
        try {
            const response = await fetch('/api/clock');
            const data = await response.json();
            el__server_clock.textContent = data.server_time;
        } catch (error) {
            el__server_clock.textContent = 'ошибка';
        }
    }

    // Запускаем
    fetchHeaderInfo();
    updateClock();
    setInterval(updateClock, 1000);
})();