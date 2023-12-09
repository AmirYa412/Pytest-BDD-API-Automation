import requests


class Client:

    def __init__(self, env):
        self.base_url = env.protocol + env.domain
        self.session = requests.Session()
        self.session.headers.update(env.headers)

    def get_request(self, path, params=None, data=None):
        with self.session as session:
            response = session.get(self.base_url+path, params=params, data=data, verify=False)
        return response

    def post_request(self, path, params=None, data=None, files=None, json=None):
        with self.session as session:
            response = session.post(self.base_url+path, params=params, data=data, files=files, json=json, verify=False)
        return response

    def put_request(self, path, params=None, data=None):
        with self.session as session:
            response = session.put(self.base_url+path, params=params, data=data)
        return response

    def delete_request(self, path, params=None, data=None):
        with self.session as session:
            response = session.delete(self.base_url+path, params=params, data=data)
        return response

    def change_header_value(self, header_key, value):
        self.session.headers[header_key] = value
