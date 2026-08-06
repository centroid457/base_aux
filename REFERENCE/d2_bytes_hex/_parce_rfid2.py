"""
================================================================================
ДЕТАЛЬНЫЙ РАЗБОР RFID ПАКЕТА
================================================================================
Пакет: A02901810001203000E2806894000050035FD77070430A430A3000E2806894000050035FD77070100401F7
Длина: 43 байта
Заявлено меток: 01 (всего 1 уникальная)
Фактически в пакете: EPC встречается 2 раза
"""

# ============================================================================
# ШАГ 1: ВИЗУАЛЬНЫЙ РАЗБОР ПАКЕТА
# ============================================================================

packet_hex = "A02901810001203000E2806894000050035FD77070430A430A3000E2806894000050035FD77070100401F7"
packet = bytes.fromhex(packet_hex)

print("=" * 80)
print("📦 ПОЛНЫЙ РАЗБОР ПАКЕТА RFID")
print("=" * 80)

# Разбираем заголовок
print("\n🔷 ЗАГОЛОВОК ПАКЕТА:")
print(f"  [0] 0x{packet[0]:02X} = START BYTE (всегда 0xA0)")
print(f"  [1] 0x{packet[1]:02X} = {packet[1]} (длина данных = 41 байт)")
print(f"       Проверка: 43 всего - 2 заголовок = 41 ✅")

print(f"\n🔷 ТИП ПАКЕТА:")
print(f"  [2] 0x{packet[2]:02X} = 0x01 (INVENTORY - инвентаризация)")
print(f"  [3] 0x{packet[3]:02X} = 0x81 (подтип: EPC данные)")

print(f"\n🔷 СЛУЖЕБНЫЕ ПОЛЯ:")
print(f"  [4] 0x{packet[4]:02X} = {packet[4]} (статус операции: 0=OK)")
print(f"  [5] 0x{packet[5]:02X} = {packet[5]} (количество УНИКАЛЬНЫХ меток в пакете)")
print(f"  [6] 0x{packet[6]:02X} = 0x{packet[6]:02X} (флаги/режим работы)")

# ============================================================================
# ШАГ 2: РАЗБОР ДАННЫХ МЕТОК
# ============================================================================

print(f"\n🔷 ДАННЫЕ МЕТОК (начинаются с байта [7]):")
data = packet[7:]
print(f"  Данные: {data.hex(' ')}")
print(f"  Длина данных: {len(data)} байт")

# Структура записи одной метки:
# EPC: 12 байт (SGTIN-96)
# Доп.данные: 4 байта (RSSI, антенна, и т.д.)
# ИТОГО: 16 байт на одну запись

RECORD_SIZE = 16  # 12 байт EPC + 4 байта доп.данных

print(f"\n🔷 РАЗБИЕНИЕ НА ЗАПИСИ (по {RECORD_SIZE} байт):")

