from flask import current_app, request, jsonify, g, make_response
from functools import wraps


def login_check(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.headers.get('token')
        if not token:
            return make_response(jsonify({'code': 403, 'msg': 'Validate error', 'result': False}), 403)
        name = current_app.redis.get('token:%s' % token).decode()
        if not name or token != current_app.redis.hget('user:%s' % name, 'token').decode():
            return make_response(jsonify({'code': 403, 'msg': 'Validate error', 'result': False}), 403)
        return func(*args, **kwargs)
    return decorator


def admin_privilege(func):
    "Check administrator permission"
    @wraps(func)
    def decorator(*args, **kwargs):
        if not hasattr(g, 'current_user') or g.current_user.role != -1:
            return make_response(jsonify({'code': 403, 'msg': 'Permission denied', 'result': False}), 403)
        return func(*args, **kwargs)
    return decorator


def operate_limit(func):
    '''Verify that the current user has access to operate by `userId`
        or the current user is administrator'''
    @wraps(func)
    def decorator(*args, **kwargs):
        if not hasattr(g, 'current_user') or g.current_user.id != request.get_json().get('userId') and g.current_user.role != -1:
            return make_response(jsonify({'code': 403, 'msg': 'permission denied', 'result': False}), 403)
        return func(*args, **kwargs)
    return decorator

def error_handle(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return make_response(jsonify({'code': 500, 'msg': str(e), 'result': False}), 500)
    return decorator

# TODO return handler