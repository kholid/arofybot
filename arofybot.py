import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton
from dbhelper import DBHelper


db = DBHelper()
if ("TELEGRAM_TOKEN" in os.environ):
    TOKEN = os.environ['TELEGRAM_TOKEN']
else:
    TOKEN = "493361673:AAH54EparefXUDq5qPcnbKm80ZqeRn07efI"


def start(bot, update):
    text = "Hi! I'm your personal assistant. What can I do for you?"
    update.message.reply_text(text)


def help(bot, update):
    text = "ArofyBot may help you with these commands:"
    text += "\n\n/start - standard bot first command"
    text += "\n/help - asking bot what he can do"
    text += "\n/outcome <number> - list your outcome"
    text += "\n/totalOutcome - sum all your outcome"
    text += "\n/askLocation - asking your location"
    update.message.reply_text(text)


def echo(bot, update):
    text = update.message.text
    update.message.reply_text(text)


def outcome(bot, update, args):
    chat_id = update.message.chat_id
    outlist = db.get_outcome(chat_id)
    amount = args[0]
    db.add_outcome(amount, chat_id)
    text = "\n".join(outlist)
    update.message.reply_text(text)


def totalOutcome(bot, update):
    chat_id = update.message.chat_id
    totalOut = db.get_total_outcome(chat_id)
    update.message.reply_text(totalOut)


def askLocation(bot, update):
    text = "would you mind sharing your location?"
    loc = KeyboardButton(text="Send Location", request_location=True)
    con = KeyboardButton(text="Send Contact", request_contact=True)
    custom_keyboard = [[loc, con]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.message.reply_text(text, reply_markup=reply_markup)


def unknown(bot, update):
    text = "can't understand your command, maybe Bot need to study more :D"
    update.message.reply_text(text)


start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
outcome_handler = CommandHandler('outcome', outcome, pass_args=True)
total_handler = CommandHandler('totalOutcome', totalOutcome)
location_handler = CommandHandler('askLocation', askLocation)
echo_handler = MessageHandler(Filters.text, echo)
unknown_handler = MessageHandler(Filters.command, unknown)


def main():
    db.setup()

    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(outcome_handler)
    dispatcher.add_handler(total_handler)
    dispatcher.add_handler(location_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
