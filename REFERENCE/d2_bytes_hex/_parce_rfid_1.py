"""
================================================================================
ПРАВИЛЬНАЯ АРХИТЕКТУРА ПАРСИНГА RFID ПАКЕТОВ
================================================================================
3 ЧЁТКИХ ШАГА:
1. Чтение ВСЕГО ответа после команды
2. Разбиение потока на отдельные пакеты
3. Классификация и парсинг КАЖДОГО пакета по его назначению

НА ОСНОВЕ ВАШИХ РЕАЛЬНЫХ ДАННЫХ:
RawData(215bytes):[A02901810005203000E28068942000502BBD609C95D842D8423000E28068942000502BBD609C951010014DA02901810005203000E2806894000040138945853E812981293000E2806894000040138945853E10100137A02901810005203400010000000000000000000051B9A9B9A934000100000000000000000000511010019FA02901810005203400E77702010000000000000000468446843400E77702010000000000000000101001B1A02901810005203000E2806894000050035FD77070430A430A3000E2806894000050035FD77070101001E7]
================================================================================
"""

import struct
from dataclasses import dataclass
from typing import List, Optional, Union
from enum import IntEnum


# ============================================================================
# ШАГ 0: ОПИСАНИЕ СТРУКТУРЫ ПРОТОКОЛА (НА ОСНОВЕ РЕАЛЬНЫХ ДАННЫХ)
# ============================================================================

class PacketType(IntEnum):
    """Типы пакетов RFID ридера"""
    INVENTORY_RESPONSE = 0x01  # Ответ инвентаризации (найдены метки)
    READ_RESPONSE = 0x02  # Ответ чтения памяти метки
    WRITE_RESPONSE = 0x03  # Ответ записи
    ERROR = 0xFF  # Ошибка
    DEVICE_INFO = 0xFE  # Информация об устройстве


class TagType(IntEnum):
    """Типы RFID меток"""
    EM4100 = 0x01  # EM4100 (125 kHz)
    MIFARE = 0x02  # Mifare Classic
    ISO18000_6C = 0x03  # UHF EPC Gen2 (ISO 18000-6C)
    UNKNOWN = 0xFF


# Структура пакета согласно вашим данным:
# A0 - стартовый байт
# XX - длина данных (следующие байты до конца данных)
# 01 - тип пакета (инвентаризация)
# 81 - подтип (EPC данные)
# XX - количество найденных меток (05 в первом пакете = 5 меток)
# XX - возможно, статус операции
# DATA - данные меток

@dataclass
class TagInfo:
    """Информация о найденной RFID метке"""
    epc: str  # EPC идентификатор в HEX
    tag_type: TagType  # Тип метки
    rssi: Optional[int] = None  # Уровень сигнала (dBm)
    antenna: Optional[int] = None  # Номер антенны
    read_count: Optional[int] = None  # Количество прочтений
    raw_data: Optional[bytes] = None  # Сырые данные для отладки

    @property
    def epc_dec(self) -> str:
        """EPC в десятичном виде"""
        try:
            return str(int(self.epc, 16))
        except:
            return self.epc

    @property
    def epc_formatted(self) -> str:
        """Форматированный EPC для вывода"""
        if len(self.epc) <= 24:
            return self.epc
        return f"{self.epc[:8]}.{self.epc[8:16]}.{self.epc[16:]}"


@dataclass
class ScanSessionInfo:
    """Информация о сеансе сканирования (служебный пакет)"""
    total_tags: int  # Всего найдено меток
    scan_duration_ms: int  # Длительность сканирования
    antenna_count: int  # Количество антенн
    status: str  # Статус: "START", "COMPLETE", "ERROR"


@dataclass
class DeviceConfig:
    """Информация о конфигурации устройства"""
    device_type: str
    firmware_version: str
    power_level: int  # Мощность передатчика (dBm)
    frequency: int  # Частота (kHz)
    antenna_mask: int  # Битовая маска активных антенн


# ============================================================================
# ШАГ 1: ЧТЕНИЕ ВСЕГО ОТВЕТА ПОСЛЕ КОМАНДЫ
# ============================================================================

