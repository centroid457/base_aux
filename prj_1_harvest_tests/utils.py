from typing import *

import time
import re
import threading
import json
import logging
import base64

from base_aux.buses.d1_serial2_new.m1_serial_client import SerialClient2
from base_aux.aux_eq.m3_eq_valid3_derivatives import *


# ======================================================================================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ======================================================================================================================
SCRIPTS: dict[str, str] = {     # PATH/TEXT
    # ------------------------------------------------------------------------------------------------------------------
    "/tmp/get__gnss_info__ubx.py": r"""
import serial, time

SOURCE_ADR: str = '/dev/ttyUSB0'
START_UBX: bytes = b'\xb5\x62'
MAX_BUFFER: int = 1000

s = serial.Serial(SOURCE_ADR, 9600, timeout=0.8)
time.sleep(0.3)
s.reset_input_buffer()            # clear previous NMEA
s.write(b'\xb5\x62\x0a\x04\x00\x00\x0e\x34')   # UBX MON-VER

buf = b''
while True:
    byte = s.read(1)
    if not byte:
        break   # timeout

    buf += byte

    if buf[-2:] == START_UBX:
        # дождались синхробайтов – читаем остаток заголовка
        header_rest = s.read(4)
        if len(header_rest) < 4:
            break   # timeout

        expected_load_length = int.from_bytes(header_rest[2:4], 'little')
        # payload + checksum(2 байта)
        load_with_checksum = s.read(expected_load_length + 2)
        if len(load_with_checksum) < expected_load_length + 2:
            break   # timeout

        full_msg: bytes = START_UBX + header_rest + load_with_checksum
        # send data in hex view
        print('UBX_RESPONSE:[' + full_msg.hex() + ']')
        break

    if len(buf) >= MAX_BUFFER:
        break

s.close()
    """,
    #     get__gnss_info__ubx = r"""
    # import serial, time, re
    # s = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.8)
    # time.sleep(0.3)
    # s.reset_input_buffer()  # если не сделать то будут сыпаться NMEA $GPGSV / ...
    # # Дадим модулю время, чтобы он мог выдать идентификационные NMEA-строки (u-blox часто шлёт $GPTXT)
    # data0_first = s.read(2048)
    # # print('ORIGINAL:' + data0_first.decode(errors='ignore'))
    #
    # while True:
    #     # 1=UBX_TXT -------------------------------
    #     data1_ubx_txt = re.findall(rb'\$GPTXT,.*', data0_first)
    #     if data1_ubx_txt:
    #         print('UBX_TXT:' + data1_ubx_txt[0].decode(errors='ignore'))
    #         break
    #
    #     # 2=UBX_RESPONSE---------------------------
    #     # u-blox UBX MON-VER
    #     # Очищаем буфер перед UBX, чтобы не было старых NMEA
    #     s.reset_input_buffer()
    #     s.write(b'\xb5\x62\x0a\x04\x00\x00\x0e\x34')
    #     time.sleep(0.5)
    #     data2_ubx_resp = s.read(256)
    #     if b'\xb5\x62\x0a\x04' in data2_ubx_resp:
    #         # print(data2_ubx_resp)
    #         # print(data2_ubx_resp.hex())
    #
    #         # raw=b'\xb5b\n\x04\xfa\x00EXT CORE 3.01 (107900)\x00\x00\x00\x00\x00\x00\x00\x0000080000\x00\x00ROM BASE 3.01 (107888)\x00\x00\x00\x00\x00\x00\x00\x00FWVER=SPG 3.01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00PROTVER=18.00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00MOD=NEO-M8N-0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00FIS=0xEF4015 (100111)\x00\x00\x00\x00\x00\x00\x00\x00\x00GPS;GLO;GAL;BDS\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00SBAS;IMES;QZSS\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    #         # hex=b5620a04fa0045585420434f524520332e3031202831303739303029000000000000000030303038303030300000524f4d204241534520332e3031202831303738383829000000000000000046575645523d53504720332e30310000000000000000000000000000000050524f545645523d31382e303000000000000000000000000000000000004d4f443d4e454f2d4d384e2d3000000000000000000000000000000000004649533d30784546343031352028313030313131290000000000000000004750533b474c4f3b47414c3b424453000000000000000000000000000000534241533b494d45533b515a535300000000000000000000000000000000
    #
    #         print(f'UBX_RESPONSE:[{data2_ubx_resp.hex()}]')
    #         break
    #
    #     # 3=MTK_RESPONSE---------------------------
    #     # MediaTek PMTK запрос версии
    #     s.reset_input_buffer()
    #     s.write(b'$PMTK605*31\r\n')
    #     time.sleep(0.3)
    #     data3_mtk_resp = s.read(256)
    #     if b'$PMTK' in data3_mtk_resp:
    #         print('MTK_RESPONSE:' + data3_mtk_resp.decode(errors='ignore'))
    #         break
    #
    #     # 4=NO_IDENT---------------------------
    #     # Если ничего не получено – печатаем начало сырых данных
    #     if not (data1_ubx_txt or data2_ubx_resp or data3_mtk_resp):
    #         print('NO_IDENT:' + data0_first[:200].hex())
    #         break
    #
    #     break
    #
    # s.close()
    # time.sleep(0.1)
    # """

    # ------------------------------------------------------------------------------------------------------------------
    "/tmp/at_client.py": r"""
import sys, time, serial, os

if len(sys.argv) < 2:
    print("Usage: python3 /tmp/at_client.py <AT command> [port] [baudrate]")
    sys.exit(1)

cmd = sys.argv[1]
port = sys.argv[2] if len(sys.argv) > 2 else "/dev/ttyUSB2"
baudrates = [115200, 9600, 57600, 38400, 19200]
if len(sys.argv) > 3:
    baudrates = [int(sys.argv[3]), ]

# Попытка освободить порт, если занят
os.system(f"fuser -k {port} 2>/dev/null")
time.sleep(0.4)

last_err = None
for baud in baudrates:
    try:
        s = serial.Serial(
            port, 
            baud, 
            timeout=0.3,
            rtscts=False, dsrdtr=False, exclusive=True)
        s.reset_input_buffer()
        s.write((cmd + "\r\n").encode())
        time.sleep(0.5)
        result = s.read(4096).decode(errors='replace')
        print(result)
        s.close()
        sys.exit(0)
    except Exception as exc:
        last_err = exc
        print(f"AT_ERROR:{exc!r}")
        try: 
            s.close()
        except:
            pass
        continue

print(f"AT_ERROR:{last_err!r}")
sys.exit(1)
    """,

    # ------------------------------------------------------------------------------------------------------------------
    "/tmp/rfid_e710.py": """
import serial
import time

print("START", "="*50)
    
try:
    ser = serial.Serial(
        port='/dev/ttyS2',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
    dataread = "a00a018101000800000000cb"
    values = bytearray([160, 10, 1, 129, 1, 0, 8, 0, 0, 0, 0, 203])    
    for step in range(3):
        print()
        print(f'{step=}')
        print("WRITE=", values)
        x = ser.write(values)
        result = b""
        while True:
            time.sleep(0.2)
            read_byte = ser.read(1)
            if read_byte:
                result += read_byte
            else:
                print(f"READ_{i}=", result)
                break
                
        time.sleep(0.75)
         
except Exception as exc:
    print(f"EXC={exc!r}")

if ser and ser.is_open:
    ser.close()

print("FINISH", "="*50)
    """,

    # ------------------------------------------------------------------------------------------------------------------
    "/tmp/rfid_scan.py": """
# ===================================================================
# /tmp/rfid_scan.py - компактный сканер RFID
# ===================================================================
import serial, time, sys

# Конфиг
PORT = '/dev/ttyS2'
BAUD = 115200
TIMEOUT = 0.5

# Команда чтения
CMD = bytes([0xA0, 0x0A, 0x01, 0x81, 0x01, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0xCB])

# Служебные EPC (фильтруем)
SERVICE_EPC = {
    "010000000000000000000051",
    "010000000000000000000680",
    "401400000000000019000001",
    "404200000000000019000003",
}

def read_response():
    # Отправить команду и прочитать ответ
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

def parse_epc(data):
    # Извлечь EPC из ответа
    epc_list = []
    i = 0
    while i < len(data):
        if data[i] != 0xA0:
            i += 1
            continue
        if i + 1 >= len(data):
            break
            
        length = data[i+1]
        if i + length + 1 > len(data):
            i += 1
            continue
            
        packet = data[i:i+length+1]
        i += length + 1
        
        # Проверяем, что это ответ на чтение
        if len(packet) < 6 or packet[2] != 0x01 or packet[3] != 0x81:
            continue
        
        # Ищем EPC в данных пакета
        for offset in range(6, len(packet) - 12):
            chunk = packet[offset:offset+12]
            # Проверяем: не нулевой, не служебный
            if any(chunk) and chunk[0] not in (0x00, 0x20, 0x30, 0x34, 0xE2):
                epc = chunk.hex().upper()
                if epc not in epc_list and epc not in SERVICE_EPC:
                    epc_list.append(epc)
                break  # нашли EPC в этом пакете, выходим
    
    return epc_list

# === MAIN ===
if __name__ == "__main__":
    data = read_response()
    tags = parse_epc(data)
    
    for epc in tags:
        print(epc)
    
    print(f"found={len(tags)}epc")
    sys.exit(0 if tags else 1)
    """,



    "/tmp/explore__rfid_full_tries.py": """
# /tmp/rfid_full_diag.py
import serial
import time
import sys

def read_all_data(ser, timeout=1.0):
    # Прочитать все данные из порта.
    response = b""
    start = time.time()
    while time.time() - start < timeout:
        chunk = ser.read(1024)
        if chunk:
            response += chunk
        else:
            time.sleep(0.05)
    return response

def parse_epc_from_response(response):
    # Извлечь все EPC из ответа
    epc_list = []
    i = 0
    while i < len(response):
        if response[i] == 0xA0:
            if i + 1 < len(response):
                length = response[i+1]
                if i + length + 1 <= len(response):
                    packet = response[i:i+length+1]
                    if len(packet) >= 6 and packet[2] == 0x01 and packet[3] == 0x81:
                        # Ищем EPC в данных
                        for offset in range(6, len(packet) - 12):
                            chunk = packet[offset:offset+12]
                            # EPC: 12 байт, не все нули, не служебные (0x20, 0x30, 0x34, 0xE2)
                            if any(chunk) and chunk[0] not in [0x20, 0x30, 0x34, 0xE2]:
                                epc = chunk.hex().upper()
                                if len(epc) == 24:
                                    epc_list.append(epc)
                                    break
                    i += length + 1
                    continue
        i += 1
    return epc_list

def print_packet_analysis(packet, label=""):
    # Детальный анализ одного пакета
    if not packet or packet[0] != 0xA0:
        return
    
    print(f"{label}")
    print(f"  HEX: {packet.hex()}")
    print(f"  LEN: {len(packet)} bytes")
    
    if len(packet) >= 6:
        print(f"  Header: {packet[0]:02X}")
        print(f"  Length: {packet[1]} bytes")
        print(f"  CMD: {packet[2]:02X}")
        print(f"  Status: {packet[3]:02X}")
        if len(packet) > 4:
            print(f"  Data len: {packet[4]:02X}{packet[5]:02X}")
            if len(packet) > 6:
                print(f"  Data: {packet[6:].hex()}")
                
                # Ищем EPC в данных
                for offset in range(6, len(packet) - 12):
                    chunk = packet[offset:offset+12]
                    if any(chunk) and chunk[0] not in [0x20, 0x30, 0x34, 0xE2]:
                        epc = chunk.hex().upper()
                        if len(epc) == 24:
                            print(f"  ★ EPC at offset {offset}: {epc}")

print("="*60)
print("RFID E710 FULL DIAGNOSTIC")
print("="*60)

# ===================================================================
# 1. ИНФОРМАЦИЯ О РИДЕРЕ (версия прошивки, параметры)
# ===================================================================
print("="*60)
print("1. READER INFO (firmware, version)")
print("="*60)

info_commands = {
    "VERSION": bytes([0xA0, 0x05, 0x01, 0x81, 0x00, 0x00, 0x00, 0x00]),
    "READER_INFO": bytes([0xA0, 0x06, 0x01, 0x81, 0x00, 0x00, 0x00, 0x00]),
    "GET_CONFIG": bytes([0xA0, 0x07, 0x01, 0x81, 0x00, 0x00, 0x00, 0x00, 0x00]),
    "GET_FW_VERSION": bytes([0xA0, 0x08, 0x01, 0x81, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
}

for name, cmd in info_commands.items():
    print(f"--- {name} ---")
    try:
        ser = serial.Serial('/dev/ttyS2', 115200, timeout=0.5)
        ser.reset_input_buffer()
        ser.write(cmd)
        time.sleep(0.3)
        response = read_all_data(ser, timeout=0.5)
        ser.close()
        
        if response:
            print(f"Response ({len(response)} bytes): {response.hex()}")
            # Парсим пакеты
            i = 0
            while i < len(response):
                if response[i] == 0xA0 and i + 1 < len(response):
                    length = response[i+1]
                    if i + length + 1 <= len(response):
                        packet = response[i:i+length+1]
                        print_packet_analysis(packet, f"  Packet at {i}")
                        i += length + 1
                        continue
                i += 1
        else:
            print("  No response")
    except Exception as e:
        print(f"  Error: {e}")

# ===================================================================
# 2. ИНВЕНТАРИЗАЦИЯ (поиск ВСЕХ меток)
# ===================================================================
print("="*60)
print("2. INVENTORY (find ALL tags)")
print("="*60)

inventory_commands = {
    "INV_6": bytes([0xA0, 0x06, 0x01, 0x81, 0x00, 0x00, 0x00, 0x00]),
    "INV_7": bytes([0xA0, 0x07, 0x01, 0x81, 0x00, 0x00, 0x00, 0x00, 0x00]),
    "INV_8": bytes([0xA0, 0x08, 0x01, 0x81, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    "INV_9": bytes([0xA0, 0x09, 0x01, 0x81, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    "INV_10": bytes([0xA0, 0x0A, 0x01, 0x81, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
}

all_epc = []
for name, cmd in inventory_commands.items():
    print(f"--- {name} ---")
    try:
        ser = serial.Serial('/dev/ttyS2', 115200, timeout=0.5)
        ser.reset_input_buffer()
        ser.write(cmd)
        time.sleep(0.5)  # Даём время на инвентаризацию
        response = read_all_data(ser, timeout=1.0)
        ser.close()
        
        if response:
            print(f"Response ({len(response)} bytes): {response.hex()[:100]}...")
            epc_list = parse_epc_from_response(response)
            if epc_list:
                print(f"  ★ Found {len(epc_list)} EPC(s):")
                for epc in epc_list:
                    print(f"    - {epc}")
                    if epc not in all_epc:
                        all_epc.append(epc)
            else:
                # Показываем структуру пакетов
                i = 0
                while i < len(response):
                    if response[i] == 0xA0 and i + 1 < len(response):
                        length = response[i+1]
                        if i + length + 1 <= len(response):
                            packet = response[i:i+length+1]
                            print_packet_analysis(packet, f"  Packet at {i}")
                            i += length + 1
                            continue
                    i += 1
        else:
            print("  No response")
    except Exception as e:
        print(f"  Error: {e}")

# ===================================================================
# 3. РЕЖИМ ЧТЕНИЯ (текущая команда)
# ===================================================================
print("="*60)
print("3. READ BANK (your current command)")
print("="*60)

read_cmd = bytes([0xA0, 0x0A, 0x01, 0x81, 0x01, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0xCB])

for attempt in range(3):
    print(f"--- Read attempt {attempt+1} ---")
    try:
        ser = serial.Serial('/dev/ttyS2', 115200, timeout=0.5)
        ser.reset_input_buffer()
        ser.write(read_cmd)
        time.sleep(0.3)
        response = read_all_data(ser, timeout=1.0)
        ser.close()
        
        if response:
            print(f"Response ({len(response)} bytes)")
            epc_list = parse_epc_from_response(response)
            if epc_list:
                print(f"  ★ Found {len(epc_list)} EPC(s):")
                for epc in epc_list:
                    print(f"    - {epc}")
                    if epc not in all_epc:
                        all_epc.append(epc)
            else:
                print("  No EPC found in response")
                # Показываем первый пакет
                i = 0
                while i < len(response):
                    if response[i] == 0xA0 and i + 1 < len(response):
                        length = response[i+1]
                        if i + length + 1 <= len(response):
                            packet = response[i:i+length+1]
                            print_packet_analysis(packet, f"  Packet at {i}")
                            i += length + 1
                            continue
                    i += 1
        else:
            print("  No response")
        time.sleep(0.5)
    except Exception as e:
        print(f"  Error: {e}")

# ===================================================================
# 4. РЕЖИМ НЕПРЕРЫВНОГО ЧТЕНИЯ
# ===================================================================
print("="*60)
print("4. CONTINUOUS READ (3 attempts)")
print("="*60)

for i in range(3):
    print(f"--- Read {i+1} ---")
    try:
        ser = serial.Serial('/dev/ttyS2', 115200, timeout=0.5)
        ser.reset_input_buffer()
        ser.write(read_cmd)
        time.sleep(0.3)
        response = read_all_data(ser, timeout=0.8)
        ser.close()
        
        epc_list = parse_epc_from_response(response)
        if epc_list:
            print(f"  Found: {', '.join(epc_list)}")
            for epc in epc_list:
                if epc not in all_epc:
                    all_epc.append(epc)
        else:
            print("  No tags")
        time.sleep(0.5)
    except Exception as e:
        print(f"  Error: {e}")

# ===================================================================
# 5. ИТОГОВЫЙ ОТЧЕТ
# ===================================================================
print("="*60)
print("5. SUMMARY")
print("="*60)

if all_epc:
    print(f"★ Total unique EPCs found: {len(all_epc)}")
    for idx, epc in enumerate(all_epc, 1):
        print(f"  Tag {idx}: {epc}")
else:
    print("No tags found!")

# Проверяем, сколько меток физически на антенне
print("="*60)
print("RECOMMENDATIONS")
print("="*60)

if len(all_epc) == 0:
    print("1. No tags detected - check antenna connection")
    print("2. Make sure tags are UHF RFID EPC Class 1 Gen 2")
    print("3. Try placing tags closer to antenna")
elif len(all_epc) == 1:
    print("1. Only one tag detected - good for testing")
    print("2. Try adding more tags to test multi-tag reading")
elif len(all_epc) >= 2:
    print(f"★ {len(all_epc)} tags detected - system working correctly!")
    print("1. Multi-tag reading works")
    print("2. You can now implement tag inventory in your application")
    
print("="*60)
    """,
}


