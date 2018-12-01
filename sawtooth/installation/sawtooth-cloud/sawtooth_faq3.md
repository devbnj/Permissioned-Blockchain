# Sawtooth REST API

### What's the difference between the ``sawtooth-rest-api --bind`` and ``--connect`` options?
* ``sawtooth-rest-api --bind`` (``-B``) specifies where your rest-api would listen. The default is http://localhost:8008
* ``sawtooth-rest-api --connect`` (``-C``) specifies where your rest-api can reach to the validator. The default is http://localhost:4004

### Is the REST API at TCP port 8080 or 8008?
* TCP Port 8008. It was 8080 before the 1.0 release and old examples and diagrams may use the old port number.

### What REST API commands are available?
* Use localhost to access the REST API from the Validator Docker container or from where the Validator is running.
* For example, to get state history (equivalent to ``sawtooth state list``) type:

```
    curl http://localhost:8008/state
```

* From the Client Docker container, access from rest-api. For example:

```
    curl http://rest-api:8008/state
```

* These are the supported REST API commands:
* POST /batches - Submit a protobuf-formatted batch list to the validator
* GET /batches - Fetch a paginated list of batches from the validator
* GET /batches/{batch_id} - Fetch the specified batch
* GET /batch_statuses - Fetch the committed statuses for a set of batches
* POST /batch_statuses - Same as GET /batch_statuses except can be used for > 15 IDs
* GET /state - Fetch a paginated list of leaves for the current state, or relative to a particular head block
* GET /state/{address} - Fetch a particular leaf from the current state
* GET /blocks - Fetch a paginated list of blocks from the validator
* GET /blocks/{block_id} - Fetch the specified block
* GET /transactions - Fetch a paginated list of transactions from the validator.
* GET /transactions/{transaction_id} - Fetch the specified transaction
* GET /receipts?id={transaction_ids} - Fetch receipts for 1 or more transactions
* POST /receipts - Same as GET /receipts except can be used for > 15 IDs
* GET /peers - Fetch a list of current peered validators

* For more information, see the Sawtooth REST API Reference at
https://sawtooth.hyperledger.org/docs/core/releases/latest/rest_api.html

### What is a transaction receipt?
* Transaction receipts are transaction execution information that is not stored in state, such as how the transaction changed state, transaction family-specific data, transaction-related events, and if the transaction was valid.
* The transaction family-specific receipt data is usually empty, but can be added by the TP with ``context.add_receipt_data()``
* To access transaction receipts, use the REST API.
* For more information, see
https://sawtooth.hyperledger.org/docs/core/releases/latest/architecture/events_and_transactions_receipts.html#transaction-receipts

### How do I retrieve a transaction receipt?
* Use the REST API. Here's a sample request (The ID is the transaction ID, listed with `sawtooth transaction list`):
``wget http://localhost:8008/receipts?id=YourTransactionIDsHere``
* Replace ``YourTransactionIDsHere`` with 1 or more comma-separated 128 hex character transaction IDs. Change `localhost` to `rest-api` for Docker. The response is several lines of JSON format output. For example, 
https://gist.github.com/danintel/0f878141c60bb566237e8db11226aa4e .
For more than 15 IDs, use ``POST /receipts`` .
For Receipts REST API details, see ``receipts`` at
https://sawtooth.hyperledger.org/docs/core/releases/latest/rest_api/endpoint_specs.html


### What does this error mean: ``[... DEBUG route_handlers] Received CLIENT_STATE_GET_RESPONSE response from validator with status NO_RESOURCE``?
-----------------------
* It means the transaction processor for this transaction is not running.

### What does this REST API error mean: ``The submitted BatchList was rejected by the validator. It was poorly formed, or has an invalid signature``
* Most likey you are not putting the transaction into a batch or the batch in a batchlist for posting to the REST API. This is required, even for a single transaction.

### I am getting this error: ``Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource at http://localhost:8008/batches?wait. (Reason: CORS header 'Access-Control-Allow-Origin' missing).``
* The Sawtooth REST API doesn't support CORS. To allow cross-origin access to the Sawtooth API, put it behind a proxy.

### What is the back pressure test?
* Back pressure is a flow-control technique to help prevent DoS attacks.
* It results in a ``Status.QUEUE_FULL`` client batch submit response or a 429 "Too Many Requests" REST API error.
* If the validator is overwhelmed it will stop accepting new batches until it can handle more work. The number of batches that validator can accept is based on a multiplier,  QUEUE_MULTIPLIER (currently 10, formerly 2), times a rolling average of the number of published batches.

# Sawtooth Using Docker


### Can I run Sawtooth without Docker?
* Yes.

### How can I run ``docker`` or ``docker-compose`` without prefixing it with ``sudo``?
* Sometimes, adding your login to group ``docker`` is recommended, such as with command: ``sudo usermod -aG docker $USER`` . However, this gives ``$USER`` root-equivalent permissions. A better alternate is to define an alias for docker and docker-compose and add to your ~/.bashrc file:

```
    alias docker='sudo docker'
    alias docker-compose='sudo docker-compose'
```

