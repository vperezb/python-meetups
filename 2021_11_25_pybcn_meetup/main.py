import os

from flask import Flask, json, render_template, jsonify, abort
import datetime

from google.cloud import datastore

datastore_client = datastore.Client()


app = Flask(__name__)

@app.get('/')
def root():
    return '<h1>Hello PyBcn example</h1>' + '<p>{}</p>'.format(os.getenv('SERVICE', 'LOCAL'))

@app.route('/private', methods = ['GET'])
def root_private():
    if os.getenv('SERVICE') != 'private':
        return 'SOY <p>{}</p>'.format(os.getenv('SERVICE'))
    return '<h1>Hello PyBcn example</h1>' + 'SOY <p>{}</p>'.format(os.getenv('SERVICE'))


@app.route('/save-stuff', methods = ['GET'])
def save_stuff():
    e = 'Put was succesfull'
    try:
        entity = datastore.Entity(key=datastore_client.key('my_entity_type'))
        entity.update({
            'hello': 'world',
            'datetime': datetime.datetime.now(),
            'hola': 'que tal'
        })
        datastore_client.put(entity)
    except Exception as e:
        pass
    return '<h1>Result</h1><p>{}</p><p><a href="/read-stuff-json">Read json</a></p>'.format(e)

@app.route('/read-stuff', methods = ['GET'])
def read_stuff():
    query = datastore_client.query(kind='my_entity_type')
    result = query.fetch(limit=10)
    return render_template('table_template.html', data = result)

@app.route('/read-stuff-json', methods = ['GET'])
def read_stuff_json():
    query = datastore_client.query(kind='my_entity_type')
    result = list(query.fetch(limit=10))
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
