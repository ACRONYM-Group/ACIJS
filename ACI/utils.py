import asyncio


def make_blocking(func):
    """
    Make a function which is technically async able to block execution
    :param func:
    :return:
    """
    async def future_wrapper(future, *args, **kwargs):
        try:
            future.set_result(await func(*args, **kwargs))
        except Exception as e:
            future.set_exception(e)

    def blocking_wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        loop.create_task(future_wrapper(future, *args, **kwargs))
        return future

    return blocking_wrapper