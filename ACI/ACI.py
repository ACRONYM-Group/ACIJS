import threading
import asyncio
import json
import time
import ACI.ACIConnection as ACIconnection
import ACI.ACIServer as ACIServer

db_node_ip = "127.0.0.1"
db_node_port = "80"
node_type = "Server"
last_response = ["None", "None", "None"]

connections = {}
server = 0


def init(aci_type, port=8765, ip="127.0.0.1", name="main"):
    """
    Call from host to start ACI

    :param aci_type:
    :param port:
    :param ip:
    :param name:
    :return:
    """
    loop = asyncio.get_event_loop()
    threading.Thread(target=create_server_or_client, args=(aci_type, port, ip, loop, last_response, name),
                     daemon=True).start()


def create_server_or_client(node_type, port, ip, loop, last_response, name):
    """
    Start the ACI Server or Client

    :param node_type:
    :param port:
    :param ip:
    :param loop:
    :param last_response:
    :param name:
    :return:
    """
    if node_type == "Server":
        server = ACIServer.Server(loop)

    if node_type == "client":
        connections[name] = ACIconnection.Connection(ip, port, loop)


def get_value(key, db_key, server="main"):
    """
    Call from host to get a value
    :param key:
    :param db_key:
    :param server:
    :return:
    """
    while len(connections) == 0:
        time.sleep(0.01)
    return connections[server].get_interface(db_key)[key]


def set_value(key, db_key, val, server="main"):
    """
    Call from host to set_value a value
    :param key:
    :param db_key:
    :param val:
    :param server:
    :return:
    """
    connections[server].get_interface(db_key)[key] = val


def write_to_disk(db_key, server="main"):
    """
    Write data to disk
    :param db_key:
    :param server:
    :return:
    """
    asyncio.run(connections[server].get_interface(db_key).write_to_disk())


def read_from_disk(db_key, server="main"):
    """
    Read data from disk
    :param db_key:
    :param server:
    :return:
    """
    asyncio.run(connections[server].get_interface(db_key).read_from_disk())


def list_database(db_key, server="main"):
    """
    List Database
    :param db_key:
    :param server:
    :return:
    """
    output = asyncio.run(connections[server].get_interface(db_key).list_databases())
    return json.loads(output)
