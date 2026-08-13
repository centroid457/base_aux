import subprocess
import re
import socket
import ipaddress
import sys
import time
from threading import Thread
from queue import Queue

"""
C:\Python3127x64\python.exe C:\__STARICHENKO_Element\PROJECTS\t001.py 
======================================================================
   ПОИСК IoT УСТРОЙСТВ NanoPi NEO Air (Debian)
======================================================================

[*] В логе устройства указан IP: 192.168.137.57
[*] Пробуем проверить его напрямую...
[+] Устройство 192.168.137.57 доступно по SSH!
[+] Вы можете подключиться: ssh root@192.168.137.57

======================================================================
   СКАНИРОВАНИЕ ИЗВЕСТНОЙ СЕТИ 192.168.137.0/24
======================================================================
[*] Быстрая проверка диапазона 192.168.137.1-100...
[+] НАЙДЕН NanoPi: 192.168.137.57 (SSH открыт)
[*] Проверка HTTP портов...
[+] НАЙДЕН Web-сервер: 192.168.137.57 (HTTP открыт)
[+] Найден IP через PowerShell: 172.24.128.1, маска: 255.255.240.0

[!] Мы в другой сети: 172.24.128.1
[*] Устройство из лога было в сети 192.168.137.x
[*] Проверьте, что вы подключены к WiFi 'Vest'
[*] Если да, возможно роутер использует другой диапазон


======================================================================
   ИТОГОВАЯ ИНФОРМАЦИЯ
======================================================================
Из лога устройства:
  - SSID: Vest
  - IP: 192.168.137.57
  - MAC: 54:78:c9:02:22:b0
  - Тип: NanoPi NEO Air (Allwinner H3)
  - ОС: Debian GNU/Linux 12 (bookworm)
  - Hostname: harvest05
  - Сервисы: SSH, Nginx, FastAPI (urozhai), Harvester

[*] Для подключения по SSH:
    ssh root@192.168.137.57
    (или ssh pi@192.168.137.57, если пользователь pi)

[*] Для проверки через браузер:
    http://192.168.137.57
    http://192.168.137.57:8000  (FastAPI)

Process finished with exit code 0
"""

# ==========================================
# 1. ОПРЕДЕЛЕНИЕ СЕТИ (исправленная версия)
# ==========================================
def get_network_info():
    """
    Определяет IP и маску активного подключения.
    Пробуем несколько методов.
    """
    # Метод 1: Через PowerShell (самый надёжный для Windows)
    try:
        ps_cmd = """
        Get-NetIPConfiguration | Where-Object {$_.NetAdapter.Status -eq 'Up' -and $_.IPv4Address} | Select-Object -First 1 -ExpandProperty IPv4Address | Select-Object -First 1 -ExpandProperty IPAddress
        """
        result = subprocess.check_output(
            ["powershell", "-Command", ps_cmd],
            encoding='utf-8', errors='ignore',
            creationflags=subprocess.CREATE_NO_WINDOW
        ).strip()
        if result:
            # Получаем маску через PowerShell
            mask_cmd = """
            Get-NetIPConfiguration | Where-Object {$_.NetAdapter.Status -eq 'Up' -and $_.IPv4Address} | Select-Object -First 1 -ExpandProperty IPv4Address | Select-Object -First 1 -ExpandProperty PrefixLength
            """
            prefix_length = subprocess.check_output(
                ["powershell", "-Command", mask_cmd],
                encoding='utf-8', errors='ignore',
                creationflags=subprocess.CREATE_NO_WINDOW
            ).strip()

            if prefix_length:
                # Конвертируем префикс в маску
                mask_int = int(prefix_length)
                mask = str(ipaddress.IPv4Network(f"0.0.0.0/{mask_int}").netmask)
                print(f"[+] Найден IP через PowerShell: {result}, маска: {mask}")
                return result, mask

    except Exception as e:
        print(f"[-] Ошибка PowerShell: {e}")

    # Метод 2: Через ipconfig (резервный)
    try:
        result = subprocess.check_output("ipconfig", encoding='cp866', errors='ignore')
    except:
        result = subprocess.check_output("ipconfig", encoding='utf-8', errors='ignore')

    lines = result.split('\n')

    # Ищем все IPv4 адреса
    ips = []
    masks = []

    for i, line in enumerate(lines):
        # Ищем IPv4
        ip_match = re.search(r"IPv4[^:]*:\s*(\d+\.\d+\.\d+\.\d+)", line)
        if ip_match:
            ips.append(ip_match.group(1))

        # Ищем маску
        mask_match = re.search(r"Маска подсети[^:]*:\s*(\d+\.\d+\.\d+\.\d+)", line)
        if not mask_match:
            mask_match = re.search(r"Subnet Mask[^:]*:\s*(\d+\.\d+\.\d+\.\d+)", line)
        if mask_match:
            masks.append(mask_match.group(1))

    # Если нашли IP и маску
    if ips and masks:
        # Берём первый не-виртуальный IP (не 169.254.x.x)
        for idx, ip in enumerate(ips):
            if not ip.startswith('169.254'):  # Исключаем APIPA
                mask = masks[idx] if idx < len(masks) else '255.255.255.0'
                print(f"[+] Найден IP через ipconfig: {ip}, маска: {mask}")
                return ip, mask

    # Метод 3: Если ничего не нашли, используем известный диапазон из лога
    print("[!] Не удалось автоматически определить IP.")
    print("[*] Использую известный диапазон сети Vest из лога устройства: 192.168.137.0/24")
    return "192.168.137.100", "255.255.255.0"  # Предполагаем, что у нас тоже .137.x


