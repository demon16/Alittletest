# coding:utf-8
from flask import request, g, jsonify
from sharebicycle import api
from sharebicycle.decorator import login_check, admin_privilege, operate_limit
from sharebicycle.model import Bike
from sharebicycle.public import db_session
from sharebicycle.utils import check_answer


@api.route('/bicycle/add', methods=['POST'])
@admin_privilege
def add_bike():
    params = request.get_json()
    new_bike = Bike(**params)
    res = Bike.add(new_bike)
    return check_answer(res, 'Add success', True)


@api.route('/bicycle/delete', methods=['POST'])
@admin_privilege
def del_bike():
    bike_id = request.get_json().get('bicycleId')
    bike = Bike.query.filter_by(id=bike_id, is_del=0).first()
    if not bike:
        return jsonify({'code': 200, 'msg': 'No this item', 'result': False})
    res = Bike.delete(bike)
    return check_answer(res, 'Delete success')

@api.route('/bicycle/modify', methods=['POST'])
@admin_privilege
def modify_bike():
    params = request.get_json()
    bike_id = request.get_json().get('bicycleId')
    bike = Bike.query.filter_by(id=bike_id, is_del=0).first()
    if not bike:
        return jsonify({'code': 200, 'msg': 'No this item', 'result': False})
    res = Bike.update(bike, params)
    return check_answer(res, 'Modify success')

@api.route('/bicycle/getInfo', methods=['POST'])
@admin_privilege
def get_bike():
    bike_id = request.get_json().get('bicycleId')
    bike = Bike.query.filter_by(id=bike_id, is_del=0).first()
    if not bike:
        return jsonify({'code': 200, 'msg': 'No this item', 'result': False})
    return jsonify({'code': 200, 'msg': 'Get success', 'result': bike.to_dict()})


@api.route('/bicycle/getList', methods=['POST'])
@admin_privilege
def get_bikes():
    params = request.get_json()
    index = params.get('pageIndex', 2)
    limit = params.get('pageSize', 1)
    sort_ = params.get('sort', 'useTime')
    offset = (index-1) * limit
    bikes = Bike.query.filter_by(is_del=0).order_by(getattr(Bike, sort_).asc())
    total = bikes.count()
    bikes = bikes.offset(offset).limit(limit)
    res = {'bicycleList': [bike.to_dict() for bike in bikes], 'total': total}
    return jsonify({'code': 200, 'msg': 'As your obey', 'result': res})