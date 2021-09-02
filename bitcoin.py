import datetime
import hashlib
import json
from flask import Flask,jsonify,request
import requests
from uuid import uuid4
from urllib.parse import urlparse
# Creating a block chain
class Blockchain:
    def __init__(self):
        # our whole chain
        self.chain=[]
        # list of transactions
        self.transactions = []
        # genesis block
        self.create_block(proof= 1 , previous_hash='0')
        # nodes in the network should be unique
        self.nodes = set()
    """   
    This class is for method is for creating block with five fields
    index, timestamp, proof, previous_hash,transactions
    """
    def create_block(self, proof, previous_hash):
        block={'index' : len(self.chain) + 1,
                'timestamp' : str(datetime.datetime.now()),
                'proof' : proof,
                'previous_hash' : previous_hash,
                'transactions' : self.transactions}
        # empty the transactions after all are added to the block
        self.transactions = []
        self.chain.append(block)
        return block
    
    # Getting the old block
    def get_previous_block(self):
        return self.chain[-1]
    
# We have a proof of work for mining the block.

# The goal is to have four leading zeros in the resultant hash.

    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False
        
        # create a hash and look if new_proof**2 - previous_proof**2 has leading 4 0s else increment the proof and check
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4]=='0000':
                check_proof =  True
            else:
                new_proof +=1
        return new_proof
            
# Hashing 
# json. dumps() accepts a json object as input and returns a string.
# The hex() function returns a string after converting the string to bytes.
    def hash(self,block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    # Checking if a block is valid or not
    def is_chain_valid(self, block):
        previous_block = self.chain[0]
        block_index=1
        while block_index < len(self.chain):
            block = self.chain[block_index]
            
            # Check if the previous hash in the current block differs from the preceding block's original hash.
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            # Check if the resultant hash of the proof**2 - previous_proof**2 does not have 4 leading 0s
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] !='0000':
                return False
            
            # update the block and increase the index
            previous_block=block
            block_index +=1
        return True

    # add transactions
    # We'll send it to Postman in json format as a sample request.
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender' : sender,
                           'receiver' : receiver,
                           'amount' : amount})
        previous_block = self.get_previous_block()
        # return the index of the current block (+1 for genesis block)
        return previous_block['index'] + 1
    
    # adding the node
    def add_node(self,address):
        # parsed_url = urlparse('http://127.0.0.1:1000/')
        # parsed_url.netloc - '127.0.0.1:1000'
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    # replacing the chain with the longest chain
    def replace_chain(self):
        # taking all of our nodes
        network = self.nodes
        longest_chain = None
        # max_length is set to the current length
        max_length = len(self.chain)
        # go through all of the nodes and see all of their chains
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            # if chain is valid
            if response.status_code == 200:
                # get its length and the chain
                length = response.json()['length']
                chain = response.json()['chain']
                # if it has the length greater than the current length update the max_length and the longest chain
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        # if longest_chain is set chain the chain to the longest_chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
    
# Creating a web app
app = Flask(__name__)


# Creating a port 1000 address for the node.
# uuid4() generates a globally unique identifier at random (UUID - generated using synchronization methods that ensure no two processes can obtain the same UUID)
node_address = str(uuid4()).replace('-', '')

# Putting together a blockchain
blockchain=Blockchain()

# Mining a block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    """
We'll use the previous block's proof to compute the new proof and build the current block using that proof and the prior hash.
    """ 
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    # We may award the bcoin if we mine a block. The miner who receives the block can be chosen.
    blockchain.add_transaction(sender = node_address, receiver = 'Bharathi', amount = 1)
    block = blockchain.create_block(proof, previous_hash)
    
    # Return the response
    response = {'message' : 'You ve just mined a block, congrats!',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash'],
                'transactions' : block['transactions']}
    # With an application/json mimetype, return a JSON representation of the supplied parameters (Multipurpose Internet Mail Extensions or MIME type).
    return jsonify(response), 200
    
# Getting the blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    # Return the response
    response = {'chain' : blockchain.chain,
                'length' : len(blockchain.chain)}
    return jsonify(response), 200
    
# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'Everything is fine. The Blockchain is correct..'}
    else:
        response = {'message': 'Weve got an issue. The Blockchain isnt trustworthy..'}
    return jsonify(response), 200

# Adding a new transaction to the blockchain
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    # We're sending the transactions to Postman in json format, thus we'll get them back in json format.
    json = request.get_json()
    # checking if it contains all of the keys
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transactions are missing', 400
    # We will add the transaction and return the answer as added if it has all of the components.
    index = blockchain.add_transaction(json['sender'],json['receiver'],json['amount'])
    response = {'message' : fThis transaction will be added to the Block {index}'}
    return jsonify(response), 201

# Our blockchain is becoming more decentralized.

#Connecting new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    # connecting all of the others nodes manually 
    json = request.get_json()
    nodes = json.get('nodes')
    # return none if node field is null
    if nodes is None:
        return 'No node', 400
# We'll manually add the nodes. This is repeated for each node.
# Because our nodes are a set, it will only include unique values if done separately for each node.
    for node in nodes:
        blockchain.add_node(node)
    # show the nodes and mark the answer as all connected
    response = {'message' : 'All of the nodes are now linked together. The node has now been added to the Bitcoin blockchain.',
                'total_nodes' : list(blockchain.nodes)}
    # http 201 created
    return jsonify(response), 201

# Replacing the chain by the longest chain
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    # If any chain is longer, the longest chain will be displayed instead, otherwise the same chain will be displayed.
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'Because the nodes are different, the longest chain is used to replace the chain..',
                    'new_chain' : blockchain.chain}
    else:
        response = {'message': 'Everything is fine. The chain is the most extensive.',
                    'new_chain' : blockchain.chain}
    return jsonify(response), 200

# Running the app on the port
app.run(host = '0.0.0.0', port = 1001)
