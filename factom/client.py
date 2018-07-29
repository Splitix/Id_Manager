import requests
import time

SLEEP = 2
FACTOM_URL = 'http://localhost:8088/v2'
WALLET_URL = 'http://localhost:8089/v2'
HEADERS = {'content-type' : 'text/plain'}

# Create a new ec address
def create_ec_address():
    data = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "generate-ec-address"
    }
    r = requests.post(WALLET_URL, json=data, headers=HEADERS)
    result_dict = r.json()
    return result_dict['result']['public']

# Exchange factoms to entry credits
def fct_to_ec(ec_address, tx_name, amount):
    data = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "new-transaction",
        "params": {
            "tx-name": tx_name
        }
    }
    r = requests.post(WALLET_URL, json=data, headers=HEADERS)
    data = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "add-input",
        "params":{
            "tx-name": tx_name,
            "address": "FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q",
            "amount": amount
        }
    }
    r = requests.post(WALLET_URL, json=data, headers=HEADERS)
    data = {
        "jsonrpc": "2.0",
        "id":0,
        "method": "add-ec-output",
        "params": {
            "tx-name": tx_name,
            "address": ec_address,
            "amount": amount
        }
    }
    r = requests.post(WALLET_URL, json=data, headers=HEADERS)
    data = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "add-fee",
        "params": {
            "tx-name": tx_name,
            "address": "FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q",
        }
    }
    r = requests.post(WALLET_URL, json=data, headers=HEADERS)
    data = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "sign-transaction",
        "params":{
            "tx-name": tx_name,
        }
    }
    r = requests.post(WALLET_URL, json=data, headers=HEADERS)
    data = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "compose-transaction",
        "params": {
            "tx-name": tx_name
        }
    }
    r = requests.post(WALLET_URL, json=data, headers=HEADERS)
    result_dict = r.json()
    r = requests.post(FACTOM_URL, json=result_dict['result'], headers=HEADERS)

# Create a new chain
def commit_chain(ec_address, content, state):
    commit,reveal = _get_commit_chain(ec_address, content, state)
    r = requests.post(FACTOM_URL, json=commit, headers=HEADERS)
    time.sleep(SLEEP)
    r = requests.post(FACTOM_URL, json=reveal, headers=HEADERS)
    result_dict = r.json()
    return result_dict['result']

# Helper for commit_chain to get commit-entry and reveal-entry API calls
def _get_commit_chain(ec_address, content, state):
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
            "ecpub": ec_address
        }
    }
    r = requests.post(WALLET_URL, json=data, headers=HEADERS)
    result_dict = r.json()
    return result_dict['result']['commit'], result_dict['result']['reveal']

# Commit a new entry to the chain
def commit_entry(ec_address, chainid, content, state):
    commit,reveal = _get_commit_entry(ec_address, chainid, content, state)
    r = requests.post(FACTOM_URL, json=commit, headers=HEADERS)
    time.sleep(SLEEP)
    r = requests.post(FACTOM_URL, json=reveal, headers=HEADERS)
    result_dict = r.json()
    return result_dict['result']

# Helper for commit_entry to get commit-entry and reveal-entry API calls
def _get_commit_entry(ec_address, chainid, content, state):
    data = {
        "id": 0,
        "jsonrpc": "2.0",
        "method": "compose-entry",
        "params": {
            "ecpub": ec_address,
            "entry": {
                "content": _hex(content),
                "chainid": chainid,
                "extids": [
                    _hex(state)
                ]
            }
        }
    }
    r = requests.post(WALLET_URL, json=data, headers=HEADERS)
    result_dict = r.json()
    return result_dict['result']['commit'], result_dict['result']['reveal']

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
    r = requests.post(FACTOM_URL, json=data, headers=HEADERS)
    result_dict = r.json()
    return result_dict['result']

# String to hex. Source: https://stackoverflow.com/a/12214880
def _hex(s):
    return "".join("{:02x}".format(ord(c)) for c in s)
