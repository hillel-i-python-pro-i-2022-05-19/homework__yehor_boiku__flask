from flask import Flask
import sqlite3
import requests
import pandas as pd
from webargs import fields
from webargs.flaskparser import use_args
from settings import DB_PATH
from create_fake_users import fake_name_and_email
from previous_hw.init_logging import init_logging

app = Flask(__name__)


@app.route('/')
def hello_world() -> str:
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
def create__phones(args: [str]) -> str:
    with Connection() as connection:
        with connection:
            connection.execute('INSERT INTO phones (contactName, phoneValue) VALUES (:contactName, :phoneValue);',
                               {'contactName': args['contactName'], 'phoneValue': args['phoneValue']})
    init_logging('add phone')
    return 'You add new phone'


@app.route('/phones/read')
def read__phones() -> str:
    with Connection() as connection:
        phones = connection.execute('SELECT * FROM phones;').fetchall()
    init_logging('Phone list request')
    return '<br>'.join([f'{phone["phoneID"]}: {phone["contactName"]} - {phone["phoneValue"]}' for phone in phones])


@app.route('/phones/update/<int:phoneID>')
@use_args({"contactName": fields.Str(required=True)}, location="query")
def update__phones(args: [str], phoneID: str) -> str:
    with Connection() as connection:
        with connection:
            connection.execute(
                "UPDATE phones "
                "SET contactName=:contactName "
                "WHERE (phoneID=:phoneID);",
                {'contactName': args['contactName'], 'phoneID': phoneID}
            )
    init_logging(f'Request for a name change by ID: {phoneID}')
    return 'You update name'


@app.route('/phones/delete/<int:phoneID>')
def delete__phones(phoneID: str) -> str:
    with Connection() as connection:
        with connection:
            connection.execute(
                'DELETE FROM phones WHERE (phoneID=:phoneID);',
                {'phoneID': phoneID}
            )
    init_logging(f'Request for deleted phone by ID: {phoneID}')
    return 'You delete phone'


#######################################################################################################################
@app.route('/requirements')
def requirements() -> str:
    with open('anacondaz.txt', 'r') as file:
        song = str(file.read())
        song_1 = song.split('\n')
        init_logging('Request for a read song')
        return "<p>".join(song_1)


@app.route('/generate-users')
def default_value() -> str:
    init_logging('You create 100 users')
    return "<p>".join(fake_name_and_email(100))


@app.route('/generate-users/<int:number>')
def create_name_and_email(number: int) -> str:
    init_logging(f'You create {number} users')
    return "<p>".join(fake_name_and_email(number))


@app.route('/space')
def astronaut() -> str:
    file_about_astronauts = requests.get('http://api.open-notify.org/astros.json')
    init_logging('Request for an astronaut count')
    return f'Number of astronauts is {str(file_about_astronauts.json()["number"])}'


@app.route('/mean')
def average_height_and_weight() -> str:
    data = pd.read_csv('people_data.csv')
    average_height_in_cm: int = round(((data[' "Height(Inches)"'].mean()) * 2.54), 2)
    average_weight_in_kg: int = round(((data[' "Weight(Pounds)"'].mean()) / 2.205), 2)
    init_logging('Request for height and weight statistics')
    return f"<p>Average height: {average_height_in_cm} cm.</p> <p>Average weight: {average_weight_in_kg} kg.</p>"


#######################################################################################################################

if __name__ == '__main__':
    init_logging()
    app.run()
