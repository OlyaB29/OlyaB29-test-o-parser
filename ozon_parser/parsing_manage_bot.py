import telebot
from telebot import types
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# t.me/parsing_manage_bot

bot = telebot.TeleBot(token=os.getenv("BOT_TOKEN"))
chat_id = os.getenv("ADMIN_TG")


def create_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    parsing_btn = types.InlineKeyboardButton(text="Запустить парсинг", callback_data='parse')
    products_btn = types.InlineKeyboardButton(text="Посмотреть последние продукты", callback_data='products')
    keyboard.add(parsing_btn)
    keyboard.add(products_btn)
    return keyboard


def send_parsing_notify(message):
    bot.send_message(chat_id, message, parse_mode="html")


@bot.message_handler(commands=['start'])
def start_bot(message):
    keyboard = create_keyboard()
    bot.send_message(message.chat.id, 'Привет, выберите, что Вам нужно', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def keyboard_answer(call):
    mess = ''
    if call.data == "parse":
        mess = "Сколько товаров нужно спарсить?"
    if call.data == "products":
        url = "http://127.0.0.1:8000/v1/products/?last_products=True"
        try:
            resp = requests.get(url).json()
            last_date = list(resp)[0]["date"]
            mess = f"<b>Товары, полученные при последнем парсинге {last_date}:</b>\n"
            for i, product in enumerate(resp):
                mess += f"{i+1}. {product['title']}, {product['link']}\n"
        except Exception as e:
            print(e)
            mess = "Список продуктов получить не удалось"
    bot.send_message(call.message.chat.id,
                     mess,
                     reply_markup=create_keyboard(),
                     parse_mode='html')


@bot.message_handler(content_types=['text'])
def parse_request(message):
    url = "http://127.0.0.1:8000/v1/products/"
    resp = requests.post(url, data={"products_count": str(message.text)} if str(message.text).isdigit() else None)
    bot.send_message(message.chat.id, resp.text, parse_mode='html')


if __name__ == "__main__":
    bot.polling(none_stop=True,interval=0)