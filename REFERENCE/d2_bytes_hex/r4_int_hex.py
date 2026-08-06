"""
================================================================================
КАК ПРАВИЛЬНО РАСШИФРОВАТЬ ЧИСЛО ИЗ HEX
================================================================================
Проблема: int(bytes.fromhex("01")) не работает
Причина: bytes.fromhex() возвращает БАЙТЫ, а int() от байтов ожидает СТРОКУ
"""

print(int("0", 16))     # 0
print(int("00", 16))    # 0
print(int("01", 16))    # 1
print(int("10", 16))    # 16
print(int("29", 16))    # 41

# ============================================================================
# БЛОК 2: ПРАВИЛЬНЫЕ СПОСОБЫ
# ============================================================================

print("\n" + "=" * 60)
print("ПРАВИЛЬНЫЕ СПОСОБЫ РАСШИФРОВКИ")
print("=" * 60)

# СПОСОБ 1: Из HEX-строки напрямую в число
print("\n1️⃣ ИЗ HEX-СТРОКИ В ЧИСЛО:")
hex_str = "01"
number = int(hex_str, 16)  # Второй аргумент - основание системы счисления
print(f"   int('{hex_str}', 16) = {number}")

hex_str = "FF"
number = int(hex_str, 16)
print(f"   int('{hex_str}', 16) = {number}")

hex_str = "ABCD"
number = int(hex_str, 16)
print(f"   int('{hex_str}', 16) = {number}")

# СПОСОБ 2: Из байтов в число
print("\n2️⃣ ИЗ БАЙТОВ В ЧИСЛО:")
# Когда у вас уже есть bytes (например, из UART)

# Один байт
single_byte = b'\x01'
number = single_byte[0]  # Индексация bytes возвращает int!
print(f"   b'\\x01'[0] = {number}")

single_byte = b'\xFF'
number = single_byte[0]
print(f"   b'\\xFF'[0] = {number}")

# Несколько байтов -> число (big-endian)
multi_bytes = b'\x12\x34'
number = int.from_bytes(multi_bytes, byteorder='big')
print(f"   int.from_bytes(b'\\x12\\x34', 'big') = {number}")

# Несколько байтов -> число (little-endian)
number = int.from_bytes(multi_bytes, byteorder='little')
print(f"   int.from_bytes(b'\\x12\\x34', 'little') = {number}")

# СПОСОБ 3: Из bytes в hex-строку, потом в число
print("\n3️⃣ BYTES -> HEX СТРОКА -> ЧИСЛО:")
data = b'\x01'
hex_str = data.hex()        # '01'
number = int(hex_str, 16)   # 1
print(f"   b'\\x01'.hex() -> '{hex_str}' -> int('{hex_str}', 16) = {number}")

data = b'\xAB\xCD'
hex_str = data.hex()        # 'abcd'
number = int(hex_str, 16)   # 43981
print(f"   b'\\xAB\\xCD'.hex() -> '{hex_str}' -> int('{hex_str}', 16) = {number}")

# ============================================================================
# БЛОК 3: ШПАРГАЛКА ВСЕХ ПРЕОБРАЗОВАНИЙ
# ============================================================================

print("\n" + "=" * 60)
print("ПОЛНАЯ ШПАРГАЛКА ПРЕОБРАЗОВАНИЙ")
print("=" * 60)

# HEX строка -> число
print("\n📌 HEX СТРОКА -> ЧИСЛО:")
print(f"   int('01', 16)     = {int('01', 16)}")
print(f"   int('FF', 16)     = {int('FF', 16)}")
print(f"   int('ABCD', 16)   = {int('ABCD', 16)}")
print(f"   int('0x01', 16)   = {int('0x01', 16)} (0x префикс игнорируется)")
print(f"   int('0x01', 0)    = {int('0x01', 0)} (автоопределение по префиксу)")

# Число -> HEX строка
print("\n📌 ЧИСЛО -> HEX СТРОКА:")
print(f"   hex(1)            = '{hex(1)}'")
print(f"   hex(255)          = '{hex(255)}'")
print(f"   f'{{1:02X}}'      = '{1:02X}' (всегда 2 символа)")
print(f"   f'{{1:04X}}'      = '{1:04X}' (всегда 4 символа)")

# Байты -> число (разные способы)
print("\n📌 БАЙТЫ -> ЧИСЛО:")
b = b'\x01'
print(f"   b'\\x01'[0]                          = {b[0]}")
print(f"   int.from_bytes(b'\\x01', 'big')      = {int.from_bytes(b, 'big')}")
print(f"   int(b'\\x01'.hex(), 16)              = {int(b.hex(), 16)}")

# Несколько байтов
b = b'\x12\x34'
print(f"   int.from_bytes(b'\\x12\\x34', 'big')    = {int.from_bytes(b, 'big')}")
print(f"   int.from_bytes(b'\\x12\\x34', 'little') = {int.from_bytes(b, 'little')}")

# Число -> байты
print("\n📌 ЧИСЛО -> БАЙТЫ:")
print(f"   (1).to_bytes(1, 'big')              = {(1).to_bytes(1, 'big')}")
print(f"   (255).to_bytes(1, 'big')            = {(255).to_bytes(1, 'big')}")
print(f"   (4660).to_bytes(2, 'big')           = {(4660).to_bytes(2, 'big')}")
print(f"   (4660).to_bytes(2, 'little')        = {(4660).to_bytes(2, 'little')}")

# ============================================================================
# БЛОК 4: ВАШ КОНКРЕТНЫЙ СЛУЧАЙ - КАК ПРАВИЛЬНО
# ============================================================================

