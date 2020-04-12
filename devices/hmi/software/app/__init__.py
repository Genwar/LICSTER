"""
This is the starting point of the flask web application. It defines the routes that available to the HMI.
"""
import os
from flask import Flask, jsonify, render_template, redirect, json, request, render_template

#
#
## The flask application instance.
#app = Flask(__name__)
#
#plc = {}
#
#from app import views
#
## Starting point.
#if __name__ == '__main__':
#    plc = Plc(ModbusTCPPlcConnector, '192.168.0.30', timeout=1)
#    # Run the webserver.
#    app.run(host="0.0.0.0", port=8080)
#
def page_not_found(e):
    """
    # The default error handler route for when a site is called that has no route provided for.
    :param e: The error message
    :return: The text that will be displayed in the browser on an error.
    """
    return jsonify(error=404, text=str(e)), 404


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.register_error_handler(404, page_not_found)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "app.sqlite"),
    )

    if test_config is None:
        # load instance config if exists
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route('/test')
    def test():
        return 'test'
    
    from . import db
    db.init_app(app)

    from . import views
    app.register_blueprint(views.bp)
    app.add_url_rule('/', endpoint='')
    
    return app