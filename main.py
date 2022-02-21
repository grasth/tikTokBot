import os, re, configparser, requests
import random

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
import urllib
import requests  # для URL запроса
from bs4 import BeautifulSoup  # для работы с HTML

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
            except Exception as e:
                await bot.send_message(chat_id=message.chat.id, text=str(type(e)))
                await bot.send_message(chat_id=message.chat.id, text=str(e.args))   
                #await bot.send_message(chat_id=message.chat.id, text='Ошибка при скачивании, неверная ссылка, видео было удалено или я его не нашел.')
    elif message.text[0] == '$':
        ticker = (message.text).replace('$', '').upper()
if ticker=='USD' or ticker =='EUR':
    urlOfTicker = "https://invest.yandex.ru/catalog/currency/" + ticker

    html = requests.get(urlOfTicker, headers)

    soup = BeautifulSoup(html.content, 'html.parser')
    csrf_token_pattern = re.compile('window.__CSRF_TOKEN__ = \"([\w\d:]+)\";')
    reqot_token_pattern = re.compile(',reqid:\'([\d\w]+)\',')

    csrf = re.findall(csrf_token_pattern, soup.decode())
    reqid = re.findall(reqot_token_pattern, soup.decode())

    url = urlOfTicker
    payload = {"operationName": "StockChartSeries",
               "variables": {"slug": "usd", "candleSize": "ONE_DAY", "isoTs": "2022-02-21T20:18:37.149Z", "amount": 2},
               "query": "query StockChartSeries($slug: String!, $candleSize: CandleSize!, $isoTs: IsoDateTime!, $amount: Int!) {\n  candles2 {\n    series(slug: $slug, candleSize: $candleSize, isoTs: $isoTs, amount: $amount) {\n      results {\n        ts\n        open\n        high\n        low\n        close\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}

    headers = {
        "Host": "invest.yandex.ru",
        "Connection": "keep-alive",
        "Content-Length": "509",
        "Origin": "https://invest.yandex.ru",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru,en-US;q=0.9,en;q=0.8",
        "x-csrf-token": str(csrf),
        "x-ssr-id": str(reqid),
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    temp = r.content.decode()

    plusOrMinus = re.compile("<div class=\"rzv7e6OPChq71rCQBr9H SUCnYTT5LFAlaqfSzDh5\"><span>([+|-]+)  ")
    plOrMin = re.findall(plusOrMinus, temp)

    pattern2 = re.compile("₽<\/span><span>([\d,]+)  %<\/span><\/div>")
    match = re.findall(pattern2, temp)
    result = (str(match))

    symbol = '₽'
    pattern = re.compile("bolbtRDz491tDq6jfmHd\">([\d,]+)<\/span>")
    match = re.findall(pattern, temp)

    print("Цена валюты " + ticker.upper() + ': ' + "%.2f" % float(str(match[0]).replace(',', '.')) + symbol)
    print("Движение цены за день: " + str(plOrMin[0]) + str(result).replace("['", "").replace("']", '') + "%")
else:
    urlOfTicker = "https://invest.yandex.ru/catalog/stock/" + ticker

    # заголовки для URL запроса.(добавляется к ссылке при URL запросе)
    headers = {
        'user agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.135 Safari/537.36"}

    # запрашиваем страницу по ссылке и помещаем в переменную html
    html = requests.get(urlOfTicker, headers)

    # парсим данные в переменную soup
    soup = BeautifulSoup(html.content, 'html.parser')

    # находим интересующий нас тэг с текущим курсом
    # (В браузере используем просмотр кода элемента для того чтобы найти это значение)

    isLot = soup.find('span', {'class': 'bxGayARGKhq9SK26MnEt'}).get_text()
    PriceNow = soup.find('span', {'class': 'bolbtRDz491tDq6jfmHd'}).get_text()
    result = ''
    Currency = soup.find('span', {'class': 's_OEpI6WApP0emKfb__p'}).get_text()
    if (isLot == 'Узнать больше о фондах'):
        PriceNow = soup.find('span', {'class': 'bolbtRDz491tDq6jfmHd'}).get_text()
        temp = ("".join(PriceNow.split()))
        temp = temp.replace(',', '.')
        result = (temp + Currency)
    else:
        temp = ("".join(PriceNow.split()))
        temp = temp.replace(',', '.')
        result = (str(round(float(temp) / 10, 1)) + Currency)

    resultMessage = ''
    PercentIntraday = soup.find('div', {'class': 'rzv7e6OPChq71rCQBr9H'}).get_text()
    pattern = re.compile("([\d,]+)  %")
    match = re.findall(pattern, PercentIntraday)
    temp = ''.join(match)
    temp = temp.replace(',', '.')
    resultMessage += "Цена акций " + ticker.upper() + ": " + result.replace('  ', '') + '\n'
    resultMessage += "Движение цены за сегодня: " + PercentIntraday[0] + temp + "%" + '\n'

    Prognoz = soup.find('dd', {'class': '_6TCcuJ2ARzl_p6vbOa2'}).get_text()
    resultMessage += "Консенсус прогноз: " + Prognoz.replace('  ', '') + '\n'

    PrognozPercent = soup.findAll('dd', {'class': '_6TCcuJ2ARzl_p6vbOa2'})
    temp = str(PrognozPercent)
    pattern = re.compile(
        "<dd class=\"_6TCcuJ2ARzl_p6vbOa2\">([\d,  ₽|$]+)<div class=\"rzv7e6OPChq71rCQBr9H SUCnYTT5LFAlaqfSzDh5 mq6wSvRObYLvnnJqmh5Q\">")
    match = re.findall(pattern, temp)
    resultMessage += "Прогнозируемая цена: " + str(match[0]).replace(',', '.').replace('  ', '') + '\n'

    PrognozPercent = soup.find('div', {
        'class': 'rzv7e6OPChq71rCQBr9H SUCnYTT5LFAlaqfSzDh5 mq6wSvRObYLvnnJqmh5Q'}).get_text()
    temp = PrognozPercent.replace('  ', '').replace(',', '.')
    resultMessage += "Прогнозируемый процент роста: " + temp + '\n'
            await bot.send_message(chat_id=message.chat.id, text=resultMessage)
        except:
            await bot.send_message(chat_id=message.chat.id, text='Неверные данные.')

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