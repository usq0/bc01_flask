from bccls00 import Blockchain
from bccls00 import Block
from urllib.parse import urlparse
from flask import Flask, jsonify, request
import time
import datetime
import json
import requests
import ast
import random

app = Flask(__name__)
app.debug = False # Flask debug mode off

@app.route('/')
def welcome():
    return 'Welcome to USQ blockchain!!'

@app.route('/init')
def init():
    if len(bc.chain) == 0:
        bc.create_genesis_block()
        bc.add_nodes(5)
        bc.nodes.append(request.environ['HTTP_HOST'])
        bc.add_accts(5)
        bc.add_txs(3)
        bc.mine()
        bc.add_txs(3)
        return "Blockchain initialised."
    else:
        return "Already initialised."

@app.route('/add/<entity>', methods=['GET'])
def add(entity):
    if entity == 'nodes':
        bc.add_nodes(1)
        return jsonify(bc.nodes), 200
    elif entity == 'accts':
        bc.add_accts(1)
        return jsonify(bc.accts), 200
    elif entity == 'txs':
        bc.add_txs(1)
        return jsonify(bc.unconfirmed_transactions), 200
    else:
        return "Invalid entity to add."

@app.route('/post/<entity>', methods=['POST'])
def post1(entity):
    if entity == 'node':
        data1 = request.get_json()
        # print('data1:', data1, data1['node'])
        if data1['node'] is None:
            return "Error: Please submit a valid node in JSON.", 400
        else:
            if data1['node'] in bc.nodes: # node already exists in bc.nodes
                res = {
                    'message': 'Node already exists.',
                    'nodes': list(bc.nodes)
                }
                return jsonify(res), 200
            else:
                bc.nodes.append(data1['node'])
                res = {
                    'message': 'New node added',
                    'new node': data1['node'],
                    'nodes': list(bc.nodes)
                }
                return jsonify(res), 201

    elif entity == 'acct':
        data1 = request.get_json()
        # print('data1:', data1['number'], data1['type'])
        if (data1['number'] is None) or (data1['type'] is None):
            return "Error: Missing account number or type in JSON.", 400      
        else:
            bc.accts.append(data1)
            res = {
                'message': 'New account added',
                'new account': data1,
                'accounts': list(bc.accts)
            }
            return jsonify(res), 201            

    elif entity == 'tx':
        data1 = request.get_json()
        if (data1['amount'] is None) or (data1['sender'] is None) or (data1['receiver'] is None):
            return "Error: Missing sender/receiver/amount in JSON.", 400      
        else:
            node = bc.nodes[random.randint(0,len(bc.nodes)-1)]
            new_transaction = bc.new_tx(node, data1['sender'], data1['receiver'], data1['amount'],0,0,0)
            bc.unconfirmed_transactions.append(new_transaction)
        res = {
                'message': 'New transaction added',
                'new transaction': data1,
                'transactions': list(bc.unconfirmed_transactions)
            }
        return jsonify(res), 201 
    else:
        return "Invalid entity to add."


@app.route('/show/<entity>', methods=['GET'])
def show(entity):
    if entity == 'chain':
        response = []
        if len(bc.chain) <= 10: # show all blocks in chain if less than 10
            for x in range(len(bc.chain)):
                response.append(bc.chain[x].__dict__)
        else:
            for x in range(len(bc.chain)-10, len(bc.chain)): # show the last 10 blocks
                response.append(bc.chain[x].__dict__)
        return jsonify(response), 200        
    elif entity == 'block': # show last block
        response = {}
        if len(bc.chain) > 0:
            response = bc.chain[-1].__dict__
        return jsonify(response), 200
    elif entity == 'nodes':
        response = bc.nodes
        return jsonify(response), 200
    elif entity == 'accts':
        response = jsonify(bc.accts)
        return response, 200
    elif entity == 'txs':
        response = bc.unconfirmed_transactions
        return jsonify(response), 200
    else:
        return "Invalid entity to show."

@app.route('/mine', methods=['GET'])
def mine():
    if len(bc.unconfirmed_transactions) > 0:
        bc.mine()
        response = bc.chain[-1].__dict__
        return jsonify(response), 200
    else:
        return "No unconfirmed transaction to mine."

@app.route('/whoru', methods=['GET'])
def who_am_i():
    response = {
        'ip': request.environ['HTTP_HOST'],
        'type': 'full_node',
        'status': 'up for ' + str(datetime.timedelta(seconds=time.time()-host_start_time))
    }
    return jsonify(response), 200

@app.route('/status/nodes', methods=['GET'])
def nodes_status():
    result = []
    for x in range(len(bc.nodes)):
        try:
            print('Trying http://'+str(bc.nodes[x])+'/whoru')
            res = requests.get('http://'+str(bc.nodes[x])+'/whoru')
            result.append(ast.literal_eval(res.text))
        except requests.exceptions.RequestException:
            res = {
                'ip':bc.nodes[x],
                'status':'Unknown',
                'type':'Unknown'
            }
            print(type(res), res)
            result.append(res)
    return jsonify(result), 200

@app.route('/ip', methods=['GET'])
def httpconnection():
    # print(request.environ)
    return jsonify(
        {'URL': request.url},
        {'client ip': request.remote_addr},
        {'client port': request.environ['REMOTE_PORT']},
        {'HTTP host': request.environ['HTTP_HOST']},
        {'server name': request.environ['SERVER_NAME']},
        {'server port': request.environ['SERVER_PORT']}
        ), 200

@app.route('/test/<sth>', methods=['POST', 'GET'])
def test(sth):
    if sth == "environ":
        return str(request.environ), 200
    elif sth == "post_node": # curl -X POST -H "Content-Type: application/json" -d '{"node": "127.0.0.1:7777"}' "http://127.0.0.1:5000/post/node"
        url='http://127.0.0.1:5000/post/node'
        nodeip = '127.0.0.1:'+str(random.randint(7000,7999))
        payload = {'node':nodeip}
        r1 = requests.post(url, json=payload)
        return jsonify(ast.literal_eval(r1.text)), 200
    elif sth == "post_acct": # curl -X POST -H "Content-Type: application/json" -d '{"number": "d77d23a45b6f448ea6221eebb0e32010", "type": "normal"}' "http://127.0.0.1:5000/post/acct"
        payload = bc.new_acct("normal")
        url='http://127.0.0.1:5000/post/acct'
        r1 = requests.post(url, json=payload)
        return jsonify(ast.literal_eval(r1.text)), 200
    elif sth == "post_tx": # curl -X POST -H "Content-Type: application/json" -d '{"sender": "d77d23a45b6f448ea6221eebb0e32010", "recipient": "d88efc8b7871469098878115b6be4b74",  "amount": 2}' "http://127.0.0.1:5000/post/tx"
        sender = bc.accts[random.randint(0,len(bc.accts)-1)]["number"]
        receiver = bc.accts[random.randint(0,len(bc.accts)-1)]["number"]
        amount = random.randint(1,999)
        payload = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount}
        url='http://127.0.0.1:5000/post/tx'
        r1 = requests.post(url, json=payload)
        return jsonify(ast.literal_eval(r1.text)), 200

# Main program
bc = Blockchain()
host_start_time = time.time()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)







