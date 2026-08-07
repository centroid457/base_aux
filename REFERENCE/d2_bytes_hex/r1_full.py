"""
================================================================================
SPRAVOCNIK: BYTES & HEX В PYTHON ДЛЯ РАБОТЫ С UART/ДАТЧИКАМИ
================================================================================
Версия: 1.0
Для кого: Инженеры, работающие с RFID, ультразвуком, Bluetooth, UART в Linux
================================================================================
"""

def _rules__raws_hex__understanding():
    data_raw: bytes = b'\x00EXT CORE 3.01 (107900)'
    print("data_raw=", data_raw)
    # data_raw= b'\x00EXT CORE 3.01 (107900)'

    data_hex_from_raw: str = data_raw.hex().upper()
    print("data_hex_from_raw=", data_hex_from_raw)
    # data_hex_from_raw= 0045585420434f524520332e3031202831303739303029

    data_raw_from_hex: bytes = bytes.fromhex(data_hex_from_raw)
    print("data_raw_from_hex=", data_raw_from_hex)
    # data_raw_from_hex= b'\x00EXT CORE 3.01 (107900)'


    # 2=если мы в начале имеем байтстроку самого hex --------------------
    output_hex_bytes = b'312c3331302c32342c30372c37392c3039362c2c30382c31352c3039392c32342a37380d0a2447504753562c342c322c31332c30392c34342c3132372c32342c31312c30332c3234392c2c31342c31332c3139302c2c31362c31332c3033372c2a37340d0a2447504753562c342c332c31332c31382c30352c3335382c2c32302c30392c3239362c32322c32312c35302c3236382c32312c32372c31382c3036342c2a37460d0a2447504753562c342c342c31332c33302c35352c3234322c2a34430d0a24474c4753562c312c312c30302a36350d0a24474e474c4c2c2c2c2c2c3135323833332e30302c562c4e2a35410d0ab5620a04fa0045585420434f52'
    print(output_hex_bytes)
    # b'312c3331302c32342c30372c37392c3039362c2c30382c31352c3039392c32342a37380d0a2447504753562c342c322c31332c30392c34342c3132372c32342c31312c30332c3234392c2c31342c31332c3139302c2c31362c31332c3033372c2a37340d0a2447504753562c342c332c31332c31382c30352c3335382c2c32302c30392c3239362c32322c32312c35302c3236382c32312c32372c31382c3036342c2a37460d0a2447504753562c342c342c31332c33302c35352c3234322c2a34430d0a24474c4753562c312c312c30302a36350d0a24474e474c4c2c2c2c2c2c3135323833332e30302c562c4e2a35410d0ab5620a04fa0045585420434f52'

    # КОРРЕКТНАЯ СТРОКА
    # output_hex_str = str(output_hex_bytes)[1:]    # НЕКОРРЕКТНО! кавычки остаются!
    output_hex_str = output_hex_bytes.decode('ascii')  # получаем чистую HEX-строку
    print(output_hex_str)
    # 312c3331302c32342c30372c37392c3039362c2c30382c31352c3039392c32342a37380d0a2447504753562c342c322c31332c30392c34342c3132372c32342c31312c30332c3234392c2c31342c31332c3139302c2c31362c31332c3033372c2a37340d0a2447504753562c342c332c31332c31382c30352c3335382c2c32302c30392c3239362c32322c32312c35302c3236382c32312c32372c31382c3036342c2a37460d0a2447504753562c342c342c31332c33302c35352c3234322c2a34430d0a24474c4753562c312c312c30302a36350d0a24474e474c4c2c2c2c2c2c3135323833332e30302c562c4e2a35410d0ab5620a04fa0045585420434f52

    output_raw = bytes.fromhex(output_hex_str)  # преобразуем в бинарные данные
    print(output_raw)
    # b'1,310,24,07,79,096,,08,15,099,24*78\r\n$GPGSV,4,2,13,09,44,127,24,11,03,249,,14,13,190,,16,13,037,*74\r\n$GPGSV,4,3,13,18,05,358,,20,09,296,22,21,50,268,21,27,18,064,*7F\r\n$GPGSV,4,4,13,30,55,242,*4C\r\n$GLGSV,1,1,00*65\r\n$GNGLL,,,,,152833.00,V,N*5A\r\n\xb5b\n\x04\xfa\x00EXT COR'


