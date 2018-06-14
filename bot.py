"""Simple Bot to reply to Telegram messages.
This is built on the API wrapper, see echobot2.py to see the same example built
on the telegram.ext bot framework.
This program is dedicated to the public domain under the CC0 license.
"""
import pyowm
API_key_weather = "4b8c4fedb3eb01be9238d9cf65ba081c"
# получаем данные о погоде
# и также проверяем правильно ли ввели мы название города
def get_data_weather(sity):
    try:
        own = pyowm.OWM (API_key_weather)
        obserwation = own.weather_at_place (sity)
        w = obserwation.get_weather ( )
        temperature = w.get_temperature ('celsius')['temp']
        status = w.get_status()
        st = "temperature {}-celsius {}-status".format(temperature,status)
        return st
    except Exception:
        return "Вы ввели не правильно название города!!"

# '561854706:AAF2FPltJ-B7YXa_me3JdmgysQ1d2lG2nZo'
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! print your sity')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(get_data_weather(update.message.text))


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("561854706:AAF2FPltJ-B7YXa_me3JdmgysQ1d2lG2nZo")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
