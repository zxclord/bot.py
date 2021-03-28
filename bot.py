import telebot
from telebot import types
bot = telebot.TeleBot('1724806373:AAF2QzqtJ1SUdR5iMVHg0PiPMIoQIuOdpQE')
isghoul = False
diary_list = []
from pyowm import OWM
from pyowm.utils.config import get_default_config


@bot.message_handler(commands=['start'])
def start(message): #начало
    sti = open('dead2.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.from_user.id,'ку, <strong>{0.first_name}</strong>\n я - виртуальная проекция вселенной умерших внутри\nдаже будучи бездушным ботом, я умудрился выебать на zxc в лобби рекрута 5 SSS ранга'
                                          '\nа вот что насчет тебя?'.format(message.from_user,bot.get_me()),parse_mode='html')
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('Да', callback_data='yes')
    item2 = types.InlineKeyboardButton('Нет', callback_data='no')
    markup.add(item1, item2)
    bot.send_message(message.from_user.id,'ты <b>гуль?</b>',reply_markup=markup,parse_mode='html')
    if isghoul:
        get_text_messages(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global isghoul
    if call.data == "yes":
        sti = open('dead3.webp', 'rb')
        bot.send_sticker(call.message.chat.id, sti)
        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text='zxc')
        bot.send_message(call.message.chat.id, 'я бы предложил тебе сходить в лобби, но я всего лишь бот..')
        bot.send_message(call.message.chat.id, 'список доступных команд: /help')
        isghoul = True
    elif call.data == "no":
        sti = open('dead1.webp', 'rb')
        bot.send_sticker(call.message.chat.id, sti)
        bot.send_message(call.message.chat.id, 'съебал.')
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text='съебал.')
    elif call.data == 'yes1':
        bot.send_message(call.message.chat.id, 'что добавить?')
        bot.register_next_step_handler(call.message,add_to)
    elif call.data == 'no1':
        bot.send_message(call.message.chat.id,'ну тогда не заебывай меня')
    elif call.data == 'yes2':
        bot.send_message(call.message.chat.id, 'что удалить?')
        bot.register_next_step_handler(call.message,delete_this)



@bot.message_handler(content_types=['text'])
def get_text_messages(message): # основной чат
    global diary_list
    if message.text == '/help':
        bot.send_message(message.from_user.id,'1) расписание zxc (/schedule)\n'
                                              '2) чекнуть на улице rain на душе pain (/weather)')
    elif message.text == '/schedule':
        bot.send_message(message.from_user.id, 'добавить/удалить или посмотреть? (/add, /delete, /show)')
        bot.register_next_step_handler(message, get_diary_list)
    elif message.text.lower() == '/weather':
        bot.send_message(message.from_user.id, 'в каком городе/стране?')
        bot.register_next_step_handler(message,get_weather)
    else:
        bot.send_message(message.from_user.id, 'список доступных команд: /help')

def get_diary_list(message): # список дел
    if message.text == '/add':
        bot.send_message(message.from_user.id, 'что добавить?')
        bot.register_next_step_handler(message,add_to)
    elif message.text == '/delete':
        bot.send_message(message.from_user.id, 'что удалить?')
        bot.register_next_step_handler(message,delete_this)
    elif message.text == '/show':
        bot.send_message(message.from_user.id, 'вот:')
        for index, item in enumerate(diary_list):
            bot.send_message(message.from_user.id,'{0}) {1}'.format(index+1,item))

def add_to(message):
    diary_list.append(message.text)
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('Да', callback_data='yes1')
    item2 = types.InlineKeyboardButton('Нет', callback_data='no1')
    markup.add(item1, item2)
    bot.send_message(message.from_user.id, 'еще?', reply_markup=markup, parse_mode='html')

def delete_this(message):
    diary_list.remove(message.text)
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton('Да', callback_data='yes2')
    item2 = types.InlineKeyboardButton('Нет', callback_data='no1')
    markup.add(item1, item2)
    bot.send_message(message.from_user.id, 'еще?', reply_markup=markup, parse_mode='html')

def get_weather(message):
    config_dict = get_default_config()
    config_dict['language'] = 'ru'
    owm = OWM('1995f90be9dd85a0f662ccf2870d160a', config_dict)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(message.text)
    w = observation.weather
    answer = 'в {place} сейчас {status}\n'.format(
        place = message.text,
        status = w.detailed_status
    )
    answer += 'средняя температура за сегодня ожидается: {average_temp} (минимальная температура: {min_temp}, максимальная: {max_temp})\n\n'.format(
        min_temp = w.temperature('celsius')['temp_min'],
        max_temp = w.temperature('celsius')['temp_max'],
        average_temp = w.temperature('celsius')['temp']
    )
    if w.rain:
        answer += 'на улице rain'
    else:
        answer += 'сегодня без дождя :('
    bot.send_message(message.from_user.id, answer)

bot.polling(none_stop=True, interval=0)