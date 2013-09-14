# -*- coding: utf-8 -*-

from flask import Flask
from electro.api import API
from electro.resource import Resource
from electro.exceptions import (
        ResourceDuplicatedDefinedError,
        )
from unittest import TestCase
from mock import Mock, patch

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
        class AddSameResource(Resource):
            def get(self): return 'pass'
        api.add_resource(AddSameResource, '/resource', endpoint='resource')
        api.add_resource(AddSameResource, '/resource/another', endpoint='another_resource')

        self.assertEqual(AddSameResource,
                app.view_functions['resource'].__dict__['view_class'])
        self.assertEqual(AddSameResource,
                app.view_functions['another_resource'].__dict__['view_class'])

        with app.test_client() as client:
            resource = client.get('/resource')
            self.assertEqual(resource.data, '"pass"')
            resource = client.get('/resource/another')
            self.assertEqual(resource.data, '"pass"')


    @patch('electro.resource.Resource')
    def test_add_url_rule(self, mock_resource):
        app = Mock()
        app.view_functions = {}
        api = API(app)
        resource_func = Mock()
        mock_resource.as_view = Mock(return_value=resource_func)
        api.add_resource(mock_resource, '/resource', endpoint="resource")

        app.add_url_rule.assert_called_once_with('/resource',
                view_func=resource_func,
                endpoint='resource')
