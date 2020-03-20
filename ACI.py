import threading
import asyncio
import time

import ACIconnection
import ACIServer

db_node_ip = "127.0.0.1"
db_node_port = "80"
node_type = "server"
last_response = ["None", "None", "None"]
server = None

connections = {}


def init(aci_type, port=8765, ip="127.0.0.1", name="main"):
    """
        Call from host to start ACI
    """
    threading.Thread(target=create_server_or_client,
                     args=(aci_type, port, ip, asyncio.get_event_loop(),
                           last_response, name), daemon=True).start()


def create_server_or_client(aci_type, port, ip, loop, last_response, name):
    """
        Start the ACI Server or Client
    """
    global server
    global connections

    node_type = aci_type
    if node_type == "server":
        server = ACIServer.Server(loop)

    if node_type == "client":
        connections[name] = ACIconnection.Connection(ip, port, loop)


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
