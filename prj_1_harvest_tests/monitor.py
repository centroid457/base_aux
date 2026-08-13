import subprocess
import socket
import json
import time
import re
from datetime import datetime

"""
C:\Python3127x64\python.exe C:\__STARICHENKO_Element\PROJECTS\abc=base_aux\prj_1_harvest_tests\monitor.py 
======================================================================
АНАЛИЗ УСТРОЙСТВА 192.168.137.57 (harvest05)
======================================================================
Время: 2026-08-13 14:35:00
======================================================================
HTTP ИНФОРМАЦИЯ
======================================================================

[+] http://192.168.137.57:80/
    Статус: 200
    Server: nginx/1.22.1
    Content-Type: text/html; charset=utf-8
    Ответ: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] http://192.168.137.57:80/status
    Статус: 200
    Server: nginx/1.22.1
    Content-Type: text/html; charset=utf-8
    Ответ: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] http://192.168.137.57:80/api
    Статус: 200
    Server: nginx/1.22.1
    Content-Type: text/html; charset=utf-8
    Ответ: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] http://192.168.137.57:80/api/status
    Статус: 200
    Server: nginx/1.22.1
    Content-Type: text/html; charset=utf-8
    Ответ: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] http://192.168.137.57:80/api/devices
    Статус: 200
    Server: nginx/1.22.1
    Content-Type: text/html; charset=utf-8
    Ответ: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] http://192.168.137.57:8000/
    Статус: 200
    Server: uvicorn
    Content-Type: text/html; charset=utf-8
    Ответ: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] http://192.168.137.57:8000/docs
    Статус: 200
    Server: uvicorn
    Content-Type: text/html; charset=utf-8
    Ответ: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] http://192.168.137.57:8000/redoc
    Статус: 200
    Server: uvicorn
    Content-Type: text/html; charset=utf-8
    Ответ: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] http://192.168.137.57:8000/api
    Статус: 200
    Server: uvicorn
    Content-Type: text/html; charset=utf-8
    Ответ: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] http://192.168.137.57:8000/api/status
    Статус: 200
    Server: uvicorn
    Content-Type: text/html; charset=utf-8
    Ответ: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] http://192.168.137.57:8000/openapi.json
    Статус: 200
    Server: uvicorn
    Content-Type: text/html; charset=utf-8
    Ответ: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

======================================================================
ДАННЫЕ ИЗ API (Urozhai FastAPI)
======================================================================

[+] Найден API: http://192.168.137.57:8000/docs
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:8000/redoc
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:8000/openapi.json
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:8000/api/v1/
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:8000/api/v1/devices
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:8000/api/v1/status
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:8000/api/v1/sensors
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:8000/api/v1/data
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:8000/api/devices
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:8000/api/sensors
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:8000/api/data
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:8000/api/harvest
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:80/docs
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:80/redoc
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:80/openapi.json
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:80/api/v1/
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:80/api/v1/devices
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:80/api/v1/status
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:80/api/v1/sensors
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:80/api/v1/data
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:80/api/devices
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:80/api/sensors
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:80/api/data
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty

[+] Найден API: http://192.168.137.57:80/api/harvest
    Status: 200
    Текст: <!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход в систему</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="sty
[-] API не найден или требует аутентификацию

[!] Для SSH доступа укажите SSH_PASSWORD или SSH_KEY_PATH
[!] Или выполните вручную:
    ssh root@192.168.137.57
    Затем:
    systemctl status harvester
    systemctl status urozhai
    journalctl -u harvester -n 50
    journalctl -u urozhai -n 50

Process finished with exit code 0
"""

# ==========================================
# КОНФИГУРАЦИЯ
# ==========================================
DEVICE_IP = "192.168.137.57"
SSH_USER = "root"  # Из лога видно root@harvest05
SSH_PASSWORD = ""  # Если нужен пароль, укажите здесь
SSH_KEY_PATH = ""  # Или путь к ключу


