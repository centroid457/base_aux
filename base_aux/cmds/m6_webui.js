// =====================================================================================================================
// Глобальный менеджер объектов (только бизнес-логика)
// =====================================================================================================================
const itemsManager = {
    items_map: new Map(),
    ws: null,                         // будет назначен снаружи

    // Сохранить ссылку на WebSocket‑клиент
    set_ws_client(wsClient) {
        this.ws = wsClient;
    },

    // Инициализация UI при загрузке страницы
    async initUI() {
        document.getElementById('btn_add_item__id').addEventListener('click', () => this.send__item_create());
        // reloadUI теперь будет вызываться отдельно (при открытии WS или сразу после старта)
    },

    // Полная очистка и перестройка UI по данным с сервера
    async reloadUI() {
        // удаляем все существующие UI-элементы
        for (const [id, ui] of this.items_map) {
            this.item_del(id);
        }

        const serverIds = await this.items_load();
        for (const idn of serverIds) {
            this.item_create(idn);
        }
    },

    // Загрузка актуального списка объектов с сервера
    async items_load() {
        try {
            const resp = await fetch('/item/list');
            const data = await resp.json();
            return data?.items || [];
        } catch {
            return [];
        }
    },

    // ---------- отправка команд (используем this.ws) ----------
    send__item_create() {
        this.ws?.send_json({
            channel: "item_control",
            action: "create_item",
        });
    },

    send__item_del(itemId) {
        this.ws?.send_json({
            item_id: itemId,
            channel: "item_control",
            action: "delete_item",
        });
    },

    item_create(itemId) {
        if (this.items_map.has(itemId)) return;
        const itemUI = new ItemUI(itemId, this.ws);   // передаём ws в UI
        this.items_map.set(itemId, itemUI);
        itemUI.init();
    },

    item_del(itemId) {
        this.items_map.get(itemId)?.destroy();
        this.items_map.delete(itemId);
    },

    // ---------- обработчики входящих данных ----------
    history_append(itemId, style, text) {
        this.items_map.get(itemId)?.history_add_line(style, text);
    },

    history_clear(itemId) {
        this.items_map.get(itemId)?.history_clear();
    },
};

// =====================================================================================================================
// UI отдельного объекта
// =====================================================================================================================
class ItemUI {
    // Принимает идентификатор и ссылку на WebSocket‑клиент
    constructor(itemId, ws) {
        this.itemId = itemId;
        this.ws = ws;                       // теперь не зависит от глобальной переменной
        this.element_ItemBox   = null;
        this.element_OutputBox = null;
        this.element_InputBox  = null;
    }

    init() {
        this.render();
        this.loadHistory();
    }

    async render() {
        const div_itembox = document.createElement('div');
        div_itembox.className = 'item__cls';

        // Header
        const header       = document.createElement('header');
        const header_div1  = document.createElement('div');
        const header_div2  = document.createElement('div');
        header.appendChild(header_div1);
        header.appendChild(header_div2);

        const spanId = document.createElement('span');
        spanId.className = 'span_item_id__cls';
        spanId.textContent = this.itemId;
        header_div1.appendChild(spanId);

        const btnClear = document.createElement('button');
        btnClear.setAttribute('data-btn_outline', "blue");
        btnClear.textContent = 'clear';
        btnClear.title = 'Clear History';
        btnClear.onclick = () => this.send__history_clear();

        const btnReconnect = document.createElement('button');
        btnReconnect.setAttribute('data-btn_outline', "blue");
        btnReconnect.textContent = 'Reconnect';
        btnReconnect.title = 'Reconnect';
        btnReconnect.onclick = () => this.send__reconnect();

        const btnClose = document.createElement('button');
        btnClose.setAttribute('data-btn_outline', "red");
        btnClose.textContent = 'X';
        btnClose.title = 'Close';
        btnClose.onclick = () => itemsManager.send__item_del(this.itemId);

        header_div2.appendChild(btnClear);
        header_div2.appendChild(btnReconnect);
        header_div2.appendChild(btnClose);

        // Output area
        const output = document.createElement('main');
        output.setAttribute('data-scrollbar__dark', '');
        this.element_OutputBox = output;

        // Input area
        const footer = document.createElement('footer');
        const input  = document.createElement('input');
        input.type        = 'text';
        input.placeholder = 'Введите команду и нажмите Enter';
        this.element_InputBox = input;
        footer.appendChild(input);

        div_itembox.appendChild(header);
        div_itembox.appendChild(output);
        div_itembox.appendChild(footer);
        this.element_ItemBox = div_itembox;
        document.getElementById('items_container__id').appendChild(div_itembox);

        // Отправка строки по Enter
        input.addEventListener('change', () => this.send__input());
    }