print("\n" + "=" * 60)
print("ВАШ СЛУЧАЙ: ЧИСЛО 1 В HEX")
print("=" * 60)

# Если у вас HEX-строка "01"
hex_string = "01"

# Правильные способы получить число 1:
print(f"\nИз hex-строки '{hex_string}':")
print(f"   int('{hex_string}', 16) = {int(hex_string, 16)}")  # ✅ ПРАВИЛЬНО

# Если у вас байты b'\x01'
bytes_data = b'\x01'

print(f"\nИз байтов {bytes_data}:")
print(f"   {bytes_data}[0] = {bytes_data[0]}")                    # ✅ ПРАВИЛЬНО
print(f"   int.from_bytes({bytes_data}, 'big') = {int.from_bytes(bytes_data, 'big')}")  # ✅ ПРАВИЛЬНО
print(f"   int({bytes_data}.hex(), 16) = {int(bytes_data.hex(), 16)}")  # ✅ ПРАВИЛЬНО (но длинно)

# Если у вас hex-литерал в коде
print(f"\nHex-литерал в коде:")
print(f"   0x01 = {0x01}")  # ✅ ПРАВИЛЬНО

# ============================================================================
# БЛОК 5: ПРАКТИЧЕСКИЙ ПРИМЕР С RFID
# ============================================================================

print("\n" + "=" * 60)
print("ПРИМЕР: ПАРСИНГ ДАННЫХ RFID")
print("=" * 60)

# Имитация данных от RFID ридера
# Допустим, пришёл пакет с RSSI в одном байте
rssi_byte = b'\x9C'  # 156 в десятичной

# СПОСОБ 1: Индексация (простой)
rssi_raw = rssi_byte[0]  # 156
rssi_dbm = -rssi_raw       # -156 dBm
print(f"RSSI byte: {rssi_byte.hex()} -> raw={rssi_raw}, dBm={rssi_dbm}")

# СПОСОБ 2: from_bytes (для нескольких байт)
antenna_bytes = b'\x01'  # Номер антенны
antenna = int.from_bytes(antenna_bytes, 'big')  # 1
print(f"Antenna byte: {antenna_bytes.hex()} -> {antenna}")

# СПОСОБ 3: Если пришла HEX-строка (например, из JSON/лога)
hex_from_log = "9C"
rssi_raw = int(hex_from_log, 16)  # 156
rssi_dbm = -rssi_raw
print(f"RSSI from log: '{hex_from_log}' -> raw={rssi_raw}, dBm={rssi_dbm}")

# ============================================================================
# БЛОК 6: ТИПИЧНЫЕ ОШИБКИ
# ============================================================================

print("\n" + "=" * 60)
print("ТИПИЧНЫЕ ОШИБКИ И КАК ИСПРАВИТЬ")
print("=" * 60)

# ❌ ОШИБКА 1: int() от bytes
try:
    result = int(b'\x01')
except ValueError as e:
    print(f"❌ int(b'\\x01')        -> ValueError: {e}")
    print(f"✅ b'\\x01'[0]           -> {b'\\x01'[0]}")

# ❌ ОШИБКА 2: Забыли указать основание
try:
    result = int("FF")  # Думает что десятичное
except ValueError as e:
    print(f"\n❌ int('FF')           -> ValueError: {e}")
    print(f"✅ int('FF', 16)        -> {int('FF', 16)}")

# ❌ ОШИБКА 3: fromhex для одного символа
print(f"\n✅ bytes.fromhex('0F')  -> {bytes.fromhex('0F')}")
print(f"❌ bytes.fromhex('F')   -> ValueError (нужно чётное количество символов)")
print(f"✅ bytes.fromhex('0F')  -> используйте '0F' вместо 'F'")

# ============================================================================
# БЛОК 7: ВИЗУАЛЬНАЯ СХЕМА ПРЕОБРАЗОВАНИЙ
# ============================================================================

print("\n" + "=" * 60)
print("ВИЗУАЛЬНАЯ СХЕМА ВСЕХ ПРЕОБРАЗОВАНИЙ")
print("=" * 60)

schema = """
  HEX СТРОКА                    ЧИСЛО (int)               БАЙТЫ (bytes)
  ──────────                    ───────────               ─────────────
     "01"                         1                      b'\\x01'
     "FF"                        255                     b'\\xFF'
   "ABCD"                       43981                    b'\\xAB\\xCD'

  ┌─────────────────────────────────────────────────────────────────┐
  │                                                                 │
  │  "01" ──── int("01", 16) ────► 1                               │
  │                                                                 │
  │  1 ──── hex(1) ──────────────► "0x1"                           │
  │  1 ──── f"{1:02X}" ─────────► "01"                             │
  │                                                                 │
  │  b'\\x01' ──── b'\\x01'[0] ────► 1                             │
  │  b'\\x01' ──── int.from_bytes(b'\\x01', 'big') ──► 1          │
  │                                                                 │
  │  1 ──── (1).to_bytes(1, 'big') ──► b'\\x01'                   │
  │                                                                 │
  │  "01" ──── bytes.fromhex("01") ──► b'\\x01'                   │
  │  b'\\x01' ──── b'\\x01'.hex() ────► "01"                      │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘

  ЗАПОМНИТЕ:
  • int("hex", 16)    — hex-строка → число
  • bytes.fromhex()   — hex-строка → байты
  • .hex()           — байты → hex-строка
  • [0]              — байты → число (один байт)
  • .from_bytes()    — байты → число (много байт)
  • .to_bytes()      — число → байты
"""

print(schema)