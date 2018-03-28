import requests
import json
import ast
from api_call import spoonacular_api_call

def spoonacular_recipe(ingredients):
    token = "YHvCM9V4j6mshPALYJaOfAvCgZJWp1jiSoOjsn93w0PY8v7ibw"
    ingredient_list =ingredients.split(', ')
    ingredient = '%2C'.join(ingredient_list)
    num_recipes = 1
    url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?"
    parameters = {'ingredients': ingredient,
                'fillIngredients': 'false',
                'limitLicense': 'false',
                'number': num_recipes,
                'ranking':1
                }

    recipe = spoonacular_api_call('GET', url, token, parameters)
    recipe_json = str(recipe.json())
    recipe_detail = recipe_json[1:-1]
    recipe_dicctionari = ast.literal_eval(recipe_detail)

    recipe_id = recipe_dicctionari["id"]
    recipe_title = recipe_dicctionari["title"]
    recipe_url_image = recipe_dicctionari["image"]
    recipe_usedIngredientCount = recipe_dicctionari["usedIngredientCount"]
    recipe_missedIngredientCount = recipe_dicctionari["missedIngredientCount"]
    recipe_likes = recipe_dicctionari["likes"]

    # print 'Recipe information: \n'
    # print '* The recipe id is: {}'.format(recipe_id) 
    # print '* The recipe title is: {}'.format(recipe_title)
    # print '* The recipe image link is: {}'.format(recipe_url_image)
    # print '* The number of ingredient asked that uses this recipe is: {}'.format(recipe_usedIngredientCount)
    # print '* The number of ingredient that missed this recipe is: {}'.format(recipe_missedIngredientCount)
    # print '* The number of people who likes this recipe is: {}'.format(recipe_likes)

    return recipe_title