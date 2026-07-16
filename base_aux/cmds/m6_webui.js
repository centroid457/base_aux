// =====================================================================================================================
// =====================================================================================================================
/**
Базовый UI одного элемента.
*/
class BaseItemUI extends ConsoleLogger {
    css_map = {};

    /**
     * @param {string}             itemId
     * @param {WsClient}    ws     экземпляр WebSocket-клиента
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
    }

    async init() {
        this.buildDOM();    // WARN: DONT PLACE IN CONSTRUCTOR!!!!
        this.init_post();
    }

    // =================================================================================================================
    ELEMENTS_SCHEMA = {
        // EXAMPLE STRUCT -----------------------------------------------
        __EXAMPLE__: {
            element: undefined,
            container_name: undefined,

            tag_name: 'button',
            attrs: {
                // <p title="TITLE"></p>
                // <input type="text" placeholder="Введите имя">
                title: 'Clear History',
            },
            props: {
                // const div = documet.createElement('div');
                // div.className = "main_div__cls";
                // div.textContent = "hello";n
                textContent: undefined,
                className: undefined,
            },
            events: {
                // element.addEventListener(e_name, e_val);
                change: (x) => console.log(x),
            },
            styles: {
                width: '100',
            },
            init: undefined,
        },

        // ROOT STRUCT -----------------------------------------------
        ROOT: {
            element: undefined,
            container_name: undefined,

            tag_name: 'div',
            props: {
                className: this.css_map.itemBox,
            },
        },
        HEADER: {
            container_name: "ROOT",
            tag_name: "header",
            attrs: {
            },
        },
        MAIN: {
            container_name: "ROOT",
            tag_name: 'main',
            attrs: {
                ['data-scrollbar__dark']: '',
            },
        },
        FOOTER: {
            container_name: "ROOT",
            tag_name: 'footer',
            attrs: {
            },
        },
        // -------------------------------------------------------------
    }

    // -----------------------------------------------------------------------------------------------------------------
    _elements_make(schema = this.ELEMENTS_SCHEMA) {
        for (const [el_name, el_schema] of Object.entries(schema)) {
            const {
                tag_name,
                container_name,
                init,
                attrs={},
                props={},
                events={},
                styles={},
            } = el_schema;
            const element = document.createElement(tag_name);
            el_schema.element = element;
            if (container_name) schema[container_name].element.appendChild(element);

            for (const [a_name, a_val] of Object.entries(attrs)) {
                element.setAttribute(a_name, a_val);
            }
            for (const [p_name, p_val] of Object.entries(props)) {
                element[p_name] = p_val;
            }
            for (const [e_name, e_val] of Object.entries(events)) {
                element.addEventListener(e_name, e_val);
            }
            for (const [s_name, s_val] of Object.entries(styles)) {
                element.style[s_name] = s_val;
            }

            if (init) init();
        }
        return schema?.ROOT?.element;
    }

    // -----------------------------------------------------------------------------------------------------------------
    buildDOM() {
        return this._elements_make();
    }

    // =================================================================================================================
    destroy() {
        this.ELEMENTS_SCHEMA?.ROOT?.element?.remove();
    }

    // NESTING =========================================================================================================
    async init_post() {
    }

    // METHS -----------------------------------------------------------------------------------------------------------
    //
}


// =====================================================================================================================
class ItemUiTerminal extends BaseItemUI {
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
        this._currentBaudrate = undefined;
        await this.history_load();
        await this.config_load();
    }

    // ======================================================
    ELEMENTS_SCHEMA = {
        // ROOT STRUCT ===============================================================
        ROOT: {
            element: undefined,
            container_name: undefined,

            tag_name: 'div',
            props: {
                className: this.css_map.itemBox,
            },
        },
        HEADER: {
            container_name: "ROOT",
            tag_name: "header",
            attrs: {
            },
        },
        MAIN: {
            container_name: "ROOT",
            tag_name: 'main',
            attrs: {
                ['data-scrollbar__dark']: '',
            },
        },
        FOOTER: {
            container_name: "ROOT",
            tag_name: 'footer',
            attrs: {
            },
        },

        // 1=HEADER ===============================================================
        header_id: {
            container_name: "HEADER",
            tag_name: 'span',
            props: {
                textContent: this.itemId,
                className: this.css_map.itemId,
            },
        },

        config_baudrate: {
            container_name: "HEADER",
            tag_name: 'select',
            props: {
                className: this.css_map.itemId,
                textContent: this.itemId,
            },
            events: {
                change: () => this._onBaudrateChange(),
            },
            styles: {
                width: '100',
            },
            init: () => this._init__config_baudrate(),
        },

        // BTNS ----------------------
        header_control: {
            container_name: "HEADER",
            tag_name: 'div',
            attrs: {
            },
        },

        btn_clear: {
            container_name: "header_control",
            tag_name: 'button',
            props: {
                textContent: 'clrHist',
                title: 'ClearHistory',
            },
            attrs: {
                ['data-btn_outline']: 'blue',
            },
            events: {
                click: () => this.sendHistoryClear(),
            },
        },
        btn_recon: {
            container_name: "header_control",
            tag_name: 'button',
            props: {
                textContent: 'ReCon',
                title: 'ReConnect',
            },
            attrs: {
                ['data-btn_outline']: 'blue',
            },
            events: {
                click: () => this.sendReconnect(),
            },
        },
        btn_discon: {
            container_name: "header_control",
            tag_name: 'button',
            props: {
                textContent: 'DisCon',
                title: 'DisConnect',
            },
            attrs: {
                ['data-btn_outline']: 'blue',
            },
            events: {
                click: () => this.sendDisconnect(),
            },
        },
        btn_close: {
            container_name: "header_control",
            tag_name: 'button',
            props: {
                textContent: 'X',
                title: 'Close',
            },
            attrs: {
                ['data-btn_outline']: 'red',
            },
            events: {
                click: () => this.sendDelete(),
            },
        },

        // 2=MAIN =================================================================

        // 3=FOOTER ===============================================================
        input: {
            container_name: "FOOTER",
            tag_name: 'input',
            attrs: {
                type: 'text',
                placeholder: 'Введите команду и нажмите Enter',
            },
            events: {
                change: () => this.callback_input(),
            },
        },

        // =========================================================================
    }

    _init__config_baudrate() {
        const opts = [undefined, 9600, 19200, 38400, 57600, 115200];
        opts.forEach(rate => {
            const opt = document.createElement('option');
            opt.value = rate;
            opt.textContent = rate;
            this.ELEMENTS_SCHEMA.config_baudrate.element.appendChild(opt);
        });
        this.ELEMENTS_SCHEMA.config_baudrate.element.value = undefined;
    }

    // =================================================================================================================
    // SEND -----
    async sendInput(text)    { if (!text) return; return await this.rpc.sendStdin(this.itemId, text); }
    async sendReconnect()    { await this.rpc.reconnectItem(this.itemId) }
    async sendDisconnect()   { await this.rpc.disconnectItem(this.itemId) }
    async sendDelete()       { await this.rpc.deleteItem(this.itemId) }
    async sendHistoryClear() { await this.rpc.clearHistory(this.itemId) }
    async sendHistoryGet()   { return await this.rpc.getHistory(this.itemId) }

    // USER METH -------------------------------------------------------------------------------------------------------
    callback_input() {
        const text = this.ELEMENTS_SCHEMA.input.element.value.trim();
        const sent = this.sendInput(text);
        if (sent) this.ELEMENTS_SCHEMA.input.element.value = '';
    }

    history_clear() {
        if (this.ELEMENTS_SCHEMA.MAIN.element) this.ELEMENTS_SCHEMA.MAIN.element.innerHTML = '';
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
        this.ELEMENTS_SCHEMA.MAIN.element.appendChild(div);
        this.ELEMENTS_SCHEMA.MAIN.element.scrollTop = this.ELEMENTS_SCHEMA.MAIN.element.scrollHeight;
    }

    async config_load() {
        const config = await this.rpc.getConfig(this.itemId);
        this._currentBaudrate = config?.baudrate;
        if (config?.baudrate) this.ELEMENTS_SCHEMA.config_baudrate.element.value = config?.baudrate;
    }

    async _onBaudrateChange() {
        const newValue = parseInt(this.ELEMENTS_SCHEMA.config_baudrate.element.value, 10);
        this.console_log("config_baudrate newValue=", newValue);

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
            this.ELEMENTS_SCHEMA.config_baudrate.element.value = oldValue;
        }
    }

}

// =====================================================================================================================
// =====================================================================================================================
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
        this.container = document.querySelector(this.config.selector_container);
        if (!this.container) throw new Error(`Контейнер "${this.config.selector_container}" не найден`);

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
        this.container.appendChild(ui.ELEMENTS_SCHEMA.ROOT.element);
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
// =====================================================================================================================
class RpcClient {
    /**
     * @param {string} url – URL RPC-эндпоинта (например "/channel__rpc")
     * @param {Function} [requestFn] – функция для запроса (по умолчанию fetchJsonPost)
     */
    constructor(url) {
        this.url = url;
    }

    __RESPONSE_SCHEMA__ = {    // just for info!
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
            }
        );
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

    async disconnectItem(item_id) {
        const response = await this._call(
            {
                channel: 'item_control',
                action: 'disconnect_item',
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
    ws.connect();
};



// =====================================================================================================================
