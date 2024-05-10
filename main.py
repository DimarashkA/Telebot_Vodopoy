import telebot
import datetime
import time
import threading
import random
import requests

bot = telebot.TeleBot('Введите токен')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, 'Привет, я чат бот, который будет напоминать тебе пить водичку')
    reminder_thread = threading.Thread(target=send_reminders, args=(message.chat.id,))
    reminder_thread.start()

@bot.message_handler(commands=['fact'])
def fact_message(message):
    facts_list = [
        'Вода составляет около 60% веса тела взрослого человека и играет ключевую роль во многих биологических процессах.',
        'Обезвоживание даже на 1-3% может существенно повлиять на функции мозга.',
        'Питье воды перед едой может способствовать снижению аппетита и уменьшению потребления калорий.'
    ]
    random_fact = random.choice(facts_list)
    bot.reply_to(message, f'Лови факт о воде: {random_fact}')

active_reminders = {}

@bot.message_handler(commands=['set_reminders'])
def set_reminders(message):
    bot.send_message(message.chat.id, 'Введите время напоминаний в формате HH:MM, разделяя их запятой (например, 08:00,13:00,20:00).')
    bot.register_next_step_handler(message, update_reminder_times)

def update_reminder_times(message):
    times = message.text.split(',')
    active_reminders[message.chat.id] = times
    bot.send_message(message.chat.id, 'Напоминания установлены на следующие времена: ' + ', '.join(times))

@bot.message_handler(commands=['stop_reminders'])
def stop_reminders(message):
    if message.chat.id in active_reminders:
        del active_reminders[message.chat.id]
        bot.send_message(message.chat.id, 'Все активные напоминания остановлены.')
    else:
        bot.send_message(message.chat.id, 'Нет активных напоминаний для остановки.')

@bot.message_handler(commands=['benefits'])
def send_benefits(message):
    benefits_text = "Пить достаточно воды помогает поддерживать здоровье кожи, похудение и общее самочувствие."
    bot.send_message(message.chat.id, benefits_text)

@bot.message_handler(commands=['log_water'])
def log_water(message):
    bot.send_message(message.chat.id, 'Сколько воды вы выпили? Отправьте количество в мл.')
    bot.register_next_step_handler(message, log_water_amount)

def log_water_amount(message):
    # Здесь можно сохранить информацию в базу данных или файл
    bot.send_message(message.chat.id, f'Записано: Вы выпили {message.text} мл воды.')

@bot.message_handler(commands=['water_stats'])
def water_stats(message):
    # Здесь можно извлечь информацию из базы данных или файла
    bot.send_message(message.chat.id, 'Статистика вашего потребления воды: [пример статистики]')

@bot.message_handler(commands=['tips'])
def send_tips(message):
    tips_text = "Лучшее время для питья воды - за 30 минут до еды. Это поможет улучшить пищеварение."
    bot.send_message(message.chat.id, tips_text)

@bot.message_handler(commands=['set_location'])
def set_location(message):
    bot.send_message(message.chat.id, 'Введите ваше местоположение для получения погодных данных.')

@bot.message_handler(commands=['weather_water'])
def weather_water(message):
    # Тут должен быть код запроса погоды и базированной на этом рекомендации по воде
    bot.send_message(message.chat.id, 'На основе текущей погоды рекомендуем выпить больше воды.')

@bot.message_handler(commands=['challenge'])
def send_challenge(message):
    bot.send_message(message.chat.id, 'Вызов: Выпейте 2 литра воды сегодня и получите значок "Гидратационный мастер"!')

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "/start - начать работу с ботом\n/set_reminders - настроить напоминания\n/stop_reminders - остановить все напоминания\n/benefits - польза воды\n/log_water - записать количество выпитой воды\n/water_stats - статистика потребления\n/tips - советы по гидратации\n/set_location - задать местоположение\n/weather_water - погодные рекомендации\n/challenge - участвовать в вызове\n/help - вызов помощи"
    bot.send_message(message.chat.id, help_text)

def send_reminders(chat_id):
    reminders = ['09:00', '12:00', '18:00']
    while True:
        now = datetime.datetime.now().strftime('%H:%M')
        if now in reminders:
            bot.send_message(chat_id, 'Напоминание: выпей стакан воды!')
            time.sleep(61)  # Пауза, чтобы избежать повторных сообщений в одну минуту
        time.sleep(1)

bot.polling(none_stop=True)




