# coding:utf-8
from flask import Blueprint

api = Blueprint('api', __name__)

from sharebicycle import decorator, public
from sharebicycle.views import user, auth, bike