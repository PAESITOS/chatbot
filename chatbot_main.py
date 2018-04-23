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
from spoonacular import spoonacular_recipe
from api_call import spoonacular_api_call
#from string_correction import correct_string
from string_correction2 import correct_string2
from string_correction2 import quick_check
from image_recognition import amazon_recognition
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging
import requests
import ast
import enchant
import json
import boto3
import io
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING,TIPUS, PHOTO, MORE_PHOTO, TYPING_REPLY, TYPING_CHOICE, MORE, QUICK_CHECKER, GET_RECIPE = range(9)

menu_keyboard = [['Start Recipe', 'Help'],
                  ['Exit'],
                  ]
boolean_answer = [['Yes','No']]
type_keyboard = [['Written'],['Images']]

markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True)
markup2 = ReplyKeyboardMarkup(boolean_answer,one_time_keyboard=True)
markup3 = ReplyKeyboardMarkup(type_keyboard, one_time_keyboard=True)

ingr_list_client = []
ingr_correct = []
ingr_correction = []


def start(bot, update):
    update.message.reply_text("Hi! My name is Ramsay Junior.  "
        "What do you want to do?",
        reply_markup=markup)

    return CHOOSING
def tipus (bot, update, user_data):
    for o in range(0,len(ingr_list_client)):
        ingr_list_client.remove(ingr_list_client[0])
        ingr_correction.remove(ingr_correction[0])
    
    for k in range(0,len(ingr_correct)):
        print (k)
        ingr_correct.remove(ingr_correct[0])
    update.message.reply_text('Do you want to write or to send a photo of the ingredients?', reply_markup=markup3)
    return TIPUS

def foto_choice(bot, update, user_data):
    update.message.reply_text('Send one igredient image')
    return PHOTO

def photo(bot, update):
    photo = bot.get_file(update.message.photo[-1].file_id).download_as_bytearray()
    label = amazon_recognition(photo)
    if label is None:
        update.message.reply_text("I can't find any ingredients on your foto.")
    else:
        ingr_correct.append(label) #Això ens proporciona un label que ha estat filtrat
    update.message.reply_text('Do you want to send another photo?', reply_markup=markup2)
    return MORE_PHOTO

def more_photo(bot, update, user_data):
    user=update.message.from_user
    if(update.message.text == 'Yes'):
        update.message.reply_text('Send me a photo of one ingredient.')
        return PHOTO
    else:
        if len(ingr_correct) > 1:
            msg = 'Is your ingredient ' + str(ingr_correct) + '?'
        else:
            msg = 'Are your ingredients '
            for i, ingr in enumerate(ingr_correct[0:-2]):
                msg = msg + str(ingr) + ', '
            msg = msg + ' & ' str(ingr[-1]) + ' ?'
        update.message.reply_text(msg, reply_markup=markup2)
        return GET_RECIPE

def regular_choice(bot, update, user_data):
    update.message.reply_text('Give me the ingredients separated with commas')
    return TYPING_REPLY

def more(bot, update,user_data):
    user = update.message.from_user
    logger.info("Ingredients of %s: %s", user.first_name, update.message.text)
    if(update.message.text == 'Yes'):
        update.message.reply_text('OK, we corrected it for you! :)')
        ingr_correct.append(ingr_correction[0])
        ingr_correction.remove(ingr_correction[0])
        ingr_list_client.remove(ingr_list_client[0])
        
        if len(ingr_correction) > 0:
            message = "Did you mean " + str(ingr_correction[0]) + ' when you said ' + str(ingr_list_client[0]) + '?'  
            update.message.reply_text(message, reply_markup=markup2) 
            #update.message.reply_text(ingr_bad, reply_markup=markup2)
            return MORE
        else :
            message = 'Is/Are your ingredient/s '

            for i in range (0,len(ingr_correct)-1):
                if i == (len(ingr_correct)-2):
                    message = message + str(ingr_correct[i]) + ' and '
                else :
                    message = message + str(ingr_correct[i]) + ', '
            message = message + str (ingr_correct[len(ingr_correct)-1]) + '? '
            update.message.reply_text(message, reply_markup=markup2)
            return GET_RECIPE

    else:
        message = 'Could you write it again, please?'
        update.message.reply_text(message)
        return QUICK_CHECKER