    // ---------- отправка команд через this.ws ----------
    send__input() {
        const line = this.element_InputBox.value.trim();
        if (!line) return;

        const sent = this.ws?.send_json({
            item_id: this.itemId,
            channel: "history_log",
            action: "stdin",
            text: line,
        });
        if (sent) {
            this.element_InputBox.value = '';
        }
    }

    send__reconnect() {
        this.ws?.send_json({
            item_id: this.itemId,
            channel: "item_control",
            action: "reconnect_item",
        });
    }

    send__history_clear() {
        this.ws?.send_json({
            item_id: this.itemId,
            channel: "item_control",
            action: "clear_history",
        });
    }

    history_clear() {
        this.element_OutputBox.innerHTML = '';
    }

    // ---------- загрузка истории с REST ----------
    async loadHistory() {
        this.element_OutputBox.innerHTML = '';
        try {
            const resp = await fetch(`/item/history/get/${this.itemId}`);
            const history = await resp.json();
            history.forEach(log_line => {
                if (log_line.input) this.history_add_line('stdin', log_line.input);
                log_line.stdout?.forEach(l => this.history_add_line('stdout', l));
                log_line.stderr?.forEach(l => this.history_add_line('stderr', l));
                log_line.debug?.forEach(l  => this.history_add_line('debug', l));
            });
        } catch (err) {
            this.history_add_line('msg_stderr__cls', `Ошибка loadHistory: ${err.message}`);
        }
    }

    history_add_line(style, text) {
        let cssClass;
        switch (style) {
            case 'stdout': cssClass = 'msg_stdout__cls'; break;
            case 'stderr': cssClass = 'msg_stderr__cls'; break;
            case 'stdin':  cssClass = 'msg_stdin__cls'; break;
            default:       cssClass = 'msg_debug__cls';
        }

        const line = document.createElement('div');
        line.className = cssClass;
        line.textContent = text;
        this.element_OutputBox.appendChild(line);
        this.element_OutputBox.scrollTop = this.element_OutputBox.scrollHeight;
    }

    destroy() {
        this.element_ItemBox?.remove();
    }
}

// =====================================================================================================================
// Запуск
// =====================================================================================================================
window.onload = async () => {
    // 1. Создаём WebSocket‑клиент (пока не подключаемся)
    const ws = new WebSocketClient('/ws/client', { autoConnect: false });

    // 2. Пробрасываем его в менеджер
    itemsManager.set_ws_client(ws);

    // 3. Настраиваем подписки на события
    //    — диспетчер входящих сообщений
    ws.callback_add('message', (msg) => {
        const itemId   = msg?.item_id;
        const channel  = msg?.channel;
        const action   = msg?.action;
        const text     = msg?.text;

        if (channel === "history_log") {
            itemsManager.history_append(itemId, action, text);
        } else if (channel === "item_control") {
            if (action === "create_item") {
                itemsManager.item_create(itemId);
            } else if (action === "delete_item") {
                itemsManager.item_del(itemId);
            } else if (action === "clear_history") {
                itemsManager.history_clear(itemId);
            }
        } else if (channel === "system") {
            // системные сообщения (пока пусто)
        }
    });

    //    — при успешном подключении перезагружаем UI
    ws.callback_add('open', async () => {
        await itemsManager.reloadUI();
    });

    //    — для отладки можно подписаться на остальные события
    ws.callback_add('close', () => console.log('WebSocket closed'));
    ws.callback_add('error', (e) => console.error('WebSocket error', e));
    ws.callback_add('reconnecting', ({ delay }) => console.log(`Reconnecting in ${delay}ms`));

    // 4. Инициализируем UI (кнопка «создать» и т.п.) и сразу загружаем данные
    await itemsManager.initUI();        // только слушатели, без данных
    await itemsManager.reloadUI();      // первая загрузка через REST

    // 5. Запускаем WebSocket (теперь onopen снова вызовет reloadUI, но это безопасно)
    ws.connect();
};


// =====================================================================================================================
