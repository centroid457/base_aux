from base_aux.breeders.m3_table_inst import TableKit, TableColumn


# =====================================================================================================================
class DeviceKit(TableKit):
    def __del__(self):
        self.disconnect()

    def connect(self) -> None:
        self("connect")

    def disconnect(self) -> None:
        self("disconnect")

    # -----------------------------------------------------------------------------------------------------------------
    def resolve_addresses(self) -> None:
        """
        GOAL
        ----
        find all devices on Uart ports
        """
        pass


# =====================================================================================================================
class _DeviceColumn_Example(TableColumn):
    """
    NOTE
    ----
    use direct dynamic creation TableColumn(index, TLines)!

    GOAL
    ----
    just an example
    """
    LINES = DeviceKit()


# =====================================================================================================================
