from flask import Flask, render_template
from config import Config
from routes.users import user_bp
from models import db
from flask_migrate import Migrate
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object(Config)
app.register_blueprint(user_bp)

db.init_app(app)

migrate = Migrate(app, db)

@app.route('/')

def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)