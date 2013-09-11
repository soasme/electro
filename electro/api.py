# -*- coding: utf-8 -*-

class API(object):

    def __init__(self, app=None, decorators=None,
            catch_all_404s=None):
        self.app = app
        self.endpoints = set()
        self.decorators = decorators or []
        self.catch_all_404s = catch_all_404s

    def add_resource(self, resource, version, *urls, **kw):
        endpoint = kw.pop('endpoint', None) or resource.__name__.lower()
        self.endpoints.add(endpoint)

        if endpoint in self.app.view_functions:
            previous_view_class = self.app.view_functions[endpoint].__dict__['view_class']
            if previous_view_class != resource:
                raise Exception, "already set"

        resource.endpoint = endpoint
        resource_func = resource.as_view(endpoint)
        for decorator in self.decorators:
            resource_func = decorator(resource_func)

        for url in urls:
            url = '/{}/{}'.format(version, url)
            self.app.add_url_rule(url, view_func=resource_func, **kw)
