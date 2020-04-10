import threading
import asyncio
import sys

try:
    from ACIConnection import *
    from ACIServer import *
    from errors import *
    from database import *
except Exception:
    print("__init__ was probably loaded, skipping imports")


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

    if asyncio.iscoroutinefunction(result.start):
        return asyncio.run(async_create(aci_class, port=8765, ip="127.0.0.1", name="main"))
    else:
        threading.Thread(target=result.start, daemon=True).start()

    return result


async def async_create(aci_class, port=8765, ip="127.0.0.1", name="main"):
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

    def wrapper():
        asyncio.run(result.start())

    threading.Thread(target=wrapper, daemon=True).start()

    return result


def stop():
    sys.exit()


run = asyncio.run
