import base64
import json
import requests

DEBUG = True

URL = 'http://localhost:8089/v2'
HEADERS = {'content-type' : 'text/plain'}

def commit_chain(ec, content, state):
    commit,reveal = _get_commit_chain_message(ec, content, state)
    data = {
        "id": 0,
        "jsonrpc": "2.0",
        "method": "commit-chain",
        "params": {
            "message": commit
            }
        }
    r = requests.request("POST", URL, data=json.dumps(data), headers=HEADERS)
    if DEBUG:
        print(r.text)
    _reveal_chain(reveal)
    return r.text

def _reveal_chain(reveal):
    data = {
        "id": 0,
        "jsonrpc": "2.0",
        "method": "reveal-chain",
        "params": {
            "entry": reveal
            }
        }
    r = requests.request("POST", URL, data=json.dumps(data), headers=HEADERS)
    if DEBUG:
        print(r.text)
    return r.text

def _get_commit_chain_message(ec, content, state):
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
    return r.text['result']['commit']['params']['message'], r.text['result']['reveal']['params']['entry']

def commit_entry(ec, chainid, content, state):
    commit,reveal = _get_commit_entry_message(ec, chainid, content, state)
    data = {
        "id": 0,
        "jsonrpc": "2.0",
        "method": "commit-entry",
        "params": {
            "message": commit
            }
        }
    r = requests.request("POST", URL, data=json.dumps(data), headers=HEADERS)
    if DEBUG:
        print(r.text)
    _reveal_entry(reveal)

def _reveal_entry(reveal):
    data = {
        "id": 0,
        "jsonrpc": "2.0",
        "method": "reveal-entry",
        "params": {
            "entry": reveal
            }
        }
    r = requests.request("POST", URL, data=json.dumps(data), headers=HEADERS)
    if DEBUG:
        print(r.text)
    return r.text

def _get_commit_entry_message(ec, chainid, content, state):
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
    return r.text['result']['commit']['params']['message'], r.text['result']['reveal']['params']['entry']

def get_entry(ec, hash):
    data = {
        "id": 0,
        "jsonrpc": "2.0",
        "method": "entry",
        "params": {
            "hash": hash
            }
        }
    r = requests.request("POST", URL, data=json.dumps(data), headers=HEADERS)
    if DEBUG:
        print(r.text)
    return r.text
