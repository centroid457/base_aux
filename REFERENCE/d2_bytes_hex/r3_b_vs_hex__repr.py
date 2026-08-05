"""
================================================================================
ПЕРЕДАЧА ДАННЫХ МЕЖДУ УСТРОЙСТВАМИ: БИНАРНЫЙ ФОРМАТ vs HEX-ПРЕДСТАВЛЕНИЕ
================================================================================
Ключевой принцип: Бинарные данные (bytes) и их HEX-представление (строка) -
это РАЗНЫЕ вещи с разными целями и накладными расходами.

RFID Reader --[BINARY UART]--> Linux Python --[BINARY UART]--> Следующее устройство
                                  |
                                  +--[HEX в лог-файл] (только для отладки)
"""


# ============================================================================
# БЛОК 1: ПОНИМАНИЕ РАЗНИЦЫ - В ЧЁМ СУТЬ
# ============================================================================
# ПРИНЦИП: Один байт данных (0-255) в HEX строке занимает 2 СИМВОЛА
# Это увеличивает объём передаваемых данных в 2 раза, но даёт преимущества

def demonstrate_hex_vs_binary():
    """
    НАГЛЯДНАЯ ДЕМОНСТРАЦИЯ: почему HEX-представление больше,
    но используется в определённых сценариях
    """
    # Исходные бинарные данные (4 байта)
    binary_data = bytes([0xAA, 0xBB, 0xCC, 0xDD])

    # HEX представление (строка из 8 символов)
    hex_string = binary_data.hex()  # 'aabbccdd'
    hex_bytes = hex_string.encode('ascii')  # 8 байт

    print("=" * 60)
    print("📊 СРАВНЕНИЕ: BINARY vs HEX ПЕРЕДАЧА")
    print("=" * 60)
    print(f"Исходные данные (binary):  {len(binary_data)} байта  -> {binary_data.hex(':')}")
    print(f"HEX строка:                {len(hex_string)} символов -> {hex_string}")
    print(f"HEX как байты (ASCII):     {len(hex_bytes)} байт     -> {hex_bytes.hex(':')}")
    print(f"\n💡 НАКЛАДНЫЕ РАСХОДЫ: {len(hex_bytes) / len(binary_data):.0f}x увеличение размера!")

    # Визуализация разницы
    print(f"\n📦 Бинарный пакет: [{' '.join(f'{b:02X}' for b in binary_data)}]")
    print(f"📝 HEX-строка:     \"{hex_string}\"")
    print(f"📏 Размеры:        {len(binary_data)} vs {len(hex_string)} (в 2 раза больше)")


demonstrate_hex_vs_binary()


# ============================================================================
# БЛОК 2: КОГДА ИСПОЛЬЗОВАТЬ БИНАРНЫЙ ФОРМАТ (ПРАВИЛЬНЫЙ ВЫБОР)
# ============================================================================
# ПРИНЦИП: Бинарный формат эффективен для передачи между устройствами,
# которые "понимают" бинарные протоколы

