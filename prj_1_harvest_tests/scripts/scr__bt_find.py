#!/usr/bin/env python3
"""
Сбор данных с ультразвуковых BLE датчиков UltraSonic.
Запуск: python3 /tmp/bt_get_mac.py [-n NAME] [-t TIMEOUT]
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
async def bt_device__get_mac_by_name(name: str, timeout: float = 10) -> str | None:
    print("bt_device__find", flush=True)
    for step in range(1):
        print(f"{step=}", flush=True)
        device = await BleakScanner.find_device_by_name(name, timeout=timeout)
        if device:
            print(f"{device.address}", flush=True)
            return device.address

    print(f"ERROR: NOTFOUND {name=}", flush=True)


# ======================================================================================================================
async def main():
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(
        description="Сбор данных с ультразвуковых BLE датчиков UltraSonic",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %(prog)s
  %(prog)s -n Ultrasonic
  %(prog)s --name Ultrasonic -t 10
        """
    )

    parser.add_argument(
        '-n', '--name',
        type=str,
        default=DEVICE_NAME,
        help='NAME устройства'
    )

    parser.add_argument(
        '-t', '--timeout',
        type=float,
        default=20.0,
        help='Таймаут ожидания в секундах (по умолчанию: 20.0)'
    )
    print(1)
    args = parser.parse_args()
    print(2)
    await bt_device__get_mac_by_name(args.name, args.timeout)


# ======================================================================================================================
if __name__ == "__main__":
    asyncio.run(main())


# ======================================================================================================================
