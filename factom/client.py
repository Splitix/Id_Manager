import base64
import json
import requests

DEBUG = True

URL = 'http://localhost:8089/v2'
HEADERS = {'content-type' : 'text/plain'}

def compose_chain(ec, content, state):
    data = {
        "id": 0,
        "jsonrpc": "2.0",
        "method": "compose-chain",
        "params": {
            "chain": {
                "firstentry": {
                    "content": content.encode('hex'),
                    "extids": [
                        state.encode('hex')
                    ]
                }
            },
            "ecpub": ec
        }
    }
    r = requests.request("POST", URL, data=json.dumps(data), headers=HEADERS)
    if DEBUG:
        print(r.text)
    return r.text

def compose_entry(ec, chainid, content, state):
    data = {
        "id": 0,
        "jsonrpc": "2.0",
        "method": "compose-entry",
        "params": {
            "ecpub": ec,
            "entry": {
                "chainid": chainid.encode('hex'),
                "content": content.encode('hex'),
                "extids": [
                    state.encode('hex')
                ]
            }
        }
    }
    r = requests.request("POST", URL, data=json.dumps(data), headers=HEADERS)
    if DEBUG:
        print(r.text)
    return r.text

def get_entry(ec, hash):
    data = {
        "id": 0,
        "jsonrpc": "2.0",
        "method": "entry",
        "params": {
            "hash": hash
        }
    r = requests.request("POST", URL, data=json.dumps(data), headers=HEADERS)
    if DEBUG:
        print(r.text)
    return r.text
}
