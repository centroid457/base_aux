// =============================================================================
/**
 * Базовый UI одного элемента.
 */
class BaseItemUI {
    elements = {
        final: null,
    };
    css_map = {};

    /**
     * @param {string}             itemId
     * @param {WebSocketClient}    ws         – экземпляр WebSocket-клиента
     * @param {Object}             cssClasses – словарь CSS-классов
     */
    constructor({
        itemId,
        ws,
        event_manager,

        selectors = {},
        urls = {},
        config = {},
    } = {}) {
        this.itemId = itemId;
        this.ws = ws;
        this.event_manager = event_manager;

        this.selectors = selectors;
        this.urls = urls;
        this.config = config;

        /** @type {{ final: HTMLElement|null, output: HTMLElement|null, input: HTMLInputElement|null }} */
        if (!("final" in this.elements)) this.elements["final"] = null;
    }

    async init() {
        this.buildDOM();    // WARN: DONT PLACE IN CONSTRUCTOR!!!!
        this.init_post();
    }

    // -----------------------------------------------------------------------------------------------------------------
    destroy() {
        this.elements.final?.remove();
    }

    // -----------------------------------------------------------------------------------------------------------------
    _send(channel, action, extra = {}) {
        //return this.ws.send_json({ item_id: this.itemId, channel, action, ...extra });
        return fetchJsonPost( this.urls.url_rpc, { item_id: this.itemId, channel, action, ...extra });
    }

    // NESTING =========================================================================================================
    async init_post() {
    }

    buildDOM() {
        // as example
        this.elements.final = document.createElement('div');
        //        this.elements.final.className = this.css_map.itemBox;

        // Header
        const header = document.createElement('header');
        const idSpan = document.createElement('span');
        //        idSpan.className = this.css_map.itemId;
        idSpan.textContent = this.itemId;
        header.appendChild(idSpan);
    }

    // SEND ------------------------------------------------------------------------------------------------------------
    sendExample()       { this._send('channel_example', 'action_example'); }

    // METHS -----------------------------------------------------------------------------------------------------------
    //
}


// ---------------------------------------------------------------------------------------------------------------------
class ItemUiTerminal extends BaseItemUI {
    elements = {
        final: null,

        output: null,
        input: null,
    };
    css_map = {
        itemBox: 'item__cls',
        itemId:  'span_item_id__cls',

        stdout:  'msg_stdout__cls',
        stderr:  'msg_stderr__cls',
        stdin:   'msg_stdin__cls',
        debug:   'msg_debug__cls',
    };

    // -----------------------------------------------------------------------------------------------------------------
    async init_post() {
        await this.history_load();
    }

    // -----------------------------------------------------------------------------------------------------------------
    buildDOM() {
        this.elements.final = document.createElement('div');
        this.elements.final.className = this.css_map.itemBox;

        // Header
        const header = document.createElement('header');
        const idSpan = document.createElement('span');
        idSpan.className = this.css_map.itemId;
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

    element__create_btn({text, title, onclick, attrs = {}} = {}) {
        const btn = document.createElement('button');
        btn.textContent = text;
        btn.title = title;
        for (const [name, val] of Object.entries(attrs)) {
            btn.setAttribute(name, val);
        }
        btn.onclick = onclick;
        return btn;
    }

    _create_buttons() {
        const wrap = document.createElement('div');

        const btns_schema = [
            {
                text: 'clear',
                title: 'Clear History',
                onclick: () => this.sendHistoryClear(), attrs: {'data-btn_outline': 'blue'}
            },
            {
                text: 'Reconnect',
                title: 'Reconnect',
                onclick: () => this.sendReconnect(), attrs: {'data-btn_outline': 'blue'}
            },
            {
                text: 'X',
                title: 'Close',
                onclick: () => this.sendDelete(), attrs: {'data-btn_outline': 'red'}
            },
        ]

        btns_schema.forEach((schema) => {
            let btn = this.element__create_btn(schema);
            wrap.appendChild(btn);
        });
        return wrap;
    }

    // -----------------------------------------------------------------------------------------------------------------
    // SET -----
    sendInput(text) {
        if (!text) return;
        const sent = this._send('item_control', 'send_stdin', { text });
        if (sent) this.elements.input.value = '';
    }
    sendReconnect()    { this._send('item_control', 'reconnect_item'); }
    sendDelete()       { this._send('item_control', 'delete_item'); }

    sendHistoryClear() { this._send('item_control', 'history_clear'); }

    // GET -----
    async sendHistoryGet() {
        const resp = await this._send('item_control', 'history_get');
        return resp?.data;
    }

    // USER METH -----------------------------------------------------------------------------------------------------------------
    history_clear() {
        if (this.elements.output) this.elements.output.innerHTML = '';
    }

    async history_load() {
        this.history_clear();
        try {
            const history = await this.sendHistoryGet();
            history.forEach(line => {
                if (line.input)           this.history_add_line('stdin', line.input);
                line.stdout?.forEach(l => this.history_add_line('stdout', l));
                line.stderr?.forEach(l => this.history_add_line('stderr', l));
                line.debug?.forEach(l  => this.history_add_line('debug', l));
            });
        } catch (err) {
            this.history_add_line('stderr', `Ошибка истории: ${err.message}`);
        }
    }

    history_add_line(style, text) {
        const div = document.createElement('div');
        div.className = this.css_map[style] || this.css_map.debug;
        div.textContent = text;
        this.elements.output.appendChild(div);
        this.elements.output.scrollTop = this.elements.output.scrollHeight;
    }
}

// =============================================================================
// Менеджер объектов
// =============================================================================
class BaseItemManager {
    /**
     * @param {WebSocketClient} config.ws                – экземпляр WebSocketClient
     * @param {string}          config.containerSelector – CSS-селектор контейнера для элементов
     * @param {Object}          [config.cssClasses]      – переопределение CSS-классов
     * @param {typeof BaseItemUI} [config.itemCls]      – класс UI элемента
     */
    constructor({
        ws,
        event_manager,
        itemCls = ItemUiTerminal,

        selectors = {},
        urls = {},
        config = {},
    } = {}) {
        // --------------
        this.ws = ws;
        this.event_manager = event_manager;
        this.itemCls = itemCls;

        this.selectors = selectors;
        this.urls = urls;
        this.config = config;

        // --------------
        this.elements = {
            container: document.querySelector(this.selectors.containerSelector),
        };
        if (!this.elements.container) throw new Error(`Контейнер "${this.selectors.containerSelector}" не найден`);

        // --------------
        this.items = new Map();   // itemId → BaseItemUI

        this.callbacks_setup();
    }

