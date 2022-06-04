from flask import Flask
import requests
import pandas as pd
from create_fake_users import fake_name_and_email

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello Aleksanr, it\'s my homework'


@app.route('/requirements')
def requirements():
    with open('anacondaz.txt', 'r') as file:
        song = str(file.read())
        song_1 = song.split('\n')
        return "<p>".join(song_1)


@app.route('/generate-users')
def default_value():
    return "<p>".join(fake_name_and_email(100))


@app.route('/generate-users/<int:number>')
def create_name_and_email(number):
    return "<p>".join(fake_name_and_email(number))


@app.route('/space')
def astronaut():
    file_about_astronauts = requests.get('http://api.open-notify.org/astros.json')
    return f'Number of astronauts is {str(file_about_astronauts.json()["number"])}'


@app.route('/mean')
def average_height_and_weight():
    data = pd.read_csv('people_data.csv')
    average_height_in_cm: int = round(((data[' "Height(Inches)"'].mean()) * 2.54), 2)
    average_weight_in_kg: int = round(((data[' "Weight(Pounds)"'].mean()) / 2.205), 2)
    return f"<p>Average height: {average_height_in_cm} cm.</p> <p>Average weight: {average_weight_in_kg} kg.</p>"


if __name__ == '__main__':
    app.run()
