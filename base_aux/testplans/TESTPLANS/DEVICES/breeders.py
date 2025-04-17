from . import atc, ptb
from base_aux.buses.m1_serial1_client import SerialClient, Enum__AddressAutoAcceptVariant
from base_aux.testplans.devices import DevicesBreeder_WithDut


# =====================================================================================================================
class DevicesBreeder__AtcPtbDummy(DevicesBreeder_WithDut):
    COUNT = 2     # setup later???
    CLS_SINGLE__ATC = atc.Device
    CLS_LIST__DUT = ptb.DeviceDummy
    # CLS_LIST__DUT = dut.Device


# =====================================================================================================================
class DevicesBreeder__Psu800(DevicesBreeder_WithDut):
    COUNT = 10
    CLS_SINGLE__ATC = atc.Device
    CLS_LIST__DUT = ptb.Device
    # CLS_LIST__PTB = ptb.Device

    @classmethod
    def resolve_addresses__cls(cls) -> None:
        pass

        class Dev(SerialClient):
            pass
            BAUDRATE = 115200
            EOL__SEND = b"\n"

        result = Dev.addresses_dump__answers("*:get name", "*:get addr")
        for port, responses in result.items():
            name_i = responses["*:get name"]
            addr_i = responses["*:get addr"]
            print(port, responses)

            if name_i == "ATC":
                filter_link = lambda dev: dev.NAME == name_i
            elif name_i == "PTB":
                filter_link = lambda dev: dev.NAME == name_i and dev.INDEX+1 == addr_i
            else:
                continue

            match = list(filter(filter_link,  cls.LIST__ALL_GENERATED))
            dev_found = match and list(match)[0]
            if dev_found:
                dev_found.ADDRESS = port

        for dev in cls.LIST__ALL_GENERATED:
            if not isinstance(dev.ADDRESS, str):
                dev.ADDRESS = Enum__AddressAutoAcceptVariant.NOT_FOUND

        pass


# =====================================================================================================================
