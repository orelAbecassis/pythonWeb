from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import dotenv

# Use dotenv to load environment variables from .env file
dotenv.load_dotenv()

# Get the DATABASE_URL environment variable
database_url = os.getenv('DATABASE_URL')

app = Flask(__name__)

# Configure SQLAlchemy with the database URL
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)


# Create all database tables
with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():
    # Retrieve the list of "Person" from the mariadb database
    persons = Person.query.all()
    return render_template('index.html', persons=persons)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