# ======================================================================================================================
# БЛОК 1: БАЗОВЫЕ ТИПЫ И ИХ СОЗДАНИЕ
# ============================================================================
# ПРИНЦИП: bytes vs bytearray - неизменяемые vs изменяемые байтовые строки

# 1.1 Создание bytes (неизменяемый)
for index, data in enumerate([
    # 1=Из строки ASCII -----------------------------------
    b'Hello',

    # 2=Из списка чисел 0-255 -----------------------------
    bytes([0x48, 0x65, 0x6C]),
    bytes([1, 10, 99, 100, 255]),

    # нечитаемые - отображаются c \x, ascii - напрямую!!!
    bytes([0x00, 0x11, 0xAA, 0xBB, 0xCC, 0xDD, 0xFF]),      # нечитаемые=b'\x00\x11\xaa\xbb\xcc\xdd\xff'
    bytes([0x30, 0x31, 0x32, 0x41, 0x42, 0x43, 0x58, 0x59, 0x5A,]),      # читаемые=b'012ABCXYZ'
    bytes([0x00, 0x11, 0x22, 0x58, 0x59, 0x5A, 0xCC, 0xDD, 0xFF]),    # СМЕШАННЫЕ=b'\x00\x11"XYZ\xcc\xdd\xff'

    # 3=Из hex-строки[0-9a-fA-F] --------------------------
    bytes.fromhex('48656C'),
    bytes.fromhex('123456'),
    # bytes.fromhex('zz'),    # ValueError: non-hexadecimal number found in fromhex() arg at position 0
    bytes.fromhex(      # МНОЖЕСТВЕННЫЕ СТРОКИ РАЗБИТЫЕ УДОБНО
        "A0290181000120"
        "3000E2806894000050035FD77070"  # ← EPC (первое чтение)
        "430A430A"                       # ← extra
        "3000E2806894000050035FD77070"  # ← EPC (второе чтение, дубликат)
        "100401F7"                       # ← extra + хвост
    )

]):
    print(index, data)

"""
0 b'Hello'
1 b'Hel'
2 b'\x01\ncd\xff'
3 b'\x00\xaa\xbb\xcc\xdd\xff'   
4 b'Hel'
5 b'\x124V'
"""
print()

# ----------------------------------------------------------------------------------------------------------------------
# 1.2 Создание bytearray (изменяемый, как list но для байтов)
buf = bytearray(10)  # Буфер из 10 нулевых байтов
buf = bytearray(b'Hello')  # Из bytes
buf = bytearray([0xAA, 0xBB])  # Из списка

# 1.3 Основные свойства
print(type(b'ABC'))  # <class 'bytes'>
print(len(b'ABC'))  # 3 (длина в байтах)
print(b'ABC'[0])  # 65 (возвращает int, не bytes!)
print(b'ABC'[0:1])  # b'A' (срез возвращает bytes)
print()


# ======================================================================================================================
# БЛОК 2: ПРЕДСТАВЛЕНИЕ БАЙТОВ - HEX/DEC/BIN
# ============================================================================
# ПРИНЦИП: bytes - это просто числа 0-255, важно как их показывать