class UARTReader:
    """
    УНИВЕРСАЛЬНЫЙ ЧИТАТЕЛЬ UART
    Принцип: Отправить команду -> прочитать ВЕСЬ ответ -> вернуть bytes
    """

    def __init__(self, port: str, baudrate: int = 115200, timeout: float = 0.5):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def send_command_and_read_all(self, command: bytes,
                                  wait_timeout: float = 1.0,
                                  idle_threshold: float = 0.1) -> bytes:
        """
        ОТПРАВКА КОМАНДЫ И ЧТЕНИЕ ВСЕГО ОТВЕТА

        Алгоритм:
        1. Очистить буфер приёма
        2. Отправить команду
        3. Читать данные пока они идут (с паузой между чтениями)
        4. Остановиться когда данные перестали поступать

        Args:
            command: байты команды
            wait_timeout: максимальное время ожидания
            idle_threshold: время тишины для определения конца передачи
        """
        import serial
        import time

        ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        ser.reset_input_buffer()  # Очистка буфера
        ser.write(command)  # Отправка команды

        response = bytearray()
        start_time = time.time()
        last_data_time = start_time

        while time.time() - start_time < wait_timeout:
            # Читаем всё что есть в буфере
            available = ser.in_waiting
            if available > 0:
                chunk = ser.read(available)
                response.extend(chunk)
                last_data_time = time.time()  # Обновляем время последних данных
            else:
                # Если данных нет дольше idle_threshold - заканчиваем
                if time.time() - last_data_time > idle_threshold:
                    break
                time.sleep(0.01)  # Маленькая пауза

        ser.close()
        return bytes(response)


# ============================================================================
# ШАГ 2: РАЗБИЕНИЕ ПОТОКА НА ОТДЕЛЬНЫЕ ПАКЕТЫ
# ============================================================================

class PacketSplitter:
    """
    РАЗБИЕНИЕ ПОТОКА БАЙТОВ НА ОТДЕЛЬНЫЕ ПАКЕТЫ

    Принцип: Ищем стартовый байт 0xA0, читаем длину, извлекаем пакет
    Структура пакета: [A0][LEN][DATA...]
    где LEN = количество байт ДАННЫХ (не включая A0 и сам LEN)
    """

    START_BYTE = 0xA0
    MAX_PACKET_SIZE = 64  # Максимальный размер пакета для защиты

    def split(self, raw_data: bytes) -> List[bytes]:
        """
        Разбить сырой поток на отдельные пакеты

        Args:
            raw_data: сырые байты от устройства

        Returns:
            Список отдельных пакетов (каждый начинается с 0xA0)
        """
        packets = []
        pos = 0

        while pos < len(raw_data):
            # Ищем стартовый байт
            if raw_data[pos] != self.START_BYTE:
                pos += 1
                continue

            # Проверяем что есть байт длины
            if pos + 1 >= len(raw_data):
                break

            # Читаем длину данных
            data_length = raw_data[pos + 1]

            # Проверяем валидность
            if data_length == 0 or data_length > self.MAX_PACKET_SIZE:
                pos += 1
                continue

            # Проверяем что весь пакет помещается в буфер
            packet_end = pos + 2 + data_length  # +2 = START + LEN
            if packet_end > len(raw_data):
                break

            # Извлекаем пакет
            packet = raw_data[pos:packet_end]
            packets.append(packet)

            # Переходим к следующему пакету
            pos = packet_end

        return packets


# ============================================================================
# ШАГ 3: КЛАССИФИКАЦИЯ И ПАРСИНГ ПАКЕТОВ
# ============================================================================

