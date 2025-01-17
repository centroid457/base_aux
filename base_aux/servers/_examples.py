from base_aux.servers.m2_server1_aiohttp import ServerAiohttpBase


server = ServerAiohttpBase()
server.start()
server.wait()
