import serial, time

SOURCE_ADR: str = '/dev/ttyUSB0'
START_UBX: bytes = b'\xb5\x62'
MAX_BUFFER: int = 1000

s = serial.Serial(SOURCE_ADR, 9600, timeout=0.8)
time.sleep(0.3)
s.reset_input_buffer()            # clear previous NMEA
s.write(b'\xb5\x62\x0a\x04\x00\x00\x0e\x34')   # UBX MON-VER

result = b''
while True:
    chunk = s.read(1)
    if not chunk:
        break   # timeout

    result += chunk

    if result[-2:] == START_UBX:
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
        print('UBX_RESPONSE:[' + full_msg.hex().upper() + ']')
        break

    if len(result) >= MAX_BUFFER:
        break

s.close()