# ==========================================
# 1. ПОЛУЧЕНИЕ ИНФОРМАЦИИ ЧЕРЕЗ HTTP
# ==========================================
def get_http_info():
    """Получает информацию через HTTP (Nginx, FastAPI)."""
    print("=" * 70)
    print("HTTP ИНФОРМАЦИЯ")
    print("=" * 70)

    # Пробуем разные порты и пути
    endpoints = [
        (80, "/"),
        (80, "/status"),
        (80, "/api"),
        (80, "/api/status"),
        (80, "/api/devices"),
        (8000, "/"),
        (8000, "/docs"),  # FastAPI Swagger
        (8000, "/redoc"),  # FastAPI ReDoc
        (8000, "/api"),
        (8000, "/api/status"),
        (8000, "/openapi.json"),  # FastAPI OpenAPI схема
        (8080, "/"),
    ]

    import requests

    for port, path in endpoints:
        url = f"http://{DEVICE_IP}:{port}{path}"
        try:
            r = requests.get(url, timeout=2)
            print(f"\n[+] {url}")
            print(f"    Статус: {r.status_code}")
            print(f"    Server: {r.headers.get('Server', 'N/A')}")
            print(f"    Content-Type: {r.headers.get('Content-Type', 'N/A')}")

            # Пытаемся распарсить JSON
            try:
                data = r.json()
                print(f"    JSON данные: {json.dumps(data, indent=4, ensure_ascii=False)[:500]}")
            except:
                # Если не JSON, показываем текст
                text = r.text[:300]
                if text.strip():
                    print(f"    Ответ: {text}")
        except requests.exceptions.ConnectionError:
            # Порт закрыт
            pass
        except Exception as e:
            print(f"[-] Ошибка {url}: {e}")


# ==========================================
# 2. ВЫПОЛНЕНИЕ КОМАНД ЧЕРЕЗ SSH
# ==========================================
def run_ssh_command(command, timeout=10):
    """
    Выполняет команду на устройстве через SSH.
    Требует paramiko или sshpass.
    """
    try:
        import paramiko
    except ImportError:
        print("[!] Установите paramiko: pip install paramiko")
        return None

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Пробуем разные способы аутентификации
        kwargs = {
            'hostname': DEVICE_IP,
            'username': SSH_USER,
            'timeout': timeout
        }

        if SSH_KEY_PATH:
            kwargs['key_filename'] = SSH_KEY_PATH
        elif SSH_PASSWORD:
            kwargs['password'] = SSH_PASSWORD

        client.connect(**kwargs)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        client.close()

        if error and 'Warning' not in error:
            return f"ERROR: {error}"
        return output
    except Exception as e:
        return f"SSH Error: {e}"


def get_system_info_ssh():
    """Получает детальную информацию через SSH."""
    print("\n" + "=" * 70)
    print("СИСТЕМНАЯ ИНФОРМАЦИЯ (через SSH)")
    print("=" * 70)

    commands = {
        "uptime": "uptime",
        "hostname": "hostname -f",
        "OS Version": "cat /etc/os-release | head -5",
        "Kernel": "uname -a",
        "CPU Info": "cat /proc/cpuinfo | grep -E 'Hardware|Revision|Serial' | head -5",
        "Memory": "free -h",
        "Disk": "df -h / /dev/mmcblk0p3",
        "Temperature": "cat /sys/class/thermal/thermal_zone0/temp 2>/dev/null || echo 'N/A'",
        "Network": "ip addr show wlan0",
        "WiFi Signal": "cat /proc/net/wireless | tail -1",
        "Running Services": "systemctl list-units --type=service --state=running | grep -E 'harvester|urozhai|nginx|ssh|wpa'",
        "Harvester Status": "systemctl status harvester --no-pager -l | head -20",
        "Urozhai Status": "systemctl status urozhai --no-pager -l | head -20",
        "Nginx Status": "systemctl status nginx --no-pager -l | head -10",
    }

    results = {}
    for name, cmd in commands.items():
        print(f"\n--- {name} ---")
        output = run_ssh_command(cmd)
        if output:
            print(output.strip())
            results[name] = output.strip()
        time.sleep(0.3)  # Небольшая пауза

    return results


# ==========================================
# 3. МОНИТОРИНГ СОСТОЯНИЯ
# ==========================================
def monitor_device(duration=60, interval=10):
    """
    Мониторит состояние устройства.
    """
    print("\n" + "=" * 70)
    print(f"МОНИТОРИНГ УСТРОЙСТВА (каждые {interval} сек, всего {duration} сек)")
    print("=" * 70)

    start_time = time.time()
    iterations = 0

    while time.time() - start_time < duration:
        iterations += 1
        timestamp = datetime.now().strftime("%H:%M:%S")

        print(f"\n[{timestamp}] Итерация {iterations}")
        print("-" * 50)

        # Получаем ключевые метрики
        metrics = {
            "CPU": run_ssh_command("top -bn1 | grep '%Cpu' | awk '{print $2+$4}'"),
            "Memory": run_ssh_command("free -m | awk '/Mem:/ {print $3\"/\"$2\" MB\"}'"),
            "Temperature": run_ssh_command(
                "cat /sys/class/thermal/thermal_zone0/temp 2>/dev/null | awk '{print $1/1000\"°C\"}'"),
            "Load": run_ssh_command("uptime | awk -F'load average:' '{print $2}'"),
            "WiFi": run_ssh_command("iwconfig wlan0 2>/dev/null | grep -E 'Signal|Bit Rate'"),
        }

        for key, value in metrics.items():
            if value and 'Error' not in value:
                print(f"  {key}: {value.strip()}")

        if iterations >= duration / interval:
            break

        time.sleep(interval)


