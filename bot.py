import logging #Библиотека логирования
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

logging.basicConfig(filename='bot.log', level=logging.INFO) #Логирование: куда записывать, какая важность ошибки важна(INFO, DEBUG, WARNING)

PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username':settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context): #2 переменные update - информация с платформы tg, contex - отдаем команды боту
    print("Вызван /start")
    #print(update)
    update.message.reply_text('Привет, пользователь!')

def talk_to_me(update, context):
    text = update.message.text #получаем текст
    print(text)
    update.message.reply_text(text)

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY) #Экземпляр бота

    dp = mybot.dispatcher #Сокращаем код
    dp.add_handler(CommandHandler("start", greet_user)) #Добавляем к диспетчеру обработчик команды "start", которы вызовет функцию
    dp.add_handler(MessageHandler(Filters.text, talk_to_me)) #обрабатываем текст функцией

    logging.info('Бот запущен')
    mybot.start_polling() #Запуск бота
    mybot.idle() #Бот слушает эфир

if__name__ = '__main__' #Если запускаем, то вызывыется main, если импортирован, то не вызывается
main() #Вызов функции 


#CommandHandler обработчик команд
#MessageHandler обработчик сообщений