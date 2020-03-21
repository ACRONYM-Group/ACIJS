import threading
import asyncio
import sys


def create(aci_class, port=8765, ip="127.0.0.1", name="main"):
    """
    Call from host to start ACI

    :param aci_class:
    :param port:
    :param ip:
    :param name:
    :return:
    """
    loop = asyncio.get_event_loop()
    result = aci_class(loop, ip, port, name)
    threading.Thread(target=result.start, daemon=True).start()

    return result


def stop():
    sys.exit()
