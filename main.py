import os, re, configparser, requests
import random
import urllib

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import urllib.request
from tiktok_downloader import snaptik
import sys

bot = Bot(token=sys.argv[1])
dp = Dispatcher(bot, storage=MemoryStorage())

def download_video(video_url, name):
    r = requests.get(video_url, allow_redirects=True)
    content_type = r.headers.get('content-type')
    if content_type == 'video/mp4':
        open(f'./videos/video{name}.mp4', 'wb').write(r.content)
    else:
        pass

if not os.path.exists('videos'):
    os.makedirs('videos')

@dp.message_handler(commands=['bibometr'])
async def start_command(message: types.Message):
    size1 = random.randint(-20,20)
    size2 = random.randint(0, 9)
    biba = "8"
    for i in range(abs(int(size1/2))):
        biba = biba + "="
    biba += "D"
    if size1 < 1:
        await message.reply(str(abs(size1)) + " см в жопе 😳" + "\n" + biba)
    else:
        await message.reply("Твой стручок: " + str(size1) + " см 😎" + "\n" + biba)

@dp.message_handler(commands=['all'])
async def ping(m):
    if not os.path.exists(str(m.chat.id).strip().replace('-', '') + '.txt'):
        f = open(str(m.chat.id).strip().replace('-', '') + '.txt', 'w')
        f.writelines(m.from_user.username)
        f.close()
        await m.reply('Добавлены в список')
    else:
        f = open(str(m.chat.id).strip().replace('-', '') + '.txt', 'r')
        if m.from_user.username in f.read():
            msg = ''
            f.seek(0)
            for line in f.read().splitlines():
                msg = msg + ' @' + line
            await m.reply(msg)
        else:
            f.close()
            f = open(str(m.chat.id).strip().replace('-', '') + '.txt', 'a+')
            f.writelines('\n' + m.from_user.username)
            f.close()
            m.reply('Добавлены в список')





@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    regxp = re.compile(
        "(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))?")
    link = regxp.findall(message.text)
    if len(link) > 0:
        print("[" + message.from_user.username +"] получена ссылка: " + link[0])
        if 'tiktok' in str(link[0]).lower():
            video_url = message.text

            try:
                snaptik(video_url).get_media()[0].download(f"./videos/result_{message.from_user.id}.mp4")
                path = f'./videos/result_{message.from_user.id}.mp4'
                with open(f'./videos/result_{message.from_user.id}.mp4', 'rb') as file:
                    await bot.send_video(
                        chat_id=message.chat.id,
                        video=file,
                        reply_to_message_id=message.message_id
                        )
                os.remove(path)
            except:
                await bot.send_message(chat_id=message.chat.id, text='Ошибка при скачивании, неверная ссылка, видео было удалено или я его не нашел.')

@dp.message_handler(commands=['set'])
async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("all", "Пинганем всех!"),
        types.BotCommand("bibometr", "Померяем твой стручок"),
        types.BotCommand("tiktokLink", "Выгрузим тикток в данный чат"),
    ])



if __name__ == "__main__":
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)