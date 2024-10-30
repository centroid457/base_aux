# from typing import *
# from testplans import DutBase
#
#
# # =====================================================================================================================
# class Device(DutBase):
#     @property
#     def VALUE(self) -> bool:
#         return self.INDEX % 2 == 0


# =====================================================================================================================
# DONT USE IT!!!
# class DeviceOverPtb(DutBase):
#     __sn_start: str = "SN"
#     BREEDER: 'DevicesBreeder'
#
#     def connect(self):
#         return self.BREEDER.PTB.connect()
#
#     @property
#     def VALUE(self) -> bool:
#         return self.INDEX % 2 == 0
#
#     @property
#     def SN(self) -> str:
#         return f"{self.__sn_start}_{self.INDEX}"
#
#     @SN.setter
#     def SN(self, value: Any) -> None:
#         self.__sn_start = str(value).upper()


# =====================================================================================================================
