# -*- coding: utf-8 -*-

from werkzeug.exceptions import HTTPException
from flask import abort

def halt(http_status_code, *args, **kw):
    try:
        abort(http_status_code)
    except HTTPException as e:
        if kw:
            e.data = kw
        raise e