    // -----------------------------------------------------------------------------------------------------------------
    init() {}
    callbacks_setup() {}

    // -----------------------------------------------------------------------------------------------------------------
    /** Полная перезагрузка списка с сервера */
    async items_reload() {
        this.items_delete()

        let serverIds = [];
        try {
            const data = await this.sendItemsListGet();
            serverIds = data || [];
        } catch { /* оставляем пустым */ }

        for (const id of serverIds) await this.item_create(id);
    }

    items_delete() {
        for (const id of this.items.keys()) this.item_delete(id);
    }

    // -----------------------------------------------------------------------------------------------------------------
    async item_create(itemId) {
        if (this.items.has(itemId)) return;

        const ui = new this.itemCls({
            itemId,
            ws: this.ws,
            event_manager: this.event_manager,

            urls: this.urls,
            selectors: this.selectors,
            config: this.config,
        });
        await ui.init()
        this.items.set(itemId, ui);
        this.elements.container.appendChild(ui.elements.final);
    }

    item_delete(itemId) {
        const ui = this.items.get(itemId);
        if (ui) {
            ui.destroy();
            this.items.delete(itemId);
        }
    }
}


// =====================================================================================================================
class ItemManager extends BaseItemManager {

    init() {
        const btn = document.querySelector(this.selectors?.selectorBtnAddNewItem);
        if (btn) {
            btn.addEventListener('click', () => {
                fetchJsonPost(this.urls.url_rpc, { channel: 'item_control', action: 'create_item' });
            });
        }
    }

    callbacks_setup() {
        this.event_manager.schema__update_values({
            "ws.onopen": async () => { await this.items_reload() },
            "ws.onclose": null,
            "ws.onmessage": (msg) => {
                if (!msg) return;

                const { item_id, channel, action, text } = msg;
                if (channel === 'history_log') {
                    this.items.get(item_id)?.history_add_line(action, text);
                } else if (channel === 'item_control') {
                    if (action === 'create_item')   this.item_create(item_id);
                    else if (action === 'delete_item') this.item_delete(item_id);
                    else if (action === 'history_clear') this.items.get(item_id)?.history_clear();
                }
            },
            "ws.onerror": null,
            "ws.onreconnecting": null,
        });
    }

    async sendItemsListGet() {
        const resp = await fetchJsonPost(this.urls.url_rpc, { channel: 'item_control', action: 'items_list_get' });
        return resp?.data;
    }

}


// =====================================================================================================================
window.onload = async () => {
    const event_manager = new EventManager();

    const ws = new WebSocketClient({
        urlOrPath: '/ws__broadcast',
        autoConnect: false,
        event_manager: event_manager,
    });

    const items_manager = new ItemManager({
        event_manager: event_manager,
        ws,

        selectors: {
            containerSelector: '#items_container__id',
            selectorBtnAddNewItem: '#btn_add_item__id'
        },
        urls: {
            url_rpc:  "/post__rpc",
        },
        config: {},
    });
    items_manager.init();

    // 5. Запускаем WebSocket (при подключении автоматически загрузит элементы)
    ws.connect();
};

// =====================================================================================================================
