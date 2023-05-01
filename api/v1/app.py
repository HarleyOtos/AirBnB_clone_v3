#!/usr/bin/python3
"""
Starts the API and return the status of your API
Registers the blueprint and runs the Flask server
"""
from flask import flask
from api.v1.views import app_views
from models import FileStorage

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontent
def teardown_storage(exception):
    """Calls storage.close()"""
    storage.close()

if __name__ = __main__:
    import os
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
