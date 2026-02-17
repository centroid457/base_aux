document.addEventListener('DOMContentLoaded', () => {
    // Элементы
    const clientIpSpan = document.getElementById('client-ip');
    const currentUrlSpan = document.getElementById('current-url');
    const serverClockSpan = document.getElementById('server-clock');
    const toggleBtn = document.getElementById('info-toggle');
    const detailsPanel = document.getElementById('details-panel');
    const detailsContent = document.getElementById('details-content');

    // Текущий URL
    currentUrlSpan.textContent = window.location.href;

    // Данные, полученные с сервера (будем хранить здесь)
    let serverData = null;

    // Функция определения клиентской информации (браузер, ОС)
    function getClientInfo() {
        const ua = navigator.userAgent;
        let browser = "Unknown";
        let os = "Unknown";

        // Простейшее определение браузера
        if (ua.indexOf("Firefox") > -1) browser = "Firefox";
        else if (ua.indexOf("Edg") > -1) browser = "Edge";
        else if (ua.indexOf("Chrome") > -1) browser = "Chrome";
        else if (ua.indexOf("Safari") > -1) browser = "Safari";

        // Определение ОС
        if (ua.indexOf("Windows NT") > -1) os = "Windows";
        else if (ua.indexOf("Mac OS X") > -1) os = "macOS";
        else if (ua.indexOf("Linux") > -1) os = "Linux";
        else if (ua.indexOf("Android") > -1) os = "Android";
        else if (ua.indexOf("iOS") > -1 || ua.indexOf("iPhone") > -1) os = "iOS";

        return {
            browser: browser,
            os: os,
            user_agent: ua,
            local_time: new Date().toLocaleString()
        };
    }

    // Функция загрузки данных с сервера
    async function fetchServerInfo() {
        try {
            const response = await fetch('/api/info');
            const data = await response.json();
            serverData = data;

            // Обновляем IP в верхней панели
            clientIpSpan.textContent = data.NETWORK.client_ip;

            // Объединяем с клиентской информацией
            const clientInfo = getClientInfo();
            serverData.CLIENT = {
                ip: data.NETWORK.client_ip,
                browser: clientInfo.browser,
                os: clientInfo.os,
                local_time: clientInfo.local_time,
                user_agent: clientInfo.user_agent
            };

            return serverData;
        } catch (error) {
            console.error('Ошибка получения данных:', error);
            clientIpSpan.textContent = 'ошибка';
            return null;
        }
    }

    // Функция отрисовки детальной информации
    function renderDetails(data, container, level = 0) {
        if (!data) return '';
        let html = '';
        const indent = level * 20; // отступ в пикселях для подгрупп

        for (const [key, value] of Object.entries(data)) {
            if (value && typeof value === 'object' && !Array.isArray(value)) {
                // Это подгруппа – рисуем заголовок и рекурсивно её содержимое
                html += `<div style="margin-left: ${indent}px; margin-top: 8px;">`;
                html += `<h4 style="margin: 0 0 4px 0; color: #2c3e50; font-size: 14px;">${key}</h4>`;
                html += renderDetails(value, null, level + 1);
                html += `</div>`;
            } else {
                // Обычная пара ключ-значение
                html += `
                    <div style="display: flex; margin-left: ${indent}px; gap: 10px; font-size: 13px; line-height: 1.5;">
                        <div style="font-weight: bold; min-width: 120px; color: #555;">${key}:</div>
                        <div style="color: #000;">${value !== null && value !== undefined ? value : '—'}</div>
                    </div>
                `;
            }
        }

        if (container) {
            container.innerHTML = html;
        }
        return html;
    }

    // Обновление часов
    async function updateClock() {
        try {
            const response = await fetch('/api/clock');
            const data = await response.json();
            serverClockSpan.textContent = data.server_time;
        } catch (error) {
            serverClockSpan.textContent = 'ошибка';
        }
    }

    // Первоначальная загрузка (IP, данные для деталей)
    fetchServerInfo();

    // Часы обновляем каждые 60 секунд
    updateClock();
    setInterval(updateClock, 60000);

    // Обработка клика по кнопке "i"
    toggleBtn.addEventListener('click', async () => {
        if (detailsPanel.classList.contains('hidden')) {
            detailsPanel.classList.remove('hidden');

            if (!serverData) {
                detailsContent.innerHTML = 'Загрузка...';
                await fetchServerInfo();
            } else {
                const clientInfo = getClientInfo();
                serverData.CLIENT.local_time = clientInfo.local_time;
                serverData.CLIENT.browser = clientInfo.browser;
                serverData.CLIENT.os = clientInfo.os;
                serverData.CLIENT.user_agent = clientInfo.user_agent;
            }

            // Передаём контейнер для отрисовки
            renderDetails(serverData, detailsContent);
        } else {
            detailsPanel.classList.add('hidden');
        }
    });
});