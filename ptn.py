from urllib.parse import quote
from bs4 import BeautifulSoup
import telebot
from requests import get

bot = telebot.TeleBot('5753169900:AAHwEViSZwA0bc6v5886gVKMkHHy2VK0WGo')


@bot.message_handler(commands=['check'])
def greet(message):
    txt = message.text.strip('/check ')
    if txt == '':
        url = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html"
    else:
        url = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=" + quote(txt)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    try:
        html = get(url, headers=headers).text
    except:
        return
    soup = BeautifulSoup(html, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    if 'Обновлено' in text:
        text = text[text.rfind('Релевантности') + 20:text.find('Обновлено')].split('\n')
        bot.send_message(message.chat.id, str('Открыта закупка ' + text[2]))
        bot.send_message(message.chat.id, str('Тип: ' + text[1]))
        bot.send_message(message.chat.id, str('Статус : ' + text[3]))
        bot.send_message(message.chat.id, str('Объект закупки: ' + text[5]))
        bot.send_message(message.chat.id, str('Заказчик: ' + text[7]))
        bot.send_message(message.chat.id, str('Стартовая цена: ' + text[9]))
        # for el in text:
        #     if el != '':
        #         bot.send_message(message.chat.id, el)
    else:
        bot.send_message(message.chat.id, 'По этому запросу ничего не нашлось.')


@bot.message_handler(commands=['start'])
def st(message):
    bot.send_message(message.chat.id, 'Здравствуйте, ' + str(message.from_user.first_name) + '. Проверка закупки по тегу: /check тег .')


bot.polling()
