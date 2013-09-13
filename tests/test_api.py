# -*- coding: utf-8 -*-

from flask import Flask
from electro.api import API
from electro.resource import Resource
from electro.errors import (
        ResourceDuplicatedDefinedError,
        )
from unittest import TestCase
from mock import Mock

class TestAPI(TestCase):

    def test_add_endpoint(self):
        app = Flask(__name__)
        api = API(app)
        api.add_resource(Resource, '/resource')

        self.assertIn('resource', api.endpoints)
        self.assertEqual('resource', Resource.endpoint)

    def test_add_duplicated_resource_should_raise_error(self):
        app = Flask(__name__)
        api = API(app)
        api.add_resource(Resource, '/resource')
        with self.assertRaises(ResourceDuplicatedDefinedError):
            class AnotherResource(Resource): pass
            api.add_resource(AnotherResource, '/resource', endpoint='resource')

    def test_add_same_resource(self):
        app = Flask(__name__)
        api = API(app)
        api.add_resource(Resource, '/resource')
        api.add_resource(Resource, '/resource')

        self.assertEqual(Resource, app.view_functions['resource'].__dict__['view_class'])

    def test_add_url_rule(self):
        app = Mock()
        app.view_functions = {}
        api = API(app)
        resource_func = Mock()
        Resource.as_view = Mock(return_value=resource_func)
        api.add_resource(Resource, '/resource')

        app.add_url_rule.assert_called_once_with('/resource',
                view_func=resource_func)
