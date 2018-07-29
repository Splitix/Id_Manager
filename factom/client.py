import json
import requests
import time

SLEEP = 2
FACTOM_URL = 'http://localhost:8088/v2'
WALLET_URL = 'http://localhost:8089/v2'
HEADERS = {'content-type' : 'text/plain'}

# Create a new chain
def commit_chain(ec, content, state):
    commit,reveal = _get_commit_chain(ec, content, state)
    r = requests.request("POST", FACTOM_URL, data=json.dumps(commit), headers=HEADERS)
    time.sleep(SLEEP)
    r = requests.request("POST", FACTOM_URL, data=json.dumps(reveal), headers=HEADERS)
    json_result = json.loads(r.text)
    return json_result['result']

# Helper for commit_chain to get commit-entry and reveal-entry API calls
def _get_commit_chain(ec, content, state):
    data = {
        "id": 0,
        "jsonrpc": "2.0",
        "method": "compose-chain",
        "params": {
            "chain": {
                "firstentry": {
                    "content": _hex(content),
                    "extids": [
                        _hex(state)
                    ]
                }
            },
            "ecpub": ec
        }
    }
    r = requests.request("POST", WALLET_URL, data=json.dumps(data), headers=HEADERS)
    json_result = json.loads(r.text)
    return json_result['result']['commit'], json_result['result']['reveal']

# Commit a new entry to the chain
def commit_entry(ec, chainid, content, state):
    commit,reveal = _get_commit_entry(ec, chainid, content, state)
    r = requests.request("POST", FACTOM_URL, data=json.dumps(commit), headers=HEADERS)
    time.sleep(SLEEP)
    r = requests.request("POST", FACTOM_URL, data=json.dumps(reveal), headers=HEADERS)
    json_result = json.loads(r.text)
    return json_result['result']

# Helper for commit_entry to get commit-entry and reveal-entry API calls
def _get_commit_entry(ec, chainid, content, state):
    data = {
        "id": 0,
        "jsonrpc": "2.0",
        "method": "compose-entry",
        "params": {
            "ecpub": ec,
            "content": content,
            "entry": {
                "chainid": chainid,
                "extids": [
                    _hex(state)
                ]
            }
        }
    }
    r = requests.request("POST", WALLET_URL, data=json.dumps(data), headers=HEADERS)
    json_result = json.loads(r.text)
    return json_result['result']['commit'], json_result['result']['reveal']

# Get an entry
def get_entry(hash):
    data = {
        "id": 0,
        "jsonrpc": "2.0",
        "method": "entry",
        "params": {
            "hash": hash
            }
        }
    r = requests.request("POST", FACTOM_URL, data=json.dumps(data), headers=HEADERS)
    json_result = json.loads(r.text)
    return json_result['result']

# String to hex. Source: https://stackoverflow.com/a/12214880
def _hex(s):
    return "".join("{:02x}".format(ord(c)) for c in s)
