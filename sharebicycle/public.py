# coding:utf-8
from flask import current_app, request, g
from sharebicycle.model import db_session, User
from sharebicycle import api


@api.before_request
def before_request():
    "Check every request wheather it has logged in"
    token = request.headers.get('token')
    name = current_app.redis.get('token:%s' % token)
    if name:
        g.current_user = User.query.filter_by(name=name.decode()).first()
        g.token = token
    return


@api.teardown_request
def handle_teardown_request(exception):
    "Dealing at the aftermath"
    db_session.remove()
