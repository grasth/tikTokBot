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

import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir=r".\dbConnect")
# connection = cx_Oracle.connect(user="admin", password="Hu),[*3S*!hg#M2&", dsn="ghoulhelperdb_high")

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
async def ping(message: types.Message):
    sql = ('insert into commandall(GROUPID, USERNAME)'
           'values(:GROUPID,:USERNAME)')

    try:
        # establish a new connection
        with cx_Oracle.connect("admin",
                               "Hu),[*3S*!hg#M2&",
                               "ghoulhelperdb_high",
                               encoding='UTF-8') as connection:
            # create a cursor
            with connection.cursor() as cursor:
                select_stmt = f'SELECT * FROM COMMANDALL WHERE GROUPID = {message.chat.id}'
                getTable = []
                for item in cursor.execute(select_stmt):
                    getTable.append(item[1])

                if message.from_user.username in getTable:
                    msg = ""
                    for username in getTable:
                         msg += f'@{username} '
                    await bot.send_message(message.chat.id, msg)
                else:
                    cursor.execute(sql, [message.chat.id, message.from_user.username])
                    await bot.send_message(message.chat.id, "Вы добавлены в таблицу")
                connection.commit()

    except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)








    # cursor = connection.cursor()
    # getTable = cursor.execute(f'select * from COMMANDALL where GROUPID={message.chat.id}')
    # for i in getTable:
    #     print(i)
    # if message.from_user.username in getTable:
    #     msg = ""
    #     for username in getTable:
    #         msg += f'@{username}'
    #     await bot.send_message(message.chat.id, msg)
    # else:
    #     cursor.executemany('insert into COMMANDALL(GROUPID, USERNAME) values (:1, :2)', [{message.chat.id}, {message.from_user.username}])
    #     await bot.send_message(message.chat.id, "Вы добавлены в таблицу")


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