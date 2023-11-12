import telebot
import os
import sqlite3
from button_markup import ListUpdater

class DB_Getter:

    path = 'db.sqlite3'

    def getAllRows(self, poles='title, author, annotation, url, image'):
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(f'SELECT {poles} FROM books')
        data = cur.fetchall()
        cur.close()
        conn.close()
        return data
    
    def getRow(self, poles='title, author, annotation, url, image', condition=None):
        if condition is None:
            raise ValueError
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(f'SELECT {poles} FROM books WHERE {condition}')
        data = cur.fetchone()
        # print(data)
        cur.close()
        conn.close()
        return data


def load_dotenv():
    # print(type(os.environ), os.environ)
    with open('.env', encoding='utf8') as f:
        vars = [ln.split('=') for ln in f.readlines()]
    for k, v in vars:
        os.environ[k] = v

load_dotenv()
data_loader = DB_Getter()
list_updater = ListUpdater(data_loader)
bot = telebot.TeleBot(token=os.environ['TOKEN'])

# args
# content-types: list[str] = 'text' | 'document' | 'audio' 
# commands: list[str] = 'start' (all that starts with slash ) 
@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    # markup = listBook_markup()
    markup = list_updater.markup
    bot.send_message(message.chat.id, f'Привет, {message.chat.first_name} 👋🏻. Пиши /help, чтобы вызвать справку.', reply_markup=markup)
    bot.register_next_step_handler(message, message_listener)

# def listBook_markup():
#     titles = data_loader.getAllRows('title')
#     kb_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     for i in range(1, len(titles), 2):
#         kb_markup.row(telebot.types.KeyboardButton(titles[i - 1][0]), telebot.types.KeyboardButton(titles[i][0]))
#     if len(titles) % 2:
#         kb_markup.row(telebot.types.KeyboardButton(titles[len(titles) - 1][0]))
#     return kb_markup

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    bot.send_message(message.chat.id, '''Используйте кнопки на клавиатуре, чтобы получить информацию об интересующей вас книге
/list - список книг
/start - перезагрузка бота
/dev - о создателе
''')

@bot.message_handler(commands=['list'])
def printListBooks(message: telebot.types.Message):
    id_title = data_loader.getAllRows('id, title')
    answer = ''
    for i, tup in enumerate(id_title):
        answer += f'{i + 1}. {tup[1]} (id: {tup[0]})\n'
    bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=['dev'])
def about_dev(message: telebot.types.Message):
    bot.send_message(message.chat.id, '👨‍💻 Администрация бота @hxBQd.\nТолько для коммерческих предложений.')

def message_listener(message: telebot.types.Message):
    if message.text in ('➡️', '⬅️'):
        change_markup(message)
        return
    book = data_loader.getRow(condition=f'title="{message.text}"')
    if book is None:
        bot.send_message(message.chat.id, 'Я не нашёл такой книги\nЗахочешь посмотреть книги напиши /start, справка - /help', reply_markup=telebot.types.ReplyKeyboardRemove())
        return
    else:
        printBook(message, book)

# @bot.message_handler(content_types=['text'])
def printBook(message: telebot.types.Message, book):
    about = f'''Название: {book[0]}
Автор: {book[1]}
Аннотация: {book[2]}
Прочитать: {book[3]}
'''
    bot.send_photo(message.chat.id, photo=book[4])  # , caption=about
    bot.send_message(message.chat.id, about, reply_to_message_id=message.id)
    bot.register_next_step_handler(message, message_listener)

def change_markup(message: telebot.types.Message):
    list_updater.create_markup(message.text)
    bot.send_message(message.chat.id, message.text, reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.send_message(message.chat.id, message.text, reply_markup=list_updater.markup)
    # print(message.text)
    bot.register_next_step_handler(message, message_listener)
    

bot.polling(non_stop=True, interval=0)