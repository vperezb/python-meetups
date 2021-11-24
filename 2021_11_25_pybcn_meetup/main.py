from flask import Flask

from google.cloud import datastore

datastore_client = datastore.Client()


app = Flask(__name__)

@app.route('/', methods = ['GET'])
def root():
    return '<h1>Hello PyBcn example</h1>'


@app.route('/save-stuff', methods = ['GET'])
def save_stuff():
    e = 'Put was succesfull'
    try:
        entity = datastore.Entity(key=datastore_client.key('my_entity_type'))
        entity.update({
            'hello': 'world'
        })
        datastore_client.put(entity)
    except Exception as e:
        return '<h1>Result</h1><p>{}</p>'.format(e)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