# ======================================================================================================================
class HarvestDevice:
    COMPILE_EOF__STR = re.compile(r".+@.+:.*#\s*")
    AT_CMD__DUMP: list[str] = [
        # =========================================================================
        "AT",  # ответ эхо - проверка функционирования модема на канал


        # =========================================================================
        # ИДЕНТИФИКАЦИЯ И ВЕРСИИ
        "ATI",  # Общая информация о производителе/модели
        "AT+CGMI",  # Запрос производителя (Manufacturer ID)
        "AT+CGMM",  # Запрос модели (Model ID)
        "AT+CGMR",  # Запрос ревизии прошивки (Revision)
        "AT+CGSN",  # Запрос IMEI (Serial Number)
        "AT+CIMI",  # Запрос IMSI (International Mobile Subscriber ID)
        "AT+GSN",  # Аналог CGSN — IMEI

        # =========================================================================
        # СОСТОЯНИЕ SIM-КАРТЫ И PIN
        "AT+CPIN?",  # Статус SIM: READY, SIM PIN, SIM PUK, SIM PIN2...
        # "AT+CPINR=\"SIM PIN\"",  # Остаток попыток ввода PIN
        # "AT+CPINR=\"SIM PUK\"",  # Остаток попыток ввода PUK
        "AT+CCID",  # ICCID (серийный номер SIM-карты)

        # =========================================================================
        # СЕТЬ И РЕГИСТРАЦИЯ
        "AT+COPS?",  # Текущий оператор (режим, формат, MCC/MNC)
        # "AT+COPS=3,2; +COPS?",  # Принудительно числовой формат + получить оператора
        "AT+CREG?",  # Статус регистрации в сети (0=нет, 1=домашняя, 5=роуминг)
        "AT+CGREG?",  # Статус GPRS/PS регистрации
        "AT+CEREG?",  # Статус EPS (LTE) регистрации

        # =========================================================================
        # УРОВЕНЬ СИГНАЛА И КАЧЕСТВО
        "AT+CSQ",  # RSSI (0-31) и BER (качество канала)
        "AT+CESQ",  # Расширенный запрос качества (RSSI, RSCP, ECN0, RSRP, RSRQ)

        # =========================================================================
        # ТЕКУЩАЯ СОТА И ЧАСТОТА
        "AT*CNTI=0",  # Информация о текущей соте (MCC, MNC, LAC, CellID, band, ARFCN)

        # =========================================================================
        # ТЕХНОЛОГИЯ РАДИОДОСТУПА (RAT)
        "AT+WS46?",  # Выбор технологии: 12=LTE, 2=3G, 0=2G/GERAN
        # "AT+COPS=3,2; +COPS?",  # (повтор для получения RAT в числовом виде)

        # =========================================================================
        # PDP / APN / ДАННЫЕ
        "AT+CGDCONT?",  # Список APN-профилей (apn, type, ip...)
        "AT+CGCONTRDP",  # Параметры активного PDP-контекста (IP, шлюз, DNS1, DNS2)
        "AT+CGPADDR",  # Список назначенных PDP-адресов (IP)
        "AT+CGACT?",  # Статус активации PDP-контекстов (0/1)
        "AT+CGATT?",  # Статус GPRS-присоединения (attached/detached)
        # "AT+CGDATA=\"PPP\"",  # Состояние data-вызова (idle/active)

        # =========================================================================
        # IMS (VoLTE / VoWiFi)
        "AT+CIMS?",  # Статус IMS-регистрации (0=не зарегистрирован, 1=зарегистрирован)
        "AT+CIREG?",  # IMS регистрация (более детально)

        # =========================================================================
        # РЕЖИМЫ ЭНЕРГОСБЕРЕЖЕНИЯ И ФУНКЦИОНАЛЬНОСТЬ
        "AT+CFUN?",  # Уровень функциональности (0=min, 1=full, 4=flight mode)
        "AT+CSCLK?",  # Режим сна (1=разрешён sleep mode)

        # =========================================================================
        # ТЕМПЕРАТУРА И ПИТАНИЕ
        "AT+CPMUTEMP?",  # Температура модуля (если поддерживается)
        "AT+CBC",  # Заряд батареи/питание (charge level, voltage)

        # =========================================================================
        # СОСЕДНИЕ СОТЫ (опционально, зависит от модуля)
        "AT+CCED?",  # Соседние соты (GSM/GPRS)
        "AT*CELLINFO?",  # Расширенная информация о сотах (vendor-specific)

        # =========================================================================
        # ОШИБКИ И СБРОСЫ (диагностика)
        "AT+CEER",  # Extended Error Report — причина последнего сбоя/разъединения
    ]

    def __init__(self, conn: SerialClient2):
        self.conn = conn
        self.hostname = None

    # ------------------------------------------------------------------------------------------------------------------
    def validate_conn(self) -> bool:
        """
        ============LOGIN
        harvest05 login:
        ---- Sent utf8 encoded message: "root\r\n" ----
        root
        Password:
        ---- Sent utf8 encoded message: "1\r\n" ----

        Linux harvest05 4.14.111 #193 SMP Thu Jun 10 18:20:47 CST 2021 armv7l

        The programs included with the Debian GNU/Linux system are free software;
        the exact distribution terms for each program are described in the
        individual files in /usr/share/doc/*/copyright.

        Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
        permitted by applicable law.
        Last login: Wed Jul 22 18:37:34 MSK 2026 on ttyS0
        root@harvest05:

        ===============secondary LOGGED_IN
        root@harvest05:~#
        ---- Sent utf8 encoded message: "root\r\n" ----
        root
        -bash: root: command not found
        root@harvest05:~#
        root@harvest05:~#
        """
        return (
                self.login_try()
                and
                self.login_check()
        )

    def login_try(self) -> bool:
        """
        harvest05 login:
        ---- Sent utf8 encoded message: "root\r\n" ----
        root
        Password:
        ---- Sent utf8 encoded message: "1\r\n" ----

        Linux harvest05 4.14.111 #193 SMP Thu Jun 10 18:20:47 CST 2021 armv7l

        The programs included with the Debian GNU/Linux system are free software;
        the exact distribution terms for each program are described in the
        individual files in /usr/share/doc/*/copyright.

        Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
        permitted by applicable law.
        Last login: Tue Aug  4 14:39:52 MSK 2026 on ttyS0
        root@harvest05:~#
        """
        data = self.conn.write_read_bytes(data="root", timeout_continue=0.5)
        if b"command not found" in data:
            # already logged in!
            return True

        elif b"Password:" in data:
            data = self.conn.write_read_bytes(data="1", timeout_start=6, timeout_continue=1.9)
            if b"root@harvest" in data:
                return True

        return False

    def login_check(self) -> bool:
        data = self.cmd_timeout__write_read_lines(cmd="hostname")
        result = bool(self.COMPILE_EOF__STR.search(data))
        return result

    def get_hostname_and_occupy(self) -> str:
        device_name = self.cmd_timeout__write_read__payload(cmd="hostname")
        self.hostname = device_name
        self.conn.occupy(device_name)
        return device_name

    # WR ===============================================================================================================
    def _cmd_cover_timeout(self, cmd: str, timeout: float | None = None) -> str:
        """
        work with SYSTEMD_PAGER

---- Sent utf8 encoded message: "SYSTEMD_PAGER=cat udevadm info -q property -n /dev/ttyUSB0  2>/dev/null\r\n" ----
SYSTEMD_PAGER=cat udevadm info -q property -n /dev/ttyUSB0  2>/dev/null
DEVPATH=/devices/platform/soc/1c1d400.usb/usb8/8-1/8-1:1.0/ttyUSB0/tty/ttyUSB0
DEVNAME=/dev/ttyUSB0
MAJOR=188
MINOR=0
SUBSYSTEM=tty
USEC_INITIALIZED=13287546
ID_BUS=usb
ID_MODEL=USB_Serial
ID_MODEL_ENC=USB\x20Serial
ID_MODEL_ID=7523
ID_SERIAL=1a86_USB_Serial
ID_VENDOR=1a86
ID_VENDOR_ENC=1a86
ID_VENDOR_ID=1a86
ID_REVISION=0264
ID_TYPE=generic
ID_USB_MODEL=USB_Serial
ID_USB_MODEL_ENC=USB\x20Serial
ID_USB_MODEL_ID=7523
ID_USB_SERIAL=1a86_USB_Serial
ID_USB_VENDOR=1a86
ID_USB_VENDOR_ENC=1a86
ID_USB_VENDOR_ID=1a86
ID_USB_REVISION=0264
ID_USB_TYPE=generic
ID_USB_INTERFACES=:ff0102:
ID_USB_INTERFACE_NUM=00
ID_USB_DRIVER=ch341
ID_USB_CLASS_FROM_DATABASE=Vendor Specific Class
ID_VENDOR_FROM_DATABASE=QinHeng Electronics
ID_MODEL_FROM_DATABASE=CH340 serial converter
ID_PATH=platform-1c1d400.usb-usb-0:1:1.0
ID_PATH_TAG=platform-1c1d400_usb-usb-0_1_1_0
ID_MM_CANDIDATE=1
DEVLINKS=/dev/serial/by-path/platform-1c1d400.usb-usb-0:1:1.0-port0 /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0
TAGS=:systemd:
CURRENT_TAGS=:systemd:
root@harvest05:~#
root@harvest05:~#

---- Sent utf8 encoded message: "timeout 4 SYSTEMD_PAGER=cat udevadm info -q property -n /dev/ttyUSB0  2>/dev/null\r\n" ----
timeout 4 SYSTEMD_PAGER=cat udevadm info -q property -n /dev/ttyUSB0  2>/dev/null
root@harvest05:~#
root@harvest05:~#

---- Sent utf8 encoded message: "timeout 4 sh -c 'SYSTEMD_PAGER=cat udevadm info -q property -n /dev/ttyUSB0  2>/dev/null'\r\n" ----
timeout 4 sh -c 'SYSTEMD_PAGER=cat udevadm info -q property -n /dev/ttyUSB0  2>/dev/null'
DEVPATH=/devices/platform/soc/1c1d400.usb/usb8/8-1/8-1:1.0/ttyUSB0/tty/ttyUSB0
DEVNAME=/dev/ttyUSB0
MAJOR=188
MINOR=0
SUBSYSTEM=tty
USEC_INITIALIZED=13287546
ID_BUS=usb
ID_MODEL=USB_Serial
ID_MODEL_ENC=USB\x20Serial
ID_MODEL_ID=7523
ID_SERIAL=1a86_USB_Serial
ID_VENDOR=1a86
ID_VENDOR_ENC=1a86
ID_VENDOR_ID=1a86
ID_REVISION=0264
ID_TYPE=generic
ID_USB_MODEL=USB_Serial
ID_USB_MODEL_ENC=USB\x20Serial
ID_USB_MODEL_ID=7523
ID_USB_SERIAL=1a86_USB_Serial
ID_USB_VENDOR=1a86
ID_USB_VENDOR_ENC=1a86
ID_USB_VENDOR_ID=1a86
ID_USB_REVISION=0264
ID_USB_TYPE=generic
ID_USB_INTERFACES=:ff0102:
ID_USB_INTERFACE_NUM=00
ID_USB_DRIVER=ch341
ID_USB_CLASS_FROM_DATABASE=Vendor Specific Class
ID_VENDOR_FROM_DATABASE=QinHeng Electronics
ID_MODEL_FROM_DATABASE=CH340 serial converter
ID_PATH=platform-1c1d400.usb-usb-0:1:1.0
ID_PATH_TAG=platform-1c1d400_usb-usb-0_1_1_0
ID_MM_CANDIDATE=1
DEVLINKS=/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0 /dev/serial/by-path/platform-1c1d400.usb-usb-0:1:1.0-port0
TAGS=:systemd:
CURRENT_TAGS=:systemd:
root@harvest05:~#
root@harvest05:~#
        """
        result = ""
        if timeout:
            result += f"timeout {timeout} "

        if cmd.startswith("SYSTEMD_PAGER"):
            cmd = f"sh -c '{cmd}'"

        result += cmd
        return result

    def cmd_timeout__write_bytes(self, cmd: str, timeout: float | None = None) -> bool:
        """
        запуск команды в среде linux с таймаутом в самой система

        2=VARIANT
        --------------------
        ---- Sent utf8 encoded message: "timeout 2 ping ya.ru\r\n" ----
        timeout 2 ping ya.ru
        PING ya.ru (77.88.44.242) 56(84) bytes of data.
        64 bytes from ya.ru (77.88.44.242): icmp_seq=1 ttl=57 time=41.1 ms
        64 bytes from ya.ru (77.88.44.242): icmp_seq=2 ttl=57 time=38.0 ms
        root@harvest05:~#
        root@harvest05:~#
        """
        # return self.conn.write_bytes(f"{cmd} & sleep {timeout}; kill %1")  # OLD-incorrect!
        return self.conn.write_bytes(self._cmd_cover_timeout(cmd, timeout))

    def cmd_timeout__write_read_bytes(self, cmd: str, timeout: float | None = None, **wr_kwargs) -> bytes:
        cmd = self._cmd_cover_timeout(cmd, timeout)
        return self.conn.write_read_bytes(cmd, **wr_kwargs)

    def cmd_timeout__write_read_lines(
            self,
            cmd: str,
            timeout: float | None = None,
            payload_only: bool | None = None,
            **wr_kwargs,
    ) -> str | list[str]:
        cmd = self._cmd_cover_timeout(cmd, timeout)

        if wr_kwargs.get("stop_line") is None:
            if self.hostname:
                pattern = rb".*root@" + self.hostname.encode() + rb":~#.*"
            else:
                pattern = rb".*root@.+:.+#.*"
            stop_line = EqValid_Regexp(pattern)
            wr_kwargs["stop_line"] = stop_line

        result = self.conn.write_read_lines(cmd, **wr_kwargs)
        if payload_only:
            result = self._stdout__parce_payload(cmd=cmd, data=result)

        print(f"[{self.conn.ADDRESS}.WRITEREAD]")
        print(f"\twrite=[", cmd, "]", sep="")
        print("\tread=[", result, "]", sep="")

        return result

    def _stdout__parce_payload(self, cmd: str, data: str | list[str]) -> str | list[str]:
        # 0=split -----------------------
        return_str = False
        if isinstance(data, str):
            return_str = True
            result = data.splitlines()
        else:
            result = data

        # 1=CMD ECHO --------------------
        if result[0].strip() == cmd.strip():
            result = result[1:]

        # 2=EOF -------------------------
        while result and (self.COMPILE_EOF__STR.match(result[-1]) or result[-1].strip() == ''):
            result = result[:-1]

        # 3=SERVICE LOGS ----------------
        # AT": "[1]   Terminated              timeout 2.0 cat /dev/ttyUSB2\nOK"
        # [AT] AT+CSQ ---> at_output='[4] 1836\n[3]   Exit 124                timeout 2.0 cat /dev/ttyUSB2\n+CSQ: 20,99\nOK'
        # Удаляем служебные строки bash о статусе фоновых процессов
        result_clear_service = [
            line for line in result
            if not re.match(r'\s*\[\d+\]\s+(?:Exit|Terminated|Done)?\s*\d*\s*', line)
        ]
        result = result_clear_service

        # 4=EXIT ------------------------
        if return_str:
            return "\n".join(result)
        else:
            return result

    # ------------------------------------------------------------------------------------------------------------------
    def cmd_timeout__write_read__payload(
            self,
            cmd: str,
            timeout_continue: float = 2.0,  # ОБЯЗАТЕЛЬНО!!!
            **wr_kwargs,
    ) -> str:
        """
        Выполняет команду на устройстве и возвращает stdout в виде строки.
        При ошибке возвращает пустую строку.
        """
        return self.cmd_timeout__write_read_lines(
            cmd,
            payload_only=True,
            timeout_continue=timeout_continue,
            **wr_kwargs)

    # ------------------------------------------------------------------------------------------------------------------
    def cmd_timeout__check_executed_success(self, cmd: str, **wr_kwargs) -> bool:
        """
        Проверяет, доступна ли команда в системе linux

        ---- Sent utf8 encoded message: "which picocom\r\n" ----
        which picocom
        /usr/bin/picocom
        root@harvest05:~#
        root@harvest05:~#
        ---- Sent utf8 encoded message: "which picocom22\r\n" ----
        which picocom22
        root@harvest05:~#
        root@harvest05:~#

        ---- Sent utf8 encoded message: "which picocom 2>/dev/null || echo NOT_FOUND\r\n" ----
        which picocom 2>/dev/null || echo NOT_FOUND
        /usr/bin/picocom
        root@harvest05:~#
        root@harvest05:~# [17686.556981] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
        ---- Sent utf8 encoded message: "which picocom1111 2>/dev/null || echo NOT_FOUND\r\n" ----
        which picocom1111 2>/dev/null || echo NOT_FOUND
        NOT_FOUND
        root@harvest05:~#
        root@harvest05:~#
        """
        ERROR_MSG = "ERROR_MSG"
        output = self.cmd_timeout__write_read__payload(f"{cmd} 2>/dev/null || echo {ERROR_MSG}", **wr_kwargs)
        print(f"{output=}")
        return ERROR_MSG not in output

    # ------------------------------------------------------------------------------------------------------------------
    def cmd_parsed__ls(
            self,
            path: str | None = None,
            filters: Base_EqValid | list | None = None,
            **wr_kwargs,
    ) -> list[str]:
        """

        ---- Sent utf8 encoded message: "ls /dev/\r\n" ----
        ls /dev/
        adsp1            kmem              nbd13               stdout  tty36  tty8
        audio            kmsg              nbd14               tty     tty37  tty9
        audio1           kvm               nbd15               tty0    tty38  ttyS0
        audio2           log               nbd2                tty1    tty39  ttyS1
        audio3           loop-control      nbd3                tty10   tty4   ttyS2
        autofs           loop0             nbd4                tty11   tty40  ttyS3
        block            loop1             nbd5                tty12   tty41  ttyS4
        btrfs-control    loop2             nbd6                tty13   tty42  ttyS5
        bus              loop3             nbd7                tty14   tty43  ttyS6
        cec0             loop4             nbd8                tty15   tty44  ttyS7
        char             loop5             nbd9                tty16   tty45  ttyUSB0
        console          loop6             net                 tty17   tty46  urandom
        cpu_dma_latency  loop7             network_latency     tty18   tty47  v4l
        cuse             mapper            network_throughput  tty19   tty48  vcs
        disk             mem               null                tty2    tty49  vcs1
        dri              memory_bandwidth  ppp                 tty20   tty5   vcs2
        dsp              mixer             psaux               tty21   tty50  vcs3
        dsp1             mixer1            ptmx                tty22   tty51  vcs4
        dsp2             mixer2            pts                 tty23   tty52  vcs5
        dsp3             mixer3            random              tty24   tty53  vcs6
        fb0              mmcblk0           rfkill              tty25   tty54  vcsa
        fd               mmcblk0boot0      rtc                 tty26   tty55  vcsa1
        full             mmcblk0boot1      rtc0                tty27   tty56  vcsa2
        fuse             mmcblk0p1         rtc1                tty28   tty57  vcsa3
        gpiochip0        mmcblk0p2         sequencer           tty29   tty58  vcsa4
        gpiochip1        mmcblk0p3         sequencer2          tty3    tty59  vcsa5
        i2c-0            mqueue            serial              tty30   tty6   vcsa6
        i2c-1            nbd0              shm                 tty31   tty60  vhci
        i2c-2            nbd1              snd                 tty32   tty61  video0
        i2c-3            nbd10             spidev0.0           tty33   tty62  watchdog
        initctl          nbd11             stderr              tty34   tty63  watchdog0
        input            nbd12             stdin               tty35   tty7   zero
        root@harvest05:~#
        """
        result = []

        # PATH
        path = path or ""
        if path and not path.endswith("/"):
            path += "/"

        # PAYLOAD
        output = self.cmd_timeout__write_read__payload(
            f"ls {path}",
            timeout=3,
            timeout_continue=1.0,
            **wr_kwargs,
        )

        # SPLIT
        parsed = output.split()

        # FILTER
        for item in parsed:
            item = item.strip()
            if not item:
                continue
            if filters and item not in filters:
                continue

            result.append(f"{path}{item}")
        return result

    # FILES ============================================================================================================
    def file_name__push(self, name: str) -> bool:
        text = SCRIPTS[name]
        return self._file_text__push(filepath=name, text=text)

    def _file_text__push(self, filepath: str = "/tmp/script.py", text: str = "") -> bool:
        """
        GOAL
        transfer file scripts into device,
        """
        # 1=MKDIR --------------------
        splited = filepath.rsplit('/', 1)
        if "/" in filepath:
            if splited[0] == "":
                dirpath = "/"
            else:
                dirpath = splited[0]
        else:
            dirpath = ""

        # mkdir -p создаст путь, если его нет.
        if dirpath not in ["", "/", None]:
            cmd = f"mkdir -p {dirpath}"
            if not self.cmd_timeout__check_executed_success(cmd):
                return False

        # 2=PUSH --------------------
        text_b64 = base64.b64encode(text.encode()).decode()
        # printf не добавляет '\n', в отличие от echo; одинарные кавычки защищают от пробелов.
        cmd = f"printf '%s' '{text_b64}' | base64 -d > {filepath}"
        return self.cmd_timeout__check_executed_success(cmd)

    def file__check_exist(self, filepath: str) -> bool:
        """
        GOAL
        Проверяет наличие скрипта на устройстве
        НЕ ПРОВЕРЯЕТ КОРРЕКТНОСТЬ!
        """
        return self.cmd_timeout__check_executed_success(f"test -f {filepath}")

    # AT ===============================================================================================================
    pass

    # def send__at_command__simple(self, cmd: str, port="/dev/ttyUSB2", timeout=1.0) -> str:
    # НЕ РАБОТАЕТ!!!
    #
    #     full_cmd = (
    #         f"timeout {timeout} bash -c 'echo -e \"{cmd}\\r\\n\" > {port}; "
    #         f"timeout {timeout} cat {port}'"
    #     )
    #     at_output = self.cmd_timeout__write_read__payload_str(full_cmd, timeout=timeout * 2)
    #     # Убираем возможное эхо команды
    #     at_output = at_output.replace(cmd + "\n", "")
    #     print(f"[{at_output=}]")
    #     return at_output
    #
    # def send__at_command__simple(self, cmd: str, port="/dev/ttyUSB2", timeout=1.0) -> str:
    #     """
    #     Отправляет AT-команду через прямой ввод-вывод в порт.
    #     Работает после того, как порт настроен (raw mode + echo off).
    #     """
    #     # Отправить команду, прочитать ответ с таймаутом через утилиту timeout
    #     # - ВАЖНО: bash -c нужен, чтобы пайп обрабатывался целиком
    #     full_cmd = (
    #         f"timeout {timeout} bash -c '"
    #         f"printf \"{cmd}\\r\\n\" > {port}; "
    #         f"timeout {timeout} cat {port}'"
    #     )
    #     at_output = self.cmd_timeout__write_read__payload_str(
    #         full_cmd,
    #         timeout=None,
    #         timeout_continue=timeout * 1.5
    #     )
    #     # Убираем пустые строки и возможное эхо (если echo не выключено)
    #     lines = [line.strip() for line in at_output.split('\n') if line.strip()]
    #     # Отфильтровываем саму команду, если echo ещё активно
    #     lines = [line for line in lines if line != cmd]
    #     at_output = '\n'.join(lines)
    #     print(f"[SIMPLE_AT] {at_output=}")
    #     return at_output

    def at_cmd__simple(self, cmd: str, port="/dev/ttyUSB2", timeout=2.0) -> str:
        """
        Отправить AT-команду на уже настроенный порт (stty raw + echo off).

        SerialClient2(COM16.115200,occupied=o,isopen=True){'write': b"timeout 2 cat /dev/ttyUSB2 & sleep 0.1; printf 'AT+COPS?\\r\\n' > /dev/ttyUSB2; sleep 0.4; kill %1 2>/dev/null\r\n"}
        SerialClient2(COM16.115200,occupied=o,isopen=True)READ(
            bytes=b'timeout 2 cat /dev/ttyUSB2 & sleep 0.1; printf \'AT+COPS?\\r\\n\' > /dev/ttyUSB2; sleep 0.4; kill %1 2>/dev/null\r\n\x1b[?2004l\r[6] 5353\r\n[5]   Exit 124                timeout 2 cat /dev/ttyUSB2\r\n\r\r\n+COPS: 0,2,"25020",7\r\r\n\r\r\nOK\r\r\n\x1b[?2004hroot@harvest05:~# \r\n\x1b[?2004l\r\x1b[?2004hroot@harvest05:~# '
            printable=timeout 2 cat /dev/ttyUSB2 & sleep 0.1; printf 'AT+COPS?\r\n' > /dev/ttyUSB2; sleep 0.4; kill %1 2>/dev/null
        [6] 5353
        [5]   Exit 124                timeout 2 cat /dev/ttyUSB2

        root@harvest05:~#
        root@harvest05:~# )
        [AT] AT+COPS? -> at_output='+COPS: 0,2,"25020",7\nOK'
        GSM operator: +COPS: 0,2,"25020",7
        OK

        НЕЛЬЗЯ ПРОСТО ДВА ПЕРВЫХ УДАЛЯТЬ!!!
        [15:19:47.271369]COM16.writeline[OK]= b"timeout 2.0 cat /dev/ttyUSB2 & sleep 0.1; printf 'AT\\r\\n' > /dev/ttyUSB2; sleep 0.4\r\n"
        [15:19:47.306637]COM16.readline[OK]= b"timeout 2.0 cat /dev/ttyUSB2 & sleep 0.1; printf 'AT\\r\\n' > /dev/ttyUSB2; sleep 0.4"
        [15:19:47.310637]COM16.readline[OK]= b'\x1b[?2004l'
        [15:19:47.313637]COM16.readline[OK]= b'[1] 3964'
        [15:19:47.410022]COM16.readline[OK]= b'OK'
        [15:19:47.836296]COM16.readline[OK]= b'\x1b[?2004hroot@harvest05:~# '
        [15:19:47.841624]COM16.readline[OK]= b'\x1b[?2004l'
        [COM16.WRITEREAD]
            write=[timeout 2.0 cat /dev/ttyUSB2 & sleep 0.1; printf 'AT\r\n' > /dev/ttyUSB2; sleep 0.4]
            read=[[1] 3964
        OK]
        [AT] AT ---> at_output=''
        FAILED
        """
        cmd_full = (
            f"cat {port} & sleep 0.1; "
            f"printf '{cmd}\\r\\n' > {port}; "
            f"sleep 0.4; "
            f"kill %1 2>/dev/null"
        )
        at_output = self.cmd_timeout__write_read__payload(
            cmd=cmd_full,
            timeout=timeout,
            timeout_continue=timeout * 0.8,
        )
        print(f"[AT]{cmd}--->{at_output}")
        return at_output

    def at_cmd__raw(
            self,
            cmd: str,
            bridge: str = "/tmp/at_client.py",
            port: str = "/dev/ttyUSB2",
            baudrate: int = 115200,
            stop_line=b"OK",

            timeout: float = 2.0,
            timeout_continue: float | None = None,
            **read_kwargs
    ) -> str | NoReturn:
        """
        !USE SIMPLE! - works quicker!
        Отправляет AT-команду через скрипт на устройстве и возвращает строку ответа.

        SerialClient2(COM16.115200,occupied=harvest05,isopen=True){'write': b"timeout 2 python3 /tmp/at_client.py 'AT+CSQ' /dev/ttyUSB2 115200\r\n"}
        SerialClient2(COM16.115200,occupied=harvest05,isopen=True)READ(
            bytes=b"timeout 2 python3 /tmp/at_client.py 'AT+CSQ' /dev/ttyUSB2 115200\r\n\x1b[?2004l\r\r\r\n+CSQ: 23,99\r\r\n\r\r\nOK\r\r\n\r\n\x1b[?2004hroot@harvest05:~# \r\n\x1b[?2004l\r\x1b[?2004hroot@harvest05:~# "
            printable=timeout 2 python3 /tmp/at_client.py 'AT+CSQ' /dev/ttyUSB2 115200
        root@harvest05:~#
        root@harvest05:~# )
        [at_output='+CSQ: 23,99\nOK']
        """
        command_line = f"python3 {bridge} '{cmd}' {port} {baudrate}"
        at_output = ""
        for _ in range(2):

            at_output = self.cmd_timeout__write_read__payload(
                command_line,
                stop_line=stop_line,
                timeout=timeout,
                timeout_continue=timeout_continue,
                **read_kwargs
            )
            # Убираем возможное эхо команды
            if at_output.startswith(cmd + "\n"):
                at_output = at_output.replace(cmd + "\n", "", 1)

            if "No such file or directory" in at_output:
                if not self.file_name__push(bridge):
                    break

        print(f"[AT]{cmd}--->{at_output}")
        return at_output

    def at_cmd__dump(self, port: str, method_simple: bool = True, timeout: float = 2.0) -> dict[str, str]:
        """
        Опрашивает AT-команды из AT_CMD__DUMP

        {
          "AT": "OK",
          "ATI": "Manufacturer: INCORPORATED\nModel: A7682E-R\nRevision: A7682M6_V1.11.1\nIMEI1: 865286077380516\nIMEI2: 865286076965218\n+GCAP: +CGSM,+FCLASS,+DS\nOK",
          "AT+CGMI": "INCORPORATED\nOK",
          "AT+CGMM": "A7682E-R\nOK",
          "AT+CGMR": "+CGMR: A011B02A7682M6_DS_FOTA\nOK",
          "AT+CGSN": "865286077380516\nOK",
          "AT+CIMI": "250470002905372\nOK",
          "AT+GSN": "865286077380516\nOK",
          "AT+CPIN?": "+CPIN: READY\nOK",
          "AT+CCID": "ERROR",
          "AT+COPS?": "+COPS: 0,2,\"25020\",7\nOK",
          "AT+CREG?": "+CREG: 0,1\nOK",
          "AT+CGREG?": "+CGREG: 0,1\nOK",
          "AT+CEREG?": "+CEREG: 0,1\nOK",
          "AT+CSQ": "+CSQ: 22,99\nOK",
          "AT+CESQ": "+CESQ: 43,99,255,255,7,38\nOK",
          "AT*CNTI=0": "ERROR",
          "AT+WS46?": "+WS46:30\nOK",
          "AT+CGDCONT?": "+CGDCONT: 1,\"IP\",\"simsim.MNC047.MCC250.GPRS\",\"10.0.188.251\",0,0,,,,\nOK",
          "AT+CGCONTRDP": "+CGCONTRDP: 1,5,\"simsim.MNC047.MCC250.GPRS\",\"10.0.188.251\",\"\",\"100.77.8.8\",\"100.77.4.4\",\"\",\"\",0,01400\nOK",
          "AT+CGPADDR": "+CGPADDR: 1,10.0.188.251\nOK",
          "AT+CGACT?": "+CGACT: 1,1\nOK",
          "AT+CGATT?": "+CGATT: 1\nOK",
          "AT+CIMS?": "ERROR",
          "AT+CIREG?": "+CME ERROR: Operation not supported",
          "AT+CFUN?": "+CFUN: 1\nOK",
          "AT+CSCLK?": "+CSCLK: 0\nOK",
          "AT+CPMUTEMP?": "ERROR",
          "AT+CBC": "+CBC: 3.830V\nOK",
          "AT+CCED?": "ERROR",
          "AT*CELLINFO?": "ERROR",
          "AT+CEER": "+CEER: \"0 Unknown\"\nOK"
        }

        Параметр	Значение
        Модель	SIMCom A7682E-R
        Прошивка	A7682M6_V1.11.1 / A011B02A7682M6_DS_FOTA
        IMEI1	865286077380516
        IMEI2	865286076965218 (две SIM)
        IMSI	250470002905372
        Оператор	25020 (Tele2 Russia)
        RAT	7 (LTE)
        WS46	30 (LTE + GSM)
        RSSI	20/31 (хороший)
        CESQ	RSRP=30, RSRQ=40 (отличный LTE)
        Регистрация	CREG/CGREG/CEREG = 0,1 (домашняя)
        PDP IP	10.0.188.251
        DNS	100.77.8.8, 100.77.4.4
        Питание	3.840V
        CFUN	1 (полный)
        CSCLK	0 (сон выключен)

        ERROR (ожидаемо для этого модуля):
        AT+CPINR — не поддерживает доп. информацию по PIN/PUK
        AT+CCID — видимо не реализован (можно попробовать AT+ICCID)
        AT*CNTI=0 — vendor-specific, не поддерживается
        AT+CGDATA="PPP" — режим не активен
        AT+CIMS?, AT+CIREG? — IMS не поддерживается
        AT+CPMUTEMP? — нет датчика температуры
        AT+CCED?, AT*CELLINFO? — нет расширенной инфы по сотам
        """
        results = {}
        method_send = self.at_cmd__simple if method_simple else self.at_cmd__raw
        for cmd in self.AT_CMD__DUMP:
            try:
                resp = method_send(cmd, port=port, timeout=timeout)
                results[cmd] = resp.strip()
            except Exception as exc:
                results[cmd] = f"PYERROR:{exc!r}"   # нет таких!
        return results

    # CMDS =============================================================================================================
    def prepare__stop__kernel_terminal_logs(self) -> bool:
        """
        GOAL
        deactivate logging kernel errors into terminal
        leave only errors (KERN_ERR and above) no warns!

        root@harvest05:~#
        root@harvest05:~# [ 2817.555181] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
        [ 3230.554402] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
        [ 3643.553379] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
        [ 4056.552119] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
        [ 4469.553782] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
        [ 4882.553558] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
        [ 5295.554909] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
        [ 5708.553030] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
        [ 6121.554739] IPv6: ADDRCONF(NETDEV_UP): wlan0: link is not ready
        """
        print("не удалось изменить режим логгирования сообщений ядра Linux в консоль")
        return self.cmd_timeout__check_executed_success(f'dmesg -n 3')

    def prepare__stop__services(self) -> bool:
        """
        GOAL
        stop all services which could interfere with tests

        systemctl stop только останавливает текущий запущенный процесс, но не меняет флаги автозагрузки (enable/disable).
После перезагрузки systemd снова запустит сервис
        """
        result: bool = True
        # Останавливаем ModemManager, если он может мешать порту - обычно занимает порты с устройствами ttyUSB*!!!
        # mm_active = self.cmd_timeout__check_executed_success("systemctl is-active ModemManager")
        for service in ["ModemManager", ]:
            result &= self.cmd_timeout__check_executed_success(f"systemctl stop {service}")
        return result

    # ------------------------------------------------------------------------------------------------------------------
    def apt_install(self, module: str, timeout_continue: float = 5, **wr_kwargs) -> bool:
        """
        if need DELETE
            sudo apt remove picocom
        """
        result = self.cmd_timeout__check_executed_success(f"apt install -y {module}", timeout_continue=timeout_continue, **wr_kwargs)
        return result

    def check__has_internet(self) -> bool:
        """
        root@harvest05:~#
        ---- Sent utf8 encoded message: "ping -c 1 -W 2 8.8.8.8\r\n" ----
        ping -c 1 -W 2 8.8.8.8
        PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.

        --- 8.8.8.8 ping statistics ---
        1 packets transmitted, 0 received, 100% packet loss, time 0ms

        root@harvest05:~#
        """
        return self.cmd_timeout__check_executed_success(
                "ping -c 1 -W 1 8.8.8.8",
                timeout_continue=2,
                timeout=3,
            )

    # INFO =============================================================================================================
    def get_info__system(self) -> dict[str, Any]:
        result = {}

        # ----- Идентификация и версия ОС -----
        result['hostname'] = self.cmd_timeout__write_read__payload("hostname", timeout=1).strip()

        raw_os = self.cmd_timeout__write_read__payload("cat /etc/os-release 2>/dev/null", timeout=3)
        os_dict = {}
        for line in raw_os.split('\n'):
            if '=' in line:
                k, v = line.split('=', 1)
                os_dict[k.strip()] = v.strip().strip('"')
        result['os'] = os_dict

        result['kernel'] = self.cmd_timeout__write_read__payload("uname -r", timeout=1).strip()
        result['architecture'] = self.cmd_timeout__write_read__payload("uname -m", timeout=1).strip()

        # ----- Модель платы -----
        # Попытка через device-tree, иначе через dmesg
        model = self.cmd_timeout__write_read__payload(
            "cat /proc/device-tree/model 2>/dev/null || cat /sys/firmware/devicetree/base/model 2>/dev/null"
            , timeout=5
        ).strip()
        if not model:
            dmesg_model = self.cmd_timeout__write_read__payload(
                "dmesg | grep 'Machine model' | head -1 | cut -d: -f2-",
                timeout=3
            ).strip()
            model = dmesg_model if dmesg_model else "N/A"
        result['board_model'] = model

        # ----- CPU -----
        cpu_lines = self.cmd_timeout__write_read__payload("cat /proc/cpuinfo 2>/dev/null", timeout=3)
        cores = 0
        model_name = ""
        for line in cpu_lines.split('\n'):
            if line.startswith("processor"):
                cores += 1
            if line.startswith("model name") and not model_name:
                model_name = line.split(":")[1].strip()
            if line.startswith("Hardware") and not model_name:
                model_name = line.split(":")[1].strip()
        result['cpu'] = {
            'model': model_name or 'ARM',
            'cores': cores
        }

        # ----- Память -----
        mem_lines = self.cmd_timeout__write_read__payload("free -m 2>/dev/null || cat /proc/meminfo", timeout=3)
        if 'Mem:' in mem_lines:
            mem_parts = mem_lines.split('\n')[1].split()
            total = mem_parts[1]
            used = mem_parts[2]
            free = mem_parts[3]
            result['memory'] = {'total_mb': int(total), 'used_mb': int(used), 'free_mb': int(free)}
        else:
            mem = {}
            for line in mem_lines.split('\n'):
                parts = line.split()
                if len(parts) >= 2:
                    mem[parts[0].rstrip(':')] = parts[1]
            result['memory'] = mem

        # ----- Накопители -----
        disk_lines = self.cmd_timeout__write_read__payload("df -h / 2>/dev/null || echo NA", timeout=3)
        if disk_lines and disk_lines != 'N/A':
            parts = disk_lines.split('\n')[1].split()
            result['disk'] = {'total': parts[1], 'used': parts[2], 'available': parts[3], 'use%': parts[4]}
        else:
            result['disk'] = 'N/A'

        # ----- Uptime -----
        uptime_raw = self.cmd_timeout__write_read__payload("cat /proc/uptime", timeout=1)
        result['uptime'] = uptime_raw.split()[0] if uptime_raw else 'N/A'

        # ----- Сетевые интерфейсы -----
        net = {}
        iface_list = self.cmd_timeout__write_read__payload("ls /sys/class/net/", timeout=3).split()
        for iface in iface_list:
            iface = iface.strip()
            if not iface or iface == 'lo':
                continue
            mac = self.cmd_timeout__write_read__payload(f"cat /sys/class/net/{iface}/address 2>/dev/null", timeout=3).strip()
            ip_addr = self.cmd_timeout__write_read__payload(
                f"ip -4 addr show {iface} 2>/dev/null | grep inet | head -1")
            net[iface] = {
                'mac': mac if mac else 'N/A',
                'ip': ip_addr.split()[1].split('/')[0] if 'inet' in ip_addr else 'N/A'
            }
        result['network'] = net

        # ----- USB‑устройства (исправляем таймаут и убираем лишний stderr) -----
        # Используем timeout_continue=2 для гарантированного чтения вывода
        usb_raw = self.cmd_timeout__write_read__payload(
            "lsusb",
            timeout = 3,
            timeout_continue=2.0  # ждём до 2 секунд после эхо
        )
        result['usb_devices'] = [line.strip() for line in usb_raw.split('\n') if line.strip() and 'lsusb' not in line]

        # ----- I2C‑шины -----
        i2c_list = self.cmd_timeout__write_read__payload("i2cdetect -l 2>/dev/null", timeout=2).split('\n')
        result['i2c_buses'] = {}
        for bus_line in i2c_list:
            if 'i2c-' in bus_line:
                bus_num = bus_line.split()[0].split('-')[1]
                scan = self.cmd_timeout__write_read__payload(
                    f"i2cdetect -y {bus_num} 2>/dev/null",
                    timeout_continue=1.5,
                    timeout=2,
                )
                # Оставляем только строки с данными
                result['i2c_buses'][f'i2c-{bus_num}'] = [x.strip() for x in scan.split('\n')[1:] if x.strip()]

        # ----- Версия U‑Boot (ищем через grep) -----
        uboot_raw = self.cmd_timeout__write_read__payload(
            "dmesg | grep -i 'u-boot\|uboot' | head -1",
            timeout=2
        ).strip()
        result['uboot'] = uboot_raw if uboot_raw else 'N/A'

        return result

    # ------------------------------------------------------------------------------------------------------------------
    def get_info__usb(self, port: str) -> dict[str, Any]:
        """
        available both variants:
            full path   - /dev/ttyUSB0
            devName     - ttyUSB0

        {
          "DEVPATH": "/devices/platform/soc/1c1d400.usb/usb8/8-1/8-1:1.0/ttyUSB0/tty/ttyUSB0",
          "DEVNAME": "/dev/ttyUSB0",
          "MAJOR": "188",
          "MINOR": "0",
          "SUBSYSTEM": "tty",
          "USEC_INITIALIZED": "12701625",
          "ID_BUS": "usb",
          "ID_MODEL": "USB_Serial",
          "ID_MODEL_ENC": "USB\\x20Serial",
          "ID_MODEL_ID": "7523",
          "ID_SERIAL": "1a86_USB_Serial",
          "ID_VENDOR": "1a86",
          "ID_VENDOR_ENC": "1a86",
          "ID_VENDOR_ID": "1a86",
          "ID_REVISION": "0264",
          "ID_TYPE": "generic",
          "ID_USB_MODEL": "USB_Serial",
          "ID_USB_MODEL_ENC": "USB\\x20Serial",
          "ID_USB_MODEL_ID": "7523",
          "ID_USB_SERIAL": "1a86_USB_Serial",
          "ID_USB_VENDOR": "1a86",
          "ID_USB_VENDOR_ENC": "1a86",
          "ID_USB_VENDOR_ID": "1a86",
          "ID_USB_REVISION": "0264",
          "ID_USB_TYPE": "generic",
          "ID_USB_INTERFACES": ":ff0102:",
          "ID_USB_INTERFACE_NUM": "00",
          "ID_USB_DRIVER": "ch341",
          "ID_USB_CLASS_FROM_DATABASE": "Vendor Specific Class",
          "ID_VENDOR_FROM_DATABASE": "QinHeng Electronics",
          "ID_MODEL_FROM_DATABASE": "CH340 serial converter",
          "ID_PATH": "platform-1c1d400.usb-usb-0:1:1.0",
          "ID_PATH_TAG": "platform-1c1d400_usb-usb-0_1_1_0",
          "ID_MM_CANDIDATE": "1",
          "DEVLINKS": "/dev/serial/by-path/platform-1c1d400.usb-usb-0:1:1.0-port0 /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0",
          "TAGS": ":systemd:",
          "CURRENT_TAGS": ":systemd:"
        }
        """
        # Отключаем пейджер, чтобы получить полный вывод без интерактива
        output = self.cmd_timeout__write_read__payload(
            f"SYSTEMD_PAGER=cat udevadm info -q property -n {port} 2>/dev/null",
            timeout_continue=0.5,
            timeout=4,
        ).split("\n")

        result = {}
        for line in output:
            if "SYSTEMD_PAGER=" in line:
                continue
            if '=' in line:
                key, val = line.split('=', 1)
                result[key.strip()] = val.strip()

        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result

    def get_info__usb_all(self, filters: list | Base_EqValid | None = None) -> dict[str, dict[str, str]]:
        """
        Собирает udev-свойства для всех физических USB-устройств в /dev/.
        Фильтрует: только устройства с ID_BUS=usb (не консоли ttyS*, не виртуальные).

        Returns:
            {
                "/dev/ttyUSB0": {"ID_VENDOR": "1a86", "ID_MODEL": "USB_Serial", ...},
                "/dev/video0":  {"ID_VENDOR": "...", "ID_MODEL": "...", ...},
                "/dev/i2c-1":   {"ID_VENDOR": "...", "ID_MODEL": "...", ...},
            }
        """
        result: dict[str, dict[str, str]] = {}

        # Получаем список ВСЕХ устройств в /dev/
        dev_list = self.cmd_parsed__ls("/dev/", filters)
        """        
        WHAT USED
            ttyUSB* — USB-UART адаптеры
            ttyACM* — USB-модемы (если есть)
            video* — веб-камеры
            i2c-* — шины I2C (часто через USB-хаб)
            snd/* — звуковые устройства
            input/* — устройства ввода
            spidev* — SPI устройства
            
            
        
        some other devices no USB 
{
  "/dev/adsp1": {
    "DEVPATH": "/devices/platform/snd_aloop.0/sound/card1/adsp1",
    "DEVNAME": "/dev/adsp1",
    "MAJOR": "14",
    "MINOR": "28",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "10866555",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/audio": {
    "DEVPATH": "/devices/platform/snd_dummy.0/sound/card0/audio",
    "DEVNAME": "/dev/audio",
    "MAJOR": "14",
    "MINOR": "4",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "10846646",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/audio1": {
    "DEVPATH": "/devices/platform/snd_aloop.0/sound/card1/audio1",
    "DEVNAME": "/dev/audio1",
    "MAJOR": "14",
    "MINOR": "20",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "10867924",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/audio2": {
    "DEVPATH": "/devices/platform/soc/1c22c00.codec/sound/card2/audio2",
    "DEVNAME": "/dev/audio2",
    "MAJOR": "14",
    "MINOR": "36",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "11653994",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/audio3": {
    "DEVPATH": "/devices/platform/soc/soc:sound/sound/card3/audio3",
    "DEVNAME": "/dev/audio3",
    "MAJOR": "14",
    "MINOR": "52",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "12165930",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/cec0": {
    "DEVPATH": "/devices/platform/soc/1ee0000.hdmi/cec0",
    "DEVNAME": "/dev/cec0",
    "MAJOR": "250",
    "MINOR": "0",
    "SUBSYSTEM": "cec"
  },
  "/dev/ttyUSB0": {
    "DEVPATH": "/devices/platform/soc/1c1d400.usb/usb8/8-1/8-1:1.0/ttyUSB0/tty/ttyUSB0",
    "DEVNAME": "/dev/ttyUSB0",
    "MAJOR": "188",
    "MINOR": "0",
    "SUBSYSTEM": "tty",
    "USEC_INITIALIZED": "13287546",
    "ID_BUS": "usb",
    "ID_MODEL": "USB_Serial",
    "ID_MODEL_ENC": "USB\\x20Serial",
    "ID_MODEL_ID": "7523",
    "ID_SERIAL": "1a86_USB_Serial",
    "ID_VENDOR": "1a86",
    "ID_VENDOR_ENC": "1a86",
    "ID_VENDOR_ID": "1a86",
    "ID_REVISION": "0264",
    "ID_TYPE": "generic",
    "ID_USB_MODEL": "USB_Serial",
    "ID_USB_MODEL_ENC": "USB\\x20Serial",
    "ID_USB_MODEL_ID": "7523",
    "ID_USB_SERIAL": "1a86_USB_Serial",
    "ID_USB_VENDOR": "1a86",
    "ID_USB_VENDOR_ENC": "1a86",
    "ID_USB_VENDOR_ID": "1a86",
    "ID_USB_REVISION": "0264",
    "ID_USB_TYPE": "generic",
    "ID_USB_INTERFACES": ":ff0102:",
    "ID_USB_INTERFACE_NUM": "00",
    "ID_USB_DRIVER": "ch341",
    "ID_USB_CLASS_FROM_DATABASE": "Vendor Specific Class",
    "ID_VENDOR_FROM_DATABASE": "QinHeng Electronics",
    "ID_MODEL_FROM_DATABASE": "CH340 serial converter",
    "ID_PATH": "platform-1c1d400.usb-usb-0:1:1.0",
    "ID_PATH_TAG": "platform-1c1d400_usb-usb-0_1_1_0",
    "ID_MM_CANDIDATE": "1",
    "DEVLINKS": "/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0 /dev/serial/by-path/platform-1c1d400.usb-usb-0:1:1.0-port0",
    "TAGS": ":systemd:",
    "CURRENT_TAGS": ":systemd:"
  },
  "/dev/vcs": {
    "DEVPATH": "/devices/virtual/vc/vcs",
    "DEVNAME": "/dev/vcs",
    "MAJOR": "7",
    "MINOR": "0",
    "SUBSYSTEM": "vc"
  },
  "/dev/dsp": {
    "DEVPATH": "/devices/platform/snd_dummy.0/sound/card0/dsp",
    "DEVNAME": "/dev/dsp",
    "MAJOR": "14",
    "MINOR": "3",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "10843084",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/dsp1": {
    "DEVPATH": "/devices/platform/snd_aloop.0/sound/card1/dsp1",
    "DEVNAME": "/dev/dsp1",
    "MAJOR": "14",
    "MINOR": "19",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "10877809",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/dsp2": {
    "DEVPATH": "/devices/platform/soc/1c22c00.codec/sound/card2/dsp2",
    "DEVNAME": "/dev/dsp2",
    "MAJOR": "14",
    "MINOR": "35",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "11801536",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/dsp3": {
    "DEVPATH": "/devices/platform/soc/soc:sound/sound/card3/dsp3",
    "DEVNAME": "/dev/dsp3",
    "MAJOR": "14",
    "MINOR": "51",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "12189275",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/vcsa": {
    "DEVPATH": "/devices/virtual/vc/vcsa",
    "DEVNAME": "/dev/vcsa",
    "MAJOR": "7",
    "MINOR": "128",
    "SUBSYSTEM": "vc"
  },
  "/dev/gpiochip0": {
    "DEVPATH": "/devices/platform/soc/1c20800.pinctrl/gpiochip0",
    "DEVNAME": "/dev/gpiochip0",
    "OF_NAME": "pinctrl",
    "OF_FULLNAME": "/soc/pinctrl@01c20800",
    "OF_COMPATIBLE_0": "allwinner,sun8i-h3-pinctrl",
    "OF_COMPATIBLE_N": "1",
    "MAJOR": "254",
    "MINOR": "0",
    "SUBSYSTEM": "gpio"
  },
  "/dev/sequencer": {
    "DEVPATH": "/devices/virtual/sound/sequencer",
    "DEVNAME": "/dev/sequencer",
    "MAJOR": "14",
    "MINOR": "1",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "12604561",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/gpiochip1": {
    "DEVPATH": "/devices/platform/soc/1f02c00.pinctrl/gpiochip1",
    "DEVNAME": "/dev/gpiochip1",
    "OF_NAME": "pinctrl",
    "OF_FULLNAME": "/soc/pinctrl@01f02c00",
    "OF_COMPATIBLE_0": "allwinner,sun8i-h3-r-pinctrl",
    "OF_COMPATIBLE_N": "1",
    "MAJOR": "254",
    "MINOR": "1",
    "SUBSYSTEM": "gpio"
  },
  "/dev/sequencer2": {
    "DEVPATH": "/devices/virtual/sound/sequencer2",
    "DEVNAME": "/dev/sequencer2",
    "MAJOR": "14",
    "MINOR": "8",
    "SUBSYSTEM": "sound",
    "USEC_INITIALIZED": "12701333",
    "TAGS": ":uaccess:",
    "CURRENT_TAGS": ":uaccess:"
  },
  "/dev/i2c-0": {
    "DEVPATH": "/devices/platform/soc/1c2ac00.i2c/i2c-0/i2c-dev/i2c-0",
    "DEVNAME": "/dev/i2c-0",
    "MAJOR": "89",
    "MINOR": "0",
    "SUBSYSTEM": "i2c-dev"
  },
  "/dev/i2c-1": {
    "DEVPATH": "/devices/platform/soc/1c2b000.i2c/i2c-1/i2c-dev/i2c-1",
    "DEVNAME": "/dev/i2c-1",
    "MAJOR": "89",
    "MINOR": "1",
    "SUBSYSTEM": "i2c-dev"
  },
  "/dev/i2c-2": {
    "DEVPATH": "/devices/platform/soc/1c2b400.i2c/i2c-2/i2c-dev/i2c-2",
    "DEVNAME": "/dev/i2c-2",
    "MAJOR": "89",
    "MINOR": "2",
    "SUBSYSTEM": "i2c-dev"
  },
  "/dev/video0": {
    "DEVPATH": "/devices/platform/soc/1cb0000.camera/video4linux/video0",
    "DEVNAME": "/dev/video0",
    "MAJOR": "81",
    "MINOR": "0",
    "SUBSYSTEM": "video4linux",
    "USEC_INITIALIZED": "12019167",
    "ID_V4L_VERSION": "2",
    "ID_V4L_PRODUCT": "sun6i-csi",
    "ID_V4L_CAPABILITIES": ":capture:",
    "ID_PATH": "platform-1cb0000.camera",
    "ID_PATH_TAG": "platform-1cb0000_camera",
    "ID_FOR_SEAT": "video4linux-platform-1cb0000_camera",
    "DEVLINKS": "/dev/v4l/by-path/platform-1cb0000.camera-video-index0",
    "TAGS": ":uaccess:seat:",
    "CURRENT_TAGS": ":uaccess:seat:"
  },
  "/dev/i2c-3": {
    "DEVPATH": "/devices/platform/soc/1ee0000.hdmi/i2c-3/i2c-dev/i2c-3",
    "DEVNAME": "/dev/i2c-3",
    "MAJOR": "89",
    "MINOR": "3",
    "SUBSYSTEM": "i2c-dev"
  },
  "/dev/spidev0.0": {
    "DEVPATH": "/devices/platform/soc/1c68000.spi/spi_master/spi0/spi0.0/spidev/spidev0.0",
    "DEVNAME": "/dev/spidev0.0",
    "MAJOR": "153",
    "MINOR": "0",
    "SUBSYSTEM": "spidev"
  }
}
        """
        # Фильтруем — оставляем только потенциально интересные устройства
        # Исключаем: ttyS* (консоли), tty0-63 (виртуальные консоли),
        if filters:
            SKIP = []
        else:
            SKIP = [
                EqValid_RegexpAnyTrue(
                    r"ttyS\d",  # tty console
                    r"tty\d*",         # virtual tty
                    r"mmcblk.*", r"nbd.*", r"loop.*",   # блочные устройства
                    r"vcs\d+", "vcsa\d+",  # виртуальные консоли
                    r"watchdog\d*",
                    r"rtc\d*",
                    r"mixer\d*",
                ),

                EqValid_EQ(
                    "stdin", "stdout", "stderr",
                    "null", "zero", "full",
                    "bus",
                    "console",
                    "random", "urandom",
                    "mem", "kmsg",
                    "vhci",
                    "rfkill",
                    "ptmx", "pts",

                    "dri", "fb0",
                    "ppp",

                    "ram",
                    "net",
                    "v4l",

                    "watchdog", "cpu_dma_latency",
                    "network_latency", "network_throughput",
                    "memory_bandwidth",
                    "kmsg", "kmem", "mem", "kvm",
                    "fuse", "cuse",
                    "rtc0", "rtc1",
                    "initctl", "autofs", "btrfs-control",
                    "gpiochip",
                    "mqueue", "shm",
                    "fd", "mapper",
                    "psaux",
                ),
            ]

        # Пропускаем заведомо не-USB устройства
        potential_devices: list[str] = [*filter(lambda x: x not in SKIP, dev_list)]

        # Для каждого потенциального устройства пробуем получить udev-свойства
        for dev_path in potential_devices:
            try:
                props = self.get_info__usb(dev_path)

                # Проверяем, что это физическое USB-устройство
                id_bus = props.get("ID_BUS", "")

                # Пропускаем, если это не USB (консоли ttyS*, виртуальные)
                if id_bus != "usb":
                    # Но сохраняем, если есть хоть какие-то полезные ID_*
                    has_useful_ids = any(
                        k.startswith("ID_") and v
                        for k, v in props.items()
                    )
                    if not has_useful_ids:
                        continue
                    # Если есть ID_PATH или DEVPATH с "usb" — оставляем
                    if "usb" not in props.get("DEVPATH", "").lower():
                        if "usb" not in props.get("ID_PATH", "").lower():
                            continue

                if props:  # сохраняем только если есть данные
                    result[dev_path] = props

            except Exception as exc:
                # Устройство может не поддерживать udev — пропускаем
                logger.debug(f"Пропущено {dev_path}: {exc}")
                continue

        print(json.dumps(result, indent=2, ensure_ascii=True))
        return result

    # PARSERS ==========================================================================================================
    @staticmethod
    def parse__gnss_info__UBX(raw: bytes) -> dict[str, str | list[str]]:
        """
        Парсит ответ UBX MON-VER (класс 0x0A, ID 0x04) и возвращает словарь:
        {
            'sw_version': str,    # версия расширенного ПО
            'hw_version': str,    # аппаратная версия (строка)
            'extensions': [       # дополнительные поля
                "ROM BASE 3.01 (107888)",
                "FWVER=SPG 3.01",
                "PROTVER=18.00",
                "MOD=NEO-M8N-0",
                "FIS=0xEF4015 (100111)",
                "GPS;GLO;GAL;BDS",
                "SBAS;IMES;QZSS"
            ]
        }
        При ошибке выбрасывает ValueError.

        UBX_RESPONSE:b5620a04fa0045585420434f524520332e3031202831303739303029000000000000000030303038303030300000524f4d204241534520332e3031202831303738383829000000000000000046575645523d53504720332e30310000000000000000000000000000000050524f545645523d31382e303000000000000000000000000000000000004d4f443d4e454f2d4d384e2d3000000000000000000000000000000000004649533d30784546343031352028313030313131290000000000000000004750533b474c4f3b47414c3b424453000000000000000000000000000000534241533b494d45533b515a535300000000000000000000000000000000

        LR-STRIPPED:	output_hex_str='b5620a04fa0045585420434f524520332e3031202831303739303029000000000000000030303038303030300000524f4d204241534520332e3031202831303738383829000000000000000046575645523d53504720332e30310000000000000000000000000000000050524f545645523d31382e303000000000000000000000000000000000004d4f443d4e454f2d4d384e2d3000000000000000000000000000000000004649533d30784546343031352028313030313131290000000000000000004750533b474c4f3b47414c3b424453000000000000000000000000000000534241533b494d45533b515a535300000000000000000000000000000000'
        LR-STRIPPED:	raw_data=b'\xb5b\n\x04\xfa\x00EXT CORE 3.01 (107900)\x00\x00\x00\x00\x00\x00\x00\x0000080000\x00\x00ROM BASE 3.01 (107888)\x00\x00\x00\x00\x00\x00\x00\x00FWVER=SPG 3.01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00PROTVER=18.00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00MOD=NEO-M8N-0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00FIS=0xEF4015 (100111)\x00\x00\x00\x00\x00\x00\x00\x00\x00GPS;GLO;GAL;BDS\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00SBAS;IMES;QZSS\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        """
        # Проверка синхронизации и типа сообщения
        if raw[:2] != b'\xb5\x62':
            raise ValueError("Невалидный UBX заголовок")
        cls, msg_id = raw[2], raw[3]
        if cls != 0x0A or msg_id != 0x04:
            raise ValueError(f"Ожидался MON-VER, получено 0x{cls:02X} 0x{msg_id:02X}")

        length = int.from_bytes(raw[4:6], 'little')
        payload = raw[6:6 + length]

        sw_version: str = payload[:30].split(b'\x00')[0].decode('ascii')
        hw_version: str = payload[30:40].split(b'\x00')[0].decode('ascii')
        extensions_hex: str = payload[40:].decode('ascii')

        # extensions – всё после 40-го байта, разделённые нулями
        extensions = [ext for ext in extensions_hex.split('\x00') if ext]

        return {
            'sw_version': sw_version,
            'hw_version': hw_version,
            'extensions': extensions,
        }


# ======================================================================================================================
