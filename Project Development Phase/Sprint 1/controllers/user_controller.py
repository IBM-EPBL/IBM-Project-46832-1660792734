from models.user import User

def create_user(user):
  User.insert_user(user)
  return user

def fetch_user_by_email(email):
  return User.fetch_user_by_email(email)