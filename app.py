
from flask import Flask, request, jsonify, redirect, url_for
from pymongo import MongoClient
import certifi
import requests
import os
import json
from bson.json_util import dumps
import re

from dotenv import load_dotenv

import selectItems
from endpoints import BASE_URL, RECIPE_URL

load_dotenv()
app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URL"), tlsCAFile=certifi.where())
db = client.dishi
saved_recipes = db.saved_recipes

file = open('ingredients.json')
ingredients = json.load(file)

recipeIdRegex = '(?<=\/)[a-zA-Z0-9]{32}(?=\?)'

def parse_json(data):
  return json.loads(dumps(data))

@app.route('/')
def index():
  return redirect(url_for('getRecipeList'))

@app.get('/recipes')
def getRecipeList():
	params = 'q=chicken' # request.args 
	url = f'{BASE_URL}&{params}'
	response = requests.get(url)
	return response.json()

@app.get('/select/health')
def showHealthOptions():
  return jsonify(ingredients=ingredients['list'], health_labels=selectItems.HEALTH_LABELS, diet_labels=selectItems.DIET_LABELS)

@app.get('/select/properties')
def showDishOptions():
  return jsonify(cuisine_types=selectItems.CUISINE_TYPES, dish_types=selectItems.DISH_TYPES, meal_types=selectItems.MEAL_TYPES)

@app.get('/saved')
def getSavedRecipesList():
	array = list(saved_recipes.find())
	return jsonify(recipes=parse_json(array))

@app.get('/recipes/<id>')
def getRecipe(id):
	url = RECIPE_URL(id)
	response = requests.get(url)
	return response.json()

@app.post('/recipes/<id>')
def saveRecipe(id):
	recipe = saved_recipes.find_one({"id": id})
	if not recipe:
		response = requests.get(RECIPE_URL(id))
		recipe = response.json()
		recipe_id = re.search(recipeIdRegex, recipe["_links"].self.href).group(0)
		saved_recipes.insert({**recipe, "id": recipe_id})
	return jsonify(recipe=parse_json(recipe))

@app.delete('/recipes/<id>')
def unsaveRecipe(id):
	recipe = saved_recipes.find_one_and_delete({"id": id})
	return jsonify(recipe=parse_json(recipe))
