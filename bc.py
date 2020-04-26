from bccls00 import Blockchain
from bccls00 import Block
from urllib.parse import urlparse
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

@app.route('/')
def welcome():
    return 'Welcome to USQ blockchain!!'

@app.route('/init')
def init():
    if len(bc.chain) == 0:
        bc.create_genesis_block()
        bc.add_nodes(5)
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

@app.route('/register/node', methods=['GET'])
def register_node():
    netloc = parsed_url.netloc
    return netloc, 200

@app.route('/ip', methods=['GET'])
def httpconnection():
    print(request.environ)
    return jsonify(
        {'URL': request.url},
        {'client ip': request.remote_addr},
        {'client port': request.environ['REMOTE_PORT']},
        {'HTTP host': request.environ['HTTP_HOST']},
        {'server name': request.environ['SERVER_NAME']},
        {'server port': request.environ['SERVER_PORT']}
        ), 200
    return request.environ, 200

@app.route('/test', methods=['POST', 'GET'])
def test():
    print(request.environ)
    return jsonify(
        {'URL': request.url},
        {'client ip': request.remote_addr},
        {'client port': request.environ['REMOTE_PORT']},
        {'HTTP host': request.environ['HTTP_HOST']},
        {'server name': request.environ['SERVER_NAME']},
        {'server port': request.environ['SERVER_PORT']}
        ), 200
    return request.environ, 200

# Main program
bc = Blockchain()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)