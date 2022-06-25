from flask import Flask
import sqlite3
import requests
import pandas as pd
from webargs import fields
from webargs.flaskparser import use_args

from application import create_fake_users as fake_name_and_email
from application.settings import DB_PATH

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello Aleksanr, it\'s my homework'


class Connection(object):
    def __init__(self):
        self._connection: sqlite3.Connection | None = None

    def __enter__(self):
        self._connection = sqlite3.connect(DB_PATH)
        self._connection.row_factory = sqlite3.Row
        return self._connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()


@app.route('/phones/create')
@use_args({"contactName": fields.Str(required=True), "phoneValue": fields.Int(required=True)}, location="query")
def create__phones(args):
    with Connection() as connection:
        with connection:
            connection.execute('INSERT INTO phones (contactName, phoneValue) VALUES (:contactName, :phoneValue);',
                               {'contactName': args['contactName'], 'phoneValue': args['phoneValue']})
    return 'You add new phone'


@app.route('/phones/read')
def read__phones():
    with Connection() as connection:
        phones = connection.execute('SELECT * FROM phones;').fetchall()
    return '<br>'.join([f'{phone["phoneID"]}: {phone["contactName"]} - {phone["phoneValue"]}' for phone in phones])


@app.route('/phones/update/<int:phoneID>')
@use_args({"contactName": fields.Str(required=True)}, location="query")
def update__phones(args, phoneID):
    with Connection() as connection:
        with connection:
            connection.execute(
                "UPDATE phones "
                "SET contactName=:contactName "
                "WHERE (phoneID=:phoneID);",
                {'contactName': args['contactName'], 'phoneID': phoneID}
            )
    return 'You update name'


@app.route('/phones/delete/<int:phoneID>')
def delete__phones(phoneID):
    with Connection() as connection:
        with connection:
            connection.execute(
                'DELETE FROM phones WHERE (phoneID=:phoneID);',
                {'phoneID': phoneID}
            )
    return 'You delete phone'


#######################################################################################################################
@app.route('/requirements')
def requirements():
    with open('application/anacondaz.txt', 'r') as file:
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
    data = pd.read_csv('application/people_data.csv')
    average_height_in_cm: int = round(((data[' "Height(Inches)"'].mean()) * 2.54), 2)
    average_weight_in_kg: int = round(((data[' "Weight(Pounds)"'].mean()) / 2.205), 2)
    return f"<p>Average height: {average_height_in_cm} cm.</p> <p>Average weight: {average_weight_in_kg} kg.</p>"


#######################################################################################################################

if __name__ == '__main__':
    app.run()