// =============================================================================
// item-manager.js — переиспользуемый менеджер элементов
// =============================================================================

/**
 * Базовый UI одного элемента.
 */
class BaseItemUI {
    /**
     * @param {string}             itemId
     * @param {WebSocketClient}    ws         – экземпляр WebSocket-клиента
     * @param {Object}             cssClasses – словарь CSS-классов
     */
    constructor(itemId, ws, cssClasses) {
        this.itemId = itemId;
        this.ws = ws;
        this.css = cssClasses;

        /** @type {{ final: HTMLElement|null, output: HTMLElement|null, input: HTMLInputElement|null }} */
        this.elements = { final: null, output: null, input: null };
    }

    // -----------------------------------------------------------------------------------------------------------------
    async init() {
        this.buildDOM();
        await this.history_load();
    }

    // -----------------------------------------------------------------------------------------------------------------
    buildDOM() {
        this.elements.final = document.createElement('div');
        this.elements.final.className = this.css.itemBox;

        // Header
        const header = document.createElement('header');
        const idSpan = document.createElement('span');
        idSpan.className = this.css.itemId;
        idSpan.textContent = this.itemId;
        header.appendChild(idSpan);
        header.appendChild(this._create_buttons());

        // Output area
        const output = document.createElement('main');
        output.setAttribute('data-scrollbar__dark', '');
        this.elements.output = output;

        // Input area
        const footer = document.createElement('footer');
        const input = document.createElement('input');
        input.type = 'text';
        input.placeholder = 'Введите команду и нажмите Enter';
        this.elements.input = input;
        footer.appendChild(input);

        this.elements.final.appendChild(header);
        this.elements.final.appendChild(output);
        this.elements.final.appendChild(footer);

        input.addEventListener('change', () => this._callback_input());
    }

    _callback_input() {
        this.sendInput(this.elements.input.value.trim());
    }

    _create_buttons() {
        const wrap = document.createElement('div');
        const addBtn = (text, title, attr, handler) => {
            const btn = document.createElement('button');
            btn.textContent = text;
            btn.title = title;
            btn.setAttribute('data-btn_outline', attr);
            btn.onclick = handler;
            wrap.appendChild(btn);
        };
        addBtn('clear', 'Clear History', 'blue', () => this.sendClearHistory());
        addBtn('Reconnect', 'Reconnect', 'blue', () => this.sendReconnect());
        addBtn('X', 'Close', 'red', () => this.sendDelete());
        return wrap;
    }

    // -----------------------------------------------------------------------------------------------------------------
    _send(channel, action, extra = {}) {
        return this.ws.send_json({ item_id: this.itemId, channel, action, ...extra });
    }

    sendInput(text) {
        if (!text) return;
        const sent = this._send('history_log', 'stdin', { text });
        if (sent) this.elements.input.value = '';
    }
    sendReconnect()    { this._send('item_control', 'reconnect_item'); }
    sendClearHistory() { this._send('item_control', 'clear_history'); }
    sendDelete()       { this._send('item_control', 'delete_item'); }

    // -----------------------------------------------------------------------------------------------------------------
    history_clear() {
        if (this.elements.output) this.elements.output.innerHTML = '';
    }

    async history_load() {
        this.history_clear();
        try {
            const history = await fetchJSON(`/item/history/get/${this.itemId}`);
            history.forEach(line => {
                if (line.input)   this.history_add_line('stdin',  line.input);
                line.stdout?.forEach(l => this.history_add_line('stdout', l));
                line.stderr?.forEach(l => this.history_add_line('stderr', l));
                line.debug?.forEach(l  => this.history_add_line('debug', l));
            });
        } catch (err) {
            this.history_add_line('stderr', `Ошибка истории: ${err.message}`);
        }
    }

    history_add_line(style, text) {
        const clsMap = {
            stdout: this.css.stdout,
            stderr: this.css.stderr,
            stdin:  this.css.stdin,
            debug:  this.css.debug,
        };
        const cls = clsMap[style] || this.css.debug;
        const div = document.createElement('div');
        div.className = cls;
        div.textContent = text;
        this.elements.output.appendChild(div);
        this.elements.output.scrollTop = this.elements.output.scrollHeight;
    }

