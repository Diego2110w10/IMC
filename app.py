from flask import Flask, render_template, request
from Flask-SQLAlchemy
from locale

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite///imc.db'

db = SQLAlchemy

@app.route('/', methods=['GET', 'POST'])

