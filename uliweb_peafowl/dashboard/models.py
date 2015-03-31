#coding=utf-8
from uliweb.orm import *
from uliweb.utils.common import get_var

def get_modified_user():
    from uliweb import request
    return request.user.id
