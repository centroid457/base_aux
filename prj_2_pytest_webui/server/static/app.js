let ws;
let currentState = {};

// Инициализация WebSocket
function initWebSocket() {
    ws = new WebSocket(`ws://${window.location.host}/ws`);
    
    ws.onopen = () => {
        console.log('WebSocket connected');
        ws.send(JSON.stringify({type: 'get_state'}));
    };
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
    };
    
    ws.onclose = () => {
        console.log('WebSocket disconnected');
        setTimeout(initWebSocket, 1000);
    };
}

// Обработка сообщений WebSocket
function handleWebSocketMessage(data) {
    if (data.type === 'state') {
        currentState = data.data;
        updateUI();
    } else if (data.type === 'output') {
        appendOutput(data.data);
    }
}

// Обновление UI
function updateUI() {
    const status = document.getElementById('status');
    status.textContent = `Статус: ${currentState.status || 'idle'}`;
    
    const currentTest = document.getElementById('current-test');
    currentTest.textContent = currentState.current_test ? 
        `Текущий тест: ${currentState.current_test}` : '';
    
    // Обновление кнопок
    const runBtn = document.getElementById('run-btn');
    const pauseBtn = document.getElementById('pause-btn');
    const stopBtn = document.getElementById('stop-btn');
    
    runBtn.disabled = currentState.status === 'running' || currentState.status === 'paused';
    pauseBtn.disabled = currentState.status !== 'running' && currentState.status !== 'paused';
    stopBtn.disabled = currentState.status !== 'running' && currentState.status !== 'paused';
    
    pauseBtn.textContent = currentState.status === 'paused' ? '▶ Продолжить' : '⏸ Пауза';
}

// Загрузка тестпланов
async function loadTestplans() {
    const response = await fetch('/api/testplans?root_path=TESTPLANS');
    const data = await response.json();
    
    const select = document.getElementById('testplan-select');
    select.innerHTML = '<option value="">Выберите тестплан</option>';
    
    data.testplans.forEach(plan => {
        const option = document.createElement('option');
        option.value = plan.name;
        option.textContent = plan.name;
        select.appendChild(option);
    });
}

// Загрузка структуры тестов
async function loadTests(testplan) {
    const response = await fetch(`/api/tests/${testplan}?root_path=TESTPLANS`);
    const data = await response.json();
    
    renderTestTree(data.tests);
}

// Отображение дерева тестов
function renderTestTree(tests) {
    const container = document.getElementById('test-tree');
    container.innerHTML = '';
    
    tests.forEach(test => {
        container.appendChild(createTreeNode(test));
    });
}

function createTreeNode(test) {
    const div = document.createElement('div');
    div.className = 'test-node';
    div.textContent = test.name;
    div.dataset.id = test.id;
    
    if (test.children && test.children.length > 0) {
        div.classList.add('has-children');
        test.children.forEach(child => {
            div.appendChild(createTreeNode(child));
        });
    }
    
    return div;
}

// Запуск тестов
async function runTests() {
    const testplan = document.getElementById('testplan-select').value;
    
    if (!testplan) {
        alert('Выберите тестплан');
        return;
    }
    
    const response = await fetch('/api/run', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            root_path: 'TESTPLANS',
            testplan: testplan
        })
    });
    
    if (response.ok) {
        console.log('Tests started');
        document.getElementById('output').textContent = '';
    }
}

// Пауза тестов
async function pauseTests() {
    const endpoint = currentState.status === 'paused' ? '/api/resume' : '/api/pause';
    const response = await fetch(endpoint, {method: 'POST'});
    
    if (response.ok) {
        console.log('Pause toggled');
    }
}

// Остановка тестов
async function stopTests() {
    const response = await fetch('/api/stop', {method: 'POST'});
    
    if (response.ok) {
        console.log('Tests stopped');
    }
}

// Добавление вывода
function appendOutput(text) {
    const output = document.getElementById('output');
    output.textContent += text;
    output.scrollTop = output.scrollHeight;
}

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    initWebSocket();
    loadTestplans();
    
    document.getElementById('testplan-select').addEventListener('change', (e) => {
        if (e.target.value) {
            loadTests(e.target.value);
        }
    });
    
    // Периодическое обновление состояния
    setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({type: 'get_state'}));
        }
    }, 1000);
});