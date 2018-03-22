#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING,DECISION, TYPING_REPLY, TYPING_CHOICE = range(4)

menu_keyboard = [['Start Recipe', 'Help'],
                  ['Exit'],
                  ]
markup = ReplyKeyboardMarkup(menu_keyboard,one_time_keyboard=True)
choose_keyboard = [['Yes'],[ 'No']]              
markup2 = ReplyKeyboardMarkup(choose_keyboard, one_time_keyboard=True)


def start(bot, update):
    update.message.reply_text("Hi! My name is Doctor Botter.  "
        "What you want to do?",
        reply_markup=markup)

    return CHOOSING


def regular_choice(bot, update, user_data):
	
	update.message.reply_text('Give me the ingredients separate with commas')
	return TYPING_REPLY



def received_information(bot, update,user_data):
	user = update.message.from_user
	logger.info("Ingredients of %s: %s", user.first_name, update.message.text)
	#ingredients.append(update.message.text)
#cridar funcio spoonacular i enviarli update.message.text com a parametre
	i=str(update.message.text)
	#update.message.reply_text('SEND RECIPE')
	
	return CHOOSING

def hel (bot,update,user_data):

	update.message.reply_text("ayuudaaaameee")
	return CHOOSING



def done(bot, update, user_data):
	
    update.message.reply_text("I hope I was useful.""Until next time!")

    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater('481223618:AAE7rQT-Y8eRio5DK6h8HaUWxkvdn6WWTYQ')

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

          states={
            CHOOSING: [RegexHandler('^Start Recipe$',
                                    regular_choice,
                                    pass_user_data=True),
                       RegexHandler('^Help$', 
                                    hel,pass_user_data=True)

           
                       ],
            DECISION: [RegexHandler('^Si$',regular_choice,pass_user_data=True),
                       RegexHandler('^No$',done,pass_user_data=True),
                       ],

            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           regular_choice,
                                           pass_user_data=True),
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True),
                           ],
        },

        fallbacks=[RegexHandler('^Exit$', done, pass_user_data=True)]
    )


    dp.add_handler(conv_handler)

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
