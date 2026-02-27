(function() {
    // внедряем стили --------------------
    const txt__header_styles = `
        .cls__header_line {
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
        .cls__header_item {
            display: flex;
            align-items: center;
            gap: 3px;
            white-space: nowrap;
        }
        .cls__header_label {
            font-weight: bold;
            color: #aaa;
        }
        .cls__header_value {
            color: #fff;
        }
        .cls__header_btn_info {
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
        .cls__header_btn_info:hover {
            color: #0af;
        }
    `;

    const el_styles_new = document.createElement('style');
    el_styles_new.textContent = txt__header_styles;
    document.head.appendChild(el_styles_new);

    // внедряем элементы ---------------------------------
    const txt__header_elements = `
        <div class="cls__header_item">
            <span class="cls__header_label">Сервис:</span>
            <span class="cls__header_value" id="id__service_name">...</span>
        </div>
        <div class="cls__header_item">
            <span class="cls__header_label">Описание:</span>
            <span class="cls__header_value" id="id__service_description">...</span>
        </div>
        <div class="cls__header_item">
            <span class="cls__header_label">Ваш IP:</span>
            <span class="cls__header_value" id="id__client_ip">...</span>
        </div>
        <div class="cls__header_item">
            <span class="cls__header_label">URL:</span>
            <span class="cls__header_value" id="id__current_url">...</span>
        </div>
        <div class="cls__header_item">
            <span class="cls__header_label">Серверное время:</span>
            <span class="cls__header_value" id="id__server_clock">...</span>
        </div>
        <a href="/service_details" class="cls__header_btn_info" title="Подробная информация">ⓘ</a>
    `;

    const el_header = document.createElement('header');
    el_header.className = 'cls__header_line';
    el_header.innerHTML = txt__header_elements

    // Вставляем хедер в самое начало body --------------
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
    async function loadHeaderInfo() {
        try {
            const response = await fetch('/api/info');
            const data = await response.json();
            el__service_name.textContent = data.static.SERVICE_INFO.name;
            el__service_description.textContent = data.static.SERVICE_INFO.description;
            el__client_ip.textContent = data.static.NETWORK.client_ip;
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
    loadHeaderInfo();
    updateClock();
    setInterval(updateClock, 1000);
})();