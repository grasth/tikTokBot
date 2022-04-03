import os
import random
import re
import sys
from time import sleep
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from bs4 import BeautifulSoup
from tiktok_downloader import snaptik

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
    size1 = random.randint(-20, 20)
    size2 = random.randint(0, 9)
    biba = "8"
    for i in range(abs(int(size1 / 2))):
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


@dp.message_handler(commands=['weather'])
async def getWeather(message: types.Message):
    try:
        resultMessage = ""
        headers = {
            'user agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/98.0.4758.102 Safari/537.36"}  # Headers для запроса
        url = "https://weather.com/ru-RU/weather/today/l/f2312a9747951a5ddc2e2678f4d7519282e4448dc9bea0157e8f805abb4e4043"
        html = requests.get(url, headers)  # Отправляем запрос
        soup = BeautifulSoup(html.content, 'html.parser')  # Получаем html страницу
        ParsedWeather = soup.findAll("span", {"class": "CurrentConditions--tempValue--3a50n"})
        resultMessage += "Ижевск\n" + str(ParsedWeather[0]).replace(
            "<span class=\"CurrentConditions--tempValue--3a50n\" data-testid=\"TemperatureValue\">", "").replace(
            "</span>", "") + ", "
        ParsedCondition = soup.findAll("div", {"class": "CurrentConditions--phraseValue--2Z18W"})
        resultMessage += str(ParsedCondition[0]).replace(
            "<div class=\"CurrentConditions--phraseValue--2Z18W\" data-testid=\"wxPhrase\">", "").replace("</div>",
                                                                                                          "")
        await message.answer(resultMessage)
    except Exception as e:
        await bot.send_message(chat_id=message.chat.id, text='Неверные данные, попробуйте еще раз')


@dp.message_handler(commands=['roll'])
async def roll(message: types.Message):
    try:
        trueOrFalse = random.choice([True, False])
        with open(f'./videos/{str(trueOrFalse)}.mp4', 'rb') as file:
            await bot.send_video(
                chat_id=message.chat.id,
                video=file,
                reply_to_message_id=message.message_id
            )

    except Exception as e:
        await bot.send_message(chat_id=message.chat.id, text='Неверные данные, попробуйте еще раз')


@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    regxp = re.compile(
        "(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))?")
    link = regxp.findall(message.text)
    headers = {
        'user agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.135 Safari/537.36"
    }
    if len(link) > 0:
        print("[" + message.from_user.username + "] получена ссылка: " + link[0])
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
                # await bot.send_message(chat_id=message.chat.id, text='Ошибка при скачивании, неверная ссылка, видео было удалено или я его не нашел.')
    elif message.text[0] == '$':
        DRIVER = 'chromedriver'
        filename = 'screenshot.png'
        driver = webdriver.Chrome(DRIVER)
        try:
            resultMessage = ""
            headers = {
                'user agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/98.0.4758.102 Safari/537.35"}  # Headers для запроса

            user = message.text.replace('$', '')
            ticker = user.upper()  # Перевод в верхний регистр для удобства
            if ticker == "BTC":
                fullUrl = "https://www.rbc.ru/crypto/currency/btcusd"
                html = requests.get(fullUrl, headers)  # Отправляем запрос
                soup = BeautifulSoup(html.content, 'html.parser').decode()  # Получаем html страницу
                pricePattern = re.compile(
                    "<div class=\"chart__subtitle js-chart-value\">([\n \d,]+)<span class=\"chart__change chart__change")
                price = re.findall(pricePattern, soup)
                PercentPattern = re.compile("<span class=\"chart__change chart__change_(grow|fall)\">([\n +\d,-.]+)([(\-\d,+%]+)\)")
                percent = re.findall(PercentPattern, soup)
                PercentPattern2 = re.compile("\(-([\d,%]+)'\)")
                SymbolPattern = re.compile("([+-]+)")
                symbol = re.findall(SymbolPattern, str(percent))
                percent2 = re.findall(PercentPattern2, str(percent))
                resultMessage += "Цена за штуку: " + str(price[0]).replace(" ", "").replace("\n", "") + " USD\n"
                resultMessage += "Движение цены за день: " + str(symbol[0]) + str(percent2[0]).replace("['", "").replace("']", "")

            elif ticker == "USD":
                fullUrl = "https://bcs-express.ru/kotirovki-i-grafiki/usd000utstom"  # Ссылка на запрос
                html = requests.get(fullUrl, headers)  # Отправляем запрос
                soup = BeautifulSoup(html.content, 'html.parser').decode()  # Получаем html страницу
                pricePattern = re.compile(
                    "<div class=\"quote-head__price-value js-quote-head-price js-price-close\">([\d,.]+)</div>")  # Regexp для получения цены
                price = re.findall(pricePattern, soup)  # Находим по регулярке значение цену
                profitPattern = re.compile(
                    "js-profit-percent\">([-+\w,%]+)</div>")  # Regexp для получения профита за день
                profit = str(re.findall(profitPattern, soup))  # Находим по регулярке значение профита за день
                resultMessage += "Цена за штуку: " + str(price[0]) + " RUB" + "\n"
                resultMessage += "Движение цены за день: " + str(
                    profit.replace("['", "").replace(",", ".").replace("']", "")) + "\n"
            elif ticker == "EUR":
                fullUrl = "https://bcs-express.ru/kotirovki-i-grafiki/eur_rub__tom"  # Ссылка на запрос
                html = requests.get(fullUrl, headers)  # Отправляем запрос
                soup = BeautifulSoup(html.content, 'html.parser').decode()  # Получаем html страницу
                pricePattern = re.compile(
                    "<div class=\"quote-head__price-value js-quote-head-price js-price-close\">([\d,.]+)</div>")  # Regexp для получения цены
                price = re.findall(pricePattern, soup)  # Находим по регулярке значение цену
                profitPattern = re.compile(
                    "js-profit-percent\">([-+\w,%]+)</div>")  # Regexp для получения профита за день
                profit = str(re.findall(profitPattern, soup))  # Находим по регулярке значение профита за день
                resultMessage += "Цена за штуку: " + str(price[0]) + " RUB" + "\n"
                resultMessage += "Движение цены за день: " + str(
                    profit.replace("['", "").replace(",", ".").replace("']", "")) + "\n"
            elif ticker != "":
                fullUrl = "https://bcs-express.ru/kotirovki-i-grafiki/" + ticker  # Ссылка на запрос
                html = requests.get(fullUrl, headers)  # Отправляем запрос
                soup = BeautifulSoup(html.content, 'html.parser').decode()  # Получаем html страницу
                pricePattern = re.compile("js-price-close\">([\d,]+)</div>")  # Regexp для получения цены
                symbolPattern = re.compile("js-currency-code\">(\w+)</div>")  # Regexp для получения валюты
                profitPattern = re.compile(
                    "js-profit-percent\">([-+\w,%]+)</div>")  # Regexp для получения профита за день
                profit = str(re.findall(profitPattern, soup))  # Находим по регулярке значение профита за день
                symbol = str(re.findall(symbolPattern, soup)[0])  # Находим по регулярке значение валюты
                price = str(re.findall(pricePattern, soup)[0]).replace(",",
                                                                       ".") + " " + symbol  # Находим по регулярке и получаем цену со знаком валюты
                resultMessage += "Цена за штуку: " + price + "\n"
                resultMessage += "Движение цены за день: " + str(
                    profit.replace("['", "").replace(",", ".").replace("']", "")) + "\n"

                driver.get("https://www.tinkoff.ru/invest/stocks/" + ticker)
                driver.maximize_window()  # For maximizing window
                driver.implicitly_wait(5)

                element = driver.find_element(by=By.CLASS_NAME, value="InvestChart__iconButton_lbuMT")
                driver.implicitly_wait(1)
                element.click()
                driver.implicitly_wait(1)

                element = driver.find_element(by=By.CLASS_NAME, value="TabsBlock-module__content_jZmZt")
                driver.implicitly_wait(1)
                element.click()
                driver.implicitly_wait(1)

                graph = driver.find_element(by=By.CLASS_NAME, value="Chart__chart_afVZ2")
                location = graph.location
                size = graph.size
                driver.save_screenshot(filename)
                _image = Image.open(filename)
                left = location['x']
                top = location['y']
                right = location['x'] + size['width']
                bottom = location['y'] + size['height']
                sleep(1)
                image = _image.crop((left, top, right, bottom))
                image.save(filename)
                sleep(1)
                driver.quit()

                with open(f'./screenshot.png', 'rb') as file:
                    await bot.send_photo(
                        chat_id=message.chat.id,
                        photo=file,
                        reply_to_message_id=message.message_id
                    )

            else:
                resultMessage += "Неверные данные, попробуйте еще раз" + "\n"
            await bot.send_message(chat_id=message.chat.id, text=resultMessage)
        except Exception as e:
            await bot.send_message(chat_id=message.chat.id, text='Неверные данные, попробуйте еще раз')


@dp.message_handler(commands=['set'])
async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("all", "Пингануть всех"),
        types.BotCommand("bibometr", "Узнать размер агрегата"),
        types.BotCommand("weather", "Узнать погоду"),
        types.BotCommand("roll", "Да или нет")
    ])


if __name__ == "__main__":
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)
