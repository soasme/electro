# -*- coding: utf-8 -*-

from json import dumps
from flask import make_response

class Presenter(object):

    mediatype = None

    def __init__(self, data, code, headers):
        self.data = data
        self.code = code
        self.headers = headers

    @classmethod
    def as_representation(cls, method, data, code, headers):
        presenter = cls(data, code, headers)
        handler = getattr(presenter, method, None)
        return handler()

    def get(self):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def put(self):
        raise NotImplementedError

    def head(self):
        raise NotImplementedError

    def options(self):
        raise NotImplementedError

class JSONPresenter(Presenter):

    mediatype = 'application/json'

    @classmethod
    def as_representation(cls, method, data, code, headers):
        data = dumps(data)
        response = make_response(data, code)
        response.headers.extend(headers)
        return response
