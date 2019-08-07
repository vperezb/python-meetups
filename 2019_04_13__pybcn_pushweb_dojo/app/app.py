from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from scripts import sender_presenter as sp

import json

def read_json(path):
    with open(path) as f:
        return json.load(f)


app = Flask(__name__)

@app.route('/', methods = ['GET'])
def sender():
    return render_template('push_sender.html')


@app.route('/send_push_by_token', methods=['POST'])
def send_push_by_token():
    push_engine = sp.__initialize_app(r'app\data\firebase_secrets\STAGING.json')
    if not request.form['push_data']:
        push_data = read_json(r'app\data\default_push_data.json')
    else:
        push_data = request.form['push_data']
    response = sp.send_to_token(request.form['fcm_token'], push_data, push_engine, False)
    return (response)

@app.route('/suscribe_token_to_topic', methods=['POST'])
def suscribe_token_to_topic():
    push_engine = sp.__initialize_app(r'app\data\firebase_secrets\STAGING.json')
    response = sp.subscribe_to_topic(request.form['topic'], [request.form['fcm_token']], push_engine)
    return (response)


@app.route('/send_push_by_topic', methods=['POST'])
def send_push_by_topic():
    push_engine = sp.__initialize_app(r'app\data\firebase_secrets\STAGING.json')
    if not request.form['push_data']:
        push_data = read_json(r'app\data\default_push_data.json')
    else:
        push_data = request.form['push_data']
    response = sp.send_to_topic(request.form['fcm_topic'], push_data, push_engine, False)
    return (response)


if __name__ == '__main__':
    app.run(debug=True)
