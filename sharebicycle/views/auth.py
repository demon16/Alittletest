# coding:utf-8
from flask import current_app, request, jsonify, g, make_response
from sharebicycle.model import User
from sharebicycle import api
from sharebicycle.decorator import login_check, error_handle
import hashlib
import time


@api.route('/login', methods=['POST'])
@error_handle
def login():
    name = (request.get_json() or {}).get('username')
    password = request.get_json().get('password')
    user = User.query.filter_by(name=name, is_del=0).first()
    if not user:
        return make_response(jsonify({'code': 200, 'msg': 'No this item', 'result': False}))
    if user.password != password:
        return make_response(jsonify({'code': 200, 'msg': 'Password error', 'result': False}))

    m = hashlib.md5()
    m.update(name.encode())
    m.update(password.encode())
    m.update(bytes(int(time.time())))
    token = m.hexdigest()

    pipeline = current_app.redis.pipeline()
    pipeline.hmset('user:%s' % user.name, {'token': token, 'mobile': user.mobile, 'app_online': 1})
    pipeline.set('token:%s' % token, user.name)
    pipeline.expire('token:%s' % token, 3600*24)
    pipeline.execute()

    return make_response(jsonify({'code': 200, 'msg': 'Login success', 'result': True, 'token': token}))


@api.route('/logout')
@error_handle
@login_check
def logout():
    user = g.current_user
    pipeline = current_app.redis.pipeline()
    pipeline.delete('token:%s' % g.token)
    pipeline.hmset('user:%s' % user.name, {'app_online': 0})
    pipeline.execute()
    return make_response(jsonify({'code': 200, 'msg': 'Logout success', 'result': True}))