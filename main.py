from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType, Message
from generator import generate_captcha
import asyncio

from settings import token, time_fast_ans, time_main_ans

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class CaptchaState(StatesGroup):
    waiting_for_captcha = State()
    verified = State()


@dp.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
@dp.message_handler(commands="test") #test future
async def send_captcha(message: types.Message, state: FSMContext):
    captcha_code = await generate_captcha()

    with open('captcha.png', 'rb') as photo:
        msg = await bot.send_photo(
            message.chat.id,
            photo,
            caption=f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>, добро пожаловать в <b>[ {message.chat.title} ]</b>, введите код капчи! (время на ввод ограничено)",
            parse_mode="HTML"
        )
    await state.set_state(CaptchaState.waiting_for_captcha)
    await state.update_data(captcha_code=captcha_code, attempts=0, message_captha=msg)

    timer = asyncio.create_task(expire_captcha(state, message.chat.id, message.from_user.id, time_main_ans))
    await asyncio.sleep(time_main_ans)
    try:
        await bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        pass


@dp.message_handler(state=CaptchaState.waiting_for_captcha)
async def check_captcha(message: types.Message, state: FSMContext):
    user_answer = message.text

    data = await state.get_data()
    captcha_code = data.get('captcha_code')
    attempts = data.get('attempts')
    message_captha = data.get('message_captha')
    await bot.delete_message(message.chat.id, message.message_id)
    if user_answer == captcha_code:
        msg = await bot.send_message(message.chat.id, f"Код верен, [{message.from_user.first_name}](tg://user?id={message.from_user.id})! Добро пожаловать!", parse_mode="Markdown")
        await bot.delete_message(message.chat.id, message_captha.message_id)
        await state.set_state(CaptchaState.verified)
        await asyncio.sleep(time_fast_ans)
        await bot.delete_message(message.chat.id, msg.message_id)


    else:
        attempts += 1
        if attempts < 3:
            msg = await bot.send_message(message.chat.id, f"[{message.from_user.first_name}](tg://user?id={message.from_user.id}), код неверен. Пожалуйста, попробуйте снова.", parse_mode="Markdown")
            await state.update_data(attempts=attempts)
            await asyncio.sleep(time_fast_ans)
            await bot.delete_message(message.chat.id, msg.message_id)


async def expire_captcha(state: FSMContext, chat_id: int, user_id: int, timeout: int):
    await asyncio.sleep(timeout)
    ustate = await state.get_state()
    if ustate != "CaptchaState:verified":
        member = await bot.get_chat_member(chat_id, user_id)
        msg = await bot.send_message(chat_id, f"[{member.user.first_name}](tg://user?id={user_id}), ваша права ограничены! Если вы не согласны с этим, обратитесь к администратору :(", parse_mode="Markdown")
        await restrict_user(chat_id, user_id)
        await asyncio.sleep(time_fast_ans)
        await bot.delete_message(chat_id, msg.message_id)
        await state.finish()

async def restrict_user(chat_id: int, user_id: int):
    permissions = types.ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_polls=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False,
        can_change_info=False,
        can_invite_users=True,
        can_pin_messages=False
    )
    await bot.restrict_chat_member(chat_id, user_id, permissions)

if __name__ == '__main__':
    executor.start_polling(dp)