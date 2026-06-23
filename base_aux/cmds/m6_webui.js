// --------------------------------------------------------------
// WebSocket
// --------------------------------------------------------------
let ws_client = null;

function ws_client__connect() {
    console.log("[WsClient]🟡try connect");

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    ws_client = new WebSocket(`${protocol}//${window.location.host}/ws/client`);

    // ---------------------------------------------------
    ws_client.onmessage = (e) => {
        const msg = JSON.parse(e.data);

        const msg__itemid = msg?.item_id;
        const msg__channel = msg?.channel;

        const msg__action = msg?.action;
        const msg__text = msg?.text;

        if (msg__channel === "history_log") {
            const ui = itemsManager.items_map.get(msg__itemid);
            if (ui) {
                let style = '';
                if (msg__action === 'stdout') style = 'msg_stdout__cls';
                else if (msg__action === 'stderr') style = 'msg_stderr__cls';
                else if (msg__action === 'stdin') style = 'msg_stdin__cls';
                else style = 'msg_debug__cls';

                ui.addHistoryLine(style, msg__text);
            }

        } else if (msg__channel === "item_control") {

            if (msg__action === "create_item") {
                if (!itemsManager.items_map.has(msg__itemid)) {
                    itemsManager.addItemElement(msg__itemid);
                }

            } else if (msg__action === "delete_item") {
                const ui = itemsManager.items_map.get(msg__itemid);
                if (ui) {
                    ui.destroy();
                    itemsManager.items_map.delete(msg__itemid);
                }

            } else if (msg__action === "clear_history") {
                const ui = itemsManager.items_map.get(msg__itemid);
                if (ui) {
                    ui.element_OutputBox.innerHTML = '';
                }
            }

        } else if (msg__channel === "system") {
            console.log(msg__text);
        }
    };

    // ---------------------------------------------------
    ws_client.onopen = async () => {
        console.log("[WsClient]🟢connected");
        // Полная перезагрузка UI с нуля
        await itemsManager.reloadUI();
    };

    ws_client.onclose = () => {
        console.log("[WsClient]🔴closed, reconnecting in 3s...");
        setTimeout(ws_client__connect, 3000);
    };
}

// --------------------------------------------------------------
// Глобальный менеджер объектов
// --------------------------------------------------------------
const itemsManager = {
    items_map: new Map(),

    // Инициализация UI при первой загрузке страницы
    async initUI() {
        document.getElementById('btn_add_item__id').addEventListener('click', () => this.createNewItem());
        await this.reloadUI();
    },

    // Полная очистка и повторное построение UI на основе данных сервера
    async reloadUI() {
        // Удаляем все существующие элементы
        for (const [id, ui] of this.items_map) {
            ui.destroy();
        }
        this.items_map.clear();

        // Загружаем актуальный список с сервера
        const serverIds = await this.get_IdsServer();
        for (const idn of serverIds) {
            this.addItemElement(idn);
        }
    },

    addItemElement(itemId) {
        if (this.items_map.has(itemId)) return;
        const itemUI = new ItemUI(itemId);
        this.items_map.set(itemId, itemUI);
        itemUI.init();
    },

    // ---------------------------------------------------
    async get_IdsServer() {
        try {
            const resp = await fetch('/item/list');
            const data = await resp.json();
            return data.items || [];
        } catch {
            return [];
        }
    },

    // ---------------------------------------------------
    async createNewItem() {
        if (ws_client?.readyState !== WebSocket.OPEN) return;

        ws_client.send(JSON.stringify({
            channel: "item_control",
            action: "create_item",
        }));
    },

    async delItem(itemId) {
        if (ws_client?.readyState !== WebSocket.OPEN) return;

        ws_client.send(JSON.stringify({
            item_id: itemId,
            channel: "item_control",
            action: "delete_item",
        }));
    }
};

// --------------------------------------------------------------
// объект
// --------------------------------------------------------------
class ItemUI {
    constructor(itemId) {
        this.itemId = itemId;
        this.element_ItemBox = null;
        this.element_OutputBox = null;
        this.element_InputBox = null;
    }