def quick_checker (bot, update,user_data):
    user = update.message.from_user
    ing = str(update.message.text)
    corrector = quick_check(ing)

    if corrector == True : 
        update.message.reply_text('Great, we changed it :)')
        ingr_correct.append(ing)
        ingr_correction.remove(ingr_correction[0])
        ingr_list_client.remove(ingr_list_client[0])
    
    else :
        message = 'We are sorry. We could not find ' + str(ing) + ' as an ingredient. We are going to remove it from your list.'
        update.message.reply_text(message)
        ingr_correction.remove(ingr_correction[0])
        ingr_list_client.remove(ingr_list_client[0])

            
    if len(ingr_correction) > 0:
        message = "Did you mean " + str(ingr_correction[0]) + ' when you said ' + str(ingr_list_client[0]) + ' ?'  
        update.message.reply_text(message, reply_markup=markup2) 
        #update.message.reply_text(ingr_bad, reply_markup=markup2)
        return MORE
    
    else :
        message = 'Is/are your ingredient/s '
        for i in range (0,len(ingr_correct)-1):
            if i == (len(ingr_correct)-2):
                message = message + str(ingr_correct[i])+ ' and '
            else :
                message = message + str(ingr_correct[i]) + ', '
            
        message = message + str (ingr_correct[len(ingr_correct)-1]) + ' ? '
        update.message.reply_text(message, reply_markup=markup2)
        return GET_RECIPE


def received_information(bot, update,user_data):


    #if len(ingr_correct)>0:
    user = update.message.from_user
    logger.info("Ingredients of %s: %s", user.first_name, update.message.text)
    ing = str(update.message.text)
    ingredient_list =ing.split(', ')   
    new_state, ingr_correct1, ingr_correction1, ingr_list_client1 = correct_string2(ingredient_list, bot, update,user_data, markup2)
    
    for i in range(0,len(ingr_correct1)):
        ingr_correct.append(ingr_correct1[i])
    
    for j in range(0,len(ingr_list_client1)):
        ingr_list_client.append(ingr_list_client1[j])
        ingr_correction.append(ingr_correction1[j])
  
    if new_state == False:
        return MORE
    else :
        message = 'Is/are your ingredient/s '
        for i in range (0,len(ingr_correct)-1):
            if i == (len(ingr_correct)-2):
                message = message + str(ingr_correct[i])+ ' and '
            else :
                message = message + str(ingr_correct[i]) + ', '

        message = message + str (ingr_correct[len(ingr_correct)-1]) + '? '
        update.message.reply_text(message, reply_markup=markup2)
        return GET_RECIPE
        

def get_recipe (bot,update,user_data):
    user = update.message.from_user
    logger.info("Ingredients of %s: %s", user.first_name, update.message.text)
    message2 = 'What would you like to do?'
    
    if(update.message.text == 'Yes'):
        #*********************¡¡¡¡¡¡¡ Aquí es fa una crida a spoonacular !!!!!!****************
        recipe_title = spoonacular_recipe(ingr_correct)
        message = 'These ingredients are ideal to prepair a delicious ' + str(recipe_title)
        update.message.reply_text(message)
        user_data.clear()
        
    
    else:
        message = 'Sorry, we could not give you a recipe.'
        user_data.clear()
        update.message.reply_text(message)
        
    update.message.reply_text(message2, reply_markup = markup)
    return CHOOSING

def hel (bot,update,user_data):

	update.message.reply_text("We are IMAGLabs. We are creating a chatbot to help you to elaborate your best meals ever. If you want to try, just select Start Recipe. Otherwise, choose Exit", reply_markup=markup)
	return CHOOSING

def done(bot, update, user_data):
    
    update.message.reply_text("I hope I was useful. Until next time!")

    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater('462835538:AAH1C3vgdWf4Kd2z6fW-TmaCK21JMC3Jphg')

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [RegexHandler('^Start Recipe$',
                                    tipus,
                                    pass_user_data=True),
                       RegexHandler('^Help$',
                                    hel,pass_user_data=True),
		      ],
            TIPUS: [RegexHandler('^Written$',regular_choice,pass_user_data=True),
                    RegexHandler('^Images$',foto_choice,pass_user_data=True),
                    ],
	    
            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           regular_choice,
                                           pass_user_data=True),
                            ],

            PHOTO: [MessageHandler(Filters.photo, photo)],
            MORE_PHOTO: [RegexHandler('^Yes$', more_photo, pass_user_data=True),
                        RegexHandler('^No$', more_photo, pass_user_data=True)],
            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True),
                           ],
            MORE: [RegexHandler('^Yes$',
                                more,
                                pass_user_data=True),
                  RegexHandler('^No$',
                              more,
                              pass_user_data=True),
                            ],
            QUICK_CHECKER: [MessageHandler(Filters.text,
                                           quick_checker,
                                           pass_user_data=True),
                            ],
            GET_RECIPE: [RegexHandler('^Yes$',
                                get_recipe,
                                pass_user_data=True),
                   RegexHandler('^No$',
                              get_recipe,
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
