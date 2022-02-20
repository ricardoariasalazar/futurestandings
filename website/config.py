import os

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = "postgres://stvecqbaffkkvl:58c895902c77f86180d0fa4737f15bca11fe64492bd0f2ddcbc5abf36bd566fa@ec2-54-172-219-6.compute-1.amazonaws.com:5432/d5g8u6ucev6dpa"
#os.environ.get('SQLALCHEMY_DATABASE_URI')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  MAIL_SERVER = 'smtp.googlemail.com'
  MAIL_PORT = 465
  MAIL_USE_SSL = True
  MAIL_USERNAME = os.environ.get('EMAIL_USER')
  MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
