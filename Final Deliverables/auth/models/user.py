from utils.db2 import conn
import ibm_db

class User():
  users_table = "profiles"

  def __init__(self, userid, name, email, password):
    self.userid = userid
    self.name = name
    self.email = email   
    self.password = password

  def __str__(self) -> str:
      return f"User(userid: {self.userid}, name: {self.name}, email: {self.email})" 

  def as_dict(self):
    return {
      'userid': self.userid,
      'name': self.name,
      'email': self.email,
      'password': self.password,
    }
      

  @staticmethod
  def create_users_table():
    sql = f"CREATE TABLE IF NOT EXISTS {User.users_table} (userid int NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1), name varchar(255), email varchar(255), password varchar(255), PRIMARY KEY(userId))"
    ibm_db.exec_immediate(conn, sql)
  
  @staticmethod
  def fetch_user_by_email(email):    
    insert_sql = f"SELECT * FROM {User.users_table} WHERE email = ?"
    prep_stmt = ibm_db.prepare(conn, insert_sql)
    ibm_db.bind_param(prep_stmt, 1, email)
    ibm_db.execute(prep_stmt)
    user = ibm_db.fetch_assoc(prep_stmt)

    if user:
      return User(
        userid=user["USERID"], name=user["NAME"], email=user["EMAIL"], password=user["PASSWORD"],
      )
    else:
      return None
    
  @staticmethod
  def insert_user(user):
    print(user)
    fetched_user = User.fetch_user_by_email(email=user.email)

    if fetched_user:
      return fetched_user

    insert_sql = f"INSERT INTO {User.users_table}(name, email, password) VALUES (?, ?, ?)"
    prep_stmt = ibm_db.prepare(conn, insert_sql)
    ibm_db.bind_param(prep_stmt, 1, user.name)
    ibm_db.bind_param(prep_stmt, 2, user.email)
    ibm_db.bind_param(prep_stmt, 3, user.password)
    print(ibm_db.execute(prep_stmt))
        
    return user
