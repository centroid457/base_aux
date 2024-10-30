import base_aux.server_templates
import pathlib
import time


server = base_aux.server_templates.ServerAiohttpBase()
server.start()
server.wait()