def show_representations(data: bytes):
    """
    Показать все представления

    BYTES:[b'HELLO\n']
    DEC:[72:69:76:76:79:10]
    HEXx:[0x48:0x45:0x4C:0x4C:0x4F:0x0A]
    HEX_:[48:45:4C:4C:4F:0A]
    BINb:[0b01001000:0b01000101:0b01001100:0b01001100:0b01001111:0b00001010]
    BIN_:[01001000:01000101:01001100:01001100:01001111:00001010]
    CHR:[H:E:L:L:O:?]
    CHR_:[HELLO?]
    """
    # byte_val = data[0]   # Получаем int
    print(f"BYTES:[", data, "]", sep="")

    print(f"DEC:[", ":".join([f"{byte_val}" for byte_val in data]), "]", sep="")

    print(f"HEXx:[", ":".join([f"0x{byte_val:02X}" for byte_val in data]), "]", sep="")
    print(f"HEX_:[", ":".join([f"{byte_val:02X}" for byte_val in data]), "]", sep="")

    print(f"BINb:[", ":".join([f"0b{byte_val:08b}" for byte_val in data]), "]", sep="")
    print(f"BIN_:[", ":".join([f"{byte_val:08b}" for byte_val in data]), "]", sep="")

    print(f"CHR:[", ":".join([f"{chr(byte_val) if 32 <= byte_val < 127 else '?'}" for byte_val in data]), "]", sep="")
    print(f"CHR_:[", "".join([f"{chr(byte_val) if 32 <= byte_val < 127 else '?'}" for byte_val in data]), "]", sep="")


show_representations(b'HELLO\n')
print()


# ======================================================================================================================
# БЛОК 3: HEX-СТРОКИ - ВЗАИМНЫЕ ПРЕОБРАЗОВАНИЯ
# ============================================================================
# ПРИНЦИП: hex строка нужна для логов/отладки/конфигов

# 3.1 bytes -> hex string (для отображения)
packet = bytes([0xAA, 0xBB, 0xCC, 0xDD])
hex_str = packet.hex().upper()  # 'aabbccdd'
print(data)
hex_str = packet.hex(':')  # 'aa:bb:cc:dd'
print(data)
hex_str = packet.hex(' ', 1)  # 'aabb ccdd' (группы по 1 байту)
print(data)

# 3.2 hex string -> bytes (парсинг данных)
data = bytes.fromhex('AABBCCDD')  #b'\xaa\xbb\xcc\xdd'
print(data)
data = bytes.fromhex('AA BB CC DD')  #b'\xaa\xbb\xcc\xdd'
print(data)
# data = bytes.fromhex('AA:BB:CC:DD')  # ValueError: non-hexadecimal number found in fromhex() arg at position 2
# data = bytes.fromhex('0xAA 0xBB')   # ValueError: non-hexadecimal number found in fromhex() arg at position 1

# 3.3 Форматирование байта для вывода
byte_val = 0x0A
print(f"0x{byte_val:02X}")  # 0x0A (всегда 2 цифры)
print(f"{byte_val:#04X}")  # 0X0A (альтернативный способ)
print()


# ======================================================================================================================
# БЛОК 4: РАБОТА С UART ПАКЕТАМИ - ПАРСИНГ
# ============================================================================
# ПРИНЦИП: Пакет имеет структуру [START][LEN][DATA][CRC][END]
# Парсим байт за байтом как конечный автомат

class UARTParser:
    """Пример парсера пакетов с датчика"""

    START_BYTE = 0xAA
    END_BYTE = 0x55

    def parse_rfid_packet(self, raw: bytes) -> dict:
        """
        Структура: [AA][LEN][TYPE][ID(4)][RSSI][CRC][55]
        AA - стартовый байт
        LEN - длина данных
        TYPE - тип метки (01=EM4100, 02=Mifare)
        ID(4) - идентификатор (4 байта, big-endian)
        RSSI - уровень сигнала
        CRC - контрольная сумма
        55 - стоп-байт
        """
        if len(raw) < 10:
            raise ValueError(f"Пакет слишком короткий: {len(raw)} байт")

        # Проверяем границы пакета
        if raw[0] != self.START_BYTE:
            raise ValueError(f"Нет стартового байта: 0x{raw[0]:02X}")
        if raw[-1] != self.END_BYTE:
            raise ValueError(f"Нет стоп-байта: 0x{raw[-1]:02X}")

        # Извлекаем данные
        data_len = raw[1]
        tag_type = raw[2]
        tag_id_bytes = raw[3:7]
        rssi = raw[7]
        crc_received = raw[8]

        # Преобразуем ID в число
        tag_id = int.from_bytes(tag_id_bytes, byteorder='big')

        # Проверяем CRC (простая сумма всех байтов данных)
        data_for_crc = raw[1:8]  # LEN + TYPE + ID + RSSI
        crc_calculated = sum(data_for_crc) & 0xFF

        return {
            'tag_id': tag_id,
            'tag_id_hex': tag_id_bytes.hex(':'),
            'tag_type': 'EM4100' if tag_type == 0x01 else 'Mifare',
            'rssi_dbm': -rssi,  # Обычно RSSI отрицательный
            'crc_valid': crc_received == crc_calculated,
            'raw': raw
        }