class RFIDPacketParser:
    """
    ПАРСИНГ ПАКЕТОВ ПО НАЗНАЧЕНИЮ

    Типы пакетов которые мы можем получить:
    1. Пакет инвентаризации (TYPE=0x01) - содержит найденные метки
    2. Пакет чтения памяти (TYPE=0x02) - данные из памяти метки
    3. Служебный пакет (TYPE=0xFE) - информация об устройстве
    4. Пакет ошибки (TYPE=0xFF) - ошибка выполнения
    """

    def parse_packet(self, packet: bytes) -> dict:
        """
        Универсальный парсер пакета

        Returns:
            dict с ключами:
            - 'type': тип пакета ('tag_found', 'device_info', 'scan_status', 'error', 'unknown')
            - 'data': распарсенные данные (зависит от типа)
        """
        if len(packet) < 4:
            return {'type': 'unknown', 'data': None, 'error': 'Packet too short'}

        # Базовая структура: [A0][LEN][TYPE][SUBTYPE][...DATA...]
        start_byte = packet[0]
        length = packet[1]
        packet_type = packet[2]
        packet_subtype = packet[3]

        if start_byte != 0xA0:
            return {'type': 'unknown', 'data': None, 'error': 'No start byte'}

        # Определяем тип пакета и парсим соответственно
        if packet_type == 0x01 and packet_subtype == 0x81:
            # ПАКЕТ ИНВЕНТАРИЗАЦИИ (найдены метки)
            return self._parse_inventory_packet(packet)

        elif packet_type == 0x02:
            # ОТВЕТ ЧТЕНИЯ ПАМЯТИ
            return self._parse_read_response(packet)

        elif packet_type == 0xFE:
            # ИНФОРМАЦИЯ ОБ УСТРОЙСТВЕ
            return self._parse_device_info(packet)

        elif packet_type == 0xFF:
            # ОШИБКА
            return self._parse_error_packet(packet)

        else:
            # Неизвестный тип
            return {
                'type': 'unknown',
                'data': {
                    'raw': packet.hex(':'),
                    'type_byte': f'0x{packet_type:02X}',
                    'subtype_byte': f'0x{packet_subtype:02X}'
                }
            }

    def _parse_inventory_packet(self, packet: bytes) -> dict:
        """
        ПАРСИНГ ПАКЕТА ИНВЕНТАРИЗАЦИИ

        Структура (из ваших данных):
        A0 - старт
        29 - длина (41 байт данных)
        01 - тип (инвентаризация)
        81 - подтип (EPC)
        00 - ? (статус?)
        05 - количество меток в этом пакете
        20 - ? (флаги?)
        [ДАННЫЕ МЕТОК]

        Данные одной метки (из вашего примера):
        3000E28068942000502BBD609C95 - EPC (14 байт = 28 hex)
        D842 - ? (возможно RSSI + антенна)
        D842 - ? (дублируется?)
        """
        tags = []

        # Извлекаем служебную информацию
        status_byte = packet[4] if len(packet) > 4 else 0
        tag_count = packet[5] if len(packet) > 5 else 0
        flags = packet[6] if len(packet) > 6 else 0

        # Начинаем парсить данные меток с 7-го байта
        data_start = 7
        remaining_data = packet[data_start:]

        # Ищем EPC по характерным признакам
        # EPC Gen2 начинается с 0x30 или 0x34 (первые 4 бита: 0011)
        pos = 0
        while pos < len(remaining_data):
            # Ищем начало EPC
            if remaining_data[pos] in (0x30, 0x34):
                # Определяем длину EPC (обычно 12-14 байт для стандартных меток)
                epc_length = self._detect_epc_length(remaining_data[pos:])

                if epc_length > 0 and pos + epc_length <= len(remaining_data):
                    epc_bytes = remaining_data[pos:pos + epc_length]
                    epc_hex = epc_bytes.hex().upper()

                    # Пытаемся извлечь дополнительные данные после EPC
                    extra_pos = pos + epc_length
                    rssi = None
                    antenna = None

                    # После EPC обычно идут 2-4 байта служебных данных
                    if extra_pos + 2 <= len(remaining_data):
                        # Пример: D842 может быть RSSI и антенна
                        extra_data = remaining_data[extra_pos:extra_pos + 4]
                        if len(extra_data) >= 2:
                            rssi = extra_data[0]  # Первый байт - RSSI
                            antenna = extra_data[1] & 0x0F  # Младшие 4 бита - антенна

                    tag = TagInfo(
                        epc=epc_hex,
                        tag_type=TagType.ISO18000_6C if epc_hex.startswith(('30', '34')) else TagType.UNKNOWN,
                        rssi=-rssi if rssi else None,
                        antenna=antenna,
                        raw_data=remaining_data[pos:pos + epc_length + 4] if extra_pos <= len(
                            remaining_data) else remaining_data[pos:]
                    )
                    tags.append(tag)

                    # Перепрыгиваем через EPC + дополнительные данные
                    pos = extra_pos + 4
                    continue

            pos += 1

        return {
            'type': 'tags_found',
            'data': {
                'tags': tags,
                'total_in_packet': tag_count,
                'flags': f'0x{flags:02X}',
                'status': 'OK' if status_byte == 0 else f'0x{status_byte:02X}'
            }
        }

    def _detect_epc_length(self, data: bytes) -> int:
        """
        Определение длины EPC по первым байтам
        EPC Gen2: длина указана в первых битах
        """
        if len(data) < 1:
            return 0

        first_byte = data[0]

        # Стандартные длины EPC
        if first_byte in (0x30, 0x34):
            # SGTIN-96: 12 байт (24 hex символа)
            return 12
        elif first_byte == 0x31:
            # Может быть 14 байт
            return 14

        # Если не можем определить - ищем до следующего 0x30/0x34 или конца
        for i in range(6, 16):  # EPC от 6 до 16 байт
            if i >= len(data):
                return len(data)
            # Если встретили следующий маркер EPC
            if data[i] in (0x30, 0x34) and i > 8:
                return i

        return min(len(data), 14)  # По умолчанию 14 байт

    def _parse_read_response(self, packet: bytes) -> dict:
        """Парсинг ответа чтения памяти метки"""
        return {
            'type': 'read_response',
            'data': {
                'raw': packet.hex(':'),
                'memory_bank': packet[4] if len(packet) > 4 else None,
                'data': packet[5:].hex(':') if len(packet) > 5 else None
            }
        }

    def _parse_device_info(self, packet: bytes) -> dict:
        """Парсинг информации об устройстве"""
        return {
            'type': 'device_info',
            'data': {
                'raw': packet.hex(':'),
                'firmware': f'{packet[4]}.{packet[5]}' if len(packet) > 5 else 'unknown',
                'protocol_version': packet[6] if len(packet) > 6 else None
            }
        }

    def _parse_error_packet(self, packet: bytes) -> dict:
        """Парсинг пакета ошибки"""
        error_codes = {
            0x01: 'No tags found',
            0x02: 'Read error',
            0x03: 'Write error',
            0x04: 'Tag lost',
            0x05: 'Memory overrun',
        }
        error_code = packet[4] if len(packet) > 4 else 0xFF
        return {
            'type': 'error',
            'data': {
                'error_code': f'0x{error_code:02X}',
                'error_message': error_codes.get(error_code, 'Unknown error')
            }
        }


