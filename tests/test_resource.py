# -*- coding: utf-8 -*-

from unittest import TestCase
from electro.resource import Resource

class TestResource(TestCase):

    def assert_parser(self, assert_value, values):
        resource = Resource()
        value = resource._parse_response(values)
        self.assertEqual(value, assert_value)

    def test_empty_content_will_return_204(self):
        self.assert_parser(('', 204, {}), '')

    def test_dict_will_return_200(self):
        self.assert_parser(('{}', 200, {}), {})

    def test_list_will_return_200(self):
        self.assert_parser(('[]', 200, {}), [])

    def test_str_will_return_200(self):
        self.assert_parser(('"test"', 200, {}), 'test')

    def test_data_with_code(self):
        self.assert_parser(('{}', 201, {}), ({}, 201))

    def test_data_with_code_and_headers(self):
        self.assert_parser(('{}', 201, {'k':'v'}), ({}, 201, {'k':'v'}))
