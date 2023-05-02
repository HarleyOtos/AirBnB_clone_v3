#!/usr/bin/python3
"""
Starts the API and return the status of your API
Registers the blueprint and runs the Flask server
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(exception):
    """Calls storage.close()"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors"""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(Exception)
def global_error_handler(err):
    """Handles Global errors"""
    if isinstance(err, HTTPException):
        if (isinstance(err).__name__ == 'NotFound'):
            err.description = "Not found"
        message = {'error': err.description}
        code = err.code
    else:
        message = {'error': err}
        code = 500
    return make_response(jsonify(message), code)

def setup_global_errors():
    """
    This updates HTTPException Class with custom error function
    """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)

if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
