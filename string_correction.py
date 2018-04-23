import json
import ast
import enchant
from api_call import spoonacular_api_call
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import time

token = "YHvCM9V4j6mshPALYJaOfAvCgZJWp1jiSoOjsn93w0PY8v7ibw"
#ingredients = raw_input("Ingredient: ")
  
def correct_string (ingredients_list, bot, update,user_data,markup2):
    diccionary = enchant.Dict('en_US')


    for i in range(0,len(ingredients_list)):
        correct_word = diccionary.check(ingredients_list[i])
        print 'el ingrediente que voy a corregir' + str(ingredients_list[i])

        if correct_word == True :
            print 'The ingredient {} is OK'.format(ingredients_list[i])
        
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
            
            #******************** This part of the code does not work by the moment. ******************
            quest = "Do you mean " + str(ingredient_final) + "? [Y/N]" 
            update.message.reply_text(quest, reply_markup = markup2, force_reply=True, selective=True)
            
            #answer = bot.get_updates()
            user = update.message.from_user
            time.sleep(10)             
            updates = bot.get_updates()

            ####It would be perfect to get the answer here --> YES or NO... It does not work
            print([u.message.text for u in updates])
            print 'Algoooooo  ' + str((update.message.text))            
            print 'Algoooooo1  ' + str((update.message.text))
            
            # answer = str(update.message.text)
            
            #print 'Imprimo answer: ' + str(answer)

            # answer = raw_input("Do you mean {}: ".format(ingredient_final))
            # if answer == 'Y' :
            #     print 'The ingredient {} is ready to ask for a recipe'.format(ingredient_final)
            
            # else :
            #     print 'We cound not find any similar ingredient.'
        

