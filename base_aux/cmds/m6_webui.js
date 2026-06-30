// --------------------------------------------------------------
// WebSocket клиент (транспорт + диспетчеризация)
// --------------------------------------------------------------
const ws_client = {
    socket: null,
    callback_onmessage: null,   // будет назначена снаружи
    callback_onopen: null,      // будет назначена снаружи

    // Удобная отправка JSON
    // Возвращает true, если сообщение реально ушло в сокет
    send_json(data) {
        if (this.socket?.readyState !== WebSocket.OPEN) {
            console.warn('[WsClient] socket not open, message dropped', data);
            return false;
        }
        this.socket.send(JSON.stringify(data));
        return true;
    },

    // Запуск WebSocket соединения
    connect() {
        if (this.socket) {
            this.socket.close();
        }

        console.log("[WsClient] ⌛ try connect");
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        this.socket = new WebSocket(`${protocol}//${window.location.host}/ws/client`);

        // ---------- обработка входящих сообщений ----------
        this.socket.onmessage = (event) => {
            const msg_json = JSON.parse(event.data);
            console.log("[WsClient] 📩", JSON.stringify(msg_json));
            // передаём управление зарегистрированному диспетчеру
            if (typeof this.callback_onmessage === 'function') {
                this.callback_onmessage(msg_json);
            }
        };

        this.socket.onopen = async () => {
            console.log("[WsClient] 🟢 connected");
            // Полная перезагрузка UI с нуля
            await itemsManager.reloadUI();
        };

        this.socket.onclose = () => {
            console.log("[WsClient] 🔴 closed, reconnecting in 3s...");
            setTimeout(() => this.connect(), 3000);
        };
    }
};

// --------------------------------------------------------------
// Глобальный менеджер объектов (только бизнес-логика)
// --------------------------------------------------------------
const itemsManager = {
    items_map: new Map(),

    // Инициализация UI при загрузке страницы
    async initUI() {
        document.getElementById('btn_add_item__id').addEventListener('click', () => this.send__item_create());
        await this.reloadUI();
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

    // ---------- отправка команд (используем ws_client.send_json) ----------
    send__item_create() {
        ws_client.send_json({
            channel: "item_control",
            action: "create_item",
        });
    },

    send__item_del(itemId) {
        ws_client.send_json({
            item_id: itemId,
            channel: "item_control",
            action: "delete_item",
        });
    },

    item_create(itemId) {
        if (this.items_map.has(itemId)) return;
        const itemUI = new ItemUI(itemId);
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

// --------------------------------------------------------------
// Диспетчер входящих WS-сообщений (назначается в ws_client)
// --------------------------------------------------------------
ws_client.callback_onmessage = (msg) => {
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
};

// --------------------------------------------------------------
// UI отдельного объекта
// --------------------------------------------------------------
class ItemUI {
    constructor(itemId) {
        this.itemId = itemId;
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

    // ---------- отправка команд через ws_client ----------
    send__input() {
        const line = this.element_InputBox.value.trim();
        if (!line) return;

        const sent = ws_client.send_json({
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
        ws_client.send_json({
            item_id: this.itemId,
            channel: "item_control",
            action: "reconnect_item",
        });
    }

    send__history_clear() {
        ws_client.send_json({
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

// --------------------------------------------------------------
// Запуск
// --------------------------------------------------------------
window.onload = async () => {
    await itemsManager.initUI();   // первичная загрузка через REST + регистрация кнопки
    ws_client.connect();           // WebSocket (onopen сам вызовет reloadUI)
};