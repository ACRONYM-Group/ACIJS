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


def init(aci_type, port=8765, ip="127.0.0.1", name="main"):
    """
        Call from host to start ACI
    """
    threading.Thread(target=createServerOrClient,
                     args=(aci_type, port, ip, asyncio.get_event_loop(),
                           lastResponse, name), daemon=True).start()


def create_server_or_client(aci_type, port, ip, loop, last_response, name):
    """
        Start the ACI Server or Client
    """
    nodeType = aci_type
    if nodeType == "server":
        server = ACIServer.server(loop)
    
    if nodeType == "client":
        connections[name] = ACIconnection.connection(ip, port, loop)


def get_val(key, db_key, server="main"):
    """
        Gets a value when called from the host
    """
    while len(connections) == 0:
        time.sleep(0.01)
    return asyncio.run(connections[server].getValue(key, db_key))


def set_val(key, dbKey, val, server="main"):
    """
        Sets a value when called from the host
    """
    asyncio.run(connections[server].setValue(key, dbKey, val))
