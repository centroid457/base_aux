from typing import *
import re


# ======================================================================================================================
def parse_rfid__split_pkgs(data_raw: bytes) -> list[bytes]:
    # print(bytes.fromhex("A004018122B8"))  # b'\xa0\x04\x01\x81"\xb8'
    print()
    print(data_raw)

    result = []
    index_start = -1

    # data_hex = data_raw.hex().upper()

    while True:
        # Ищем начало пакета 0xA0
        index_start: int = data_raw.find(0xA0, index_start + 1)
        print(f"{index_start=}")
        if index_start == -1:
            break

        pkg_length: int = data_raw[index_start + 1]
        pkg: bytes = data_raw[index_start: index_start + 2 + pkg_length]
        result.append(pkg)

    return result


# ----------------------------------------------------------------------------------------------------------------------
def test__split_pkg():
    assert parse_rfid__split_pkgs(bytes.fromhex("A004018122B8")) == [bytes.fromhex("A004018122B8"), ]
    assert (
            parse_rfid__split_pkgs(bytes.fromhex("A02901810001203000E2806894000050035FD77070430A430A3000E2806894000050035FD77070100401F7"))
            ==
            [bytes.fromhex("A02901810001203000E2806894000050035FD77070430A430A3000E2806894000050035FD77070100401F7"), ]
    )
    assert (
            parse_rfid__split_pkgs(bytes.fromhex("A02901810002203000E2806894000040138945853E812981293000E2806894000040138945853E10040146A02901810002203000E2806894000050035FD77070430A430A3000E2806894000050035FD77070100401F6"))
            ==
            [
                bytes.fromhex("A02901810002203000E2806894000040138945853E812981293000E2806894000040138945853E10040146"),
                bytes.fromhex("A02901810002203000E2806894000050035FD77070430A430A3000E2806894000050035FD77070100401F6"),
            ]
    )


# ======================================================================================================================