class BinaryProtocolSender:
    """
    ОТПРАВКА В БИНАРНОМ ФОРМАТЕ
    Когда использовать:
    - Устройство-приёмник тоже embedded (Arduino, STM32, ESP32)
    - Важен минимальный размер пакета
    - Высокая скорость передачи (экономия каждого байта)
    - Данные структурированы и известны обеим сторонам
    """

    @staticmethod
    def pack_rfid_data_binary(rfid_id: int, rssi: int, antenna: int, timestamp: int) -> bytes:
        """
        Упаковка RFID данных в компактный бинарный пакет
        Структура пакета: [TYPE(1)][LEN(1)][RFID_ID(5)][RSSI(1)][ANT(1)][TIME(4)][CRC(1)]
        ВСЕГО: 14 байт
        """
        packet = bytearray()

        # Заголовок
        packet.append(0x02)  # STX (Start of Text)

        # RFID ID как BCD (Binary Coded Decimal) - экономим место
        # 10-значный ID помещается в 5 байт вместо 10 в ASCII
        rfid_bytes = bytearray(5)
        for i in range(4, -1, -1):
            rfid_bytes[4 - i] = (rfid_id // (100 ** i) % 100)  # Каждый байт хранит 2 цифры
        packet.extend(rfid_bytes)

        # Данные
        packet.append(rssi & 0xFF)  # 1 байт на RSSI
        packet.append(antenna & 0xFF)  # 1 байт на номер антенны

        # Timestamp как 32-битное целое (4 байта)
        packet.extend(timestamp.to_bytes(4, 'big'))

        # CRC
        crc = sum(packet) & 0xFF
        packet.append(crc)

        packet.append(0x03)  # ETX (End of Text)

        return bytes(packet)


# Пример бинарной передачи
binary_packet = BinaryProtocolSender.pack_rfid_data_binary(
    rfid_id=1234567890,
    rssi=60,
    antenna=1,
    timestamp=1234567890
)
print(f"\n📦 БИНАРНЫЙ ПАКЕТ RFID: {len(binary_packet)} байт")
print(f"   {binary_packet.hex(' ')}")


# ============================================================================
# БЛОК 3: КОГДА ИСПОЛЬЗОВАТЬ HEX-ПРЕДСТАВЛЕНИЕ (ОСОБЫЕ СЛУЧАИ)
# ============================================================================
# ПРИНЦИП: HEX используется когда канал связи "текстовый" или нужна отладка

class HexProtocolSender:
    """
    ОТПРАВКА В HEX-ФОРМАТЕ (ТЕКСТОВОМ)
    Когда использовать:
    - Канал связи текстовый (UART с терминалом, HTTP, MQTT, WebSocket)
    - Нужна отладка человеком (видно глазами в логах)
    - Приёмник - компьютер/сервер с текстовыми парсерами
    - Протокол требует ASCII (AT-команды, SIM800, ESP8266 AT)
    - Данные проходят через текстовые системы (JSON, XML, CSV)
    """

    @staticmethod
    def pack_rfid_data_hex(rfid_id: int, rssi: int, antenna: int, timestamp: int) -> str:
        """
        Упаковка RFID данных в HEX-строку
        Формат: "STX,02,1234567890,3C,01,499602D2,CRC"
        ВСЕГО: ~38 символов (байт)
        """
        # Формируем HEX-строку как текстовый протокол
        parts = [
            "STX",  # Текстовый заголовок
            "02",  # Версия протокола
            f"{rfid_id:010d}",  # ID как строка (10 цифр)
            f"{rssi:02X}",  # RSSI в HEX (2 символа)
            f"{antenna:02X}",  # Номер антенны (2 символа)
            f"{timestamp:08X}",  # Timestamp в HEX (8 символов)
        ]

        message = ",".join(parts)

        # CRC как XOR всех байтов сообщения
        crc = 0
        for byte in message.encode('ascii'):
            crc ^= byte
        message += f",{crc:02X}"

        return message

    @staticmethod
    def pack_rfid_data_hex_compact(rfid_id: int, rssi: int, antenna: int, timestamp: int) -> str:
        """
        Компактный HEX формат без разделителей
        "02499602D23C01499602D2A7"
        """
        data = bytearray()

        # Упаковываем в бинарный формат сначала
        data.append(0x02)  # STX
        data.extend(rfid_id.to_bytes(5, 'big'))
        data.append(rssi)
        data.append(antenna)
        data.extend(timestamp.to_bytes(4, 'big'))

        # CRC
        crc = sum(data) & 0xFF
        data.append(crc)

        # Конвертируем ВСЁ в HEX строку
        return data.hex().upper()


# Демонстрация
rfid_id = 1234567890
rssi = 60
antenna = 1
timestamp = 1234567890

print(f"\n📝 HEX ПРЕДСТАВЛЕНИЯ RFID ДАННЫХ:")
print(f"   Читаемый HEX:   {HexProtocolSender.pack_rfid_data_hex(rfid_id, rssi, antenna, timestamp)}")
print(f"   Компактный HEX: {HexProtocolSender.pack_rfid_data_hex_compact(rfid_id, rssi, antenna, timestamp)}")


# ============================================================================
# БЛОК 4: ПРАКТИЧЕСКИЕ СЦЕНАРИИ - КОГДА ЧТО ВЫБРАТЬ
# ============================================================================

class RealWorldScenarios:
    """
    РЕАЛЬНЫЕ СЦЕНАРИИ И ПРАВИЛЬНЫЙ ВЫБОР ФОРМАТА
    """

    @staticmethod
    def scenario_1_mcu_to_mcu():
        """
        СЦЕНАРИЙ 1: STM32 -> STM32 через UART
        ВЫБОР: БИНАРНЫЙ ФОРМАТ
        ПРИЧИНА: Оба устройства embedded, быстрый парсинг, экономия трафика
        """
        # Отправитель (RFID ридер на STM32)
        rfid_id = 0x1234567890AB
        rssi = 45

        # Бинарный пакет: 8 байт
        binary = bytearray([0xAA])  # Стартовый байт
        binary.extend(rfid_id.to_bytes(6, 'big'))
        binary.append(rssi)
        binary.append(sum(binary) & 0xFF)  # CRC

        print(f"\n🔌 SCENARIO 1 (MCU -> MCU):")
        print(f"   Формат: BINARY")
        print(f"   Размер: {len(binary)} байт")
        print(f"   Данные: {binary.hex(' ')}")
        return binary

    @staticmethod
    def scenario_2_linux_uart_to_pc():
        """
        СЦЕНАРИЙ 2: Linux (Python) -> PC через UART/USB
        ВЫБОР: БИНАРНЫЙ + HEX ДЛЯ ОТЛАДКИ
        ПРИЧИНА: Python легко парсит бинарный, но нужен режим отладки
        """
        rfid_id = 1234567890

        # Основной режим - бинарный
        binary_mode = bytes([0xAA, 0x07, 0x01, 0x12, 0x34, 0x56, 0x78, 0x3C, 0x55])

        # Режим отладки - HEX
        hex_mode = f"RFID:{rfid_id:010d},RSSI:60,ANT:1\\r\\n".encode('ascii')

        print(f"\n💻 SCENARIO 2 (Linux -> PC):")
        print(f"   Production режим (binary): {binary_mode.hex(' ')}")
        print(f"   Debug режим (hex/text):    {hex_mode}")
        return binary_mode, hex_mode

    @staticmethod
    def scenario_3_http_mqtt():
        """
        СЦЕНАРИЙ 3: Устройство -> MQTT/HTTP на сервер
        ВЫБОР: HEX СТРОКА В JSON
        ПРИЧИНА: JSON текстовый, бинарные данные нужно кодировать
        """
        import json

        rfid_data = bytes([0x01, 0x12, 0x34, 0x56, 0x78, 0x3C])

        # Создаём JSON с HEX-строкой
        message = {
            "device": "RFID_READER_01",
            "timestamp": "2024-01-15T10:30:00Z",
            "rfid_tag": {
                "type": "EM4100",
                "id": "1234567890",
                "raw_hex": rfid_data.hex(),  # Бинарные данные как HEX
                "rssi": -60
            }
        }

        json_message = json.dumps(message)

        print(f"\n☁️ SCENARIO 3 (MQTT/HTTP):")
        print(f"   Формат: JSON с HEX-полем")
        print(f"   Размер: {len(json_message)} байт")
        print(f"   Данные: {json_message[:100]}...")
        return json_message

    @staticmethod
    def scenario_4_gateway_forwarding():
        """
        СЦЕНАРИЙ 4: RFID Ридер -> Шлюз -> Удалённый сервер
        ВЫБОР: БИНАРНЫЙ МЕЖДУ УСТРОЙСТВАМИ, HEX ДЛЯ СЕРВЕРА
        ПРИЧИНА: Шлюз конвертирует бинарный протокол в HTTP/JSON
        """

        class RFIDGateway:
            def forward_to_server(self, binary_packet: bytes) -> str:
                """Конвертация бинарного пакета в JSON для сервера"""
                # Парсим бинарный пакет
                if binary_packet[0] != 0xAA or binary_packet[-1] != 0x55:
                    raise ValueError("Invalid packet")

                tag_type = binary_packet[2]
                tag_id = int.from_bytes(binary_packet[3:7], 'big')
                rssi = binary_packet[7]

                # Конвертируем в JSON (автоматически в HEX не нужно,
                # поля становятся числами/строками)
                import json
                return json.dumps({
                    "tag_id": f"{tag_id:010d}",
                    "tag_type": "EM4100" if tag_type == 0x01 else "Unknown",
                    "rssi_dbm": -rssi
                })

        gateway = RFIDGateway()
        binary_packet = bytes([0xAA, 0x07, 0x01, 0x12, 0x34, 0x56, 0x78, 0x3C, 0xA2, 0x55])
        json_output = gateway.forward_to_server(binary_packet)

        print(f"\n🌉 SCENARIO 4 (Gateway):")
        print(f"   Вход (binary):  {binary_packet.hex(' ')}")
        print(f"   Выход (JSON):   {json_output}")
        return json_output


# ============================================================================
# БЛОК 5: ПРАВИЛА ВЫБОРА ФОРМАТА (ШПАРГАЛКА)
# ============================================================================

def format_selection_guide():
    """
    ПРАВИЛА ВЫБОРА: BINARY или HEX
    """
    print("\n" + "=" * 70)
    print("📋 ШПАРГАЛКА: КОГДА ИСПОЛЬЗОВАТЬ BINARY vs HEX")
    print("=" * 70)

    rules = [
        ("✅ BINARY (байты)", [
            "MCU <-> MCU через UART/SPI/I2C",
            "Нужна максимальная скорость и минимальный размер",
            "Обе стороны знают структуру пакета (фиксированный протокол)",
            "Энергоэффективные устройства (Bluetooth LE, LoRa, ZigBee)",
            "Потоковая передача данных (аудио, видео, сырые данные АЦП)"
        ]),
        ("✅ HEX STRING (текст)", [
            "Передача в JSON/XML/CSV/HTTP/MQTT",
            "Нужна отладка и читаемость человеком",
            "Канал связи текстовый (AT-команды модема, SMS)",
            "Приёмник не знает точную структуру (универсальный парсер)",
            "Данные проходят через текстовые прокси/логи",
            "Нужна самодиагностика (видно глазами в терминале)"
        ]),
        ("⚠️ ГИБРИДНЫЙ ПОДХОД", [
            "Основной канал - бинарный",
            "Есть команда переключения в debug mode (HEX)",
            "Шлюз конвертирует: BINARY(in) -> JSON(HEX out)",
            "Логирование: пишем и бинарные дампы, и HEX строки"
        ])
    ]

    for title, items in rules:
        print(f"\n{title}:")
        for item in items:
            print(f"  • {item}")


# ============================================================================
# БЛОК 6: ПРАКТИЧЕСКАЯ РЕАЛИЗАЦИЯ ДЛЯ ВАШЕГО СЛУЧАЯ
# ============================================================================

class RFIDDataForwarder:
    """
    ВАШ РЕАЛЬНЫЙ СЦЕНАРИЙ:
    RFID -> Linux (Python) -> дальше по UART

    ПРАВИЛЬНЫЙ ПОДХОД: БИНАРНЫЙ МЕЖДУ УСТРОЙСТВАМИ
    НО с возможностью HEX для отладки
    """

    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode
        self.packet_count = 0

    def create_forwarding_packet(self, rfid_id: int, rssi: int,
                                 tag_type: int, timestamp: int) -> bytes:
        """
        Создание пакета для пересылки
        В production: бинарный (12 байт)
        В debug: текстовый HEX (~40 байт)
        """
        self.packet_count += 1

        if not self.debug_mode:
            # РЕЖИМ PRODUCTION: компактный бинарный пакет
            packet = bytearray()

            # Фиксированный заголовок
            packet.extend(b'RFID')  # 4 байта - сигнатура

            # Данные (8 байт)
            packet.append(self.packet_count & 0xFF)  # Счётчик пакетов
            packet.append(tag_type)  # Тип метки
            packet.extend(rfid_id.to_bytes(4, 'big'))  # ID (4 байта)
            packet.append(rssi & 0xFF)  # RSSI
            packet.append(antenna := 0x01)  # Антенна

            # CRC16 (более надёжная чем CRC8)
            crc = self._crc16(bytes(packet))
            packet.extend(crc.to_bytes(2, 'big'))

            return bytes(packet)

        else:
            # РЕЖИМ DEBUG: читаемая строка
            debug_msg = (
                f"[PKT:{self.packet_count:04d}] "
                f"RFID:{rfid_id:010d} "
                f"TYPE:{tag_type:02X} "
                f"RSSI:{-rssi}dBm "
                f"TIME:{timestamp:08X}\r\n"
            )
            return debug_msg.encode('ascii')

    def _crc16(self, data: bytes) -> int:
        """CRC-16/XMODEM"""
        crc = 0x0000
        for byte in data:
            crc ^= (byte << 8)
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc <<= 1
                crc &= 0xFFFF
        return crc

    def switch_to_debug(self):
        """Переключение в режим отладки по команде"""
        self.debug_mode = True
        print("🔄 Переключено в DEBUG MODE (HEX строки)")

    def switch_to_production(self):
        """Возврат в production режим"""
        self.debug_mode = False
        print("🔄 Переключено в PRODUCTION MODE (бинарный)")


# Демонстрация
forwarder = RFIDDataForwarder()

print("\n" + "=" * 70)
print("🎯 ВАШ РАБОЧИЙ СЦЕНАРИЙ С RFID")
print("=" * 70)

# Production mode
print("\n📦 PRODUCTION MODE (бинарный):")
binary_pkt = forwarder.create_forwarding_packet(1234567890, 60, 0x01, 1234567890)
print(f"   Размер: {len(binary_pkt)} байт")
print(f"   Данные: {binary_pkt.hex(' ')}")

# Debug mode
forwarder.switch_to_debug()
print("\n🐛 DEBUG MODE (текстовый HEX):")
debug_pkt = forwarder.create_forwarding_packet(1234567890, 60, 0x01, 1234567890)
print(f"   Размер: {len(debug_pkt)} байт")
print(f"   Данные: {debug_pkt}")


# ============================================================================
# БЛОК 7: ВАЖНЫЕ ВЫВОДЫ И BEST PRACTICES
# ============================================================================

def final_recommendations():
    print("\n" + "=" * 70)
    print("🎓 ФИНАЛЬНЫЕ РЕКОМЕНДАЦИИ")
    print("=" * 70)

    print("""
1. ДЛЯ ПЕРЕДАЧИ МЕЖДУ УСТРОЙСТВАМИ:
   ✓ Используйте БИНАРНЫЙ формат (bytes)
   ✓ Структура: [START][TYPE][LEN][PAYLOAD][CRC][END]
   ✓ Размер пакета 8-64 байта для UART

2. HEX НУЖЕН ТОЛЬКО ДЛЯ:
   ✓ Отладки (логи, терминал, Wireshark)
   ✓ Текстовых протоколов (HTTP, MQTT, JSON)
   ✓ AT-команд (модемы, GSM модули)

3. НЕ ДЕЛАЙТЕ:
   ✗ Не передавайте HEX между MCU (трата 50% трафика)
   ✗ Не используйте ASCII для числовых данных (парсинг медленный)
   ✗ Не храните бинарные данные как HEX в БД (если не нужен поиск)

4. ГИБРИДНЫЙ ПОДХОД:
   ✓ Добавьте команду переключения debug/production режима
   ✓ В production: бинарный компактный формат
   ✓ В debug: читаемый HEX для анализа проблем

5. ДЛЯ ВАШЕГО СЛУЧАЯ (RFID через Linux):
   RFID Reader -> [BINARY UART] -> Linux Python -> [BINARY UART] -> Next Device
                                     └-> [HEX LOG FILE] (для отладки)
                                     └-> [JSON + HEX] -> Server (если нужно)
""")


# Запускаем все демонстрации
if __name__ == "__main__":
    demonstrate_hex_vs_binary()

    # Все сценарии
    RealWorldScenarios.scenario_1_mcu_to_mcu()
    RealWorldScenarios.scenario_2_linux_uart_to_pc()
    RealWorldScenarios.scenario_3_http_mqtt()
    RealWorldScenarios.scenario_4_gateway_forwarding()

    format_selection_guide()
    final_recommendations()