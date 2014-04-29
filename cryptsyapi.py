#!/usr/bin/python3

import httplib2
import urllib
import json
import hmac
import hashlib
import time


class cryptsyapi:

    def __init__(self):
        self.key = ''
        self.secret = ''
        self.signature = ''
        self.uri = 'https://api.cryptsy.com/api'

    def load_key(self):
        f = open('cryptsy.key', 'r')
        self.key = f.readline().strip('\n')
        f.close()

    def load_secret(self):
        f = open('cryptsy.secret', 'r')
        self.secret = f.readline().strip('\n')
        f.close()

    def sign(self, data):
        key = self.secret.encode()
        digestmod = hashlib.sha512
        msg = data.encode()
        self.signature = hmac.new(key, msg, digestmod).hexdigest()

    def request(self, method, body={}):
        body['nonce'] = int(time.time())
        body['method'] = method
        post_data = urllib.parse.urlencode(body)
        self.sign(post_data)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Sign': self.signature,
            'Key': self.key
            }
        h = httplib2.Http()
        resp, content = h.request(self.uri, 'POST', headers=headers, body=post_data);
        if resp['status'] == '200':
            data = json.loads(content.decode())
            return(data)
        return(None)

    def getinfo(self):
        return(self.request('getinfo'))

    def marketorders(self, marketid):
        body = {}
        body['marketid'] = marketid
        data = self.request('marketorders', body)
        if data:
            return(data)
        return(None)

    def createorder(self, marketid, ordertype, quantity, price):
        print(marketid)
        body = {}
        body['marketid'] = marketid
        body['ordertype'] = ordertype
        body['quantity'] = quantity
        body['price'] = price
        data = self.request('createorder', body)
        print(data)
        return(data)

    def myorders(self, marketid):
        body = {}
        body['marketid'] = marketid
        data = self.request('myorders', body)
        if data:
            return(data['return'])
        return(None)

