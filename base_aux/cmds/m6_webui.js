// =============================================================================
/**
 * Базовый UI одного элемента.
 */
class BaseItemUI extends ConsoleLogger {
    elements = {
        final: null,
    };
    css_map = {};

    /**
     * @param {string}             itemId
     * @param {WsClient}    ws         – экземпляр WebSocket-клиента
     * @param {Object}             cssClasses – словарь CSS-классов
     */
    constructor({
        itemId,
        ws,
        event_manager,
        rpc,
        config = {},
    } = {}) {
        super();
        this.itemId = itemId;
        this.ws = ws;
        this.event_manager = event_manager;
        this.rpc = rpc;
        this.config = config;

        /** @type {{ final: HTMLElement|null, main: HTMLElement|null, input: HTMLInputElement|null }} */
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

    // METHS -----------------------------------------------------------------------------------------------------------
    //
}


// ---------------------------------------------------------------------------------------------------------------------
class ItemUiTerminal extends BaseItemUI {
    elements = {
        final: null,

        main: null,
        input: null,
        baudrateSelect: null,
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
        await this.config_load();
    }

    // -----------------------------------------------------------------------------------------------------------------
    buildDOM() {
        this.elements.final = document.createElement('div');
        this.elements.final.className = this.css_map.itemBox;

        // =============================================
        // 1=Header
        const header = document.createElement('header');

        const idSpan = document.createElement('span');
        idSpan.className = this.css_map.itemId;
        idSpan.textContent = this.itemId;

        // === ДОБАВЛЕНО: выпадающий список baudrate ===
        const baudSelect = document.createElement('select');
        baudSelect.style.width = '100';
        const standardBaudrates = [undefined, 9600, 19200, 38400, 57600, 115200];
        standardBaudrates.forEach(rate => {
            const opt = document.createElement('option');
            opt.value = rate;
            opt.textContent = rate;
            baudSelect.appendChild(opt);
        });
        baudSelect.value = undefined;
        this._currentBaudrate = undefined;

        baudSelect.addEventListener('change', () => this._onBaudrateChange());

        this.elements.baudrateSelect = baudSelect;

        header.appendChild(idSpan);
        header.appendChild(baudSelect);
        header.appendChild(this._create_buttons());

        // =============================================
        // 2=Output area
        const main = document.createElement('main');

        main.setAttribute('data-scrollbar__dark', '');
        this.elements.main = main;

        // 3=Input area
        const footer = document.createElement('footer');

        const input = document.createElement('input');
        input.type = 'text';
        input.placeholder = 'Введите команду и нажмите Enter';
        this.elements.input = input;
        input.addEventListener('change', () => this._callback_input());
        footer.appendChild(input);

        // =============================================
        // 100=FINAL
        this.elements.final.appendChild(header);
        this.elements.final.appendChild(main);
        this.elements.final.appendChild(footer);
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
    // SEND -----
    async sendInput(text) {
        if (!text) return;
        const sent = await this.rpc.sendStdin(this.itemId, text);
        if (sent) this.elements.input.value = '';
    }
    async sendReconnect()    { await this.rpc.reconnectItem(this.itemId) }
    async sendDelete()       { await this.rpc.deleteItem(this.itemId) }
    async sendHistoryClear() { await this.rpc.clearHistory(this.itemId) }
    async sendHistoryGet()   { return await this.rpc.getHistory(this.itemId) }

    // USER METH -----------------------------------------------------------------------------------------------------------------
    history_clear() {
        if (this.elements.main) this.elements.main.innerHTML = '';
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
        this.elements.main.appendChild(div);
        this.elements.main.scrollTop = this.elements.main.scrollHeight;
    }

    async config_load() {
        const config = await this.rpc.getConfig(this.itemId);
        this._currentBaudrate = config?.baudrate;
        if (config?.baudrate) this.elements.baudrateSelect.value = config?.baudrate;
    }

    // === ДОБАВЛЕНО: обработчик изменения baudrate ===
    async _onBaudrateChange() {
        const newValue = parseInt(this.elements.baudrateSelect.value, 10);
        this.console_log("baudrateSelect newValue=", newValue);

        const oldValue = this._currentBaudrate;

        try {
            const success = await this.rpc.changeConfig(this.itemId, { baudrate: newValue });
            this.console_log(success);

            if (!success) {
                throw new Error('Сервер вернул ошибку');
            }
            this._currentBaudrate = newValue;
        } catch (e) {
            this.console_error(`Ошибка изменения baudrate для ${this.itemId}:`, e);
            this._currentBaudrate = oldValue;
            this.elements.baudrateSelect.value = oldValue;
        }
    }

}

// =============================================================================
// Менеджер объектов
// =============================================================================
class BaseItemManager {
    SCHEMA__CALLBACKS_WS = {};

    /**
     * @param {WsClient} config.ws                – экземпляр WsClient
     * @param {string}          config.selector_container – CSS-селектор контейнера для элементов
     * @param {Object}          [config.cssClasses]      – переопределение CSS-классов
     * @param {typeof BaseItemUI} [config.itemCls]      – класс UI элемента
     */
    constructor({
        ws,
        event_manager,
        rpc,
        itemCls = ItemUiTerminal,
        config = {},
    } = {}) {
        // --------------
        this.ws = ws;
        this.event_manager = event_manager;
        this.itemCls = itemCls;
        this.rpc = rpc;
        this.config = config;

        // --------------
        this.elements = {
            container: document.querySelector(this.config.selector_container),
        };
        if (!this.elements.container) throw new Error(`Контейнер "${this.config.selector_container}" не найден`);

        // --------------
        this.items = new Map();   // itemId → BaseItemUI
    }

