import random
import secrets
import json
import requests
from time import time
from hashlib import sha256

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        print("block string: " + block_string)
        return sha256(block_string.encode()).hexdigest()

    def proof_of_work(self, nonce, difficulty): # difficulty is the no of beginning zeros required
        computed_hash = self.compute_hash()
        print(str(self.nonce) + " " + computed_hash)
        while not computed_hash.startswith("0" * difficulty): 
            self.nonce += 1
            computed_hash = self.compute_hash()
            print(str(self.nonce) + " " + computed_hash)
        return computed_hash

    def block_valid(self, difficulty, hash2check):
        return (hash2check.startswith("0" * difficulty) and hash2check == self.compute_hash())

class Blockchain:
    no_blockchains = 0

    def __init__(self):
        self.nodes = []
        self.accts = []
        self.chain = []
        self.unconfirmed_transactions = []
        self.account_bytes = 8
        Blockchain.no_blockchains += 1

    def create_genesis_block(self):
        genesis_block = Block(0, [], time(), "0", 0)
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def add_nodes(self, count):
        if count > 10: count = 10
        if count == 0: print(T_RED + "0 node added.", T_DEFAULT)
        else:
            for x in range(count):
                while True:
                    new_node = "127.0.0.1:" + str(random.randint(6000,7000))
                    if new_node in self.nodes: continue
                    else: 
                        self.nodes.append(new_node)
                        break
            #print(T_RED + str(count) + " nodes added:", T_DEFAULT)
            print(self.nodes)
            
    def new_acct(self, acct_type):
        acct = {
            "number": secrets.token_hex(self.account_bytes),
            "type": acct_type
        }
        return acct

    def add_accts(self, count):
        acct_no_list = []
        for x in range(len(self.accts)):
            acct_no_list.append(self.accts[x]['number'])     
        # print(json.dumps(acct_no_list))  
        if count > 10: count = 10
        if count == 0: print(T_RED + "0 account .", T_DEFAULT)        
        else:
            for y in range(count):
                while True:
                    new_acct_no = self.new_acct(acct_type="normal")
                    if new_acct_no['number'] in acct_no_list: continue
                    else: break
                acct_no_list.append(new_acct_no['number'])
                self.accts.append(new_acct_no)
        #    print(json.dumps(acct_no_list))    
            print(json.dumps(self.accts, indent=1))        

    def new_tx(self, node, sender, receiver, amount, mining_fee=0, priority=0, confirmed=0):
        tx = {
            "node": node,
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "mining_fee": mining_fee,
            "priority": priority,
            "confirmed": confirmed}
        return tx     

    def add_txs(self, count):
        if len(self.nodes) > 0 and len(self.accts) > 0:
            if count > 10: count = 10
            if count == 0: print(T_RED + "0 transaction added.", T_DEFAULT)
            else:
                for x in range(count):
                    node = self.nodes[random.randint(0,len(self.nodes)-1)]
                    sender = self.accts[random.randint(0,len(self.accts)-1)]["number"]
                    while True:                    
                        receiver = self.accts[random.randint(0,len(self.accts)-1)]["number"]
                        if receiver != sender: break
                    amount = random.randint(1,999)
                    new_transaction = self.new_tx(node, sender, receiver, amount, 0, 0, 0)
                    self.unconfirmed_transactions.append(new_transaction)
                    print(json.dumps(self.unconfirmed_transactions[-1]))
        else:
            print("Please first add nodes and accounts before generating transactions.\n")

    def mine(self):
        last_tx = len(self.unconfirmed_transactions)-1
        if last_tx > 0:
            new_block = Block(len(self.chain), self.unconfirmed_transactions, time(), self.chain[-1].hash, 0)
            start_time = time()
            new_block_hash = new_block.proof_of_work(nonce=0, difficulty=1)
            print("Mining time (sec):" + str(time() - start_time))
            self.chain.append(new_block)
            # print("New block string: " + json.dumps(new_block.__dict__))
            self.chain[-1].hash = new_block_hash
            #print(json.dumps(self.chain[-1].__dict__, indent=1))
            self.unconfirmed_transactions = []
