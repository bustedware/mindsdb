from flask import Flask, url_for
from flask_restx import Api
import json
from flask import g

from mindsdb_server.interfaces.datastore.datastore import DataStore
from mindsdb_server.interfaces.native.mindsdb import MindsdbNative


class Swagger_Api(Api):
    """
    This is a modification of the base Flask Restplus Api class due to the issue described here
    https://github.com/noirbizarre/flask-restplus/issues/223
    """
    @property
    def specs_url(self):
        return url_for(self.endpoint("specs"), _external=False)

def initialize_flask(config):
    app = Flask(__name__)

    app.config['SWAGGER_HOST'] = 'http://localhost:8000/mindsdb_server'
    authorizations = {
        'apikey': {
            'type': 'apiKey',
            'in': 'query',
            'name': 'apikey'
        }
    }

    api = Swagger_Api(app, authorizations=authorizations, security=['apikey'], url_prefix=':8000')

    return app, api

def initialize_interfaces(config,app):
    with app.app_context():
        g.default_store = DataStore(config)
        g.mindsdb_native = MindsdbNative(config)
