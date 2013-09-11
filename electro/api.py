# -*- coding: utf-8 -*-

class API(object):

    def __init__(self, app=None, decorators=None,
            catch_all_404s=None):
        self.app = app
        self.decorators = decorators or []
        self.catch_all_404s = catch_all_404s
