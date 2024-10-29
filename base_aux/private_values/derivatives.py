# =====================================================================================================================
# DONOT apply PrivateBase nesting!

class PrivateAuth:
    """Typical structure for AUTH

    :ivar USER: user login name
    :ivar PWD: password
    """
    USER: str
    PWD: str


class PrivateTgBotAddress:
    """Typical structure for Telegram bot address

    :ivar LINK_ID: just a bot id, not important
    :ivar NAME: just a bot public name, not important
    :ivar TOKEN: bot token for connection, important!
    """
    LINK_ID: str     # @mybot20230913
    NAME: str        # MyBotPublicName
    TOKEN: str


# =====================================================================================================================