* For details, see https://docs.docker.com/install/linux/linux-postinstall/#manage-docker-as-a-non-root-user

### I get this error running ``docker-compose -f sawtooth-default.yaml up`` : ``Error: files exist, rerun with --force to overwrite existing files``
* This occurs when docker was not halted cleanly. Run the following first:

```
    sudo docker-compose -f sawtooth-default.yaml down
```
* Then this:

```
    sudo docker-compose -f sawtooth-default.yaml up
```
* An alternate solution is to force it to ignore the existing files:

```
    docker-compose -f docker/compose/sawtooth-default.yaml up --force
```

### I get this error running ``docker-compose -f sawtooth-default.yaml up`` : ``ERROR: Couldn't connect to Docker daemon at http+docker://localhost - is it running?``
* If it's at a non-standard location, specify the URL with the DOCKER_HOST environment variable.
* You may not have enough permission to run. Try prefixing with sudo: ``sudo docker-compose ...``
* To determine if sure docker is running and to start Docker, type:
```
    service docker status
    sudo service docker start
```

### I get this error running ``docker run hello-world`` :  ``Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get http://%2Fvar%2Frun%2Fdocker.sock/v1.37/containers/json: dial unix /var/run/docker.sock: connect: permission denied``
* Try running with sudo. For example: sudo docker run hello-world.
* Here's a few aliases you can add to your ``~/.bashrc`` file:

```
    alias docker='sudo docker'
    alias docker-compose='sudo docker-compose'
```

### I get this error running ``docker run hello-world`` : ``docker: Error response from daemon: Get https://registry-1.docker.io/v2/: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers).``
* If it worked before, first try restarting docker:

```
   sudo service docker start; sudo service docker stop
```

* If you are behind a network firewall, it is usually a proxy problem. Proxy configurations are firewall-dependent, but this might serve as a pattern:

```
    # /etc/default/docker
    export http_proxy="http://proxy.mycompany.com:911/"
    export https_proxy="https://proxy.mycompany.com:912/"
    export no_proxy=".mycompany.com,10.0.0.0/8,192.168.0.0/16,localhost,127.0.0.0/8"
```

```
    # /etc/systemd/system/docker.service.d/override.conf
    Environment="HTTP_PROXY=http://proxy.mycompany.com:911/"
    Environment="HTTPS_PROXY=http://proxy.mycompany.com:912/"
    Environment="FTP_PROXY=http://proxy.mycompany.com:911/"
    Environment="NO_PROXY=.mycompany.com,10.0.0.0/8,192.168.0.0/16,localhost,127.0.0.0/8"
```

### I get this error: ``ERROR: repository . . . not found: does not exist or no pull access``
* Also a proxy problem--see the answer above.

### I get this error: `` ERROR: Service . . . failed to build: Get . . . net/http: request canceled while waiting for connection
* Also a proxy problem--see the answer above.

### I get this error running docker-compose: ``ERROR: for validator  Cannot create container for service validator: Conflict. The container name "/validator" is already in use by container ...``
* The container already exists. You need to remove or rename it. To remove:

```
    sudo docker ps -a # list container IDs
    sudo docker stop [container ID]
    sudo docker rm [container ID]
```

### How do I display the logs for a Docker container?
* Use the ``sudo docker logs`` command followed by the container name.
The container name may be found with the ``sudo docker ps`` command.
For example: ``sudo docker logs validator`` display the log for the container named ``validator`` .

### I get this error running docker-compose: ``ERROR: Version in "./docker-compose.yaml" is unsupported.``
* You may be running an old version of Docker, perhaps from your Linux package manager. Instead, install Docker from docker.com. Sawtooth requires Docker Engine 17.03.0-ce or better. For Docker CE for Ubuntu, use https://docs.docker.com/install/linux/docker-ce/ubuntu/
* Here's a sample script that installs Docker CE on Ubuntu:
https://gist.github.com/askmish/76e348e34d93fc22926d7d9379a0fd08

### If I run ``docker`` or ``docker-compose`` it hangs and does nothing.
* The docker daemons may not be running. To check, run:

```
     $ ps -ef | grep dockerd
```

* To start, run:

```
    $ sudo systemctl restart docker.service
```

### How do I manually start and stop docker on Linux?
```
    $ sudo service docker start
    $ service docker status
    $ sudo service docker stop
```

### How do I enable and disable automatic start of docker on boot on Linux?
```
    $ sudo systemctl enable docker
    $ systemctl status docker
    $ sudo systemctl disable docker
```

### Can I connect a client to the REST API running in a Docker container?
* Yes. The ``docker-compose.yaml`` needs the following lines for the REST container:

