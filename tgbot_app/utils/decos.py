import asyncio
import time
from functools import wraps

from aiogram.utils.exceptions import BotBlocked, UserDeactivated, ChatNotFound

from tgbot_app.utils.db_api import deactivate_user


def reset_state(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        await kwargs['state'].reset_state()
        return await func(*args, **kwargs)
    return wrapper


def adv_sending_control(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            start = time.time()

            result = await func(*args, **kwargs)

            work_time = time.time() - start
            if work_time < 1:
                await asyncio.sleep(1 - work_time)

            return result

        except (BotBlocked, UserDeactivated, ChatNotFound):
            await deactivate_user(kwargs['user_id'])
            return 0
        except Exception as error:
            print(f'ADV SENDING ERROR: {error} | {type(error)}')
            return 0

    return wrapper
