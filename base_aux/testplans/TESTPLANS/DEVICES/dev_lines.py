from base_aux.loggers.m1_print import *
from base_aux.testplans.devices_base import *
from base_aux.breeders.m3_table_inst import *
from base_aux.testplans.TESTPLANS.DEVICES import atc, ptb
from base_aux.testplans.devices_kit import DeviceKit


# =====================================================================================================================
class DeviceLines__AtcPtbDummy(DeviceKit):
    ATC = TableLine(atc.DeviceDummy(3))
    DUT = TableLine(*[ptb.DeviceDummy(index) for index in range(2)])


# =====================================================================================================================
class DeviceLines__Psu800(DeviceKit):
    ATC = TableLine(atc.Device(3))
    DUT = TableLine(*[ptb.Device(index) for index in range(10)])

    def resolve_addresses(self) -> None:
        class Dev(SerialClient):
            BAUDRATE = 115200
            EOL__SEND = b"\n"

        result = Dev.addresses_dump__answers("*:get name", "*:get addr")
        print(result)
        for port, responses in result.items():
            name_i = responses["*:get name"]
            addr_i = responses["*:get addr"]
            Print(f"{port}{responses}")

            if name_i == "ATC":
                filter_link = lambda dev: dev.NAME == name_i
            elif name_i == "PTB":
                filter_link = lambda dev: dev.NAME == name_i and dev.INDEX+1 == addr_i
            else:
                continue

            match = list(filter(filter_link,  self.iter_lines_insts()))
            dev_found = match and list(match)[0]
            if dev_found:
                dev_found.ADDRESS = port

        for dev in self.iter_lines_insts():
            if not isinstance(dev.ADDRESS, str):
                dev.ADDRESS = Enum__AddressAutoAcceptVariant.NOT_FOUND

        pass


# =====================================================================================================================
if __name__ == '__main__':
    DeviceLines__Psu800().resolve_addresses()


# =====================================================================================================================
