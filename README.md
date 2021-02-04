# bc01_flask
## Basic Python blockchain on Flask

### ========= Fresh Docker install ===========
```
cd ~
cd docker
git clone https://github.com/usq0/bc01_flask.git
cd bc01_flask
docker build -t bc01_flask .
docker run -i -p 6666:5000 bc01_flask
```
Run additional servers on other ports:
```
docker run -d -p 6667:5000 bc01_flask
docker run -d -p 6668:5000 bc01_flask
```
Use telnet or nc to check if the servers are running:
```
telnet 127.0.0.1 6666
nc -vz 127.0.0.1 6666
```
### ========== Remove containers and image, then reinstall =============
```
docker container ls
docker container stop xxxxxxxxxxxx
docker container prune
docker image ls
docker image rm bc01_flask
rm -rf bc01_flask
git clone https://github.com/usq0/bc01_flask.git
cd bc01_flask
docker build -t bc01_flask .
docker run -d -p 6666:5000 bc01_flask
```

### =========== Test steps ===============

HTTP GET:
```
http://127.0.0.1:6666                       # welcome page
http://127.0.0.1:6666/init                  # initialise, create one blockchain, aand a few fake nodes, accounts, transactions
http://127.0.0.1:6666/add/nodes             # add one node
http://127.0.0.1:6666/add/accts             # add one account
http://127.0.0.1:6666/add/txs               # add one transaction (unconfirmed)
http://127.0.0.1:6666/show/chain            # show all blocks in chain
http://127.0.0.1:6666/show/block            # show the last block
http://127.0.0.1:6666/show/nodes            # show all nodes
http://127.0.0.1:6666/show/accts            # show all accounts
http://127.0.0.1:6666/show/txs              # show all unconfirmed transactions
http://127.0.0.1:6666/mine                  # mine one block from all unconfirmed transactions
http://127.0.0.1:6666/whoru                 # show server HTTP_HOST, type of node and uptime
http://127.0.0.1:6666/ip                    # show HTTP, and TCP/IP details of both client and server
```

HTTP POST:
```
http://127.0.0.1:6666/post/node             # POST a new node to server
http://127.0.0.1:6666/post/acct             # POST a new account to server
http://127.0.0.1:6666/post/tx               # POST a new transaction to server
```

To test the above three, use the following links to send "requests.post(url, json=payload)" to the above:
```
http://127.0.0.1:6666/test/environ
http://127.0.0.1:6666/test/post_node
http://127.0.0.1:6666/test/post_acct
http://127.0.0.1:6666/test/post_tx
```

To test using CURL or Postman:
```
curl -X POST -H "Content-Type: application/json" -d '{"node": "127.0.0.1:5000"}' "http://127.0.0.1:6666/post/node"
curl -X POST -H "Content-Type: application/json" -d '{"number": "d77d23a45b6f448ea6221eebb0e32010", "type": "normal"}' "http://127.0.0.1:6666/post/acct"
curl -X POST -H "Content-Type: application/json" -d '{"sender": "d77d23a45b6f448ea6221eebb0e32010", "recipient": "d88efc8b7871469098878115b6be4b74",  "amount": 2}' "http://127.0.0.1:6666/post/tx"
```

