from base_aux.servers.server_aiohttp import ServerAiohttpBase


server = ServerAiohttpBase()
server.start()
server.wait()
