from base_aux.servers import ServerAiohttpBase


server = ServerAiohttpBase()
server.start()
server.wait()
