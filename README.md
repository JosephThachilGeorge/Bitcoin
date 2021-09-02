# Bitcoin

Nodes Json 


{
    "nodes" : ["http://127.0.0.1:1001",
               "http://127.0.0.1:1002",
               "http://127.0.0.1:1003"]
}


 Nodes Json



Transaction Json 

Adding Transactions

To add a transaction, copy the content from transaction.json and POST it in JSON format to http://127.0.0.1:1001/add_transaction in Postman:


transaction Json 


How to change Blockchain into Cryptocurrency?

Below instructions need to follow:

Let see first how to add transaction 

self.transactions = [] transaction to be created before 

self.create_block Function 

Then ; add_transaction(self, sender, receiver, amount) 


Let see now how to create Consensus

self.nodes = set()    this is for init method

add_node(self, address)   add node method for adding a new node

replace_chain(self)   replace chain with long one 


How to decentralize the Blockchain and how to apply consensus and transaction?

Below instructions need to follow:

In this sample coin, there are three nodes. They utilize the addresses and ports listed below (Flask):

Node 1: http://127.0.0.1:1001/
Node 2: http://127.0.0.1:1002/
Node 3: http://127.0.0.1:1003/
To decentralize the bitcoin network, mine blocks, send transactions, and apply consensus, copies of the code (bitcoin.py) have been created:

Node 1: bitcoin_node_1_1001.py
Node 2: bitcoin_node_2_1002.py
Node 3: bitcoin_node_3_1003.py
 
Postman Request 
Once the application is running on Flask, Postman requests are used to query the blockchain, create transactions, and apply consensus. In this case, port 1001 was utilized (Node 1).
GET
Get Chain: http://127.0.0.1:1001/get_chain
Mine Block: http://127.0.0.1:1001/mine_block
Replace Chain: http://127.0.0.1:1001/replace_chain
POST
Add Transaction: http://127.0.0.1:1001/add_transaction
Connect Node: http://127.0.0.1:1001/connect_node