    // -----------------------------------------------------------------------------------------------------------------
    init() {
        this.callbacks_setup();
        this.init_post();
    }

    callbacks_setup() {
        this.event_manager.schema__update_values(this.SCHEMA__CALLBACKS_WS);
    }

    // -----------------------------------------------------------------------------------------------------------------
    init_post() {}

    // -----------------------------------------------------------------------------------------------------------------
    /** Полная перезагрузка списка с сервера */
    async items_reload() {
        this.items_delete()

        let serverIds = [];
        try {
            const data = await this.rpc.getItemsList();
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
            rpc: this.rpc,
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
    SCHEMA__CALLBACKS_WS = {
        ws_onopen: async () => { await this.items_reload() },
        ws_onclose: null,
        ws_onmessage: (msg) => {
            if (!msg) return;

            const { item_id, channel, action, load } = msg;
            if (channel === 'history_log') {
                this.items.get(item_id)?.history_add_line(action, load);
            } else if (channel === 'item_control') {
                if (action === 'create_item')   this.item_create(item_id);
                else if (action === 'delete_item') this.item_delete(item_id);
                else if (action === 'history_clear') this.items.get(item_id)?.history_clear();
            }
        },
        ws_onerror: null,
        ws_onreconnect: null,
    }

    init_post() {
        const btn = document.querySelector(this.config?.selector_BtnAddNewItem);
        if (btn) {
            btn.addEventListener('click', () => {
                this.rpc.createItem();
            });
        }
    }
}


// =====================================================================================================================
window.onload = async () => {
    const event_manager = new EventManager();
    const rpc = new RpcClient('/channel__rpc');
    const ws = new WsClient({
        url: '/channel__ws_broadcast',
        autoConnect: false,
        event_manager,
    });

    const items_manager = new ItemManager({
        event_manager,
        ws,
        rpc,
        config: {
            selector_container: '#items_container__id',
            selector_BtnAddNewItem: '#btn_add_item__id'
        },
    });
    items_manager.init();

    // 5. Запускаем WebSocket (при подключении автоматически загрузит элементы)
    ws.connect();
};


// =====================================================================================================================
class RpcClient {
    /**
     * @param {string} url – URL RPC-эндпоинта (например "/channel__rpc")
     * @param {Function} [requestFn] – функция для запроса (по умолчанию fetchJsonPost)
     */
    constructor(url) {
        this.url = url;
    }

    __RESPONSE_SCHEMA = {    // just for info!
        ok: 0,
        load: {},
    }

    // -----------------------------------------------------------------------------------------------------------------
    // LEVEL-1=LOWER
    async _call({channel, action, item_id, load={}} = {}) {
        const resp = await fetchJsonPost(
            this.url,
            {
                channel,
                action,
                item_id,
                load,
            });
        return resp;   // возвращаем полный ответ, чтобы клиент мог извлечь data
    }

    // -----------------------------------------------------------------------------------------------------------------
    // LEVEL-2=UPPER
    // 1=UDP=no need ANY answer result ------
    async createItem() {
        const response = await this._call(
            {
                channel: 'item_control',
                action: 'create_item',
            }
        );
        return response?.ok;
    }

    async deleteItem(item_id) {
        const response = await this._call(
            {
                channel: 'item_control',
                action: 'delete_item',
                item_id,
            }
        );
        return response?.ok;
    }

    async reconnectItem(item_id) {
        const response = await this._call(
            {
                channel: 'item_control',
                action: 'reconnect_item',
                item_id,
            }
        );
        return response?.ok;
    }

    async clearHistory(item_id) {
        const response = await this._call(
            {
                channel: 'item_control',
                action: 'history_clear',
                item_id,
            }
        );
        return response?.ok;
    }

    // 2=NEED ANSWER-1=at least status ---------------------
    async sendStdin(item_id, load) {
        const response = await this._call(
            {
                channel: 'item_control',
                action: 'send_stdin',
                item_id,
                load,
            }
        );
        return response?.ok;
    }

    async changeConfig(item_id, load={}) {
        const response = await this._call(
            {
                channel: 'item_control',
                action: 'config_change',
                item_id,
                load,
            }
        );
        return response?.ok;
    }

    // 3=NEED ANSWER-2=data ---------------------------------
    async getConfig(item_id) {
        const response = await this._call(
            {
                channel: 'item_control',
                action: 'config_get',
                item_id,
            }
        );
        return response?.load;  //{ baudrate: 115200, }
    }

    async getHistory(item_id) {
        const response = await this._call(
            {
                channel: 'item_control',
                action: 'history_get',
                item_id,
            }
        );
        return response?.load;
    }

    async getItemsList() {
        const response = await this._call(
            {
                channel: 'item_control',
                action: 'items_get',
            }
        );
        return response?.load;
    }

}


// =====================================================================================================================
