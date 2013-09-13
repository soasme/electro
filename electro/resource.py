# -*- coding: utf-8 -*-

from flask import request, Response
from flask import json
from flask.views import MethodView

class Resource(MethodView):

    vendors = []
    method_decorators = []

    def dispatch_request(self, *args, **kw):
        method = getattr(self, request.method.lower(), None)
        # if the request method is HEAD and we don't have a handler for it
        # retry with GET
        if method is None and request.method == 'HEAD':
            method = getattr(self, 'get', None)

        if method is None:
            raise NotImplementedError(request.method)

        for decorator in self.method_decorators:
            method = decorator(method)

        response = method(*args, **kw)

        if isinstance(response, Response):
            return response

        data, code, headers = self._parse_response(response)
        presenter = next((v for v in self.vendors
            if v.mediatype==request.access_mediatype), None)

        if not presenter:
            return response

        return presenter.as_representation(method, data, code, headers)

    def _parse_response(self, value):
        if not isinstance(value, tuple):
            if value == '':
                code = 204
            else:
                code = 200
                value = json.dumps(value)
            return value, code, {}

        try:
            data, code, headers = value
        except ValueError:
            try:
                data, code = value
                headers = {}
            except ValueError:
                data, code, headers = value, 200, {}

        data = json.dumps(data)
        return data, code, headers
