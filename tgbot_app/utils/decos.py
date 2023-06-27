from functools import wraps


def reset_state(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        await kwargs['state'].reset_state()
        return await func(*args, **kwargs)
    return wrapper
