from datetime import date, datetime
import os
from random import randint
import requests as req
from keys import SPOONACULAR_BASE_URL, SPOONACULAR_API_KEY
import ibm_cos
from models.food import Food

def analyze_image(image_file_from_client):
  # init 
  if not os.path.isdir("./upload"):
    os.makedirs("./upload")
    
  rand_img_filename = str(randint(100, 100000000)) + "." + image_file_from_client.filename.split('.')[1]
  local_path = os.path.join('upload', rand_img_filename)

  # save
  image_file_from_client.save(local_path)        
  image_ibm_cos_url = ibm_cos.upload_file(local_path, rand_img_filename)
  
  nutrition_details = _fetch_nutrition_details(image_ibm_cos_url)

  # delete
  os.remove(local_path)
  ibm_cos.delete_item(rand_img_filename)

  return nutrition_details


def _fetch_nutrition_details(image_url):
  # fetch details
  url =  "https://api.spoonacular.com/" + "food/images/analyze?imageUrl=" + image_url
  res = req.get(url + "", headers={ 'x-api-key':'2fd2334422db49928ff833cf3ab5d110' })
    
  print(res.status_code)

  if res.ok:
    result = res.json()
    nutrition_data = result['nutrition']
    return {
      'name': result['category']['name'],
      'accuracy': result['category']['probability'],
      # unit: calories      
      'calories': nutrition_data['calories']['value'],
      # unit: g
      'fat': nutrition_data['fat']['value'],
      # unit: g
      'protein': nutrition_data['protein']['value'],
      # unit: g
      'carbs': nutrition_data['carbs']['value'],
    }
  else:
    return {
      'name': f'unknown/exceed/{res.status_code}',
      'accuracy': 0,
      # unit: calories      
      'calories': 0,
      # unit: g
      'fat': 0,
      # unit: g
      'protein': 0,
      # unit: g
      'carbs': 0,
    }

def save_food(userid, food):    
  return Food.insert_food(userid, food)

def fetch_food(userid):    
  return Food.fetch_foods_by_userid(userid)
  