# ==========================================
# 2. УЛУЧШЕННОЕ ARP-СКАНИРОВАНИЕ
# ==========================================
def arp_scan_improved(ip_range):
    """
    Сканирует сеть используя ARP + проверку характерных портов.
    Теперь более агрессивно и с правильным диапазоном.
    """
    print("\n" + "=" * 60)
    print(f"[*] Сканирую диапазон: {ip_range}")
    print("=" * 60)

    network = ipaddress.IPv4Network(ip_range, strict=False)
    devices = []

    # Быстрый опрос всех хостов
    print("[*] Отправляю ARP-запросы...")
    for ip in network.hosts():
        subprocess.run(
            ["ping", "-n", "1", "-w", "50", str(ip)],
            capture_output=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

    time.sleep(1)  # Даём время на заполнение ARP-таблицы

    # Получаем ARP-таблицу
    print("[*] Получаю ARP-таблицу...")
    arp_output = subprocess.check_output("arp -a", encoding='cp866', errors='ignore')

    # Парсим результат
    found_ips = []
    for line in arp_output.split('\n'):
        match = re.search(r"(\d+\.\d+\.\d+\.\d+)\s+(([0-9a-fA-F]{2}[-:]){5}[0-9a-fA-F]{2})", line)
        if match:
            ip = match.group(1)
            mac = match.group(2)
            if not ip.endswith('.255') and not ip.endswith('.254') and not ip.startswith('224.'):
                print(f"[+] Найден хост: {ip} ({mac})")
                found_ips.append((ip, mac))

    # Проверяем порты для каждого найденного хоста
    if found_ips:
        print(f"\n[*] Проверяю характерные порты для {len(found_ips)} хостов...")
        q = Queue()
        threads = []

        for ip, mac in found_ips:
            t = Thread(target=check_nanopi_ports, args=(ip, mac, q))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        while not q.empty():
            devices.append(q.get())

    return devices


def check_nanopi_ports(ip, mac, q):
    """
    Проверяет порты, характерные для NanoPi с Debian.
    """
    ports_to_check = {
        22: "SSH (OpenSSH)",
        80: "HTTP (Nginx)",
        8000: "FastAPI/Urozhai",
        8080: "HTTP Alt",
        443: "HTTPS",
        1883: "MQTT",
        1880: "Node-RED",
        3000: "Grafana/Node.js",
        5000: "Flask",
    }

    open_ports = []
    for port, desc in ports_to_check.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(f"{port} ({desc})")
            sock.close()
        except:
            pass

    # Пробуем получить hostname
    hostname = ""
    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except:
        pass

    # Определяем, похоже ли на NanoPi
    is_nanopi = False
    if hostname and ('nano' in hostname.lower() or 'harvest' in hostname.lower() or 'urozhai' in hostname.lower()):
        is_nanopi = True
    elif len(open_ports) >= 2:
        is_nanopi = True

    q.put({
        'ip': ip,
        'mac': mac,
        'hostname': hostname,
        'open_ports': open_ports,
        'is_nanopi': is_nanopi
    })


# ==========================================
# 3. ПРЯМОЕ ПОДКЛЮЧЕНИЕ К ИЗВЕСТНОМУ IP
# ==========================================
def probe_known_device(ip="192.168.137.57"):
    """
    Пробуем подключиться к известному IP из лога.
    """
    print("\n" + "=" * 60)
    print(f"[*] Проверяю известный IP из лога: {ip}")
    print("=" * 60)

    # Проверяем порты
    ports = [22, 80, 8000, 8080]
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"[+] Порт {port} ОТКРЫТ")
            if port == 80 or port == 8000:
                try:
                    import requests
                    r = requests.get(f"http://{ip}:{port}/", timeout=3)
                    print(f"  HTTP {r.status_code}, Server: {r.headers.get('Server', 'N/A')}")
                    print(f"  Заголовки: {dict(r.headers)}")
                except:
                    pass
        sock.close()

    # Пробуем SSH
    print(f"\n[*] SSH доступ: ssh root@{ip} (или другой пользователь)")

    return ip


