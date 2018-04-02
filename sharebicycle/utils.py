from flask import jsonify, make_response

def check_answer(res, msg, data=False):
    if isinstance(res, str):
        "error"
        return make_response(jsonify({'code': 200, 'msg': res, 'result': False}))
    else:
        if data:
            return make_response(jsonify({'code': 200, 'msg': msg, 'result': res.to_dict()}))
        return make_response(jsonify({'code': 200, 'msg': msg, 'result': True}))
        