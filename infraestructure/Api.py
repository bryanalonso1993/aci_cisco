#!/usr/env bin python3.8
import requests
import json
import sys
from Logger import ControllerLogger

logger = ControllerLogger()

class ControllerApic(object):
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.header = {'content-type': 'application/json'}
        self.url = "https://" + self.ip + "/api/node/"

    def generate_token(self):
        requests_token = requests.post("https://" + self.ip + "/api/aaaLogin.json", data=json.dumps({
            "aaaUser": {
                "attributes": {
                    "name": self.username,
                    "pwd": self.password
                }
            }
        }), headers=self.header, verify=False)
        if requests_token.status_code == 200:
            return requests_token.json()['imdata'][0]['aaaLogin']['attributes']['token']
        else:
            logger.set_log_app('error', 'Error endpoint {},response code:{}'.format("generate token",
                                                                                    requests_token.status_code))
            sys.exit(1)

    def execute_method_api(self, method, query_params):
        if method.lower() == 'get':
            logger.set_log_app('info', 'query endpoint {}'.format(self.url+query_params))
            response_data = requests.get(self.url+query_params, cookies={'APIC-cookie': self.generate_token()},
                                        headers=self.header, verify=False)
        elif method.lower() == 'post':
            logger.set_log_app('info', 'query endpoint {}'.format(self.url + query_params))
            response_data = requests.post(self.url+query_params, cookies={'APIC-cookie': self.generate_token()},
                                        headers=self.header, verify=False)
        elif method.lower() == 'put':
            logger.set_log_app('info', 'query endpoint {}'.format(self.url + query_params))
            response_data = requests.put(self.url+query_params, cookies={'APIC-cookie': self.generate_token()},
                                        headers=self.header, verify=False)
        else:
            logger.set_log_app('error', 'method unsupported {}'.format(self.url + query_params))
            sys.exit(1)
        if response_data.status_code == 200:
            return response_data.json()['imdata']
        else:
            logger.set_log_app('error', 'Error endpoint {},response code:{}'.format(self.url+query_params,
                                                                                    response_data.status_code))
            return None