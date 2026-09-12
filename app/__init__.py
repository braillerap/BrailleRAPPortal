from flask import Flask
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


print (app.config)



from app import routes