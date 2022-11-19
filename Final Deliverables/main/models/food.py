from datetime import datetime
import ibm_db
from utils.db2 import conn

class Food():
  table = "foods"

  def __init__(self, name, time, calories, fat, protein, carbs, accuracy=0):
    self.name = name
    self.time = time
    self.accuracy = accuracy
    self.calories = calories
    self.fat = fat
    self.protein = protein
    self.carbs = carbs

  def __str__(self) -> str:
      return f"{Food.table}({self.name})" 
      

  @staticmethod
  def create_foods_table():
    sql = ''
    sql += 'CREATE TABLE IF NOT EXISTS '+ Food.table + '('
    sql += 'foodid int NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),'
    sql += 'userid int,'
    sql += 'name varchar(255),'
    sql += 'time float NOT NULL,'
    sql += 'calories float NOT NULL,'
    sql += 'fat float NOT NULL,'
    sql += 'protein float NOT NULL,'
    sql += 'carbs float NOT NULL,'
    sql += 'PRIMARY KEY(foodid)'
    sql += ')'
    ibm_db.exec_immediate(conn, sql)

  @staticmethod
  def insert_food(userid, food):
    insert_sql = f"INSERT INTO {Food.table}(userid, name, time, calories, fat, protein, carbs) VALUES (?, ?, ?, ?, ?, ?, ?)"
    prep_stmt = ibm_db.prepare(conn, insert_sql)
    ibm_db.bind_param(prep_stmt, 1, userid)
    ibm_db.bind_param(prep_stmt, 2, food.name)
    ibm_db.bind_param(prep_stmt, 3, food.time)
    ibm_db.bind_param(prep_stmt, 4, food.calories)
    ibm_db.bind_param(prep_stmt, 5, food.fat)
    ibm_db.bind_param(prep_stmt, 6, food.protein)
    ibm_db.bind_param(prep_stmt, 7, food.carbs)
    ibm_db.execute(prep_stmt)
    
    return food
  
  @staticmethod
  def fetch_foods_by_userid(userid):
    sql = f"SELECT * FROM {Food.table} WHERE userid = ? ORDER BY time desc"
    prep_stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(prep_stmt, 1, userid)
    ibm_db.execute(prep_stmt)
    
    foods = []

    while ibm_db.fetch_row(prep_stmt) != False:
      foods.append({
        "name": ibm_db.result(prep_stmt, "NAME"),
        'time': datetime.fromtimestamp(ibm_db.result(prep_stmt, "TIME")),
        "accuracy": 0,
        "calories": ibm_db.result(prep_stmt, "CALORIES"),
        "fat": ibm_db.result(prep_stmt, "FAT"),
        "protein": ibm_db.result(prep_stmt, "PROTEIN"),
        "carbs": ibm_db.result(prep_stmt, "CARBS")
      })

    return foods