# ============================================================================
# ШАГ 4: ОБЪЕДИНЯЮЩИЙ КЛАСС - ЧИСТЫЙ ИНТЕРФЕЙС
# ============================================================================

class RFIDReader:
    """
    ГЛАВНЫЙ КЛАСС ДЛЯ РАБОТЫ С RFID РИДЕРОМ

    Использование:
        reader = RFIDReader('/dev/ttyS2')
        result = reader.scan()  # Одно сканирование

        print("Найденные метки:")
        for tag in result['tags']:
            print(f"  EPC: {tag.epc}")
            print(f"  RSSI: {tag.rssi} dBm")

        print("Служебная информация:")
        for service in result['service_packets']:
            print(f"  {service['type']}: {service['data']}")
    """

    def __init__(self, port: str, baudrate: int = 115200):
        self.reader = UARTReader(port, baudrate)
        self.splitter = PacketSplitter()
        self.parser = RFIDPacketParser()

        # Стандартная команда инвентаризации (из вашего кода)
        self.INVENTORY_CMD = bytes([
            0xA0, 0x0A, 0x01, 0x81,  # Заголовок
            0x01,  # Количество циклов
            0x00,  # Опции
            0x08,  # Параметр
            0x00, 0x00, 0x00, 0x00,  # Резерв
            0xCB  # CRC
        ])

    def scan(self) -> dict:
        """
        ПОЛНЫЙ ЦИКЛ СКАНИРОВАНИЯ

        Returns:
            dict:
                'tags': List[TagInfo] - найденные метки
                'service_packets': List[dict] - служебные пакеты
                'raw_data': bytes - сырые данные (для отладки)
                'statistics': dict - статистика сканирования
        """
        # ШАГ 1: Читаем весь ответ
        raw_data = self.reader.send_command_and_read_all(self.INVENTORY_CMD)

        # ШАГ 2: Разбиваем на пакеты
        packets = self.splitter.split(raw_data)

        # ШАГ 3: Парсим каждый пакет
        tags = []
        service_packets = []

        for packet in packets:
            result = self.parser.parse_packet(packet)

            if result['type'] == 'tags_found':
                tags.extend(result['data']['tags'])
            elif result['type'] in ('device_info', 'error', 'read_response'):
                service_packets.append(result)

        # Формируем результат
        return {
            'tags': tags,
            'service_packets': service_packets,
            'raw_data': raw_data,
            'statistics': {
                'total_packets': len(packets),
                'total_tags': len(tags),
                'unique_tags': len(set(tag.epc for tag in tags)),
                'raw_bytes': len(raw_data)
            }
        }


