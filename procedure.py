# coding=utf-8

class Procedure:
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env
    
    def get_params(self):
        return self.params

    def get_body(self):
        return self.body

    def get_environment(self):
        return self.env
