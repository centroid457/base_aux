# TRANSPORT = "serial"
# TRANSPORT = "ssh"
TRANSPORT = "rssh"

ADDRESS = "harvest14"

# SKIP or INSTALL ALL MODULES/UTILES on iot
PRE_SKIP = True
# PRE_SKIP = False


if TRANSPORT == "serial":
    ADDRESS = None  # used only one any found!

