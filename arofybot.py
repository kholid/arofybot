import os
import telegram

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


TOKEN = os.environ['TELEGRAM_TOKEN']


def start(bot, update):

    text = "Hi! I'm your personal assistant. What can I do for you?"
    update.message.reply_text(text)


def help(bot, update):

    text = "Some commands are still in progress, please wait"
    update.message.reply_text(text)


def echo(bot, update):

    chat_id = update.message.chat_id
    text = update.message.text
    bot.send_message(chat_id, text)


def unknown(bot, update):

    chat_id = update.message.chat_id
    text = "Bot can't understand your command, maybe Bot need to study more :D"
    bot.send_message(chat_id, text)


start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', start)
echo_handler = MessageHandler(Filters.text, echo)
unknown_handler = MessageHandler(Filters.command, unknown)


def main():
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