    // -------- Удаление --------
    destroy() {
        this.elements.final?.remove();
    }
}

// =============================================================================
// Менеджер объектов
// =============================================================================
class ItemManager {
    /**
     * @param {Object} config
     * @param {WebSocketClient} config.ws                – экземпляр WebSocketClient
     * @param {string}          config.containerSelector – CSS-селектор контейнера для элементов
     * @param {Object}          [config.cssClasses]       – переопределение CSS-классов
     * @param {typeof BaseItemUI} [config.ItemUIClass]   – класс UI элемента
     */
    constructor({ ws, containerSelector, cssClasses = {}, ItemUIClass = BaseItemUI }) {
        this.ws = ws;
        this.container = document.querySelector(containerSelector);
        if (!this.container) throw new Error(`Контейнер "${containerSelector}" не найден`);

        this.css = Object.assign({
            itemBox: 'item__cls',
            itemId:  'span_item_id__cls',
            stdout:  'msg_stdout__cls',
            stderr:  'msg_stderr__cls',
            stdin:   'msg_stdin__cls',
            debug:   'msg_debug__cls',
        }, cssClasses);

        this.ItemUIClass = ItemUIClass;
        this.items = new Map();   // itemId → BaseItemUI

        this._setupListeners();
    }

    _setupListeners() {
        this.ws.callback_add('message', (msg) => {
            if (!msg) return;
            const { item_id, channel, action, text } = msg;
            if (channel === 'history_log') {
                this.items.get(item_id)?.history_add_line(action, text);
            } else if (channel === 'item_control') {
                if (action === 'create_item')   this.itemCreate(item_id);
                else if (action === 'delete_item') this.itemDelete(item_id);
                else if (action === 'clear_history') this.items.get(item_id)?.history_clear();
            }
        });

        this.ws.callback_add('open', async () => {
            await this.reloadAll();
        });
    }

    /** Полная перезагрузка списка с сервера */
    async reloadAll() {
        for (const id of this.items.keys()) this.itemDelete(id);
        let serverIds = [];
        try {
            const data = await fetchJSON('/item/list');
            serverIds = data?.items || [];
        } catch { /* оставляем пустым */ }
        for (const id of serverIds) await this.itemCreate(id);
    }

    /** Создать элемент (если ещё нет) */
    async itemCreate(itemId) {
        if (this.items.has(itemId)) return;
        const ui = new this.ItemUIClass(itemId, this.ws, this.css);
        this.items.set(itemId, ui);
        await ui.init();
        this.container.appendChild(ui.elements.final);
    }

    /** Удалить элемент */
    itemDelete(itemId) {
        const ui = this.items.get(itemId);
        if (ui) {
            ui.destroy();
            this.items.delete(itemId);
        }
    }

    /**
     * Инициализация глобальной кнопки «создать» (может вызываться извне)
     * @param {string} addButtonSelector – CSS-селектор кнопки
     */
    initGlobalUI(addButtonSelector) {
        const btn = document.querySelector(addButtonSelector);
        if (btn) {
            btn.addEventListener('click', () => {
                this.ws.send_json({ channel: 'item_control', action: 'create_item' });
            });
        }
    }
}


// =====================================================================================================================
window.onload = async () => {

    // 1. WebSocket-клиент (ваш универсальный класс, код приведён ниже)
    const ws = new WebSocketClient('/ws/client', { autoConnect: false });

    // 3. Создаём менеджер с конфигурацией
    const manager = new ItemManager({
        ws,
        containerSelector: '#items_container__id',   // куда добавлять элементы
        // cssClasses – если нужно переопределить классы
        // ItemUIClass – если нужен кастомный рендеринг
    });

    // 4. Инициализируем кнопку добавления
    manager.initGlobalUI('#btn_add_item__id');

    // 5. Запускаем WebSocket (при подключении автоматически загрузит элементы)
    ws.connect();
};

// =====================================================================================================================