# ============================================================================
# ШАГ 5: КРАСИВЫЙ ВЫВОД РЕЗУЛЬТАТОВ
# ============================================================================

class RFIDResultPrinter:
    """Форматированный вывод результатов сканирования"""

    @staticmethod
    def print_full_report(scan_result: dict):
        """Полный отчёт о сканировании"""
        print("\n" + "=" * 70)
        print("📡 RFID SCAN REPORT")
        print("=" * 70)

        # Статистика
        stats = scan_result['statistics']
        print(f"\n📊 СТАТИСТИКА:")
        print(f"  Пакетов получено: {stats['total_packets']}")
        print(f"  Меток найдено:    {stats['total_tags']}")
        print(f"  Уникальных меток: {stats['unique_tags']}")
        print(f"  Сырых байт:       {stats['raw_bytes']}")

        # Найденные метки
        tags = scan_result['tags']
        if tags:
            print(f"\n🏷️ НАЙДЕННЫЕ МЕТКИ ({len(tags)}):")
            for i, tag in enumerate(tags, 1):
                print(f"\n  [{i}] EPC: {tag.epc_formatted}")
                print(f"      Тип: {tag.tag_type.name}")
                if tag.rssi is not None:
                    print(f"      RSSI: {tag.rssi} dBm")
                if tag.antenna is not None:
                    print(f"      Антенна: {tag.antenna}")
        else:
            print("\n❌ Метки не найдены")

        # Служебные пакеты
        service = scan_result['service_packets']
        if service:
            print(f"\n🔧 СЛУЖЕБНЫЕ ПАКЕТЫ ({len(service)}):")
            for pkt in service:
                print(f"  [{pkt['type']}] {pkt['data']}")

        # Сырые данные (компактно)
        raw = scan_result['raw_data']
        print(f"\n📦 RAW DATA: {len(raw)} bytes")
        print(f"  {raw[:64].hex(' ')}...")

        print("\n" + "=" * 70)

    @staticmethod
    def print_tags_only(scan_result: dict):
        """Только EPC меток (для передачи дальше)"""
        for tag in scan_result['tags']:
            print(tag.epc)

    @staticmethod
    def print_json_output(scan_result: dict):
        """Вывод в JSON формате для передачи на сервер"""
        import json

        output = {
            'timestamp': 'AUTO',  # Нужно добавить временную метку
            'tags': [
                {
                    'epc': tag.epc,
                    'rssi': tag.rssi,
                    'antenna': tag.antenna,
                    'type': tag.tag_type.name
                }
                for tag in scan_result['tags']
            ],
            'total': len(scan_result['tags'])
        }

        print(json.dumps(output, indent=2))


# ============================================================================
# ДЕМОНСТРАЦИЯ НА ВАШИХ РЕАЛЬНЫХ ДАННЫХ
# ============================================================================