```
    expose:
      - 8008
    ports:
      - '8008:8008'
```
* Then connect your client to processor to port ``http://localhost:4040``
This might be a command line option for the client
(for example, ``intkey --url http://localhost:4040``).
Otherwise, you need to modify the source if the REST API URL is hard-coded
for your client.


### Can I connect a transaction processor to the validator running in a Docker container?
* Yes. The ``docker-compose.yaml`` needs the following lines for the validator container (which maps Docker container TCP port 4004 to external port 4040):

```
    expose:
      - 4004
    ports:
      - '4040:4004'
```

* Then connect your transaction processor to port ``tcp://localhost:4040``
* If the port is mapped to 4004 (that is, not mapped to 4040), use ``tcp://localhost:4040``
The port might be a command line option for the TP.
(for example, ``intkey-tp-python -v tcp://localhost:4040`` ).
Otherwise, you need to modify the source if the validator port is hard-coded
for your TP.

### I get ``You cannot remove a running container`` error removing docker containers
* Before running ``docker rm $(docker ps -aq)``, first stop the running containers with
``sudo docker stop $(docker ps -q)``

### How do I run Sawtooth with Kubernetes?
* Kubernetes requires VirtualBox or some other virtual machine software.
Documentation on using Kubernetes with Minikube for Sawtooth on Linux or Mac hosts is available here:
https://sawtooth.hyperledger.org/docs/core/nightly/master/app_developers_guide/kubernetes.html
https://sawtooth.hyperledger.org/docs/core/nightly/master/app_developers_guide/creating_sawtooth_network.html#kubernetes-start-a-multiple-node-sawtooth-network

### Can Docker run inside a virtual machine?
* Yes. For example, I run Docker with Sawtooth containers on a VirtualBox virtual machine instance on a Windows 10 host.

### How do I persist data on Docker containers?
* You add an external volume. You make a directory for your volume and add it using ``volumes:`` in your Docker .yaml file. For a Sawtooth-specific tutorial, see this blog: http://goshtastic.blogspot.com/2018/04/making-new-transaction-family-on.html
Also see the Docker storage documentation at https://docs.docker.com/storage/
* If you do not ``down`` the container or reboot the Docker host, the container will not be destroyed.
* For a list of directories used by Sawtooth, see https://github.com/danintel/sawtooth-faq/blob/master/validator.rst#what-files-does-sawtooth-use
It is best to set `$SAWTOOTH_HOME` so all the configuration and data is under one root directory.

### I get this error running Docker: ``ERROR: manifest for hyperledger/sawtooth-validator:1.1 not found``
* You are following instructions for the unreleased ``nightly`` build, Sawtooth 1.1. There are no Docker images for the unreleased Sawtooth 1.1 release. Instead use the ``latest`` build documentation at https://sawtooth.hyperledger.org/docs/core/releases/latest/app_developers_guide.html

# Sawtooth Glossary


##### See Also
* Sawtooth Glossary
    https://sawtooth.hyperledger.org/docs/core/nightly/master/glossary.html
* Sawtooth Architecture Definitions
    https://sawtooth.hyperledger.org/docs/core/releases/latest/architecture/permissioning_requirement.html#definitions
* PoET Definitions
    https://sawtooth.hyperledger.org/docs/core/releases/latest/architecture/poet.html#definitions


### Glossary
* Address (aka State Address)
    For Sawtooth, each radix address (or Node ID) into a Merkle Trie is 70 hex characters (35 bytes). The first 6 characters, the prefix, encode the name space (of the TF) and the remaining bytes are implementation-dependent. The prefix is either the first 6 characters of the SHA-512 hash of the namespace, or a hex word for base name spaces. See the list of TF prefixes in the Appendix
* AVR
    Attestation Verification Report. Response body signature, signed with the IAS Report Key
* back pressure
    Flow-control technique to help prevent denial of service attacks. Sawtooth uses this to reject unusually-frequent submissions from a client
* Batch
    A set of transactions that must be made together (atomic commit) to maintain state consistency. Batches are unique to Sawtooth
* Block
    A set of records of permanent transactions; these blocks are linked into a blockchain. A block is similar to a page in a ledger book, where the ledger book is a blockchain
* Block 0 or Block Zero
    See Genesis Block
* Blockchain
    A single-link list of blocks. The blockchain is immutable, distributed, and cryptographically-secured. Located at ``/var/lib/sawtooth/block-00.lmdb``
* Block ID
    128 hex character ID (64 bytes) identifying a block in a blockchain
* BFT
    Byzantine Fault Tolerance. Consensus is possible with malicious actors (Byzantine Generals Problem). BFT is stronger than CFT and uses voting
* C
    Sign-up delay; number of blocks a validator has to wait before participating in elections (when using PoET)
* C Test
    A node must wait C blocks after admission before its blocks will be accepted. This is to prevent trying to game identities and some obscure corner scenarios
* CCL
    Coordination and Commit Log (used by PDO)
* CFT
    Crash Fault Tolerance. Consensus possible even with failed components
* Client
    Any program that creates a transaction; interfaces with the validator using REST. Does not have to be a web-based app
* Consensus algorithm
    Method to decide what block to add next to a blockchain
* Context
    The snapshot of the global state. Specifically, the subset of the state required for the transaction, based on the input and output addresses specified in the transaction.
* Classical Consensus
    Uses an agreement or voting mechanism to select a leader (vs. Nakamoto-style consensus)
    E.g., PBFT and Raft
* Crypto
    Cryptography--encryption, authentication, and hashing. It does not mean blockchain or digital currency
* Dapps
    Ethereum Decentralized Applications. These are written in Solidity and are supported by Sawtooth Seth
* DAML
    Digital Asset Modeling Language. Codifies financial agreements.
* Distributed Ledger
    See Blockchain
* DLT
    Distributed Ledger Technology; Blockchain is a DLT
* Docker
    A light-weight OS-level VM technology which isolates processes into separate "containers"
* Duplicity
    A faulty node sending deceitful or inconsistent messages to other nodes
* CSV
    Comma separated values. E.g.: ``a,b,c,d``
* Curve25519
    An ECDH (Elliptic Curve Diffie-Hellman) key agreement protocol used by Sawtooth. Used by validators in ZMQ connections to exchange keys
* Data model
    Can be any format (CSV, protobufs, etc.)
* Deterministic
    Means consistent, or the same. For Sawtooth, serialization must be deterministic, meaning the encoding is always in the same order and always the same for the same data. This excludes timestamps and counters in your data. Many JSON libraries do not encode data deterministically
* EPID
    Enhanced Privacy ID. An anonymous credential system; used by PoET
* Enclave
    SGX-protected area of data and code to provide confidentiality and integrity even against privileged malware
* Endpoint
    The URL sent to the REST API. For example ``http://localhost:8008/state`` .
    Also refers to the validator connection URI.
    For example, ``tcp://localhost:4004`` .
    For more information, see
    https://sawtooth.hyperledger.org/docs/core/releases/latest/rest_api/endpoint_specs.html
* EVM
    Ethereum Virtual Machine. Executes machine-independent code for Ethereum. Supported by Seth on Sawtooth
* Fork
    When network nodes have two competing nodes at the head of a blockchain
* Genesis Block
    First block in the blockchain (block 0). Has initial on-chain settings, such as the consensus algorithm and configuration information
* Global State Agreement
    Verification of the global state (ledger) contents among peers. It is included in the Sawtooth consensus process
* Gossip
    A decentralized message broadcast mechanism that uses forwarding to random peers (Sawtooth Validator nodes)
* GS
    Global State or Ledger. For Sawtooth this is stored internally as a Merkle Tree
* Hyperledger
    "Hyperledger is an open source collaborative effort created to advance cross-industry blockchain technologies. It is a global collaboration, hosted by The Linux Foundation." See: https://www.hyperledger.org/
* IAS
    Intel Attestation Server. Used to authenticate PoET SGX keys; runs in public Internet at https://as.sgx.trustedservices.intel.com/
* In State
    See on-chain
* IntKey
    Integer key TP. Sample Sawtooth TP that implements set/increment/decrement/show operations
* Journal
    A group of Sawtooth Validator components that work together to handle batches and proposed blocks. This includes validating proposed blocks and publishing batches into blocks. See https://sawtooth.hyperledger.org/docs/core/nightly/master/architecture/journal.html
* k
    Claim limit, number of blocks a validator can publish before it must sign-up again (when using PoET). The default is k=50
* K Test
    The node can publish at most K blocks before its peers require it to recertify itself
* Ledger
    Key-value store whose values are agreed on by all nodes (validators) in the network
* Liveness
    A consensus algorithm property where the nodes eventually must agree on a value
* LMDB
    Lightning Memory-mapped Database are sparse random-access files in ``/var/lib/sawtooth`` . The Merkle Tree and Blockchain use LMDB
* Marshalling
    serialization of data
* Merkle Tree (or Trie)
    a radix search tree data structure with addressable nodes. Used to store state. Located at ``/var/lib/sawtooth/merkle-00.lmdb``
* n
    Nodes in a blockchain network
* Nakamoto-style Consensus
    Uses some sort of lottery-based mechanism, such as Proof of Work (vs. Classical Consensus) to win the right to commit a block.
     E.g., PoW or PoET.
* Node ID
    Address
* Node
    See Validator
* Nonce
    A one-time number; usually random, but must not predictably repeat (such as after reboot/restart)
* Off-chain
    Information stored externally to the blockchain
* On-chain
    Information stored internally in the blockchain
* One-say, all-adopt
    Strategy where only a single multicast round of messages reaches agreement
* Oracle
    An agent that finds and verifies real world occurrences and submits this information to a blockchain for use by smart contracts. Oracles are 3rd-party services.
* Payload
    Data processed by the TP and only the TP. Can be any format (CSV, protobufs, etc.) Data model is defined by TF. Payload is encoded using MIME's Base64 (``A-Za-z0-9+/``) + ``=`` for 0 mod 4 padding
* PBFT
    Practical Byzantine Fault Tolerance. A "classical" consensus algorithm that uses a state machine. Uses leader and block election. PBFT is a three-phase, network-intensive algorithm (n^2 messages), so is not scalable to large networks
* PDO
    Private Data Object. Blockchain objects that are kept private through encryption. See links to paper, code, and presentation at https://twitter.com/kellymolson/status/1019299515646406656
* Permissioned Blockchain (aka Private Blockchain)
    participants must ID themselves to a network (e.g., Hyperledger Sawtooth or Hyperledger Fabric)
* Permissioning
    For the validator, controls what nodes are allowed to connect.
    For the transaction processor, controls what transactions and batches are accepted, based on signing keys. See https://sawtooth.hyperledger.org/docs/core/nightly/master/architecture/permissioning_requirement.html
* Permissionless Blockchain (aka Public Blockchain)
    anyone can join network (e.g., Bitcoin, Ethereum)
* PoET
    Proof of Elapsed Time (optional Nakamoto-style consensus algorithm used for Sawtooth). PoET with SGX has BFT. PoET CFT has CFT. Not CPU-intensive as with PoW-style algorithms, although it still can fork and have stale blocks. See PoET specification at https://sawtooth.hyperledger.org/docs/core/releases/latest/architecture/poet.html
* PoET CFT
    PoET running without SGX, which has CFT
* PoET Simulator Mode
    Another name for PoET CFT
* PoW
    Proof of Work. Completing work (CPU-intensive Nakamoto-style consensus algorithm). Usually used in permissionless blockchains
* PoS
    Proof of Stake. Nakamoto-style consensus algorithm based on the most wealth or age (stake)
* Private Blockchain
    See Permissioned Blockchain
* Proposal
    proposed block from a validator to add to a blockchain
* Protobuf
    Serialization/data interchange library used by Sawtooth
* Pruning Queue
    Message broadcasting optimization that reduces broadcasting of all messages to all nodes
* Public Blockchain
    See Permissionless Blockchain
* r
    Rate, measurement of performance in transactions per second
* Raft
    Consensus algorithm that elects a leader for a term of arbitrary time. Leader replaced if it times-out. Raft is faster than PoET, but is not BFT (Raft is CFT). Also Raft does not fork.
* Remix
    A popular web-based IDE for Solidity
* Replica
    Another term for node or validator
* REST
    Representational State Transfer. Industry-standard web-based API. REST is available on a Sawtooth validator node through TCP port 8008. For more information, see the Sawtooth REST API Reference at https://sawtooth.hyperledger.org/docs/core/releases/latest/rest_api.html
* ST
    Sawtooth
* Sabre
    TF that implements on-chain smart contracts with the WebAssembly VM. For more information, see Sabre RFC at https://github.com/hyperledger/sawtooth-rfcs/blob/master/text/0007-wasm-smart-contracts.md
* Sawtooth
    Hyperledger Sawtooth is a modular enterprise blockchain platform for building, deploying, and running distributed ledgers
* Sawtooth Lake
    Sawtooth's original code name before Intel contributed Sawtooth to the Linux Foundation's Hyperledger consortium
* Seed Nodes or Seed Peers
    Initial hard-coded set of peers a node knows about. The list expands with the Gossip algorithm
* Solidity
    A contract-oriented programming language used to implement smart contracts. Compiles into Ethereum VM code and is supported by Seth
* Stale block
    A block proposed to be at the head of a blockchain, but lost to a competing block that became the head as decided by the consensus algorithm
* Static Nodes or Static Peers
    A hard-coded set of peers a node knows about, but may not change
* TEE
    Trusted Execution Environment. Secure area of a microprocessor that guarantees confidentiality and integrity of code and data loaded.  SGX is an example of a TEE
* TF
    Transaction Family. Consists of the Client, State, and TP.
    See https://www.hyperledger.org/blog/2017/06/22/whats-a-transaction-family
* TP
    Transaction Processor. Processes transactions for a specific TF. Runs on Validator. Similar to a Ethereum "smart contract" or Bitcoin "chain code"
* Transaction Receipt
    Off-chain store about information about transaction execution. Located at ``/var/lib/sawtooth/txn_receipts-00.lmdb``
* Truffle
    Popular Ethereum development environment
* TXN
    Transaction
* Safety
    A consensus algorithm property where the "honest" (non-Byzantine) nodes agree on the same value
* Sawtooth
    Permissioned blockchain platform for running distributed ledgers
* Seth
    Ethereum-compatible Sawtooth Transaction Processor. Supports running Ethereum Virtual Machine
* secp256k1
    An ECDSA (Elliptic Curve DSA) cryptographic algorithm used by Sawtooth with a 32-byte key. Used for Validator and TP. Bitcoin also uses this algorithm
* Serialization
    A scheme to encode data as a byte stream. For Sawtooth the serialization must be deterministic, meaning the encoding is always in the same order and always the same for the same data. Protobufs are often used in Sawtooth Serialization, but that is not a requirement. A simpler alternative, for example, is CSV
* SGX
    Intel Software Guard Extensions. Specialized hardware that provides enclaves with protected code and data. Used to implement PoET SGX
* State
    The current information for each Transaction Family. The global state is stored in a Merkle Tree. View local validator through http://localhost:8008/state
* State Address
    See Address
* Sybil Attacks
    Using forged identities in a blockchain network to subvert the reputation system. Was named after the book and movie
* Transaction
    A single entry in a the distributed ledger (blockchain). The contents are TF-dependent
* Transactor
    The Sawtooth client that creates a transaction, or the part that that communicates with the validator
* Validator
    Validates transactions and sends to the appropriate TP; proposes new blocks for block chain usually in a network of validator nodes
* VM
    Virtual Machine
* Wasm
    See WebAssembly
* WebAssembly
    A stack-based VM newly-implemented in major web browsers. It is well-suited for the purposes of smart contract execution due to its sandboxed design, growing popularity, and tool support. Sabre implements WebAssembly
* XO
    Example Sawtooth TP that implements the Tic-tac-toe game
* Z Test
    Test a block-claiming validator is not winning too frequently. It is a defense-in-depth mechanism
* ZMQ (aka 0MQ, ZeroMQ)
    Zero Message Queue. A message transport API available on Linux; used by Sawtooth Validator nodes
* ZKP
    Zero Knowledge Proof. One party proving they know a value *x* without conveying *x*
* zkSNARKS
    Zero Knowledge Succinct Non-interactive Arguments of Knowledge, which allow proof of correctness, given public and private input


# Appendix - Sawtooth Transaction Family Prefixes

### This is an unofficial list of some Transaction Family (TF) prefixes.
There is no central registry, most or all of these TFs are found on GitHub
( https://github.com/ especially https://github.com/hyperledger and
https://github.com/hyperledger-labs ).

* Sawtooth addresses are 70 hex characters.
* The prefix is either the first 6 characters of the SHA-512 hash of the namespace, or, for some base namespaces, a "hex word".
* The Sawtooth Validator registry is an outlier. It uses the SHA-256 hash (not SHA-512) and hashes "validator_registry" (not "sawtooth_validator_registry").
The remainder of the address is TF-specific and defined for each TF.
Listing of a TF does not imply endorsement.

* All data payloads are encoded in base64 after serializing.
Sawtooth headers are serialized with Protobuf.

* For base TF specifications, see
https://sawtooth.hyperledger.org/docs/core/releases/latest/transaction_family_specifications/

```
+---------------+-----------+--------+-----------------------------------------+
| TRANSACTION   | SERIAL-   |        |                                         |
| FAMILY NAME   | IZATION   | PREFIX | PREFIX ENCODING                         |
+===============+===========+========+=========================================+
| settings      | Protobuf  | 000000 | Validator settings.  Only required TF   |
+---------------+-----------+--------+-----------------------------------------+
| identity      | Protobuf  | 00001d | Validator Identity for TP/Validator keys|
+---------------+-----------+--------+-----------------------------------------+
| sawtooth      | Protobuf  | 6a4372 | PoET Validator Registry. Used by PoET   |
| _validator    |           |        | consensus to track other validators.    |
| _registry     |           |        | See note above about hash prefix .      |
+---------------+-----------+--------+-----------------------------------------+
| blockinfo     | Protobuf  | 00b10c | Validator Block Info.  Used for SETH    |
|               |           |        |                                         |
|               |           |        | 00b10c00 metadata namespace             |
|               |           |        | info about other namespaces             |
|               |           |        |                                         |
|               |           |        | 00b10c01 block info namespace           |
|               |           |        | historic block info                     |
|               |           |        |                                         |
|               |           |        | 00b10c0100....00<block # in hex>        |
|               |           |        | info on block at block #                |
+---------------+-----------+--------+-----------------------------------------+
| sabre         | Protobuf  | 00ec00 | WebAssembly VM: NamespaceRegistry       |
|               |           |        |                                         |
|               |           | 00ec01 | Wasm: ContractRegistry                  |
|               |           |        |                                         |
|               |           | 00ec02 | Wasm: Contracts                         |
+---------------+-----------+--------+-----------------------------------------+
| seth          | Protobuf  | a68b06 | SETH (Sawtooth Ethereum VM)             |
+---------------+-----------+--------+-----------------------------------------+
| pdo\_         | Protobuf  | aa2a93 | Private Data Objects (PDO)              |
| contract\_    |           |        | Contract Instance Registry              |
| instance\_    |           |        |                                         |
| registry      |           |        |                                         |
+---------------+-----------+--------+-----------------------------------------+
| pdo\_         | Protobuf  | 0b936f | Private Data Objects (PDO)              |
| contract\_    |           |        | Contract Enclave Registry               |
| enclave\_     |           |        |                                         |
| registry      |           |        |                                         |
+---------------+-----------+--------+-----------------------------------------+
| ccl\_         | Protobuf  | db13a2 | Private Data Objects (PDO)              |
| contract\_    |           |        | Coordination and Commit Log (CCL)       |
| contract\_    |           |        | Contract State Registry                 |
| state\_       |           |        |                                         |
| registry      |           |        |                                         |
+---------------+-----------+--------+-----------------------------------------+
|  **SOME EXAMPLE TFs**                                                        |
+---------------+-----------+--------+-----------------------------------------+
| battleship    | JSON      | 6e10df | Battleship example game                 |
+---------------+-----------+--------+-----------------------------------------+
| intkey        | CBOR      | 1cf126 | Integer Key. Full production example    |
+---------------+-----------+--------+-----------------------------------------+
| smallbank     | Protobuf  | 332514 | Small Bank example app                  |
+---------------+-----------+--------+-----------------------------------------+
| xo            | CSV-UTF8  | 5b7349 | Tic-tac-toe example game                |
+---------------+-----------+--------+-----------------------------------------+
| supply_chain  | Protobuf  | 3400de | Asset (Fish) Supply Chain example app   |
+---------------+-----------+--------+-----------------------------------------+
| marketplace   | Protobuf  | cd6744 | Marketplace example app                 |
+---------------+-----------+--------+-----------------------------------------+
| transfer\-    | JSON-UTF8 | 19d832 | Simple Tuna Supply Chain app.           |
| chain         |           |        | Used for edX LFS171x class              |
+---------------+-----------+--------+-----------------------------------------+
| simplewallet  | CSV-UTF8  | 7e2664 | Simple Wallet minimal example           |
+---------------+-----------+--------+-----------------------------------------+
| cookiejar     | CSV-UTF8  | a4d219 | Cookie Jar minimal example              |
+---------------+-----------+--------+-----------------------------------------+
| simple\_      | Protobuf  | 5d6af4 | Simple Supply example used for future   |
| supply        |           |        | edX LFS201 class                        |
+---------------+-----------+--------+-----------------------------------------+
| pirate-talk   | UTF8      | aaaaaa | Pirate Talk minimal example             |
+---------------+-----------+--------+-----------------------------------------+
| cookie-maker  | raw       | 1a5312 | Cookie Maker minimal example            |
+---------------+-----------+--------+-----------------------------------------+
|  **SOME THIRD-PARTY PRODUCTION TFs**                                         |
+---------------+-----------+--------+-----------------------------------------+
| rbac          | Protobuf  | 8563d0 | T-Mobile NEXT Identity Platform         |
+---------------+-----------+--------+-----------------------------------------+
| sawtoothekyc  | Protobuf  | dbf420 | Primechain Blockchain-eKYC bank records |
+---------------+-----------+--------+-----------------------------------------+
| pub_key       | Protobuf  | a23be1 | REMME REMChain                          |
+---------------+-----------+--------+-----------------------------------------+
| bitagora\-    | JSON      | b42861 | Bitagora voting ballot                  |
| ballots       |           |        |                                         |
+---------------+-----------+--------+-----------------------------------------+
| bitagora\-    | JSON      | 154f9c | Bitagora voting polls                   |
| polls         |           |        |                                         |
+---------------+-----------+--------+-----------------------------------------+
```

# Appendix: Sawtooth Settings

### This is an unofficial list of some Transaction Family (TF) settings.
* There is no central registry, most or all of these can be found on github.

##### The following are some Sawtooth settings.
Since Sawtooth settings are extensible and include transaction family-specific settings, this list is incomplete.

* You can list existing settings with the
``sawtooth settings list --url http://localhost:8008`` command.
For options, append ``help`` to the command.
* You can set a setting with the ``sawset proposal create --url http://localhost:8008`` command.  For example,
``sawset proposal create --url http://localhost:8008 --key /etc/sawtooth/keys/validator.priv sawtooth.publisher.max_batches_per_block=200``
* Some baseline settings are documented at https://sawtooth.hyperledger.org/docs/core/releases/1.0/transaction_family_specifications/settings_transaction_family.html
* Transactor settings are documented at https://sawtooth.hyperledger.org/docs/core/nightly/master/sysadmin_guide/configuring_permissions.html
  and at https://sawtooth.hyperledger.org/docs/core/nightly/master/transaction_family_specifications/settings_transaction_family.html
* PoET settings are documented at https://sawtooth.hyperledger.org/docs/core/nightly/master/sysadmin_guide/configure_sgx.html
* Validator settings are documented at https://sawtooth.hyperledger.org/docs/core/nightly/master/architecture/injecting_batches_block_validation_rules.html#on-chain-validation-rules
  and https://sawtooth.hyperledger.org/docs/core/nightly/master/architecture/injecting_batches_block_validation_rules.html#on-chain-configuration

* ``sawtooth.config.authorization_type``
    Example setting--never used.  To set authorization type, use command line option ``sawtooth-validator --network-auth {trust|challenge}``

* ``sawtooth.consensus.algorithm``
    Consensus algorithm (e.g., ``poet`` (PoET SGX or PoET CFT) or ``devmode`` (default) or ``raft`` or any other pluggable consensus engine you provide)

* ``sawtooth.consensus.block_validation_rules``
    Lists validation rules to use in deciding what blocks to add to the blockchain.
    See https://sawtooth.hyperledger.org/docs/core/nightly/master/architecture/injecting_batches_block_validation_rules.html
* ``sawtooth.consensus.max_wait_time``
    Maximum devmode consensus wait time, in seconds
* ``sawtooth.consensus.min_wait_time``
    Minimum devmode consensus wait time, in seconds
* ``sawtooth.consensus.raft.election_tick``
    RAFT consensus election tick, in seconds. E.g., 1500
* ``sawtooth.consensus.raft.heartbeat_tick``
    RAFT consensus heartbeat tick, in seconds. E.g., 150
* ``sawtooth.consensus.raft.peers``
    JSON list of each peer node's public key. Only required RAFT setting.
    Key is from ``/etc/sawtooth/keys/validator.pub`` .
    Example:
    ``["0276f8fed116837eb7646f800e2dad6d13ad707055923e49df08f47a963547b631",\
    "035d8d519a200cdb8085c62d6fb9f2678cf71cbde738101d61c4c8c2e9f2919aa"]``
* ``sawtooth.consensus.raft.period``
    RAFT consensus period, in seconds. E.g., 3. Higher settings cause larger blocks, small settings have faster performance with smaller, quicker block publication, but causes more network traffic.
* ``sawtooth.consensus.valid_block_publishers``
    List of public keys for allowed block publishers. For devmode
* ``sawtooth.gossip.time_to_live``
    Expiration time for the Gossip node communication protocol
* ``sawtooth.identity.allowed_keys``
    List of keys allowed to make identity transactions to the identity TP
* ``sawtooth.poet.enclave_module_name``
    Python module name implementing the PoET enclave.
    Set to ``sawtooth_poet_sgx.poet_enclave_sgx.poet_enclave``
* ``sawtooth.poet.initial_wait_time``
    For C Test: initial time to wait in seconds before proposing a block (e.g., 25; default 3000)
* ``sawtooth.poet.key_block_claim_limit``
    For K Test: maximum number of blocks a validator may claim with a PoET keypair before it needs to refresh its signup information (default 250)
* ``sawtooth.poet.population_estimate_sample_size``
    Sample size, in blocks, to compute the local mean wait time (default 50).
    The local mean wait time multiplied by random_float(0,1) yields the PoET duration time.
    For production, we recommend 500 to get stable population estimates. Most enterprise networks have stable populations and so a long sample length is preferable. 
* ``sawtooth.poet.report_public_key_pem``
    Public key used by Validator Registry TP to verify attestation reports.
    From ``/etc/sawtooth/ias_rk_pub.pem`` or (for PoET CFT) ``/etc/sawtooth/simulator_rk_pub.pem``
* ``sawtooth.poet.target_wait_time``
    Target time to wait in seconds before proposing a block (e.g., 5; default 20)
* ``sawtooth.poet.valid_enclave_basenames``
    Adds the enclave basename for your enclave to the blockchain for the validator registry transaction processor to use to check signup information.
    From ``poet enclave --enclave-module sgx basename``
* ``sawtooth.poet.valid_enclave_measurements``
    Adds the enclave measurement for your enclave to the blockchain for the validator registry transaction processor to use to check signup information.
    From ``poet enclave --enclave-module sgx measurement`` or (for PoET CFT) ``poet enclave measurement``
* ``sawtooth.poet.ztest_minimum_win_count``
    For Z Test: minimum win count, to test a node is not winning too frequently
* ``sawtooth.publisher.max_batches_per_block``
    Maximum batches allowed per block (e.g., 100)
* ``sawtooth.settings.vote.approval_threshold``
    Minimum number of votes required to accept or reject a proposal (default 1)
* ``sawtooth.settings.vote.authorized_keys``
    List of public keys for authorized voters for on-chain settings.
    The initial setting is in the Genesis Block, Block 0
* ``sawtooth.settings.vote.proposals``
    List of proposals to make changes to settings (base64-encoded ``SettingCandidates`` protobuf)
* ``sawtooth.swa.administrators``
    List of public keys for authorized administrators to create, change, or delete Sabre contract and namespace registries.

* ``sawtooth.validator.batch_injectors``
    Comma-separated list of batch injectors to load.
    Parsed by validator at beginning of block publishing for each block
* ``sawtooth.validator.block_validation_rules``
    On-chain validation rules; enforced by the block validator
* ``sawtooth.validator.max_transactions_per_block``
    Maximum transactions allowed per block
* ``sawtooth.validator.transaction_families``
    List of permitted transaction families.
    If not set, all transaction families are permitted.
    Example setting:
    ``[{"family":"sawtooth_settings", "version":"1.0"}, {"family":"xo", "version":"1.0"}]``
    *Dan's ProTip*: ``sawtooth_settings`` is a required TF. ``sawtooth_validator_registry`` is required if you use PoET.

* ``transactor``
    Public keys of authorized signers (of any kind, batch or transaction)
* ``transactor.batch_signer``
    Public keys of authorized batch signers
* ``transactor.transaction_signer``
    Public keys of authorized transaction signers
* ``transactor.transaction_signer.[transaction family name]``
    Public keys of authorized transaction signers for a transaction processor.
    For a partial list of transaction family names,
    see https://github.com/danintel/sawtooth-faq/blob/master/prefixes.rst
* ``transactor.transaction_signer.intkey``
    Public keys of authorized intkey TF signers
* ``transactor.transaction_signer.sawtooth_identity``
    Public keys of authorized sawtooth_identity TF signers
* ``transactor.transaction_signer.settings``
    Public keys of authorized settings TF signers
* ``transactor.transaction_signer.validator_registry``
    Public keys of authorized validator_registry TF signers
* ``transactor.transaction_signer.xo``
    Public keys of authorized xo TF signers


[Prev](sawtooth_faq2.md) [Next](sawtooth_faq4.md)

© Copyright 2018, Intel Corporation.

© Portions Copyright 2018, Chainbelow Inc