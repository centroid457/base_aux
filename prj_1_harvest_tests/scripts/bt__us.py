#!/usr/bin/env python3
"""
Сбор данных с ультразвуковых BLE датчиков UltraSonic.
Запуск: python3 /tmp/bt_ultrasonic.py [PACKETS_MAX] [TIMEOUT]
"""

from typing import *
import sys
import time
import asyncio
import re
from bleak import BleakScanner, BleakClient, BLEDevice


# ======================================================================================================================
TX_UUID = "dec01433-ceb1-cec0-dec0-ff0123456789"
DEVICE_NAME = "UltraSonic"

PACKETS_MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 3
TIMEOUT = float(sys.argv[2]) if len(sys.argv) > 2 else 20.0

# Паттерны полей (датчик шлет каждое поле отдельным уведомлением)
_FIELD_PATTERNS = {
    "UTC": r'"UTC":\s*"?(\d+)"?',
    "Distance up": r'"Distance up":\s*"?([\d.]+)"?',
    "Distance side": r'"Distance side":\s*"?([\d.]+)"?',
    "Temperature": r'"Temperature":\s*"?([\d.]+)"?',
    "Battery": r'"Battery":\s*"?([\d.]+)"?',
    "Percentage": r'"Percentage":\s*"?([\d.]+)"?',
}


# ======================================================================================================================
async def bt_device__find(name: str) -> BLEDevice | None:
    print("bt_device__find", flush=True)
    device = None
    for step in range(5):
        print(f"scan {step=}")
        device = await BleakScanner.find_device_by_name(name, timeout=2.0)
        if device:
            break

    if device:
        print(f"DEVICE_FOUND:{device.address}", flush=True)
    else:
        print("ERROR:device_not_found", flush=True)

    return device


# ======================================================================================================================
async def main():
    device = await bt_device__find(DEVICE_NAME)
    if not device:
        return

    # 2. Подключение и сбор
    packets: list[bytes] = []
    new_packet: list[bytes] = []

    def callback__on_new_line(_sender, line: bytearray) -> None:
        nonlocal packets, new_packet

        print(f"raw_bytearray=[", line, "]", sep="")
        line_bytes = bytes(line)
        print(f"raw_bytes=[", line_bytes, "]", sep="")
        # text_line = line.decode('utf8', errors='replace')
        # print(f"text_line=[{text_line}]")
        new_packet.append(line_bytes)

        if b"Percentage" in line_bytes and new_packet:
            new_packet__bytes: bytes = b"\n".join(new_packet)
            packets.append(new_packet__bytes)
            print(f"PACKET_FINISHED:[{new_packet__bytes}]", flush=True)
            print(f"PACKET_HEX:[{new_packet__bytes.hex().upper()}]", flush=True)
            new_packet = []

    try:
        print("TRY:connect", flush=True)
        async with BleakClient(device.address) as client:
            if not client.is_connected:
                print("ERROR:connect_failed", flush=True)
                return

            print("CONNECTED", flush=True)
            await client.start_notify(TX_UUID, callback__on_new_line)
            print("wait msgs", flush=True)

            # Ждем нужное количество пакетов или таймаут
            start = time.time()
            while True:
                if len(packets) >= PACKETS_MAX:
                    print(f"stop_listen: {PACKETS_MAX=}")
                    break
                if (time.time() - start) >= TIMEOUT:
                    print(f"stop_listen: {TIMEOUT=}")
                    break

                await asyncio.sleep(0.2)

            await client.stop_notify(TX_UUID)

    except Exception as exc:
        print(f"ERROR connection:{exc!r}", flush=True)

    # 3. Результат
    print(f"PACKETS_COUNT:{len(packets)}", flush=True)

    if packets:
        print(f"ALL_PACKETS:")
        for pkt in packets:
            """
            ALL_PACKETS:
	b'"UTC":329571\n"Distance up":058\n"Distance side":000\n"Temperature":022\n"Battery":099\n"Percentage":022'
	b'"UTC":329576\n"Distance up":058\n"Distance side":000\n"Temperature":022\n"Battery":099\n"Percentage":022'
	b'"UTC":329581\n"Distance up":058\n"Distance side":000\n"Temperature":022\n"Battery":099\n"Percentage":022'
            """
            print(f"\t{pkt}")

    print(f"FINISHED")


# ======================================================================================================================
if __name__ == "__main__":
    asyncio.run(main())


# ======================================================================================================================