# Пример использования
packet = bytes([
    0xAA,  # START
    0x07,  # LEN
    0x01,  # TYPE (EM4100)
    0x12, 0x34, 0x56, 0x78,  # ID
    0x3C,  # RSSI (60 = -60 dBm)
    0xA2,  # CRC (сумма 07+01+12+34+56+78+3C = A2)
    0x55  # END
])

parser = UARTParser()
result = parser.parse_rfid_packet(packet)
print(result['tag_id_hex'])  # 12:34:56:78
print(result['crc_valid'])  # True

# ======================================================================================================================
# БЛОК 5: ЧТЕНИЕ ИЗ UART В LINUX
# ============================================================================
# ПРИНЦИП: /dev/ttyUSB0 выдаёт bytes, читаем в буфер, ищем пакеты

import serial  # pip install pyserial


def read_uart_stream(port='/dev/ttyUSB0', baudrate=115200):
    """
    Чтение потока байтов из UART с поиском пакетов
    Возвращает полные пакеты между START и END байтами
    """
    ser = serial.Serial(port, baudrate, timeout=1)
    buffer = bytearray()
    START = 0xAA
    END = 0x55
    MAX_PACKET = 64  # Максимальный размер пакета

    try:
        while True:
            if ser.in_waiting:
                # Читаем все доступные байты
                chunk = ser.read(ser.in_waiting)
                buffer.extend(chunk)

                # Ищем полные пакеты в буфере
                while True:
                    # Ищем START байт
                    if START not in buffer:
                        buffer.clear()
                        break

                    start_pos = buffer.index(START)
                    # Удаляем мусор до START
                    if start_pos > 0:
                        del buffer[:start_pos]

                    # Ищем END байт
                    if END not in buffer[1:]:
                        break  # Ждём ещё данных

                    end_pos = buffer.index(END, 1)

                    # Проверяем размер
                    if end_pos >= MAX_PACKET:
                        # Слишком длинный, удаляем START и ищем дальше
                        del buffer[0]
                        continue

                    # Извлекаем полный пакет
                    packet = bytes(buffer[:end_pos + 1])
                    del buffer[:end_pos + 1]

                    yield packet  # Отдаём пакет
    finally:
        ser.close()


# ======================================================================================================================
# БЛОК 6: ПРЕОБРАЗОВАНИЕ ЧИСЕЛ В БАЙТЫ И ОБРАТНО
# ============================================================================
# ПРИНЦИП: Все данные датчиков - это числа, упакованные в байты

# 6.1 Целые числа -> байты (для отправки команд)
value = 12345
# Big-endian (старший байт вперёд, как в сети)
as_bytes_be = value.to_bytes(2, byteorder='big')  # b'\x30\x39'
# Little-endian (младший байт вперёд, как в x86)
as_bytes_le = value.to_bytes(2, byteorder='little')  # b'\x39\x30'

# 6.2 Байты -> целое число (чтение показаний датчика)
data = b'\x12\x34'  # Пришло от ультразвукового датчика
distance = int.from_bytes(data, byteorder='big')  # 4660 мм
distance_le = int.from_bytes(data, byteorder='little')  # 13330 мм

# 6.3 Float -> bytes (показания датчиков)
import struct

