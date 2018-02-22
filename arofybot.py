import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import replykeyboardmarkup, keyboardbutton
from dbhelper import DBHelper


db = DBHelper()
TOKEN = os.environ['TELEGRAM_TOKEN']


def start(bot, update):
    text = "Hi! I'm your personal assistant. What can I do for you?"
    update.message.reply_text(text)


def help(bot, update):
    text = "ArofyBot may help you with these commands:"
    text += "\n\n/start - standard bot first command"
    text += "\n/help - asking bot what he can do"
    text += "\n/outcome <number> - list your outcome"
    update.message.reply_text(text)


def echo(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    bot.send_message(chat_id, text)


def unknown(bot, update):
    chat_id = update.message.chat_id
    text = "can't understand your command, maybe Bot need to study more :D"
    bot.send_message(chat_id, text)


def outcome(bot, update, args):
    chat_id = update.message.chat_id
    outlist = db.get_outcome(chat_id)
    amount = args[0]
    db.add_outcome(amount, chat_id)
    text = "\n".join(outlist)
    bot.send_message(text, chat_id)


def totalOutcome(bot, update):
    chat_id = update.message.chat_id
    totalOut = db.get_total_outcome(chat_id)
    bot.send_message(totalOut, chat_id)


def askLocation(bot, update):
    text = "would you mind sharing your location?"
    loc = keyboardbutton(text="Send Location", request_location=True)
    con = keyboardbutton(text="Send Contact", request_contact=True)
    custom_keyboard = [[loc, con]]
    reply_markup = replykeyboardmarkup(custom_keyboard)
    bot.send_message(text, reply_markup=reply_markup)


start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
echo_handler = MessageHandler(Filters.text, echo)
unknown_handler = MessageHandler(Filters.command, unknown)
outcome_handler = CommandHandler('outcome', outcome, pass_args=True)
total_handler = CommandHandler('totalOutcome', totalOutcome)
location_handler = CommandHandler('askLocation', askLocation)


def main():
    db.setup()

    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(unknown_handler)
    dispatcher.add_handler(outcome_handler)
    dispatcher.add_handler(total_handler)
    dispatcher.add_handler(location_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
