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
from string_correction import correct_string
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from google.cloud import vision
from google.cloud.vision import types

import logging
import requests
import ast
import enchant
import json
import io
import os
# Enable logging
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/marti/Envs/chatbot/chatbot_prova/apikey.json"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING,TIPUS,DECISION, TYPING_REPLY, TYPING_CHOICE, MORE, MORE_PHOTOS, PHOTO= range(8)

menu_keyboard = [['Start Recipe', 'Help'],
                  ['Exit'],
                  ]
markup = ReplyKeyboardMarkup(menu_keyboard,one_time_keyboard=True)
choose_keyboard = [['Yes'],[ 'No']]              
markup2 = ReplyKeyboardMarkup(choose_keyboard, one_time_keyboard=True)
type_keyboard = [['Written'],['Images']]
markup3 = ReplyKeyboardMarkup(type_keyboard, one_time_keyboard=True) 
choose_photo = [['Yes'],[ 'No']]              
markup4 = ReplyKeyboardMarkup(choose_photo, one_time_keyboard=True)

ingr_list = []
ingr_bad = []
correct_list = []
ingredient_final = ''

def start(bot, update):
    update.message.reply_text("Hi! My name is Doctor Botter.  ""What you want to do?",reply_markup=markup)

    return CHOOSING

def tipus (bot,update,user_data):
	update.message.reply_text('You want to write or send us a photo of the ingredients?',reply_markup=markup3)
	return TIPUS

def foto_choice(bot, update, user_data):	
	update.message.reply_text('Send a ingredient image')
	#update.message.reply_text('you want another recipe?',reply_markup=markup2)
	return PHOTO

def written_choice(bot, update, user_data):
	user = update.message.from_user
	logger.info("Ingredients of %s: %s", user.first_name, update.message.text)
	update.message.reply_text('Give me the ingredients separate with commas')
	return TYPING_REPLY

def photo(bot, update):

    user = update.message.from_user
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    photo_file.download('ingredient.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'ingredient.jpg')
    

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.join(
      os.path.dirname(__file__),
       'ingredient.jpg')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    ##### AQUÍ VA EL FILTRE DE LABELS GENERALS #####

    print('Labels:')
    #for label in labels(0):
    print(labels[0].description)
    ingr=labels[0].description
    ingr_list.append(ingr)
    #update.message.reply_text(ingr)
    print(ingr_list)
    update.message.reply_text('Do you want to send one more ingredient?',reply_markup=markup4)

    return MORE_PHOTOS

def more(bot, update,user_data):
    user = update.message.from_user
    logger.info("Ingredients of %s: %s", user.first_name, update.message.text)
    if(update.message.text == 'Yes'):
      update.message.reply_text('OK, now I can know which is this ingredient :)')
      #*********Spoonacular get recipe****************
      print ('La llista correcta es: {}',correct_list)
      #---------------------------------------------------------->(ABANS DE CRIDAR A LA FUNCIO DE SPOONACULAR, S'HA DAJUNTAR LA LLISTA: ingr_bad + coorect_list)
      recipe_title = 'Omelet'
      #recipe_title = spoonacular_recipe(correct_list)
      update.message.reply_text('The Reciepe you can do is:' + recipe_title)
      update.message.reply_text("What you want to do?",reply_markup=markup)
      return CHOOSING

    else:
      update.message.reply_text('Can you write all the ingredients again, please?')
      return TYPING_REPLY


def more_photos(bot, update,user_data):
    user = update.message.from_user
    if(update.message.text == 'Yes'):
      update.message.reply_text('Send me a photo of one ingredient.')
      return PHOTO
    else:
      
      #*********Spoonacular get recipe****************
      recipe_title = spoonacular_recipe(ingr_list)

      update.message.reply_text('recipe_title')
      #update.message.reply_text("What you want to do?",reply_markup=markup)
      return CHOOSING

def received_information(bot, update,user_data):
  user = update.message.from_user
  logger.info("Ingredients of %s: %s", user.first_name, update.message.text)
	#ingredients.append(update.message.text)
  #cridar funcio spoonacular i enviarli update.message.text com a parametre
  ing=str(update.message.text)
  ingredient_list =ing.split(', ')
  print ing
  print ingredient_list

  for i in range(0,len(ingredient_list)): 
    correction(i, ingredient_list, bot, update, user_data)
    
  if len(ingr_bad) > 0:
    num_ingr_dolents = len(ingr_bad)
    update.message.reply_text("We have found that you have written some ingredients incorrect. Are these correct?") 
    update.message.reply_text( ingr_bad, reply_markup=markup2)
    return MORE

  else:
    #*********Spoonacular get recipe****************
    recipe_title = 'Omelet'
    #recipe_title = spoonacular_recipe(correct_list)
    update.message.reply_text("The Reciepe you can do is:" + recipe_title)
    update.message.reply_text("What you want to do?",reply_markup=markup)
    return CHOOSING

def correction(num_list, ingredients_list, bot, update, user_data):
      #********************String correction****************
  diccionary = enchant.Dict('en_US')
  ingredient_final = '' 
  correct_word = diccionary.check(ingredients_list[num_list])
  print 'el ingrediente que voy a corregir es: ' + str(ingredients_list[num_list])

  if correct_word == True :
      print 'The ingredient {} is OK',format(ingredients_list[num_list])
      correct_list.append(ingredients_list[num_list])
      return   
  else :
      # print 'The ingredient {} is not founs... WAIT \n'.format(ingredients_list[i])
      # url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/ingredients/autocomplete?"
      # parameters = {
       #         'query':ingredients_list[i]
       #         }
      # ingredient_correct = spoonacular_api_call('Get', url, token, parameters)
       # ingredient_correct_json = str(ingredient_correct.json())
      # ingredient_name = ingredient_correct_json[1:-1]
       # ingredient_dicctionari = ast.literal_eval(ingredient_name)
      # ingredient_final = ingredient_dicctionari[0]["name"]
       ingredient_final = 'tomato'
       ingr_bad.append(ingredient_final)   
       return 

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
    updater = Updater('462835538:AAH1C3vgdWf4Kd2z6fW-TmaCK21JMC3Jphg')

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(entry_points=[CommandHandler('start', start)],

          states={
            CHOOSING: [RegexHandler('^Start Recipe$',
                                    tipus,
                                    pass_user_data=True),
                       RegexHandler('^Help$', 
                                    hel,pass_user_data=True)

            
                       ],
	          TIPUS: [RegexHandler('^Written$',
                                written_choice,
                                pass_user_data=True),
                    RegexHandler('^Images$',
                                foto_choice,
                                pass_user_data=True),
                       ],
            DECISION: [RegexHandler('^Si$',
                                    written_choice,
                                    pass_user_data=True),
                       RegexHandler('^No$',
                                    done,
                                    pass_user_data=True),
                       ],
 	          MORE: [RegexHandler('^Yes$',
                                more,
                                pass_user_data=True),
                  RegexHandler('^No$',
                              more,
                              pass_user_data=True),
                       ],
            MORE_PHOTOS: [RegexHandler('^Yes$',
                                more_photos,
                                pass_user_data=True),
                  RegexHandler('^NO$',
                              more_photos,
                              pass_user_data=True),
                       ],
            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           written_choice,
                                           pass_user_data=True),
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True),
                           ],
            
            PHOTO: [MessageHandler(Filters.photo, photo),
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
