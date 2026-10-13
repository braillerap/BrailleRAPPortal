from flask import Flask
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_NAME = "brapportal.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, DB_NAME)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


print (app.config)



from app import routes