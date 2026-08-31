import sys, time, serial, os

if len(sys.argv) < 2:
    print("Usage: python3 scr__gsm_at_client.py <AT command> [port] [baudrate]")
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