# ==========================================
# 4. СКАНИРОВАНИЕ С ИСПОЛЬЗОВАНИЕМ ИЗВЕСТНОЙ СЕТИ
# ==========================================
def scan_known_network():
    """
    Сканирует сеть 192.168.137.0/24, так как из лога видно,
    что устройство получило IP 192.168.137.57.
    """
    print("\n" + "=" * 70)
    print("   СКАНИРОВАНИЕ ИЗВЕСТНОЙ СЕТИ 192.168.137.0/24")
    print("=" * 70)

    # Прямая проверка известных IP
    known_devices = []

    # Проверяем все IP в диапазоне .1 - .100
    print("[*] Быстрая проверка диапазона 192.168.137.1-100...")
    for i in range(1, 101):
        ip = f"192.168.137.{i}"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)

        # Проверяем SSH (самый надёжный признак)
        result = sock.connect_ex((ip, 22))
        if result == 0:
            print(f"[+] НАЙДЕН NanoPi: {ip} (SSH открыт)")
            known_devices.append({
                'ip': ip,
                'port': 22,
                'type': 'SSH'
            })
        sock.close()

    # Также проверяем HTTP порт
    print("[*] Проверка HTTP портов...")
    for i in range(1, 101):
        ip = f"192.168.137.{i}"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)

        result = sock.connect_ex((ip, 80))
        if result == 0:
            print(f"[+] НАЙДЕН Web-сервер: {ip} (HTTP открыт)")
            known_devices.append({
                'ip': ip,
                'port': 80,
                'type': 'HTTP'
            })
        sock.close()

    return known_devices


# ==========================================
# ГЛАВНАЯ ЛОГИКА
# ==========================================
if __name__ == "__main__":
    print("=" * 70)
    print("   ПОИСК IoT УСТРОЙСТВ NanoPi NEO Air (Debian)")
    print("=" * 70)

    # Сначала пробуем подключиться к известному IP из лога
    known_ip = "192.168.137.57"
    print(f"\n[*] В логе устройства указан IP: {known_ip}")
    print("[*] Пробуем проверить его напрямую...")

    # Проверяем известный IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((known_ip, 22))
    if result == 0:
        print(f"[+] Устройство {known_ip} доступно по SSH!")
        print(f"[+] Вы можете подключиться: ssh root@{known_ip}")
    else:
        print(f"[-] Устройство {known_ip} не отвечает (возможно, IP изменился)")
    sock.close()

    # Сканируем известную сеть
    devices = scan_known_network()

    # Пытаемся определить нашу сеть
    my_ip, my_mask = get_network_info()

    if my_ip.startswith('192.168.137'):
        print(f"\n[+] Мы в той же сети: {my_ip}")
        # Сканируем ARP
        network = ipaddress.IPv4Network(f"{my_ip}/24", strict=False)
        arp_devices = arp_scan_improved(str(network))

        # Выводим результаты
        print("\n\n" + "=" * 70)
        print("   НАЙДЕННЫЕ УСТРОЙСТВА")
        print("=" * 70)

        for dev in arp_devices:
            if dev['is_nanopi']:
                print(f"\n{'*' * 50}")
                print(f"  >>> NanoPi (Debian IoT) <<<")
                print(f"{'*' * 50}")
            print(f"  IP:        {dev['ip']}")
            print(f"  MAC:       {dev['mac']}")
            if dev['hostname']:
                print(f"  Hostname:  {dev['hostname']}")
            if dev['open_ports']:
                print(f"  Сервисы:   {', '.join(dev['open_ports'])}")
                print(f"  >> SSH: ssh user@{dev['ip']}")
                print(f"  >> Web: http://{dev['ip']}")
    else:
        print(f"\n[!] Мы в другой сети: {my_ip}")
        print("[*] Устройство из лога было в сети 192.168.137.x")
        print("[*] Проверьте, что вы подключены к WiFi 'Vest'")
        print("[*] Если да, возможно роутер использует другой диапазон")

    print("\n\n" + "=" * 70)
    print("   ИТОГОВАЯ ИНФОРМАЦИЯ")
    print("=" * 70)
    print("Из лога устройства:")
    print(f"  - SSID: Vest")
    print(f"  - IP: 192.168.137.57")
    print(f"  - MAC: 54:78:c9:02:22:b0")
    print(f"  - Тип: NanoPi NEO Air (Allwinner H3)")
    print(f"  - ОС: Debian GNU/Linux 12 (bookworm)")
    print(f"  - Hostname: harvest05")
    print(f"  - Сервисы: SSH, Nginx, FastAPI (urozhai), Harvester")

    print("\n[*] Для подключения по SSH:")
    print(f"    ssh root@192.168.137.57")
    print(f"    (или ssh pi@192.168.137.57, если пользователь pi)")

    print("\n[*] Для проверки через браузер:")
    print(f"    http://192.168.137.57")
    print(f"    http://192.168.137.57:8000  (FastAPI)")