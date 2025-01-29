from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import logging
import json
import os
import random
from datetime import datetime, timedelta

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Файл для хранения данных
DATA_FILE = 'user_data.json'

# Валюта
CURRENCY = "🍜"  # Эмодзи лапши как валюта

# Загрузка данных пользователей
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Сохранение данных пользователей
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

# Команда /noodles
def noodles(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    data = load_data()
    if user_id not in data:
        data[user_id] = {"noodles": 0, "currency": 0, "level": 1, "nickname": update.message.from_user.first_name}
    data[user_id]["noodles"] += 0.5
    data[user_id]["currency"] += 1
    save_data(data)
    update.message.reply_text(f"Добавлено 0.5 м лапши! Всего лапши: {data[user_id]['noodles']} м. Валюта: {data[user_id]['currency']} {CURRENCY} 😋")

# Команда /leaderboard
def leaderboard(update: Update, context: CallbackContext):
    data = load_data()
    sorted_users = sorted(data.items(), key=lambda x: x[1]['noodles'], reverse=True)
    leaderboard_message = "🏆 Таблица лидеров:\n"
    for user_id, user_data in sorted_users:
        leaderboard_message += f"{user_data['nickname']}: {user_data['noodles']} м лапши, Уровень: {user_data['level']} 🌟\n"
    update.message.reply_text(leaderboard_message)

# Команда /cook
def cook(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Добавить приправы 🌶", callback_data='add_spices')],
        [InlineKeyboardButton("Приготовить лапшу 🍜", callback_data='cook_noodles')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите действие:', reply_markup=reply_markup)

# Обработка callback-запросов
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = str(query.from_user.id)
    data = load_data()
    if query.data == 'add_spices':
        if data[user_id]['currency'] >= 5:
            data[user_id]['currency'] -= 5
            data[user_id]['noodles'] += 1
            save_data(data)
            query.edit_message_text(text=f"Приправы добавлены! Теперь у вас {data[user_id]['noodles']} м лапши. 🌶")
        else:
            query.edit_message_text(text="Недостаточно валюты для добавления приправ! 😔")
    elif query.data == 'cook_noodles':
        if data[user_id]['noodles'] >= 1:
            data[user_id]['noodles'] -= 1
            data[user_id]['currency'] += 10
            save_data(data)
            query.edit_message_text(text=f"Лапша приготовлена! Вы получили 10 {CURRENCY}. 🍜")
        else:
            query.edit_message_text(text="Недостаточно лапши для приготовления! 😢")

# Команда /upgrade
def upgrade(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    data = load_data()
    if data[user_id]['currency'] >= 20:
        data[user_id]['currency'] -= 20
        data[user_id]['level'] += 1
        save_data(data)
        update.message.reply_text(f"Уровень повышен! Теперь ваш уровень: {data[user_id]['level']} 📈")
    else:
        update.message.reply_text("Недостаточно валюты для повышения уровня! 🚫")

# Команда /buy
def buy(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Купить приправы (5 🍜) 🌶", callback_data='buy_spices')],
        [InlineKeyboardButton("Купить ингредиенты (10 🍜) 🥕", callback_data='buy_ingredients')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите, что хотите купить:', reply_markup=reply_markup)


# Команда /me
def me(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    data = load_data()
    if user_id in data:
        user_data = data[user_id]
        update.message.reply_text(f"👤 Ник: {user_data['nickname']}\n🍜 Лапша: {user_data['noodles']} м\n💰 Валюта: {user_data['currency']} {CURRENCY}\n📈 Уровень: {user_data['level']}")
    else:
        update.message.reply_text("Вы еще не начали собирать лапшу! 🍜")

# Основная функция
def main():
    # Вставьте сюда ваш токен
    updater = Updater("7723033569:AAFlg_R_Cta3IPuz8pC7y4W5cIz_qLcfUds")
    dp = updater.dispatcher

    # Регистрация команд
    dp.add_handler(CommandHandler("noodles", noodles))
    dp.add_handler(CommandHandler("leaderboard", leaderboard))
    dp.add_handler(CommandHandler("cook", cook))
    dp.add_handler(CommandHandler("upgrade", upgrade))
    dp.add_handler(CommandHandler("buy", buy))
    dp.add_handler(CommandHandler("me", me))
    dp.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