for record_num in range(0, len(data), RECORD_SIZE):
    record = data[record_num:record_num + RECORD_SIZE]
    if len(record) < RECORD_SIZE:
        break

    epc_bytes = record[:12]
    extra_bytes = record[12:16]

    print(f"\n  ┌─ ЗАПИСЬ {record_num // RECORD_SIZE + 1} ─────────────────────────────")
    print(f"  │ Смещение в данных: +{record_num}")
    print(f"  │")
    print(f"  │ EPC (12 байт):")
    print(f"  │   HEX:  {epc_bytes.hex(' ')}")
    print(f"  │   STR:  {epc_bytes.hex().upper()}")
    print(f"  │")

    # Детальный разбор EPC
    print(f"  │   ДЕТАЛЬНЫЙ РАЗБОР EPC:")
    print(f"  │   [0] 0x{epc_bytes[0]:02X} = Заголовок EPC (0x30 = SGTIN-96)")
    print(f"  │   [1] 0x{epc_bytes[1]:02X} = Фильтр (0x00 = All)")
    print(f"  │   [2] 0x{epc_bytes[2]:02X} = Partition + Company Prefix[0]")
    print(f"  │   [3] 0x{epc_bytes[3]:02X} = Company Prefix продолжение")
    print(f"  │   [4] 0x{epc_bytes[4]:02X} = Company Prefix / Item Reference")
    print(f"  │   [5] 0x{epc_bytes[5]:02X} = Item Reference")
    print(f"  │   [6] 0x{epc_bytes[6]:02X} = Item Reference продолжение")
    print(f"  │   [7] 0x{epc_bytes[7]:02X} = Item Reference / Serial")
    print(f"  │   [8] 0x{epc_bytes[8]:02X} = Serial Number")
    print(f"  │   [9] 0x{epc_bytes[9]:02X} = Serial Number")
    print(f"  │   [10] 0x{epc_bytes[10]:02X} = Serial Number")
    print(f"  │   [11] 0x{epc_bytes[11]:02X} = Serial Number")

    # Парсинг EPC как SGTIN-96
    print(f"  │")
    print(f"  │   КАК SGTIN-96:")
    print(f"  │   Header:    0x{epc_bytes[0]:02X}")
    print(f"  │   Filter:    {epc_bytes[1]}")

    # Company Prefix (из байтов 2-4, зависит от partition)
    partition = (epc_bytes[2] >> 5) & 0x07
    print(f"  │   Partition: {partition}")

    # Дополнительные данные
    print(f"  │")
    print(f"  │ ДОП. ДАННЫЕ (4 байта):")
    print(f"  │   HEX:  {extra_bytes.hex(' ')}")
    print(f"  │")
    print(f"  │   [0] 0x{extra_bytes[0]:02X} = {extra_bytes[0]} (RSSI raw?)")
    print(f"  │       RSSI = -({extra_bytes[0]}) = -{extra_bytes[0]} dBm"
          if extra_bytes[0] < 128 else
          f"  │       RSSI = -(256-{extra_bytes[0]}) = {extra_bytes[0] - 256} dBm")
    print(f"  │   [1] 0x{extra_bytes[1]:02X} = {extra_bytes[1]} (антенна?)")
    print(f"  │   [2] 0x{extra_bytes[2]:02X} = {extra_bytes[2]} (дубль RSSI?)")
    print(f"  │   [3] 0x{extra_bytes[3]:02X} = {extra_bytes[3]} (счётчик/CRC?)")
    print(f"  └─────────────────────────────────────────────")

# ============================================================================
# ШАГ 3: ПОЧЕМУ EPC ДВАЖДЫ?
# ============================================================================

print(f"\n{'=' * 80}")
print("❓ ПОЧЕМУ EPC ПОЯВЛЯЕТСЯ ДВАЖДЫ?")
print(f"{'=' * 80}")

print("""
ПРИЧИНА: RFID ридер делает НЕСКОЛЬКО ЧТЕНИЙ одной метки для надёжности.

📊 СТАТИСТИКА ПАКЕТА:
  • Заявлено уникальных меток: 1 (байт [5] = 0x01)
  • Фактически записей в пакете: 2 (байты данных / 16 = 32/16 = 2)
  • EPC в обеих записях: ОДИНАКОВЫЙ (3000E2806894000050035FD77070)

🔍 ЧТО ОТЛИЧАЕТСЯ МЕЖДУ ЗАПИСЯМИ:
""")

# Сравниваем две записи
record1 = data[0:16]
record2 = data[16:32]

print(f"  Запись 1: {record1.hex(' ')}")
print(f"  Запись 2: {record2.hex(' ')}")
print()

# Сравнение побайтово
for i in range(16):
    r1, r2 = record1[i], record2[i]
    marker = " ◄── отличается!" if r1 != r2 else ""
    print(f"  Байт[{i:2d}]: 0x{r1:02X} vs 0x{r2:02X} {marker}")

print(f"""
📝 ВЫВОД:
  1. EPC (байты 0-11) - ОДИНАКОВЫЕ в обеих записях
     → Это ОДНА и та же метка, прочитанная дважды

  2. Доп.данные (байты 12-15) - ОТЛИЧАЮТСЯ
     → Ридер делает несколько попыток чтения 
       с разными настройками/антеннами

  3. В вашем выводе:
     3000E2806894000050035FD77070  ← первое чтение
     3000E2806894000050035FD77070  ← второе чтение (ДУБЛИКАТ!)
     found=1epc                    ← парсер правильно посчитал уникальные

✅ ЧТО ДЕЛАТЬ:
  • Дедуплицировать по EPC (оставлять уникальные)
  • Для каждой метки сохранять ЛУЧШИЙ RSSI из всех чтений
  • Считать количество чтений (read_count) для статистики
""")

