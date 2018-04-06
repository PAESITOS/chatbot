import json
import ast
import enchant
from api_call import spoonacular_api_call
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import time

token = "YHvCM9V4j6mshPALYJaOfAvCgZJWp1jiSoOjsn93w0PY8v7ibw"
ingr_list_client = []
ingr_correct = []
ingr_correction = []


def correct_string2 (ingredient_list, bot, update, user_data, markup2):
    for k in range(0,len(ingr_list_client)):
        ingr_list_client.remove(ingr_list_client[0])
        ingr_correction.remove(ingr_correction[0])
    
    for j in range(0,len(ingr_correct)):
        ingr_correct.remove(ingr_correct[0])


    for i in range(0,len(ingredient_list)): 
        correction(i, ingredient_list, bot, update, user_data)
    
    if len(ingr_correction) > 0:
        message = str(len(ingr_correction)) + ' ingredient(s) on your list is/are misspelled.'
        message2 = 'Did you mean ' + str(ingr_correction[0]) + ' when you said ' + str(ingr_list_client[0]) + '?'  
        update.message.reply_text(message) 
        update.message.reply_text(message2, reply_markup=markup2)
        return False, ingr_correct, ingr_correction, ingr_list_client

    else:
        return True, ingr_correct, ingr_correction, ingr_list_client


def correction(num_list, ingredients_list, bot, update, user_data):
  correct_word = quick_check(ingredients_list[num_list])
    
  if correct_word == True :
        ingr_correct.append(ingredients_list[num_list])
        return   
  
  else :
      
        ingr_list_client.append(ingredients_list[num_list])
        url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/food/ingredients/autocomplete?"
        parameters = {
                'query':ingredients_list[num_list]
                }
        ingredient_correct = spoonacular_api_call('Get', url, token, parameters)
        ingredient_correct_json = str(ingredient_correct.json())
        ingredient_name = ingredient_correct_json[1:-1]
        ingredient_dicctionari = ast.literal_eval(ingredient_name)
        ingredient_final = ingredient_dicctionari[0]["name"]
        ingr_final = ingredient_final.encode('ascii')
        ingr_correction.append(ingr_final)   
        return 


def quick_check (ingredient):
    diccionary = enchant.Dict('en_US')
    correct_word = diccionary.check(ingredient)

    return correct_word