#!/usr/bin/env python3
# Скрипт для чтения данных с ультразвуковых BLE датчиков.
import sys
import time
import asyncio
from bleak import BleakScanner, BleakClient

UART_TX_UUID = "dec01433-ceb1-cec0-dec0-ff0123456789"
DEVICE_NAME = "UltraSonic"
TIMEOUT = 15
PACKETS_MIN = 3

async def main():
    target_mac = sys.argv[1] if len(sys.argv) > 1 else None

    print("SCAN_START", flush=True)

    # 1. Поиск устройства
    device = None
    if target_mac:
        device = await BleakScanner.find_device_by_address(target_mac, timeout=5.0)
        if device:
            print(f"DEVICE_FOUND_BY_MAC:{device.address}", flush=True)

    if not device:
        device = await BleakScanner.find_device_by_name(DEVICE_NAME, timeout=10.0)
        if device:
            print(f"DEVICE_FOUND:{device.address}", flush=True)

    if not device:
        print("ERROR:Device not found")
        return

    # 2. Подключение и сбор данных
    packets = []
    start_time = time.time()

    def on_data(sender, data):
        try:
            msg = data.decode('utf-8', errors='replace').strip()
            if msg:
                packets.append(msg)
                print(f"PACKET:{msg}", flush=True)
        except Exception:
            pass

    try:
        print("CONNECTING...", flush=True)
        async with BleakClient(device.address, timeout=15.0) as client:
            print(f"CONNECTED:{client.is_connected}", flush=True)

            if not client.is_connected:
                print("ERROR:Connection failed")
                return

            await client.start_notify(UART_TX_UUID, on_data)
            print("WAITING_DATA...", flush=True)

            while len(packets) < PACKETS_MIN and (time.time() - start_time) < TIMEOUT:
                await asyncio.sleep(0.1)

            await client.stop_notify(UART_TX_UUID)
            print("DISCONNECTED", flush=True)

    except Exception as e:
        print(f"ERROR:{e}", flush=True)
        return

    print(f"PACKETS_COUNT:{len(packets)}", flush=True)
    if packets:
        print(f"LAST_PACKET:{packets[-1]}", flush=True)
    print("DONE", flush=True)

if __name__ == "__main__":
    asyncio.run(main())