temperature = 23.5
temp_bytes = struct.pack('f', temperature)  # 4 байта IEEE 754
temp_back = struct.unpack('f', temp_bytes)[0]

# 6.4 Работа со знаковыми числами
# Ультразвуковой датчик может вернуть -1 при ошибке
negative_val = -100
signed_bytes = negative_val.to_bytes(2, byteorder='big', signed=True)
restored = int.from_bytes(signed_bytes, byteorder='big', signed=True)
print(f"Знаковое: {restored}")  # -100


# ======================================================================================================================
# БЛОК 7: РАБОТА С BIT-ПОЛЯМИ (ФЛАГИ И МАСКИ)
# ============================================================================
# ПРИНЦИП: Один байт может нести 8 флагов состояния

class SensorFlags:
    """Флаги состояния датчика в одном байте"""
    SENSOR_OK = 0x01  # Бит 0
    DATA_READY = 0x02  # Бит 1
    ERROR = 0x04  # Бит 2
    LOW_BATTERY = 0x08  # Бит 3
    CALIBRATED = 0x10  # Бит 4


def parse_status_byte(status: int) -> dict:
    """Разобрать байт статуса на флаги"""
    return {
        'sensor_ok': bool(status & SensorFlags.SENSOR_OK),
        'data_ready': bool(status & SensorFlags.DATA_READY),
        'error': bool(status & SensorFlags.ERROR),
        'low_battery': bool(status & SensorFlags.LOW_BATTERY),
        'calibrated': bool(status & SensorFlags.CALIBRATED),
    }


# Пример: пришёл байт 0x13 (0001 0011)
status_byte = 0x13
flags = parse_status_byte(status_byte)
print(flags)  # {'sensor_ok': True, 'data_ready': True, ...}

# Установка/сброс флагов для отправки
cmd = 0x00
cmd |= SensorFlags.CALIBRATED  # Установить флаг
cmd &= ~SensorFlags.ERROR  # Сбросить флаг

# ======================================================================================================================
# БЛОК 8: BIT-ОПЕРАЦИИ ДЛЯ РАСПАКОВКИ ДАННЫХ
# ============================================================================
# ПРИНЦИП: Данные могут быть не выровнены по байтам (12-битные АЦП и т.п.)

# 8.1 Извлечение битового поля (старшие 4 бита)
byte_val = 0xAB  # 1010 1011
high_nibble = (byte_val >> 4) & 0x0F  # 0x0A (старшие 4 бита)
low_nibble = byte_val & 0x0F  # 0x0B (младшие 4 бита)

# 8.2 Сборка из двух полубайтов
high = 0x0A
low = 0x0B
combined = (high << 4) | low  # 0xAB

# 8.3 Извлечение 12-битного значения из 2 байтов
# (например, АЦП ультразвукового датчика)
data = bytes([0xAB, 0xCD])
# Извлекаем 12 бит (старшие 12 из 16)
value_12bit = ((data[0] << 8) | data[1]) >> 4  # Сдвиг на 4 бита


# ======================================================================================================================
# БЛОК 9: КОНТРОЛЬНЫЕ СУММЫ (CRC, XOR, SUM)
# ============================================================================
# ПРИНЦИП: Проверка целостности пакета

def crc8_maxim(data: bytes) -> int:
    """CRC-8 Maxim/Dallas (используется в 1-Wire, RFID)"""
    crc = 0x00
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x01:
                crc = (crc >> 1) ^ 0x8C
            else:
                crc >>= 1
    return crc


def xor_checksum(data: bytes) -> int:
    """XOR-контрольная сумма (часто в простых датчиках)"""
    result = 0
    for byte in data:
        result ^= byte
    return result


def sum_checksum(data: bytes) -> int:
    """Сумма всех байт (младший байт)"""
    return sum(data) & 0xFF


# Пример проверки целостности
packet = bytes([0x01, 0x02, 0x03])
checksum = xor_checksum(packet)
print(f"XOR checksum: 0x{checksum:02X}")

