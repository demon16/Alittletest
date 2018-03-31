from flask import jsonify

def check_answer(res, msg, data=False):
    if isinstance(res, str):
        "error"
        return jsonify({'code': 200, 'msg': res, 'result': False})
    else:
        if data:
            return jsonify({'code': 200, 'msg': msg, 'result': res.to_dict()})
        return jsonify({'code': 200, 'msg': msg, 'result': True})
        