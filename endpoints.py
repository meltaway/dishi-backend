import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = f'{os.getenv("API_URL")}?app_id={os.getenv("APP_ID")}&app_key={os.getenv("APP_KEY")}&type=public'

def RECIPE_URL(id):
	return f'{os.getenv("API_URL")}/{id}?app_id={os.getenv("APP_ID")}&app_key={os.getenv("APP_KEY")}&type=public'