# ======================================================================================================================
# БЛОК 10: СТРОКИ И БАЙТЫ (КОДИРОВКИ)
# ============================================================================
# ПРИНЦИП: UART может передавать текст (AT-команды, GPS NMEA)

# 10.1 Строка -> байты (для отправки AT-команды)
at_command = "AT+VERSION\r\n"
cmd_bytes = at_command.encode('ascii')  # b'AT+VERSION\r\n'

# 10.2 Байты -> строка (парсинг GPS NMEA)
nmea_raw = b'$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47\r\n'
nmea_str = nmea_raw.decode('ascii')
print(nmea_str.split(',')[0])  # $GPGGA

# 10.3 Обработка ошибок декодирования
noisy_data = b'Temp: 23\xb0C\xff'  # \xb0 - знак градуса, \xff - ошибка
clean_text = noisy_data.decode('ascii', errors='replace')  # Temp: 23�C�
clean_text = noisy_data.decode('ascii', errors='ignore')  # Temp: 23C
clean_text = noisy_data.decode('latin-1')  # Temp: 23°Cÿ

# ======================================================================================================================
# БЛОК 11: РАБОТА С БУФЕРОМ (КОЛЬЦЕВОЙ БУФЕР)
# ============================================================================
# ПРИНЦИП: UART шлёт непрерывный поток, нужно эффективное хранение

from collections import deque


class RingBuffer:
    """Простой кольцевой буфер для UART данных"""

    def __init__(self, max_size=4096):
        self.buffer = deque(maxlen=max_size)

    def write(self, data: bytes):
        """Добавить данные в буфер"""
        self.buffer.extend(data)

    def find_packet(self, start_byte=0xAA, end_byte=0x55):
        """Найти пакет в буфере"""
        # Конвертируем в bytes для поиска
        data = bytes(self.buffer)
        start_idx = data.find(bytes([start_byte]))
        if start_idx == -1:
            return None

        end_idx = data.find(bytes([end_byte]), start_idx + 1)
        if end_idx == -1:
            return None

        # Извлекаем пакет
        packet = data[start_idx:end_idx + 1]

        # Удаляем обработанные данные из буфера
        for _ in range(end_idx + 1):
            self.buffer.popleft()

        return packet


# Пример использования
rb = RingBuffer()
rb.write(b'\x00\x01\xAA\x07\x01\x12\x34\x56\x78\x3C\xA2\x55\xFF')
packet = rb.find_packet()
print(packet.hex(':') if packet else "Пакет не найден")

# ======================================================================================================================
# БЛОК 12: СТРУКТУРЫ ДАННЫХ (struct)
# ============================================================================
# ПРИНЦИП: Описание формата пакета одной строкой

import struct

# 12.1 Упаковка данных для отправки (формат: <little-endian, B-байт, H-2байта)
# Отправляем команду: [TYPE=0x01][VALUE=1000][CRC_PLACEHOLDER]
packet_without_crc = struct.pack('<BH', 0x01, 1000)
crc = sum(packet_without_crc) & 0xFF
packet = packet_without_crc + bytes([crc])
print(packet.hex(':'))  # 01:e8:03:e9

# 12.2 Распаковка принятого пакета
# Принимаем: [STATUS(B)][DISTANCE_MM(H)][TEMPERATURE(f)]
received = bytes([0x00, 0x42, 0x0F, 0x00, 0x00, 0xDC, 0x41])
status, distance_mm, temperature = struct.unpack('<BHf', received[:7])
print(f"Статус: {status}, Дистанция: {distance_mm} мм, Темп: {temperature:.1f}°C")


# 12.3 Форматы struct (памятка)
# B - unsigned char (1 байт)
# H - unsigned short (2 байта)
# I - unsigned int (4 байта)
# f - float (4 байта)
# > - big-endian (сетевой порядок)
# < - little-endian (x86)

# ======================================================================================================================
# БЛОК 13: ПРАКТИЧЕСКИЙ ПРИМЕР - RFID + УЛЬТРАЗВУК
# ============================================================================
# ПРИНЦИП: Объединяем всё вместе для реального сценария

