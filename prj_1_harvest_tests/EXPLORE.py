# ===================================================================
# scr__rfid_scan.py - ВЕРСИЯ С ПРЯМЫМ ИЗВЛЕЧЕНИЕМ EPC
# ===================================================================
import serial, time, sys, re
from typing import *


PORT = '/dev/ttyS2'
BAUD = 115200
TIMEOUT = 0.5

# READ BANK
CMD = bytes([0xA0, 0x0A, 0x01, 0x81, 0x01, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0xCB])


def read__data() -> bytes | NoReturn:
    ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
    ser.reset_input_buffer()
    ser.write(CMD)

    response = b""
    start = time.time()
    while time.time() - start < 1.0:
        chunk = ser.read(ser.in_waiting or 1)
        if chunk:
            response += chunk
        else:
            time.sleep(0.05)
    ser.close()
    return response


def parse__pkgs(data: bytes) -> list[str]:
    data_hex: str = data.hex().upper()

    pkgs = []
    # for


def _parse__epc(data):
    epc_list = []
    i = 0

    while i < len(data):
        # Ищем начало пакета 0xA0
        if data[i] != 0xA0:
            i += 1
            continue

        if i + 1 >= len(data):
            break

        length = data[i + 1]
        if i + length + 1 > len(data):
            i += 1
            continue

        packet = data[i:i + length + 1]
        i += length + 1

        # Проверяем тип пакета (0x01 0x81 - инвентаризация)
        if len(packet) < 6 or packet[2] != 0x01 or packet[3] != 0x81:
            continue

        # Ищем EPC данные
        # Обычно EPC начинается после заголовка (примерно с 7-го байта)
        # Ищем последовательности, которые начинаются с 0x30 или 0x34 (характерно для EPC)
        for j in range(5, len(packet)):
            # Пропускаем одиночные байты и ищем начало EPC
            if packet[j] in (0x30, 0x34):  # Характерное начало EPC
                # Проверяем, что дальше идут данные
                remaining = len(packet) - j
                if remaining >= 14:  # Минимум 14 байт для полного EPC
                    # Извлекаем до 20 байт (40 hex символов)
                    epc_bytes = packet[j:j + min(20, remaining)]

                    # Фильтруем - оставляем только hex-символы
                    hex_str = ''
                    for b in epc_bytes:
                        hex_str += f'{b:02X}'

                    # Проверяем, что строка похожа на EPC (начинается с 30/34 и достаточной длины)
                    if len(hex_str) >= 20:  # Минимум 10 байт = 20 символов
                        # Обрезаем до разумной длины (20-28 символов)
                        for cut_len in [28, 26, 24, 22, 20]:
                            candidate = hex_str[:cut_len]
                            if candidate.startswith(('30', '34')) and candidate not in epc_list:
                                epc_list.append(candidate)
                                break
                    break

    return epc_list


def parse_epc_advanced(data: bytes):
    # Улучшенный парсер EPC
    epc_list = []
    hex_data = data.hex().upper()

    # Ищем EPC по характерным признакам:
    # 1. Начинаются с 3000, 300E, 3400
    # 2. Имеют длину 20-28 символов
    patterns = [
        r'(3000[0-9A-F]{16,24})',  # 3000 + 16-24 hex символов
        r'(300E[0-9A-F]{16,24})',  # 300E + 16-24 hex символов
        r'(3400[0-9A-F]{16,24})',  # 3400 + 16-24 hex символов
    ]

    for pattern in patterns:
        matches = re.findall(pattern, hex_data)
        for match in matches:
            # Оставляем только полные EPC (обычно 24-28 символов)
            if len(match) >= 24:
                # Обрезаем до стандартной длины если нужно
                if len(match) > 28:
                    match = match[:28]
                if match not in epc_list:
                    epc_list.append(match)

    # Если не нашли - пробуем найти любые длинные hex-строки
    if not epc_list:
        long_hex = re.findall(r'([0-9A-F]{24,28})', hex_data)
        for candidate in long_hex:
            if candidate.startswith(('30', '34')) and candidate not in epc_list:
                epc_list.append(candidate)

    return epc_list


# === MAIN ===
if __name__ == "__main__":
    data = read__data()

    # Отладка: покажем сырые данные
    print(f"RawData({len(data)}bytes):[{data.hex().upper()}]", file=sys.stderr)

    tags = parse_epc_advanced(data)

    for epc in tags:
        print(epc)

    print(f"found={len(tags)}epc")
    sys.exit(0 if tags else 1)