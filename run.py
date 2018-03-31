# coding:utf-8
from flask import Flask
import redis


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.secret_key = app.config['SECRET_KEY']
    app.redis = redis.Redis(host=app.config['REDIS_HOST'],
                            port=app.config['REDIS_PORT'],
                            db=app.config['REDIS_DB'])
    app.debug = app.config['DEBUG']
    app.host = app.config['HOST']
    app.port = app.config['PORT']

    from sharebicycle import api

    app.register_blueprint(api, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.debug, host=app.host, port = app.port)