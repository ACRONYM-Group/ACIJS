import websockets
import threading
import asyncio
import json
import time
import ACIconnection
import ACIServer

dbNodeIP = "127.0.0.1"
dbNodePort = "80"
nodeType = "server"
lastResponse = ["None", "None", "None"]


connections = {}

#Call from host to start ACI
def init(type, port=8765, ip="127.0.0.1", name="main"):
    loop = asyncio.get_event_loop()
    newThread = threading.Thread(target=createServerOrClient, args=(type, port, ip, loop, lastResponse, name), daemon=True)
    newThread.start()

#Start the ACI Server or Client
def createServerOrClient(type, port, ip, loop, lastResponse, name):
    nodeType = type
    if nodeType == "server":
        server = ACIServer.server(loop)
    
    if nodeType == "client":
        connections[name] = ACIconnection.connection(ip, port, loop)
        
#Interface Methods for host application
#Call Get() from the host to return a value

def get(key, dbKey, server="main"):
    if len(connections) == 0:
        while len(connections) == 0:
            time.sleep(0.01)
    output = asyncio.run(connections[server].getValue(key, dbKey))
    return output

#Call set() from the host to set a value

def set(key, dbKey, val, server="main"):
    asyncio.run(connections[server].setValue(key, dbKey, val))



