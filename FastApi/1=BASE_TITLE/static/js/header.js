(function() {
    // Встроенные стили (можно вынести в отдельный CSS, но для автономности оставим здесь)
    const styles = `
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

    // Добавляем стили в head
    const styleEl = document.createElement('style');
    styleEl.textContent = styles;
    document.head.appendChild(styleEl);

    // Создаём хедер
    const header = document.createElement('header');
    header.className = 'info-bar';
    header.innerHTML = `
        <div class="info-item">
            <span class="label">Сервис:</span>
            <span class="value" id="service-name">Загрузка...</span>
        </div>
        <div class="info-item">
            <span class="label">Описание:</span>
            <span class="value" id="service-description">Загрузка...</span>
        </div>
        <div class="info-item">
            <span class="label">Ваш IP:</span>
            <span class="value" id="client-ip">...</span>
        </div>
        <div class="info-item">
            <span class="label">URL:</span>
            <span class="value" id="current-url">...</span>
        </div>
        <div class="info-item">
            <span class="label">Серверное время:</span>
            <span class="value" id="server-clock">...</span>
        </div>
        <a href="/service_details" class="info-toggle" title="Подробная информация">ⓘ</a>
    `;

    // Вставляем хедер в самое начало body
    document.body.insertBefore(header, document.body.firstChild);

    // Получаем ссылки на элементы
    const serviceNameEl = document.getElementById('service-name');
    const serviceDescEl = document.getElementById('service-description');
    const clientIpEl = document.getElementById('client-ip');
    const currentUrlEl = document.getElementById('current-url');
    const serverClockEl = document.getElementById('server-clock');

    // Устанавливаем текущий URL
    currentUrlEl.textContent = window.location.href;

    // Функция загрузки данных с сервера
    async function fetchHeaderInfo() {
        try {
            const response = await fetch('/api/info');
            const data = await response.json();
            serviceNameEl.textContent = data.SERVICE.name;
            serviceDescEl.textContent = data.SERVICE.description;
            clientIpEl.textContent = data.NETWORK.client_ip;
        } catch (error) {
            console.error('Ошибка загрузки данных хедера:', error);
            serviceNameEl.textContent = 'Ошибка';
            serviceDescEl.textContent = 'Ошибка';
            clientIpEl.textContent = 'Ошибка';
        }
    }

    // Функция обновления часов
    async function updateClock() {
        try {
            const response = await fetch('/api/clock');
            const data = await response.json();
            serverClockEl.textContent = data.server_time;
        } catch (error) {
            serverClockEl.textContent = 'ошибка';
        }
    }

    // Запускаем
    fetchHeaderInfo();
    updateClock();
    setInterval(updateClock, 1000);
})();