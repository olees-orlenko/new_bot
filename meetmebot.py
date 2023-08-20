import logging
import os

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

load_dotenv()

MY_GITHUB = os.getenv('MY_GITHUB')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def menu(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    buttons = ReplyKeyboardMarkup([['/my_photo', '/my_old_photo', '/my_hobby'],
                                  ['/my_first_love',
                                   '/what_is_GPT',
                                   '/SQL_vs_NoSQL']],
                                  resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='{}, вот, что ты можешь узнать бо мне.'.format(name),
        reply_markup=buttons
    )


def send_photo(update, context):
    chat = update.effective_chat
    my_photo = open('media/photo/my_photo.png', 'rb')
    context.bot.send_photo(chat.id, my_photo)
    button = ReplyKeyboardMarkup([['/my_old_photo',
                                   '/my_hobby']],
                                 resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Так я сейчас выгляжу.',
        reply_markup=button
    )


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    buttons = ReplyKeyboardMarkup([['/my_photo', '/my_old_photo'],
                                  ['/my_hobby']],
                                  resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Приятно познакомиться! '
        'Хочешь узнать меня получше?'.format(name),
        reply_markup=buttons
    )


def old_me(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    my_old_photo = open('media/photo/old_photo.png', 'rb')
    button_2 = ReplyKeyboardMarkup([['/my_hobby']], resize_keyboard=True)
    context.bot.send_photo(chat.id, my_old_photo)
    context.bot.send_message(
        chat_id=chat.id,
        text='{}, так я выглядела 15 лет назад.'.format(name),
        reply_markup=button_2
    )


def send_message(update, context):
    chat = update.effective_chat
    buttons = ReplyKeyboardMarkup([['/my_first_love', '/what_is_GPT'],
                                  ['/SQL_vs_NoSQL']],
                                  resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Мое главное увлечение - масляная живопись. '
        'В коллекции около 20 работ, '
        'половина из которых сделана на заказ и подарена друзьям. '
        'Одну из моих картин приобрели для дополнения к интерьеру кофейни.',
        reply_markup=buttons
    )
    context.bot.send_message(
        chat_id=chat.id,
        text='Если хочешь, можешь послушать историю моей первой любви!',
        reply_markup=buttons
    )


def send_audio_1(update, context):
    chat = update.effective_chat
    buttons = ReplyKeyboardMarkup([['/what_is_GPT']],
                                  resize_keyboard=True)
    context.bot.send_audio(chat.id, open('media/audio/my_first_love.wav',
                                         'rb'))
    context.bot.send_message(
        chat_id=chat.id,
        text='Если тебе понравилась моя история, поставь лайк.',
        reply_markup=buttons
    )


def send_audio_2(update, context):
    chat = update.effective_chat
    buttons = ReplyKeyboardMarkup([['/SQL_vs_NoSQL']],
                                  resize_keyboard=True)
    context.bot.send_audio(chat.id, open('media/audio/GPT.wav', 'rb'))
    context.bot.send_message(
        chat_id=chat.id,
        text='Так я объясняю своей бабушке, что такое GPT.',
        reply_markup=buttons
    )


def send_audio_3(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    buttons = ReplyKeyboardMarkup([['/my_photo', '/my_old_photo', '/my_hobby'],
                                  ['/my_first_love',
                                   '/what_is_GPT',
                                   '/SQL_vs_NoSQL']],
                                  resize_keyboard=True)
    context.bot.send_audio(chat.id, open('media/audio/SQL.wav', 'rb'))
    context.bot.send_message(
        chat_id=chat.id,
        text='{}, спасибо, что послушал(а) меня.'.format(name),
        reply_markup=buttons
    )


def my_github(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    context.bot.send_message(chat_id=chat.id,
                             text='{}, вот ссылка на мой репозиторий с '
                             'исходниками этого бота: '
                             f'{MY_GITHUB}.'.format(name))


def goodbye(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    context.bot.send_message(chat_id=chat.id,
                             text='{}, мне было приятно поделиться с тобой '
                             'информацией о себе! До новых встреч!'.format
                             (name))


def main():
    updater = Updater(token=TELEGRAM_TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('my_photo', send_photo))
    updater.dispatcher.add_handler(CommandHandler('my_old_photo', old_me))
    updater.dispatcher.add_handler(CommandHandler('my_hobby', send_message))
    updater.dispatcher.add_handler(CommandHandler('my_first_love',
                                                  send_audio_1))
    updater.dispatcher.add_handler(CommandHandler('what_is_gpt', send_audio_2))
    updater.dispatcher.add_handler(CommandHandler('sql_vs_nosql',
                                                  send_audio_3))
    updater.dispatcher.add_handler(CommandHandler('my_github', my_github))
    updater.dispatcher.add_handler(CommandHandler('stop', goodbye))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, menu))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