# ==========================================
# 4. ПОЛУЧЕНИЕ ДАННЫХ ИЗ API
# ==========================================
def get_api_data():
    """
    Пробует получить данные из FastAPI (urozhai).
    """
    print("\n" + "=" * 70)
    print("ДАННЫЕ ИЗ API (Urozhai FastAPI)")
    print("=" * 70)

    import requests

    # FastAPI обычно имеет документацию
    api_paths = [
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api/v1/",
        "/api/v1/devices",
        "/api/v1/status",
        "/api/v1/sensors",
        "/api/v1/data",
        "/api/devices",
        "/api/sensors",
        "/api/data",
        "/api/harvest",
    ]

    for port in [8000, 80, 8080]:
        for path in api_paths:
            url = f"http://{DEVICE_IP}:{port}{path}"
            try:
                r = requests.get(url, timeout=2)
                if r.status_code == 200:
                    print(f"\n[+] Найден API: {url}")
                    print(f"    Status: {r.status_code}")

                    # Пробуем JSON
                    try:
                        data = r.json()
                        print(f"    Данные: {json.dumps(data, indent=2, ensure_ascii=False)[:1000]}")
                        return data
                    except:
                        print(f"    Текст: {r.text[:300]}")
            except:
                pass

    print("[-] API не найден или требует аутентификацию")
    return None


# ==========================================
# 5. ПОИСК ДРУГИХ УСТРОЙСТВ (через SSH)
# ==========================================
def find_other_devices():
    """
    Использует SSH на harvest05 для поиска других устройств в сети.
    """
    print("\n" + "=" * 70)
    print("ПОИСК ДРУГИХ УСТРОЙСТВ (через SSH на harvest05)")
    print("=" * 70)

    commands = [
        "arp -a",
        "ip neigh show",
        "cat /etc/hosts",
        "cat /var/lib/dhcp/dhclient.leases 2>/dev/null",
    ]

    for cmd in commands:
        output = run_ssh_command(cmd)
        if output and 'Error' not in output:
            print(f"\n--- {cmd} ---")
            print(output)


# ==========================================
# 6. ПОЛУЧЕНИЕ ЛОГОВ
# ==========================================
def get_logs():
    """
    Получает логи harvester и urozhai.
    """
    print("\n" + "=" * 70)
    print("ЛОГИ СЕРВИСОВ")
    print("=" * 70)

    log_commands = [
        ("Harvester", "journalctl -u harvester --no-pager -n 50"),
        ("Urozhai", "journalctl -u urozhai --no-pager -n 50"),
        ("Nginx", "tail -50 /var/log/nginx/access.log 2>/dev/null || journalctl -u nginx --no-pager -n 30"),
    ]

    for name, cmd in log_commands:
        print(f"\n--- {name} ---")
        output = run_ssh_command(cmd)
        if output and 'Error' not in output:
            print(output[-1000:])  # Последние 1000 символов


# ==========================================
# ГЛАВНАЯ ФУНКЦИЯ
# ==========================================
def main():
    print("=" * 70)
    print(f"АНАЛИЗ УСТРОЙСТВА {DEVICE_IP} (harvest05)")
    print("=" * 70)
    print(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 1. HTTP информация
    get_http_info()

    # 2. API данные
    get_api_data()

    # 3. Системная информация через SSH (если есть доступ)
    if SSH_PASSWORD or SSH_KEY_PATH:
        get_system_info_ssh()
        get_logs()
        find_other_devices()
    else:
        print("\n[!] Для SSH доступа укажите SSH_PASSWORD или SSH_KEY_PATH")
        print("[!] Или выполните вручную:")
        print(f"    ssh root@{DEVICE_IP}")
        print("    Затем:")
        print("    systemctl status harvester")
        print("    systemctl status urozhai")
        print("    journalctl -u harvester -n 50")
        print("    journalctl -u urozhai -n 50")

    # 4. Быстрый мониторинг
    if SSH_PASSWORD or SSH_KEY_PATH:
        print("\n[?] Запустить мониторинг на 30 секунд? (y/n): ", end="")
        answer = input().lower()
        if answer == 'y':
            monitor_device(duration=30, interval=10)


if __name__ == "__main__":
    main()


# ======================================================================================================================
