import html
import logging

from aiogram import types, F, Router
from aiogram.filters.command import Command

from main import memes

from tools.utils import config
from tools.utils import is_spam, group_id

logger = logging.getLogger(__name__)
router = Router()
channel = config.channel


@router.message(Command(commands="start", ignore_case=True), F.chat.type == "private")
async def start_handler(message: types.Message):
    first_name = message.from_user.first_name

    await message.reply(f"Привет {first_name}, тут ты можешь отправить мне котиков. Принимаю только видосики и картинощки")


@router.message(F.content_type.in_({'photo'}), F.chat.type == "private")
async def work_send_tax(message: types.Message):
    uid = message.from_user.id
    if uid in config.banned_user_ids:
        text = "не хочу с тобой разговаривать"
        await message.reply(text, parse_mode=None)
    else:
        logging.info('info about message %s', message)
        logging.info('id of file %s', message.photo[-1].file_id)
        await memes.send_photo(channel, photo=message.photo[-1].file_id)
        await message.reply("Спасибо за котю! Пока-пока")


@router.message(F.content_type.in_({'video'}), F.chat.type == "private")
async def work_send_demo(message: types.Message):
    uid = message.from_user.id
    if uid in config.banned_user_ids:
        text = "не хочу с тобой разговаривать"
        await message.reply(text, parse_mode=None)
    else:
        logging.info('info about message %s', message)
        logging.info('id of file %s', message.video.file_id)
        content = message.video.file_id
        await memes.send_video(channel, video=content)
        await message.reply("Спасибо за котю! Пока-пока")


@router.message(F.chat.type.in_({'group', 'supergroup'}))
async def handle_group_messages(message: types.Message):
    if is_spam(message):
        await message.delete()
        await memes.ban_chat_member(chat_id=group_id, user_id=message.from_user.id)
        logging.info(f"User {message.from_user.id} banned for spamming")
        await message.answer(f"Пользователь {message.from_user.first_name} был заблокирован за спам.")
    else:
        logging.info(f"Received message from {message.from_user.first_name}: {message.text}")