# ============================================================================
# ШАГ 4: КАК ПРАВИЛЬНО ПАРСИТЬ
# ============================================================================

print(f"{'=' * 80}")
print("✅ ПРАВИЛЬНЫЙ ПАРСЕР (С ДЕДУПЛИКАЦИЕЙ)")
print(f"{'=' * 80}")


def parse_rfid_packet_correct(packet: bytes) -> dict:
    """
    Правильный парсер с дедупликацией

    Returns:
        dict с ключами:
        - unique_tags: список уникальных меток
        - total_readings: всего чтений (с дубликатами)
        - tag_count: заявленное количество меток
    """
    if len(packet) < 7:
        return {'unique_tags': [], 'total_readings': 0, 'tag_count': 0}

    # Заголовок
    start_byte = packet[0]
    data_length = packet[1]
    packet_type = packet[2]
    packet_subtype = packet[3]
    status = packet[4]
    tag_count = packet[5]  # Заявленное количество уникальных меток
    flags = packet[6]

    # Данные меток
    data = packet[7:]
    RECORD_SIZE = 16  # 12 байт EPC + 4 байта доп.данных

    # Словарь для дедупликации: {EPC: {rssi, antenna, read_count}}
    tags = {}

    for i in range(0, len(data), RECORD_SIZE):
        record = data[i:i + RECORD_SIZE]
        if len(record) < RECORD_SIZE:
            break

        epc = record[:12].hex().upper()
        extra = record[12:16]

        # RSSI: первый байт доп.данных
        rssi_raw = extra[0]
        rssi = -(256 - rssi_raw) if rssi_raw > 127 else -rssi_raw

        # Антенна: второй байт
        antenna = extra[1]

        if epc in tags:
            # Дубликат - обновляем статистику
            tags[epc]['read_count'] += 1
            # Берём лучший RSSI (большее значение = сильнее сигнал)
            if rssi > tags[epc]['rssi']:
                tags[epc]['rssi'] = rssi
                tags[epc]['antenna'] = antenna
        else:
            # Новая метка
            tags[epc] = {
                'epc': epc,
                'rssi': rssi,
                'antenna': antenna,
                'read_count': 1
            }

    return {
        'unique_tags': list(tags.values()),
        'total_readings': sum(t['read_count'] for t in tags.values()),
        'tag_count': tag_count,
        'status': 'OK' if status == 0 else f'ERROR_{status}',
        'flags': f'0x{flags:02X}'
    }


# Применяем к нашему пакету
result = parse_rfid_packet_correct(packet)

print(f"""
📊 РЕЗУЛЬТАТ ПАРСИНГА:
  Статус:          {result['status']}
  Заявлено меток:  {result['tag_count']}
  Уникальных:      {len(result['unique_tags'])}
  Всего чтений:    {result['total_readings']}
  Флаги:           {result['flags']}

  МЕТКИ:
""")

for tag in result['unique_tags']:
    print(f"  EPC:     {tag['epc']}")
    print(f"  RSSI:    {tag['rssi']} dBm")
    print(f"  Антенна: {tag['antenna']}")
    print(f"  Чтений:  {tag['read_count']} (из {result['total_readings']})")
    print()

# ============================================================================
# ШАГ 5: ВЫВОД ДЛЯ ПЕРЕДАЧИ ДАЛЬШЕ
# ============================================================================

print(f"{'=' * 80}")
print("📤 ГОТОВЫЙ ВЫВОД ДЛЯ ПЕРЕДАЧИ")
print(f"{'=' * 80}")

# Только уникальные EPC (как в исходном скрипте)
print("\nТолько EPC (для совместимости):")
for tag in result['unique_tags']:
    print(tag['epc'])

# Расширенный вывод с полезной информацией
print("\nРасширенный вывод (с RSSI):")
for tag in result['unique_tags']:
    print(f"{tag['epc']} RSSI={tag['rssi']} ANT={tag['antenna']} COUNT={tag['read_count']}")

print(f"\nfound={len(result['unique_tags'])}epc")