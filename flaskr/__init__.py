import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/test')
    def test():
        return 'Testing... 1... 2... 3... Testing...'

    from . import games
    app.register_blueprint(games.bp)
    app.add_url_rule('/', endpoint='index')

    return app