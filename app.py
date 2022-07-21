
from flask import Flask, request, jsonify, redirect, url_for
from pymongo import MongoClient
import certifi
import requests
import os
import json
from bson.json_util import dumps

from dotenv import load_dotenv

import selectItems

load_dotenv()
app = Flask(__name__)

client = MongoClient("mongodb+srv://dishiadmin:d1sh1adm1n@cluster0.pjb3s.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = client.dishi
saved_recipes = db.saved_recipes

file = open('ingredients.json')
ingredients = json.load(file)

def parse_json(data):
  return json.loads(dumps(data))

@app.route('/')
def index():
  return redirect(url_for('getRecipeList'))

@app.get('/recipes')
def getRecipeList():
	params = 'type=public&q=chicken' # request.args 
	url = f'{os.getenv("API_URL")}?{params}&app_id={os.getenv("APP_ID")}&app_key={os.getenv("APP_KEY")}'
	response = requests.get(url)
	return response.json()

@app.get('/select/health') # INGREDIENTS, HEALTH_LABELS, DIET_LABELS
def showHealthOptions():
  return jsonify(ingredients=ingredients['list'], health_labels=selectItems.HEALTH_LABELS, diet_labels=selectItems.DIET_LABELS)

@app.get('/select/properties') # CUISINE_TYPES, DISH_TYPES, MEAL_TYPES
def showDishOptions():
  return jsonify(cuisine_types=selectItems.CUISINE_TYPES, dish_types=selectItems.DISH_TYPES, meal_types=selectItems.MEAL_TYPES)

@app.get('/saved')
def getSavedRecipesList():
	array = list(saved_recipes.find())
	return jsonify(recipes=parse_json(array))

@app.get('/recipes/<id>')
def getRecipe(id):
	return 'Hello World!'

@app.get('/recipes/<id>/save')
def saveRecipe(id):
	return 'Hello World!'

@app.get('/recipes/<id>/unsave')
def unsaveRecipe(id):
	return 'Hello World!'
