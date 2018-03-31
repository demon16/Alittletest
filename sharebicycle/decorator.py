from flask import current_app, request, jsonify, g
from functools import wraps

def login_check(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.headers.get('token')
        if not token:
            return jsonify({'code': 200, 'msg': 'Validate error', 'result': False})
        name = current_app.redis.get('token:%s' % token).decode()
        if not name or token != current_app.redis.hget('user:%s' % name, 'token').decode():
            return jsonify({'code': 200, 'msg': 'Validate error', 'result': False})
        return func(*args, **kwargs)
    return decorator


def admin_privilege(func):
    "Check administrator permission"
    @wraps(func)
    def decorator(*args, **kwargs):
        if not hasattr(g, 'current_user') or g.current_user.role != -1:
            return jsonify({'code': 200, 'msg': 'Permission denied', 'result': False})
        return func(*args, **kwargs)
    return decorator


def operate_limit(func):
    '''Verify that the current user has access to operate by `userId`
        or the current user is administrator'''
    @wraps(func)
    def decorator(*args, **kwargs):
        if not hasattr(g, 'current_user') or g.current_user.id != request.get_json().get('userId') and g.current_user.role != -1:
            return jsonify({'code': 200, 'msg': 'permission denied', 'result': False})
        return func(*args, **kwargs)
    return decorator

# TODO error handler

# TODO return handler