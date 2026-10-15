# ==============================================
# 1=USE HEX - best transmitting data +parsing
# 2=USE HEX.UPPER - best parsing

# 1/ in text lines use bytes_data.hex().upper()
import re

# PACK DATA
bytes_data_1: bytes = b"\t(value\x00)\n"
bytes_data_2: bytes = b"\t(value\x31)\n"
output_txt: str = f"START_SCAN\nDATA_HEX:[{bytes_data_1.hex().upper()}]\nDATA_HEX:[{bytes_data_2.hex().upper()}]\nSTATUS:OK\n"
print(output_txt)

# UNPACK data
results_hex: list[str] = re.findall(r"DATA_HEX:\[([0-9A-F]+)\]", output_txt)
print(f"{results_hex=}")
results_bytes = [bytes.fromhex(line_hex) for line_hex in results_hex]
print(f"{results_bytes=}")

