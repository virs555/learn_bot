from glob import glob
from emoji import emojize
import ephem
import logging #Библиотека логирования
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from random import randint, choice




import settings

logging.basicConfig(filename='bot.log', level=logging.INFO) #Логирование: куда записывать, какая важность ошибки важна(INFO, DEBUG, WARNING)

PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username':settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context): #2 переменные update - информация с платформы tg, contex - отдаем команды боту
    print("Вызван /start")
    context.user_data['emoji'] = get_smile(context.user_data) #context.user_data словарь привязанный к пользователю
    update.message.reply_text(f"Привет, пользователь {context.user_data['emoji']}!")

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    text = update.message.text #получаем текст
    print(text)
    update.message.reply_text(f" {text} {context.user_data['emoji']}")

def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data ['emoji']


def planet_study(update, context):
    print('Вызван /planet')
    text = update.message.text
    print(text)
    if text.split()[-1] == 'Mars':
        mars = ephem.Mars('2020/11/26')
        update.message.reply_text(ephem.constellation(mars))

def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Ваше число {user_number}, мое число {bot_number}, вы выиграли!'
    elif user_number == bot_number:
        message = f'Ваше число {user_number}, мое число {bot_number}, ничья...'
    else:
        message = f'Ваше число {user_number}, мое число {bot_number}, вы проиграли.'
    return message

def guess_number(update, context):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message)

def send_cat_picture(update, context):
    cat_photo_list = glob('images/cat*.jp*g')
    cat_photo_filename = choice(cat_photo_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_photo_filename, 'rb'))

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY) #Экземпляр бота

    dp = mybot.dispatcher #Сокращаем код
    dp.add_handler(CommandHandler("start", greet_user)) #Добавляем к диспетчеру обработчик команды "start", которы вызовет функцию
    dp.add_handler(CommandHandler("planet", planet_study)) #Добавляем к диспетчеру обработчик команды "planet", которы вызовет функцию
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me)) #обрабатываем текст функцией

    logging.info('Бот запущен')
    mybot.start_polling() #Запуск бота
    mybot.idle() #Бот слушает эфир

if__name__ = '__main__' #Если запускаем, то вызывыется main, если импортирован, то не вызывается
main() #Вызов функции 


#CommandHandler обработчик команд
#MessageHandler обработчик сообщений