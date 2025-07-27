from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Importa modelos para que se registren
from app.models import *

@app.route("/")
def index():
    return "✅ Software Notarios corriendo"

if __name__ == "__main__":
    app.run(debug=True)