def demo_with_real_data():
    """
    Демонстрация парсинга на ваших реальных данных из логов
    """
    # Ваши реальные данные из первого сканирования
    raw_hex = (
        "A02901810005203000E28068942000502BBD609C95D842D842"
        "3000E28068942000502BBD609C951010014D"
        "A02901810005203000E2806894000040138945853E81298129"
        "3000E2806894000040138945853E10100137"
        "A02901810005203400010000000000000000000051B9A9B9A9"
        "34000100000000000000000000511010019F"
        "A02901810005203400E7770201000000000000000046844684"
        "3400E77702010000000000000000101001B1"
        "A02901810005203000E2806894000050035FD77070430A430A"
        "3000E2806894000050035FD77070101001E7"
    )

    raw_data = bytes.fromhex(raw_hex)

    # Шаг 2: Разбиваем на пакеты
    splitter = PacketSplitter()
    packets = splitter.split(raw_data)

    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ НА РЕАЛЬНЫХ ДАННЫХ")
    print("=" * 70)
    print(f"\nВсего сырых байт: {len(raw_data)}")
    print(f"Найдено пакетов: {len(packets)}")

    # Шаг 3: Парсим каждый пакет
    parser = RFIDPacketParser()
    all_tags = []

    for i, packet in enumerate(packets):
        print(f"\n--- ПАКЕТ {i + 1} ---")
        print(f"Размер: {len(packet)} байт")
        print(f"Hex: {packet.hex(':')}")

        result = parser.parse_packet(packet)
        print(f"Тип: {result['type']}")

        if result['type'] == 'tags_found':
            data = result['data']
            for tag in data['tags']:
                print(f"  EPC: {tag.epc_formatted}")
                # if tag.rssi:
                print(f"  RSSI: {tag.rssi} dBm")
                # if tag.antenna:
                print(f"  Антенна: {tag.antenna}")
                all_tags.append(tag)

    print(f"\n{'=' * 70}")
    print(f"ИТОГО УНИКАЛЬНЫХ МЕТОК: {len(set(t.epc for t in all_tags))}")
    print(f"ВСЕГО ПРОЧТЕНИЙ: {len(all_tags)}")

    # Выводим уникальные метки
    unique = {}
    for tag in all_tags:
        if tag.epc not in unique:
            unique[tag.epc] = tag

    print(f"\nУНИКАЛЬНЫЕ МЕТКИ:")
    for epc, tag in unique.items():
        print(f"  {tag.epc_formatted} (RSSI: {tag.rssi} dBm)")


# ============================================================================
# ТЕСТИРОВАНИЕ НА РЕАЛЬНЫХ ДАННЫХ
# ============================================================================

if __name__ == "__main__":
    # Демонстрация на реальных данных из логов
    demo_with_real_data()

    # Дополнительно: анализ второго сканирования (где 4 метки)
    print("\n\n" + "=" * 70)
    print("АНАЛИЗ ВТОРОГО СКАНИРОВАНИЯ (4 метки)")
    print("=" * 70)

    raw_hex_2 = (
        "A02901810004203000E2806894000050035FD77070430A430A"
        "3000E2806894000050035FD77070101001E8"
        "A02901810004203400010000000000000000000051B9A9B9A9"
        "3400010000000000000000000051101001A0"
        "A02901810004203000E2806894000040138945853E81298129"
        "3000E2806894000040138945853E10100138"
        "A02901810004203400E7770201000000000000000046844684"
        "3400E77702010000000000000000101001B2"
    )

    raw_data_2 = bytes.fromhex(raw_hex_2)
    splitter = PacketSplitter()
    packets_2 = splitter.split(raw_data_2)
    parser = RFIDPacketParser()

    tags_2 = []
    for packet in packets_2:
        result = parser.parse_packet(packet)
        if result['type'] == 'tags_found':
            tags_2.extend(result['data']['tags'])

    print(f"Всего пакетов: {len(packets_2)}")
    print(f"Всего меток: {len(tags_2)}")
    print(f"Уникальных: {len(set(t.epc for t in tags_2))}")

    for tag in tags_2:
        print(f"  {tag.epc_formatted} (RSSI: {tag.rssi} dBm)")

    print("\n" + "=" * 70)
    print("АРХИТЕКТУРА ГОТОВА К ИСПОЛЬЗОВАНИЮ")
    print("Для реального устройства:")
    print("  reader = RFIDReader('/dev/ttyS2')")
    print("  result = reader.scan()")
    print("  RFIDResultPrinter.print_full_report(result)")
    print("=" * 70)