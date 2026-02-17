document.addEventListener('DOMContentLoaded', () => {
    // Элементы
    const clientIpSpan = document.getElementById('client-ip');
    const currentUrlSpan = document.getElementById('current-url');
    const serverClockSpan = document.getElementById('server-clock');
    const showDetailsBtn = document.getElementById('show-details-btn');
    const detailsPanel = document.getElementById('details-panel');
    const detailsContent = document.getElementById('details-content');

    // Установка текущего URL (выполняется сразу)
    currentUrlSpan.textContent = window.location.href;

    // Функция обновления IP и детальной информации
    async function fetchInfo() {
        try {
            const response = await fetch('/api/info');
            const data = await response.json();

            // IP клиента
            clientIpSpan.textContent = data.network.client_ip;

            // Детальная информация (для панели)
            // Сохраняем данные в атрибут или просто будем использовать при показе
            window.detailsData = data;
        } catch (error) {
            console.error('Ошибка получения информации:', error);
            clientIpSpan.textContent = 'недоступно';
        }
    }

    // Функция обновления часов (получает серверное время)
    async function updateClock() {
        try {
            const response = await fetch('/api/clock');
            const data = await response.json();
            serverClockSpan.textContent = data.server_time;
        } catch (error) {
            console.error('Ошибка получения времени:', error);
            serverClockSpan.textContent = 'ошибка';
        }
    }

    // Запускаем получение IP и деталей
    fetchInfo();

    // Обновляем часы каждые 60 секунд (можно меньше, например 10 с)
    updateClock(); // сразу при загрузке
    setInterval(updateClock, 60000); // 60 000 мс = 1 минута

    // Обработка кнопки "Подробнее"
    showDetailsBtn.addEventListener('click', () => {
        if (detailsPanel.classList.contains('hidden')) {
            // Показываем панель и заполняем данными
            detailsPanel.classList.remove('hidden');
            showDetailsBtn.textContent = 'Скрыть подробную информацию';

            if (window.detailsData) {
                renderDetails(window.detailsData);
            } else {
                detailsContent.textContent = 'Данные ещё не загружены, попробуйте обновить страницу.';
            }
        } else {
            detailsPanel.classList.add('hidden');
            showDetailsBtn.textContent = 'Показать подробную информацию о сервисе';
        }
    });

    // Функция форматирования и отображения детальной информации
    function renderDetails(data) {
        const lines = [];

        // Сервис
        lines.push('=== СЕРВИС ===');
        lines.push(`Имя: ${data.service.name}`);
        lines.push(`Описание: ${data.service.description}`);
        lines.push(`Автор: ${data.service.author}`);
        lines.push(`Фреймворк: ${data.service.framework}`);
        lines.push(`Запущен: ${data.service.start_time}`);
        lines.push('');

        // Система
        lines.push('=== СИСТЕМА ===');
        lines.push(`ОС: ${data.system.os} ${data.system.os_version}`);
        lines.push(`Имя хоста: ${data.system.hostname}`);
        lines.push(`Процессор: ${data.system.processor}`);
        lines.push(`Архитектура: ${data.system.machine}`);
        lines.push(`Последняя загрузка: ${data.system.boot_time}`);
        lines.push(`Пользователь: ${data.system.username} (${data.system.user_level})`);

        if (data.system.load && Object.keys(data.system.load).length > 0) {
            lines.push(`Загрузка CPU (1/5/15 мин): ${data.system.load.load_1min} / ${data.system.load.load_5min} / ${data.system.load.load_15min}`);
        }
        lines.push('');

        // Сеть
        lines.push('=== СЕТЬ ===');
        lines.push(`Ваш IP: ${data.network.client_ip}`);
        lines.push(`Сервер (hostname): ${data.network.server_hostname}`);
        lines.push('');

        // Серверное время
        lines.push(`Серверное время (на момент запроса): ${data.server_time}`);

        detailsContent.textContent = lines.join('\n');
    }
});