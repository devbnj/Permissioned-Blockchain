# Hyperledger Sawtooth

## Blockchain

## Hyperledger Sawtooth
Hyperledger Sawtooth is a modular enterprise blockchain platform for building, deploying, and running distributed ledgers. The design philosophy targets keeping ledgers distributed and making smart contracts safe, particularly for enterprise use. Hyperledger Sawtooth includes a novel consensus algorithm, Proof of Elapsed Time (PoET), which targets large distributed validator populations with minimal resource consumption. No special hardware is required to run Sawtooth or PoET.

## Useful Sawtooth links
* [Sawtooth introduction](https://sawtooth.hyperledger.org/docs/core/nightly/master/introduction.html)
* [Sawtooth introduction and download](https://www.hyperledger.org/projects/sawtooth)
* [GitHub repository for Sawtooth Core](https://github.com/hyperledger/sawtooth-core)
* [Sawtooth documentation, with several guides and references, including:](https://sawtooth.hyperledger.org/docs/core/nightly/master/)
* [Sawtooth Application Developer's Guide](https://sawtooth.hyperledger.org/docs/core/nightly/master/appdevelopersguide.html)
* [Sawtooth Architecture](https://sawtooth.hyperledger.org/docs/core/releases/latest/architecture.html)
* [Sawtooth White Paper](https://www.hyperledger.org/wp-content/uploads/2018/01/HyperledgerSawtoothWhitePaper.pdf)
* [Sawtooth chat main channel](https://chat.hyperledger.org/channel/sawtooth)
* [Sawtooth mailing list](https://lists.hyperledger.org/g/sawtooth)
* [Official Sawtooth FAQ](https://www.hyperledger.org/wp-content/uploads/2018/01/HyperledgerSawtoothFAQ.pdf)
* [Sawtooth FAQ](https://github.com/danintel/sawtooth-faq)

## Good introductory videos
* [Hyperledger Sawtooth 1.0: Market Significance & Technical Overview (Hyperledger, 2018, 61:27) (registration required)](https://gateway.on24.com/wcc/gateway/linux/1101876/1585244/hyperledger-sawtooth-v10-market-significance-and-technical-overview)
* [Webinars](https://www.hyperledger.org/resources/webinars)
* [Hyperledger Sawtooth 1.0 Architecture and App Development (Bitwise IO, 2018, 31:26)](https://www.youtube.com/watch?v=uBebFQM49Xk)
* [Others](https://www.youtube.com/results?searchquery=Hyperledger+Sawtooth)

## Good advanced videos
A list of Hyperledger [Sawtooth videos](https://github.com/danintel/sawtooth-faq/blob/master/settings.rst) (mostly Sawtooth Technical Forum recordings)

## Courses available on Hyperledger Sawtooth
* EdX has a "Blockchain for Business" course that reviews Blockchain technology and includes an introduction to [Sawtooth and other Hyperledger blockchain software](https://www.edx.org/course/blockchain-business-introduction-linuxfoundationx-lfs171x-0)
* An intermediate EdX course, edx 201 "Hyperledger Sawtooth for Application Developers" is under final review for release. It will use [Simple Supply Chain as an example](https://github.com/hyperledger/education-sawtooth-simple-supply)
* A self-paced course is [Cryptomoji, which where students extend a Cryptokitties clone](https://github.com/hyperledger/education-cryptomoji)
* The Kerala Blockchain Academy offers a [Certified Hyperledger Sawtooth Developer (CHD) program at IITM-K, India](http://www.iiitmk.ac.in/kba/).

## Sawtooth exams
A Certified Hyperledger [Sawtooth Administrator exam is being offered](https://www.hyperledger.org/blog/2018/09/05/hyperledger-fabric-sawtooth-certification-exams-coming-soon)
and [the exam outline](https://www.hyperledger.org/resources/training/hyperledger-sawtooth-certification).

## Example applications
* A simple application that implements a cookie jar [showing just the Sawtooth API](https://github.com/danintel/sawtooth-cookiejar)
* A example application that [implements a simple wallet application](https://github.com/askmish/sawtooth-simplewallet)
* A more complex example that implements a [supply chain example and demonstrates many of the key concepts behind the implementation of a complete Sawtooth application](https://github.com/hyperledger/sawtooth-supply-chain)
* An example application that shows how to  exchange quantities of [customized "Assets" with other users on the blockchain](https://github.com/hyperledger/sawtooth-marketplace)

## Live demos of a Sawtooth Application
* [A Sawtooth Supply Chain demo, AssetTrack](https://demo.bitwise.io/) .
* Another demo, for [tracking fish](https://demo.bitwise.io/fish/) .
* A [Sawbucks demo](https://demo.bitwise.io/sawbucks/) .
* A [Supply Chain Traceability demo](https://provenance.sawtooth.me/) .
* The [source and docs of demos](https://github.com/hyperledger/sawtooth-marketplace/)

## Hyperledger Sawtooth Application Developers Forum
* Provides opportunities to discuss technical application development questions with developers experienced with Hyperledger Sawtooth.
* The forum is held on Wednesdays 9-10am Central Time using Zoom video conferencing. An Asia-time friendly Developers Forum is held Thursday at 2pm India Time.
* For details and current contact information for both forums, see
https://chat.hyperledger.org/channel/sawtooth for details.

## Hyperledger and Sawtooth
* Sawtooth (or Hyperledger Sawtooth) is a blockchain implementation initially contributed by Intel Corporation and now maintained by the Sawtooth community. Sawtooth does not have to be deployed on Intel hardware; however, Sawtooth does include the optional PoET consensus module, which uses Intel SGX to provide an efficient, Byzantine Fault Tolerant consensus mechanism that does not rely on [expensive and inefficient mining algorithms](https://www.hyperledger.org/projects/sawtooth).
* Hyperledger is a consortium that includes Sawtooth as well as other blockchain implementations. "Hyperledger is an open source collaborative effort created to advance cross-industry blockchain technologies. [It is a global collaboration, hosted by The Linux Foundation"](https://www.hyperledger.org/).

## Sawtooth, Sawtooth Lake, and Hyperledger Sawtooth
* Sawtooth Lake was Intel's original code name for its blockchain research project, named after a lake in the Sawtooth Mountains of central Idaho. After it was contributed to the Linux Foundation's Hyperledger consortium, the name was changed to Hyperledger Sawtooth. Sawtooth is just shorthand for Hyperledger Sawtooth and are the same thing.

## Differences between Hyperledger Sawtooth and Hyperledger Fabric
* Hyperledger Sawtooth and Fabric are two independent implementations of a blockchain under the Linux Foundation's Hyperledger Blockchain project.
* Here are some differences:
   * Fabric's Smart Contract must be written in GoLang or Javascript. Sawtooth transaction processors can be written in multiple languages, such as Rust, Python, Go, or JavaScript. SDKs for other languages are being added.
   * Fabric has "endorsing peers" and ordering services to pre-process transactions. Sawtooth has a validator that handles everything from validating the transactions and distributing the transaction to peer nodes.
   * Fabric stores data in a leveldb or couchdb, with a separate ledger per channel. Sawtooth stores all data in a central lmdb database with each transaction family using a separate address prefix.
   * Fabric has multiple components, including Orderers, Peers, CAs, CouchDB, and Tools. Sawtooth has the Sawtooth Validator and a Transaction Processor for each Transaction Family. The Validator's REST API communicates with a client.
   * Read [skcript.com article](https://www.skcript.com/svr/hyperledger-fabric-to-sawtooth)

## Differences between Sawtooth and other blockchains
* State agreement, which assures each node has cryptographically-verifiable, identical copies of the blockchain
* novel Byzantine Fault Tolerant (BFT) consensus, through PoET
* Unpluggable consensus on-the-fly (without restarting)
* Multi-language SDK support (Python, Go, Javascript, Rust, with more being added)
* Parallel transaction processing
* [Sawtooth differentiation and philosophy](https://www.hyperledger.org/blog/2016/11/02/meet-sawtooth-lake)

## Difference between a blockchain and a database?
* A database has one master copy. A blockchain has multiple authoritative copies
* A database can be changed after a commit. A blockchain's records are immutable and cannot be undone after a commit
* A database must have a trusted central authority

## Immutable blockchain meaning
* It means that blocks already committed cannot be "undone", reversed or deleted. The block's transactions are in the blockchain forever. The only way to undo a transaction is to add another transaction to reverse a previous transaction. So if the value of a=1 and a transaction sets a=2, the only way to undo it is to set a=1 again. However regardless of what the current value of a is, all three of those transactions are permanently a part of the blockchain. The record of them will never be lost, and in fact you could rewind state to what it was in previous blocks if you needed.
* This is different from immutable variables. The difference is that with blockchain *transactions* are immutable. With some programming languages (such as Rust), *variables* are immutable.

## Version of Sawtooth that is running
```
    $ sawtooth --version
    sawtooth-cli (Hyperledger Sawtooth) version 1.0.5
```

## ``sawtooth``, ``sawadm``, ``sawnet``, and ``sawset`` CLI commands
* **sawadm** Administration tasks such as creating the genesis batch file or validator key generation
* **sawnet** Interact with Sawtooth network, such as comparing chains across nodes
* **sawset** Change genesis block settings or views, create, and vote on new block proposals
* **sawtooth** Interact with a Sawtooth validator, such as batches, blocks, identity, keygen, peers, settings, state, and transaction information
* Read [the Sawtooth CLI Command Reference](https://sawtooth.hyperledger.org/docs/core/releases/latest/cli.html)

### Error running ``sawnet peers`` or ``sawnet list-blocks``
* These commands were added after the Sawtooth 1.0.5 release and are not available in earlier releases.

### Detecting a ``forked blockchain`` in a Sawtooth network
* Use sawnet compare-chains and look for a different set of block(s) at the head of the chains.
* This is distinct from the case where one node has a blockchain that's not up-to-date, but has conflicting heads ("forked").
* Forking can occur if the Sawtooth network is partitioned and cannot fully communicate.
* It can also be the result of a bug in transaction processing (for example, transactions don't serialize in a deterministic way).

### ``Failed to reach common ancestor`` meaning in sawnet compare-chains command
* It means the blockchains have no blocks in common, including the genesis block. This usually happens when a second node is added with its own genesis node. Only the first node in a Sawtooth network should be created with a genesis block.

## Support for Hyperledger Composer on Sawtooth
* Composer is not supported for Sawtooth. [Besides, IBM has reduced Composer development to maintenance mode](https://lists.hyperledger.org/g/composer/message/125)

## Hyperledger Explorer support for Sawtooth
* At present, there is no support. There is a [Sawtooth Explorer](https://github.com/hyperledger/sawtooth-explorer).
* It may or may not be merged with Hyperledger Explorer in the future.
* Sawtooth Explorer provides visibility into the Sawtooth blockchain for node operators.

## Encryption algorithms used by Sawtooth
* Transaction signing with ECDSA 256-bit key using curve secp256k1 (same as Bitcoin)
* ZeroMQ (ZMQ or 0MQ) used for communications. ZMQ uses CurveZMQ for encryption and authentication, which uses ECDH 256-bit key with curve Curve25519 for key agreement.
* PoET uses AES-GCM to encrypt its monotonic counter
* Names are hashed with SHA-512 or SHA-256

## Global State explanation with an example
* Global state is where sawtooth and TPs read/write blockchain data. Examples are a-plenty if you look at the github repo examples (intkey, XO, etc.)
* The "state" is implemented as a Radix Merkle Trie over the LMDB database, where the 'keys' are 35 bytes (70 characters) and the scheme for the keys is up to the TP developer. The first 3 bytes (6 chars) of the key identifies a unique TP namespace and it is recommended to avoid colliding with other TP namespaces.
* To enable your TP to read/write (or in context parlance "get/set") data at addresses, you need to specify those addresses *a priori* in the Transaction inputs/outputs. Otherwise you will get Authorization errors. The addresses your TP will read or write to need to be deterministic.
* Using the SimpleWallet application as an example (see example application links above), the blockchain will contain transactions showing deposits, withdrawals and transfers between accounts. The global state will contain the balance in the different accounts corresponding at the current point in time, after all transactions in the chain have been processed.

## Connections between the ``Merkle Radix Trie`` and the blockchain
* The blockchain itself just stores transactions, not state, so reading the data in the last block does not say much by itself. Data in the blockchain is also immutable and can never change (except by adding new blocks). The radix trie (also called tree) is a different data structure that is used to make fast queries to the state. The root of the Merkle Trie is a hash. One can easily identify if something changed when the root hash changes. The Merkle Trie addressing allows quick retrieval at an address and partial queries of address prefixes.

## Are 32-byte IDs within a transaction family large enough to avoid collisions?
* Yes. If they are being generated with a random distribution, the chances are vanishingly rare. A UUID is only 16-bytes and if you generated a billion per second, it would take 100 years before you would expect 50% odds of a collision.

## Sawtooth's inherent capability to support large network populations of nodes
* One of the reasons is the homogeneous nature of Sawtooth Nodes. You don't have different nodes with specialized functions, so it's easy to setup and manage many nodes. Secondly, and more importantly, the PoET consensus mechanism has been designed for large networks. It's not very efficient in small networks and you'll likely get much better performance with other mechanisms in a small network, but PoET handles large populations easily.

## Sawtooth security evaluation
* Yes. This is a pre-1.0 release audit, that was required to be [part of the Linux Foundation's Hyperledger project](https://www.hyperledger.org/blog/2018/05/22/hyperledger-sawtooth-security-audit)

## Examples of Sawtooth permissions
* off-chain permissioning is in /etc/sawtooth/validator.toml (see validator.toml.example)
* on-chaining permissioning is recorded on-chain. See block 0 for examples, such as sawtooth.settings.vote.authorizedkeys
* transaction key permissioning controls what clients can submit transactions, based on signing keys (transactor.transactionsigner, transaction.transactionsigner.[name of TP], transactor.batchsigner)
* validation key permissioning controls what nodes are allowed to connect to the Sawtooth network
* transaction family permissioning controls what TFs are supported by this Sawtooth network, sawtooth.validator.transactionfamilies
* there are policies and roles from the optional Sawtooth Identity Transaction Processor, documented at https://sawtooth.hyperledger.org/docs/core/releases/latest/transactionfamilyspecifications/identitytransactionfamily.html

## Does Sawtooth restore state when a peer restarts or when a peer is out-of-sync with the network?
* Yes.

## When content at an address is changed several times by the transactions in a block, what appears in the state (Merkle Tree)?
* The only thing that hits state is the aggregate (final) set of address changes due to the transactions in the block. If multiple transactions in a single block modify an address, there will only be one 'set'. You could see the transaction level changes in the receipts if you needed to.

## In order to create a Sawtooth application, do I need to clone and modify the entire sawtooth-core repository?
* No. It can be done that way, but it's not recommended.
* All you need to write is the client application and the Transaction Processor.
* The core Sawtooth functionality should be installed as packages instead of being built from source and integrated with your application.
* Here's some simple sample applications that are in standalone source repositories:
   * Simple Wallet, https://github.com/askmish/sawtooth-simplewallet
   * Cookie Jar, https://github.com/danintel/sawtooth-cookiejar
   * Cryptomoji,  https://github.com/hyperledger/education-cryptomoji A self-paced course using a Cryptokitties clone written in Sawtooth
   * Simple Supply Chain, https://github.com/hyperledger/education-sawtooth-simple-supply  This will be the example in a future edX.org course on Sawtooth app development

## Sawtooth ``global state agreement``
* Sawtooth writes state to a verifiable structure called a *Radix Merkle Trie* and the verification part (the root hash) is included in the consensus process. That means that agreement is not just on the ordering of transactions but also on the resulting contents of the entire database.
* This guards against a variety of possible failures during the application of a transaction (e.g. different library version installed, a write failure, a local database corruption, numerical representation differences).
* Of course, the feature is mainly targeted at protecting the integrity of a production network, but it is also helpful during development. Running applications over test networks can help identify nondeterminism and that will only be apparent if you form consensus over state.

## How can CPU vulnerabilities such as Spectre and Meltdown impact Sawtooth?
* Sawtooth is a CPU-agnostic blockchain platform. It includes an optional TEE/SGX feature which enhances BFT protections for PoET. PoET is designed following a defense-in-depth approach. There are three or so mechanisms that work in different aspects of the protocol independently from the TEE. This includes three tests performed by PoET:
   * c-test: A node must wait c blocks after admission before its blocks will be accepted - this is to prevent trying to game identities and some obscure corner scenarios.
   * K-test: The node can publish at most K blocks before its peers require it to recertify itself.
   * z-test: And perhaps most importantly a node may not publish at frequency greater than z
* Finally, should a node run a compromised consensus protocol, the main characteristic at risk would be *fairness*. It would not be able to impact *correctness* network-wide. That is, it cannot publish invalid transactions. If it does the other nodes will just reject those transactions and the associated block(s) and they will not commit network-wide.

## Are Docker containers required to run Sawtooth?
* Docker is a quick and easy way to get Sawtooth up and running.
* However, unlike other Hyperledger ledgers, Sawtooth does not require Docker.
* Follow the instructions to [run on Ubuntu](https://sawtooth.hyperledger.org/docs/core/releases/latest/appdevelopersguide/ubuntu.html)
* For specific apps, you can run without docker by manually running commands in a Dockerfile as follows:
   * Install Sawtooth on an Ubuntu following the instructions in the *Sawtooth Applications Developer's Guide*
   * Create the Genesis Block. See Guide in previous step
   * Install required packages listed under the RUN line in the Dockerfile for each container
   * Install your application's transaction processor and client.
   * Make sure your client app connects to the REST API at http://localhost:8008 instead of http://rest-api:8008
   * Make sure your transaction processor connects to tcp://localhost:4004 instead of tcp://validator:4004
   * Start the Validator, REST API, and Settings TP:
   ```
     $ sudo -u sawtooth sawtooth-validator -vv &
     $ sudo -u sawtooth sawtooth-rest-api -vvv &
     $ sudo -u sawtooth settings-tp -vv &

     # -- alternatively
     $ sudo sawtooth-validator -vv
   ``` 
   * Start your application-specific transaction processor(s). See the CMD line in the Dockerfile for your TP
   * Start your application client (see CMD in your client Dockerfile)

## Cloud services supporting Sawtooth Blockchain
* AWS and Alibaba Cloud offer Sawtooth, Fabric. Other cloud providers plan to offer Sawtooth on their cloud service.

## Does Sawtooth support Ethereum?
* Yes, through Seth, Sawtooth's Ethereum-compatible Transaction Processor. It implements a Ethereum Virtual Machine (EVM) so Seth can run Ethereum Dapps written in Solidity. Seth uses Hyperledger Burrow as the code base.

## Can Sawtooth be used for blockchain mining?
* No. There is no inherent need to incentivize miners in a private/permissioned blockchain. Part of the permissioned model is that everyone involved has a personal stake in the verifying the data, so you do not need to pay them. This contrasts with a public deployment where you are asking strangers to verify the data for you. In that case you probably do need to incentivize them somehow, and a currency is a common way to do so.

## Is there a ``head node`` or ``master node`` in Sawtooth?
* Sawtooth has no concept of a "head node" or "master node".
Once multiple nodes are up and running, each node has the same genesis block (block 0) and treats all other nodes as peers.
* The first validator node on the network has no special meaning, other than being the node that created the genesis block.

## Sawtooth Role
* A Role is a set of permissions. [Identities could be assigned one or more roles](https://sawtooth.hyperledger.org/docs/core/nightly/master/sysadminguide/configuringpermissions.html). A role is a convenient shorthand because role(s) can be assigned to several identities rather than tediously assigning individual permissions to each identity.

## What Sawtooth Roles are defined?
* **transactor** can sign transactions and batches
* **transactor.batchsigner** can sign batches
* **transactor.transactionsigner** can sign transactions
* **transaction.transactionsigner.[transaction processor name]** can sign transactions for a specific TP
* **network** nodes authorized to make peer requests
* **network.consensus** nodes authorized to broadcast new blocks with Gossip

# Sawtooth Installation and Configuration

## Install Sawtooth packages
* The following setups the Sawtooth stable repository, lists the packages, and installs the core packages (sawtooth, python3-sawtooth-cli, python3-sawtooth-sdk, python3-sawtooth-signing):
```
    $ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 8AA7AF1F1091A5FD
    $ sudo add-apt-repository 'deb http://repo.sawtooth.me/ubuntu/1.0/stable xenial universe'
    $ sudo apt update
    $ sudo apt-get install -y sawtooth
    # -- clean up
    $ sudo apt autoremove
```
* Read up-to-date [installation information](https://sawtooth.hyperledger.org/docs/core/releases/latest/sysadminguide/installation.html)

### Changing Sawtooth settings
* Change the .toml configuration files in /etc/sawtooth .
* Examples are in the directory are installed as .toml.example .
* Read [the details](https://sawtooth.hyperledger.org/docs/core/nightly/master/sysadminguide/configuringsawtooth.html)
* Configuration files are:
   * validator.toml - Validator configuration file
   * restapi.toml - REST API configuration file
   * cli.toml - Sawtooth CLI configuration file
   * poetenclave.toml - PoET SGX Enclave configuration file
   * path.toml - Directory path configuration (or use $SAWTOOTHHOME)
   * identity.toml - Identity TP configuration file
   * settings.toml - Settings TP configuration file
   * logconfig.toml - Log configuration file
   * More transaction-processor specific configuration files may be present.

### Error installing ``Ubuntu packages: "Could not get lock /var/lib/dpkg/lock"``
* The file lock is probably left over from a previous failed install.
* The solution is 
```
$ sudo rm  /var/lib/dpkg/lock
```
* This assumes you're not multitasking and installing something else in another terminal on the same host.

### Error installing sawtooth-cxx-sdk: ``"Depends: protobuf but it is not installable"``
* The C++ SDK package is in the nightly repository.
* Until the package dependency is fixed, here's a workaround to force an install:
```
    $ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 44FC67F19B2466EA
    $ sudo apt-add-repository "deb [trusted=yes] http://repo.sawtooth.me/ubuntu/nightly bionic universe"
    $ sudo apt update
    $ apt download sawtooth-cxx-sdk
    $ sudo dpkg -i  sawtooth-cxx-sdk1.1.1.dev808amd64.deb
    $ pkg contents sawtooth-cxx-sdk
```

### Error running sawtooth ``setting list or xo list : Error 503: Service Unavailable``
* This usually occurs when there is no genesis node created. To create, type the following:
```
    # --- Create the genesis node:
    sawtooth keygen
    sawset genesis
    sudo -u sawtooth sawadm genesis config-genesis.batch
    # --- Start the validator:
    sudo sawadm keygen
    sudo -u sawtooth sawtooth-validator -vv
```

### Error running ``sudo -u sawtooth sawadm genesis config-genesis.batch : Permission denied``
* The ownership or permission is wrong. To fix it, type:
```
    $ sudo chown sawtooth:sawtooth /var/lib/sawtooth
    $ sudo chmod 750 sawtooth:sawtooth /var/lib/sawtooth
    $ ls -ld /var/lib/sawtooth

    drwxr-x--- 2 sawtooth sawtooth 4096 Jun  2 14:43 /var/lib/sawtooth
```

### How to delete all blockchain data
* Type the following: 
```
sudo -u sawtooth rm -rf /var/lib/sawtooth/*
```
* This deletes the entire database. The command is meant for development purposes only.

### Deleting or changing a specific block in the blockchain
* You cannot delete blocks -- they are immutable by design.
* You can create a new transaction (or block of transactions) that reverse a previous transaction.

### Error running ``sawnet peers`` or ``sawnet list-blocks``
* These commands were added after the Sawtooth 1.0.4 release and are not available in earlier releases.

### Changing on-chain settings without deleting the blockchain?
* Use the sawset command. This allows you to change settings such as maximum batches per block or target wait time.

### Error ``gpg: keyserver receive failed: keyserver error when executing sudo apt-key adv --keyserver hkp://keyserver...``
* This error means your machine couldn't add the supplied key to trusted list. This key is later used to authenticate and get sawtooth package.
* One of the possible reason for this error is that your machine is trying to connect to keyserver through a proxy server. Add proxy server details in the command to solve this issue. For example: 
```
    $ sudo apt-key adv --keyserver-options http-proxy=http://[username:password]@[proxyserver]:[port] --keyserver hkp://keyse... (notice usage of flag --keyserver-options here).
```

### Error repository ... ``xenial InRelease' doesn't support architecture 'i386'``
* Following could be possibilities:
   * You installed on a 32-bit-only system. Install on a 64-bit system.
   * You are using 64-bit system, but your linux variant has enabled additional architecture i386. apt is expecting the repository for all configured architectures on your machine. One safe way to solve this error would be to tell apt to get only 64-bit repository. For example, sudo add-apt-repository 'deb [arch=amd64] http://repo.sawtooth.me/ubuntu.....'.


### Error running ``sawset: ModuleNotFoundError: No module named 'colorlog'``
* Something went wrong with installing Python dependencies or they were removed.
* In this case, install colorlog with 
```
   $ sudo apt install python3-colorlog or withpip3 install colorlog
```

### Error starting Sawtooth: lmdb.DiskError: /var/lib/sawtooth/poet-key-state-03efb2aa.lmdb: No space left on device
* Besides the obvious problem of no disk space, it could be your OS or filesystem does not support sparse files. The LMDB databases used by Sawtooth are 1TB sparse (mostly unallocated) files.

### Error running sawtooth sawadm genesis config-genesis.batch:  Processing config-genesis.batch... Error: Unable to read config-genesis.batch
* This error can occur when there is no sawtooth user and group.
* This should have been done by the package postinst script.
* To add, type
``` 
    $ addgroup --system sawtooth; adduser --system --ingroup sawtooth sawtooth
```
* It could be a file or directory permission problem. Change the file ownership with 
```
    $ chown sawtooth:sawtooth config-genesis.batch 
    # --- and move it to a sawtooth-writable directory. 
    # --- For example 
    $ mv config-genesis.batch /tmp; cd /tmp
```
* Another cause could be that the file doesn't exist. Create it with 
```
    $ sawset genesis
```

## Building Sawtooth from source
* Use git to download the source, then buildall to build. Type ./bin/buildall for options. For example:
```
    $ sawtooth --version
    $ git clone https://github.com/hyperledger/sawtooth-core
    $ cd sawtooth-core
    $ ./bin/buildall -l python
```
* Read [details here](https://github.com/hyperledger/sawtooth-core/blob/master/BUILD.md)

## Installing Sawtooth on FreeBSD
* Sawtooth is supported for Ubuntu Linux with binary packages.
* For other other \*IX-like systems, including FreeBSD, you can build from source.
* The following blog may help: https://wiki.freebsd.org/HyperledgerSawtooth
* This is based on FreeBSD 11.1. Docker is not required to run Sawtooth.
* See also this bug for the status of the FreeBSD Sawtooth port: https://bugs.freebsd.org/bugzilla/showbug.cgi?id=228581

### Error installing Sawtooth: Error starting userland proxy: ``listen tcp 0.0.0.0:8080: bind: address already in use``
* You already have a program running that uses TCP port 8080. Either kill it or change the port you use to something else.
* To find the process(es) that have port 8080 open, type 
```
    $ sudo lsof -t -i:8080
```
* Then kill the processes. Check again that they have not restarted. Also check that they are not Docker containers that have restarted.

### Error after setting up a Sawtooth network: ``Can't send message PINGRESPONSE back to ... because connection OutboundConnectionThread- tcp://192.168.0.100:8800 not in dispatcher``
* The usual problem when you get this message is configuring the peer endpoints
   * If you are using Ubuntu directly instead of Docker, use the Validator's hostname or IP address instead of the default (validator), which only works with Docker, or localhost, which may not be routable
   * If you are using Docker, make sure the Docker ports are mapped to the Ubuntu OS, and that the OS IP address/port is routable between the two machines. Check the expose: and ports: entries in your docker-compose.yaml file or similar file
   * Verify network connectivity to the remote machine with ping
   * Verify port connectivity telnet aremotehostname 8800 (replace aremotehostname with the remote peer's hostname or IP address). Control-c out if it connects
   * Verify network and port connectivity in the other direction (remote to local)
   * Check peer configuration in your local and remote /etc/sawtooth/validator.toml files. Check the peering and endpoint lines. Check the seeds line (for dynamic peering) or peers line (for static peering)

### Unmet dependencies ``errors installing Sawtooth on Ubuntu 18.04 LTS``
* Ubuntu 18.04 LTS is supported only in the nightly development packages. Use Ubuntu 16.04 LTS for the stable release packages.
* You can also [install Sawtooth with Docker](https://sawtooth.hyperledger.org/docs/core/releases/latest/appdevelopersguide/docker.html)

### Error installing Sawtooth: ``No matching distribution found for sawtoothrestapi``
* You tried to install Sawtooth using Python pip.
* I don't know if this could work. I know installing Sawtooth using Ubuntu/Debian installation tools (such as apt, apt-get, dpkg, aptitude) works OK.

### Error with add-apt-repository: ``Couldn't connect to accessibility bus: Failed to connect to socket . . . Connection refused``
* It is just a warning and you can ignore it. Verify the Sawtooth repository was added in /etc/apt/sources.list The cause is the command tried to start a graphic display (probably over SSH) when it was not available. A workaround to remove the warning is to add 
```
    export NOATBRIDGE=1 to ~/.bashrc
```

### Error starting Sawtooth on Docker: ``No response from ... beginning heartbeat pings``
* This means there is a problem with the genesis node and peer nodes connecting.

## List sawtooth command line options
* For the Sawtooth CLIs (``sawadm, sawset, sawnet, sawtooth``), append -h after the command to list subcommands (for example, sawadm -h ). For the Sawtooth subcommands, append -h after the subcommand (for example, ``sawadm keygen -h``).

### Error - No module named ... ``error running a Sawtooth program``
* The No module named error occurs in Python when a Python module is missing. The usual fix is to install the corresponding Python package. Something you need to prepend python3- to the name. So, for example, if you get a No module named 'netifaces' error, install the missing package with something like 
```
    $ apt install python3-netifaces
```

### Error: ``no transaction processors registered for processor type sawtoothsettings: 1.0 ``
* Start the Settings TP, as follows 
```
    $ sudo -u sawtooth settings-tp -v
```
* The Settings TP is always required for all Sawtooth nodes, even if you did not add or change any settings.

### Error trying to install Sawtooth: ``Failed to fetch http://repo.sawtooth.me/ubuntu/bumper/stable/dists/xenial/universe/binary-amd64/Packages  404  Not Found``
* The Sawtooth stable documentation is wrong. There is no such thing as a bumper/stable release. The released (stable) packages are at http://repo.sawtooth.me/ubuntu/1.0/stable xenial universe The older Sawtooth 1.0.5 documentation has the correct location: https://sawtooth.hyperledger.org/docs/core/releases/1.0.5/

[Next](sawtooth_faq2.md)

© Copyright 2018, Intel Corporation.

© Portions Copyright 2018, Chainbelow Inc