import asyncio


def make_blocking(func):
    """
    Make a function which is technically async able to block execution
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        print("Calling")
        return asyncio.run(func(*args, **kwargs))

    return wrapper
