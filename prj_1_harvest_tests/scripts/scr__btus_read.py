#!/usr/bin/env python3
"""
Сбор данных с ультразвуковых BLE датчиков UltraSonic.
Запуск: python3 /tmp/bt_ultrasonic.py [-m MAC] [-p PACKETS_MAX] [-t TIMEOUT]
"""

from typing import *
import sys
import time
import asyncio
import argparse
import re
from bleak import BleakScanner, BleakClient, BLEDevice

# ======================================================================================================================
TX_UUID = "dec01433-ceb1-cec0-dec0-ff0123456789"
DEVICE_NAME = "UltraSonic"


# ======================================================================================================================
async def bt_device__get_mac_by_name(name: str) -> str | None:
    print("bt_device__find", flush=True)
    for step in range(1):
        print(f"scan {step=}")
        device = await BleakScanner.find_device_by_name(name, timeout=10.0)
        if device:
            print(f"DEVICE_FOUND:{device.address}", flush=True)
            return device.address

    print(f"ERROR:device_not_found {name=}", flush=True)


# ======================================================================================================================
async def main():
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(
        description="Сбор данных с ультразвуковых BLE датчиков UltraSonic",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %(prog)s
  %(prog)s -m AA:BB:CC:DD:EE:FF
  %(prog)s --mac AA:BB:CC:DD:EE:FF -p 5 -t 30
  %(prog)s -t 15 -p 2
  %(prog)s --pockets 10 --timeout 60
        """
    )

    parser.add_argument(
        '-m', '--mac',
        type=str,
        default=None,
        help='MAC-адрес устройства (если не указан, будет выполнен поиск по имени)'
    )

    parser.add_argument(
        '-t', '--timeout',
        type=float,
        default=20.0,
        help='Таймаут ожидания в секундах (по умолчанию: 20.0)'
    )

    parser.add_argument(
        '-p', '--pockets',
        type=int,
        default=3,
        help='Количество пакетов для сбора (по умолчанию: 3)'
    )

    args = parser.parse_args()

    device_mac = args.mac or await bt_device__get_mac_by_name(DEVICE_NAME)
    if not device_mac:
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
        async with BleakClient(device_mac) as client:
            if not client.is_connected:
                print("ERROR:connect_failed", flush=True)
                return

            print("CONNECTED", flush=True)
            await client.start_notify(TX_UUID, callback__on_new_line)
            print("wait msgs", flush=True)

            # Ждем нужное количество пакетов или таймаут
            start = time.time()
            while True:
                if len(packets) >= args.pockets:
                    print(f"stop_listen: pockets={args.pockets}")
                    break
                if (time.time() - start) >= args.timeout:
                    print(f"stop_listen: timeout={args.timeout}")
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