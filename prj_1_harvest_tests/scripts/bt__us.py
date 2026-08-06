#!/usr/bin/env python3
"""
Сбор данных с ультразвуковых BLE датчиков UltraSonic.
Запуск: python3 /tmp/bt_ultrasonic.py [PACKETS_MAX] [TIMEOUT]
"""

import sys
import time
import asyncio
import re
from bleak import BleakScanner, BleakClient

# ===== НАСТРОЙКИ =====
TX_UUID = "dec01433-ceb1-cec0-dec0-ff0123456789"
DEVICE_NAME = "UltraSonic"

PACKETS_MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 3
TIMEOUT = float(sys.argv[2]) if len(sys.argv) > 2 else 20.0

# Паттерны полей (датчик шлет каждое поле отдельным уведомлением)
FIELD_PATTERNS = {
    "UTC": r'"UTC":\s*"?(\d+)"?',
    "Distance up": r'"Distance up":\s*"?([\d.]+)"?',
    "Distance side": r'"Distance side":\s*"?([\d.]+)"?',
    "Temperature": r'"Temperature":\s*"?([\d.]+)"?',
    "Battery": r'"Battery":\s*"?([\d.]+)"?',
    "Percentage": r'"Percentage":\s*"?([\d.]+)"?',
}


# ===== ЛОГИКА =====
def parse_fields(raw_chunk: str) -> dict[str, str]:
    """Извлекает все найденные поля из фрагмента данных."""
    result = {}
    for field_name, pattern in FIELD_PATTERNS.items():
        match = re.search(pattern, raw_chunk)
        if match:
            result[field_name] = match.group(1)
    return result


def make_packet(fields_accumulator: dict[str, str]) -> str:
    """Собирает JSON-строку из накопленных полей."""
    parts = []
    for field in ["UTC", "Distance up", "Distance side", "Temperature", "Battery", "Percentage"]:
        if field in fields_accumulator:
            val = fields_accumulator[field]
            # Числовые поля без кавычек
            if field == "UTC":
                parts.append(f'"{field}":{val}')
            else:
                parts.append(f'"{field}":{val}')
    return "{" + ",".join(parts) + "}"


async def main_async():
    """Основная асинхронная логика (только bleak требует asyncio)."""
    # 1. Сканирование
    print("SCAN_START", flush=True)
    device = None
    for step in range(5):
        print(f"scan {step=}")
        device = await BleakScanner.find_device_by_name(DEVICE_NAME, timeout=2.0)
        if device:
            break

    if not device:
        print("ERROR:device_not_found", flush=True)
        return

    print(f"DEVICE_FOUND:{device.address}", flush=True)

    # 2. Подключение и сбор
    packets = []
    current_fields: dict[str, str] = {}
    last_utc = None

    def on_notify(sender, data):
        nonlocal current_fields, last_utc

        print(f"raw=", data)
        try:
            text = data.decode('utf-8', errors='replace')
        except:
            return

        print(f"text=", text)

        # Парсим поля из уведомления
        parsed = parse_fields(text)
        current_fields.update(parsed)

        # Если получили новый UTC - значит начался новый пакет
        if "UTC" in parsed:
            new_utc = parsed["UTC"]
            if last_utc is not None and new_utc != last_utc:
                # Сохраняем предыдущий пакет
                packet = make_packet(current_fields)
                packets.append(packet)
                print(f"PACKET:{packet}", flush=True)
            last_utc = new_utc

    try:
        async with BleakClient(device.address) as client:
            if not client.is_connected:
                print("ERROR:connect_failed", flush=True)
                return

            print("CONNECTED", flush=True)
            await client.start_notify(TX_UUID, on_notify)

            # Ждем нужное количество пакетов или таймаут
            start = time.time()
            while len(packets) < PACKETS_MAX and (time.time() - start) < TIMEOUT:
                await asyncio.sleep(0.2)

            await client.stop_notify(TX_UUID)

    except Exception as e:
        print(f"ERROR:{e}", flush=True)
        return

    # 3. Результат
    print(f"PACKETS_COUNT:{len(packets)}", flush=True)

    if packets:
        print(f"ALL_PACKETS:")
        for pkt in packets:
            print(f"\t{pkt}")

    print(f"STATUS:OK")


if __name__ == "__main__":
    asyncio.run(main_async())