def process_sensor_stream():
    """
    Читаем RFID метки и данные ультразвукового датчика
    Собираем в структуру и отправляем дальше
    """
    # Имитация принятых данных
    rfid_packet = bytes.fromhex('AA 07 01 12 34 56 78 3C A2 55')
    ultrasonic_packet = bytes.fromhex('BB 04 0F 42 00 00 00 55')

    result = {
        'timestamp': 1234567890,
        'rfid': None,
        'distance_mm': None
    }

    # Парсим RFID
    if rfid_packet[0] == 0xAA:
        tag_id = int.from_bytes(rfid_packet[3:7], 'big')
        result['rfid'] = {
            'id': f"{tag_id:010d}",
            'type': 'EM4100' if rfid_packet[2] == 0x01 else 'Unknown',
            'rssi': -rfid_packet[7]
        }

    # Парсим ультразвук
    if ultrasonic_packet[0] == 0xBB:
        distance = int.from_bytes(ultrasonic_packet[2:4], 'big')
        result['distance_mm'] = distance

    # Формируем выходной пакет для передачи
    # [TIME(4)][RFID_ID(4)][DISTANCE(2)][RSSI(1)]
    output = bytearray()
    output.extend(result['timestamp'].to_bytes(4, 'big'))

    if result['rfid']:
        rfid_id = int(result['rfid']['id'])
        output.extend(rfid_id.to_bytes(4, 'big'))
        output.append(result['rfid']['rssi'] & 0xFF)

    output.extend(result['distance_mm'].to_bytes(2, 'big'))

    # Добавляем простую контрольную сумму
    checksum = sum(output) & 0xFF
    output.append(checksum)

    return bytes(output)


# Запуск примера
final_packet = process_sensor_stream()
print(f"Итоговый пакет: {final_packet.hex(':')}")


# ======================================================================================================================
# БЛОК 14: ОТЛАДКА И ЛОГГИРОВАНИЕ
# ============================================================================
# ПРИНЦИП: Для отладки UART нужен читаемый вывод

def hexdump(data: bytes, title: str = "HEX DUMP"):
    """Форматированный дамп байтов как в Wireshark"""
    print(f"\n{title}:")
    print("        00 01 02 03 04 05 06 07  08 09 0A 0B 0C 0D 0E 0F")
    print("-" * 60)

    for i in range(0, len(data), 16):
        chunk = data[i:i + 16]
        hex_part = ' '.join(f'{b:02X}' for b in chunk)
        # ASCII представление
        ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        print(f"{i:08X}: {hex_part:<48} {ascii_part}")


# Пример дампа пакета
packet = bytes.fromhex('AA 07 01 12 34 56 78 3C A2 55')
hexdump(packet, "RFID PACKET")

# ======================================================================================================================
# БЛОК 15: ПОЛЕЗНЫЕ ОДНОСТРОЧНИКИ (ШПАРГАЛКА)
# ============================================================================

# Конвертация одного байта
b = 65
hex_str = f"{b:02X}"  # 41
bin_str = f"{b:08b}"  # 01000001

# Байты в число и обратно
num = int.from_bytes(b'\x12\x34', 'big')  # 4660
bts = (4660).to_bytes(2, 'big')  # b'\x12\x34'

# Проверка бита
is_set = (0xAB >> 3) & 1  # Проверить 3-й бит

# Циклический сдвиг байта
rotated = ((0xAB << 1) | (0xAB >> 7)) & 0xFF

# Быстрый XOR всех байтов
checksum = 0
for b in b'\x01\x02\x03':
    checksum ^= b

# Поиск подстроки в байтах
pos = b'\x00\xAA\xBB\x55'.find(b'\xAA\xBB')

# Инвертирование битов в байте
inverted = 0x0F ^ 0xFF  # = 0xF0

print("\n" + "=" * 60)
print("Справочник загружен. Используйте blocks как модуль или копируйте примеры.")
print("=" * 60)


# ======================================================================================================================
