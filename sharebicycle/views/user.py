# coding:utf-8
from flask import request, g, jsonify
from sharebicycle import api
from sharebicycle.decorator import login_check, admin_privilege, operate_limit, error_handle
from sharebicycle.model import User
from sharebicycle.public import db_session
from sharebicycle.utils import check_answer


@api.route('/user/add', methods=['POST'])
@error_handle
def add_user():
    params = request.get_json()
    name = params.get('username')
    password = params.get('password')
    # vcode = params.get('vcode')
    mobile = params.get('mobile')

    # TODO vcode shuold be dealed with redis
    user = User.query.filter_by(name=name, is_del=0).first()
    if user:
        return jsonify({'code': 200, 'msg': 'User already exists', 'result': False})
    new_user = User(name=name, password=password, mobile=mobile)
    res = User.add(new_user)
    return check_answer(res, 'ojbk', True)

@api.route('/user/delete', methods=['POST'])
@error_handle
@admin_privilege
def del_user():
    user_id = request.get_json().get('userId')
    user = User.query.filter_by(id=user_id, is_del=0).first()
    if not user:
        return jsonify({'code': 200, 'msg': 'No this item', 'result': False})
    res = User.delete(user)
    return check_answer(res, 'Delete success')

@api.route('/user/modify', methods=['POST'])
@error_handle
@operate_limit
def modify_user():
    params = request.get_json()
    user_id = request.get_json().get('userId')
    user = User.query.filter_by(id=user_id, is_del=0).first()
    if not user:
        return jsonify({'code': 200, 'msg': 'No this item', 'result': False})
    res = User.update(user, params)
    return check_answer(res, 'Modify success')

@api.route('/user/getInfo', methods=['POST'])
@error_handle
@operate_limit
def get_user():
    user_id = request.get_json().get('userId')
    user = User.query.filter_by(id=user_id, is_del=0).first()
    if not user:
        return jsonify({'code': 200, 'msg': 'No this item', 'result': False})
    return jsonify({'code': 200, 'msg': 'Get success', 'result': user.to_dict()})

@api.route('/user/setBlacklist', methods=['POST'])
@error_handle
@admin_privilege
def add_blacklist():
    user_id = request.get_json().get('userId')
    remark = request.get_json().get('reason', 'I am administrator.')
    user = User.query.filter_by(id=user_id, is_del=0).first()
    if not user:
        return jsonify({'code': 200, 'msg': 'No this item', 'result': False})
    user.remark = remark
    user.status = 2
    res = User.update(user)
    return check_answer(res, 'Get in blacklist')

@api.route('/user/release', methods=['POST'])
@error_handle
@admin_privilege
def release_user():
    user_id = request.get_json().get('userId')
    remark = request.get_json().get('reason', 'I am administrator.')
    user = User.query.filter_by(id=user_id, is_del=0).first()
    if not user:
        return jsonify({'code': 200, 'msg': 'No this item', 'result': False})
    user.remark = remark
    user.status = 0
    res = User.update(user)
    return check_answer(res, 'Get out blacklist')

@api.route('/user/getList', methods=['POST'])
@error_handle
@admin_privilege
def get_users():
    params = request.get_json()
    index = params.get('pageIndex', 2)
    limit = params.get('pageSize', 1)
    sort_ = params.get('sort', 'name')
    offset = (index-1) * limit
    users = User.query.filter_by(is_del=0).order_by(getattr(User, sort_).asc())
    total = users.count()
    users = users.offset(offset).limit(limit)
    res = {'userList': [user.to_dict() for user in users], 'total': total}
    return jsonify({'code': 200, 'msg': 'As your obey', 'result': res})