    init() {
        this.render();
        this.loadHistory();
    }

    render() {
        const div_itembox = document.createElement('div');
        div_itembox.className = 'item__cls';

        // Header
        const header = document.createElement('header');
        const header_div1 = document.createElement('div');
        const header_div2 = document.createElement('div');
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
        btnClear.onclick = () => this.sendDelHistory();

        const btnReconnect = document.createElement('button');
        btnReconnect.setAttribute('data-btn_outline', "blue");
        btnReconnect.textContent = 'Reconnect';
        btnReconnect.title = 'Reconnect';
        btnReconnect.onclick = () => this.sendReconnect();

        const btnClose = document.createElement('button');
        btnClose.setAttribute('data-btn_outline', "red");
        btnClose.textContent = 'X';
        btnClose.title = 'Close';
        btnClose.onclick = () => itemsManager.delItem(this.itemId);

        header_div2.appendChild(btnClear);
        header_div2.appendChild(btnReconnect);
        header_div2.appendChild(btnClose);

        // Output area
        const output = document.createElement('main');
        output.setAttribute('data-scrollbar__dark', '');
        this.element_OutputBox = output;

        // Input area
        const footer = document.createElement('footer');
        const input = document.createElement('input');
        input.type = 'text';
        input.placeholder = 'Введите команду и нажмите Enter';
        this.element_InputBox = input;
        footer.appendChild(input);

        div_itembox.appendChild(header);
        div_itembox.appendChild(output);
        div_itembox.appendChild(footer);
        this.element_ItemBox = div_itembox;
        document.getElementById('items_container__id').appendChild(div_itembox);

        input.addEventListener('change', () => this.sendInput());
    }

    // ---------------------------------------------------
    sendInput() {
        if (ws_client?.readyState !== WebSocket.OPEN) return;

        const io_line = this.element_InputBox.value.trim();
        if (io_line) {
            ws_client.send(JSON.stringify({
                item_id: this.itemId,
                channel: "history_log",
                action: "stdin",  // FIXME: or just stdin/msg_stdin__cls
                text: io_line,
            }));
            this.element_InputBox.value = '';
        }
    }

    sendReconnect() {
        if (ws_client?.readyState !== WebSocket.OPEN) return;

        ws_client.send(JSON.stringify({
            item_id: this.itemId,
            channel: "item_control",
            action: "reconnect_item",
        }));
    }

    sendDelHistory() {
        if (ws_client?.readyState !== WebSocket.OPEN) return;

        ws_client.send(JSON.stringify({
            item_id: this.itemId,
            channel: "item_control",
            action: "clear_history",
        }));
    }

    // ---------------------------------------------------
    async loadHistory() {
        this.element_OutputBox.innerHTML = '';
        try {
            const resp = await fetch(`/item/history/get/${this.itemId}`);
            const history = await resp.json();
            history.forEach(log_line => {
                if (log_line.input) this.addHistoryLine('msg_stdin__cls', log_line.input);
                log_line.stdout?.forEach(l => this.addHistoryLine('msg_stdout__cls', l));
                log_line.stderr?.forEach(l => this.addHistoryLine('msg_stderr__cls', l));
                log_line.debug?.forEach(l => this.addHistoryLine('msg_debug__cls', l));
            });
        } catch (err) {
            this.addHistoryLine('msg_stderr__cls', `Ошибка loadHistory: ${err.message}`);
        }
    }

    addHistoryLine(style_cls, text) {
        const line = document.createElement('div');
        line.className = style_cls;
        line.textContent = text;
        this.element_OutputBox.appendChild(line);
        this.element_OutputBox.scrollTop = this.element_OutputBox.scrollHeight;
    }

    // ---------------------------------------------------
    destroy() {
        this.element_ItemBox?.remove();
    }
}

// --------------------------------------------------------------
// Запуск
// --------------------------------------------------------------
window.onload = async () => {
    await itemsManager.initUI();    // первичная загрузка, через REST, регистрирует кнопку и запускает reloadUI
    ws_client__connect();           // запуск WebSocket (onopen сам вызовет reloadUI)
};