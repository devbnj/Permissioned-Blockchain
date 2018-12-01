# Sawtooth - Transaction Processing

### Will a client send a transaction request to all the validators in the network?
* No, it would just need to send the batch to one validator, then that validator will broadcast the batch to the rest of its peers.
* If the validator is down, your connection attempt from the app would fail.
* The app could run into error in trying again (in a retry loop) or trying another validator.

### Does Sawtooth have a way to control what participants have access to what assets in the business network and under what conditions?
* Blockchains, including Sawtooth, can be deployed as permissioned networks, wherein transactions are visible to the participants of the permissioned network, but not visible to the general public.

## What transaction processors are required?
* Just the Settings TP, ``settings`` .
* The Validator Registry TP,  ``sawtooth_validator_registry`` , is required if you use PoET.

## What does the Settings TP do?
* The Settings TP provides on-chain configs to be applied to the Sawtooth Validators, so that you can change operational parameters without restarting the validators or the whole sawtooth network.
* Also, you could write your own settings-tp, that stores the settings the same way but enforces different rules on how they are updated.

### Is there an example where the Settings TP is used in another TP?
* Yes. check out [sawtooth.identity.allowed_keys in the Identity TP](https://github.com/hyperledger/sawtooth-core/blob/master/families/identity/sawtooth_identity/processor/handler.py)

### Can different Validator Nodes have different Transaction Processors running?
* No. The set of TPs must be the same for all validator nodes in a Sawtooth network.
* The TP versions must also match across nodes--support the same set of ops.
* This is so the transaction and state validation will be successful.

### How do I support multiple versions of a Transaction Processor?
* You have two choices:
   * A single TP can register itself to handle multiple versions. When the TP receives a transaction, it looks at the transaction's version field and decides how to handle it in the Apply() method.
   * Multiple TPs, each handling a specific version.
* In any case, all nodes need to support the same set of versions for a specific Transaction Family.

### How do I support multiple Transaction Families in a Transaction Processor?
* This is usually not a preferred best practice.
* But if the functionality of the different TFs are closely related, you can have a TP support multiple TFs. Just have the TP register multiple TFs at startup, instead of just one TF.

### How do I upgrade a transaction processor version?
* Bump up the version number of the TP and register with the validator. Submit transactions to the TP with the updated version number. If you want to reuse the existing TP, then you'll need to stop the existing one and register the new one.

### Can a Validator Node have multiple TPs (processes) running for the same TF?
* Yes, one or more TPs, handling the same or different Transaction Families, may be running and register with a validator.
* This is one way to achieve parallelism.
* Another way to achieve parallelism is to write a multi-threaded TP.
   * The transactions are sent to transaction processors supporting the same transaction family in a round-robin fashion.

## What are inputs and outputs in Sawtooth?
* In a Sawtooth transaction, inputs get listed for the transaction (what addresses the TP can read). Outputs list what are the outputs for the transaction (what addresses the TP can modify). [The inputs and outputs lists are specific to a transaction.](https://sawtooth.hyperledger.org/docs/core/releases/1.0/architecture/transactions_and_batches.html)

### Why use round-robin if the transaction processors are identical?
* This is useful when the when the validator's parallel scheduler is used.
* Multiple transactions can be processed in parallel when the inputs/outputs do not conflict.

## Where do I deploy transaction processors?
* Each validator node runs all transaction processors supported for the Sawtooth network.
* Sawtooth includes features for asynchronously deploying and upgrading the Transaction Processors.
* In a typical deployment you will have multiple Transaction Processors.

## What happens if a validator receives a transaction but does not have a TP for it?
* If a validator receives a transaction that it does not have a transaction processor for, the validator will wait until a TP connects that can handle that transaction.
* The validator will stay online and participate with the network and other services, but it will not be able to validate transactions for which it does not have the associated Transaction Processor.
   * That validator would fall behind the rest of the validators on the network while it waits.
   * Hence it will not update state (for any state transitions) that include or depend on such transactions *until* the transaction processor is deployed for that node.
   * Once deployed on that validator, the validator will be able to catch up with the network.

## How can I limit what Transaction Processors run on a Validator Node?
* You can also limit which transactions are accepted on the network by setting
``sawtooth.validator.transaction_families`` If that setting is not set, all transaction processors are accepted.
This setting is ignored in dev-mode consensus.

## Where do transactions originate?
* From the client. The client sends a transaction to a validator, in a batch with one or more transactions. The transactions are sent to the validator, via the REST API, for the validator to add to the blockchain.

## Can the same transaction appear in multiple blocks?
* No. Each block has a unique set of transaction. A block is composed of batches, which is composed of transactions. Each transaction has a unique ID and appears only once in a blockchain. There may be, however, differences in ordering of blocks at a validator due to scheduling, transaction dependencies, etc.

### What mechanism prevents a rogue TP from operating and corrupting data?
* The design is as such that rogue TPs can't harm legitimate TPs. When you run a network of validators, each validator has to have same version of TPs. If a rogue TP is modifying your TPs data, the same TP has to run in the rest of the validators in the network, to be able to affect the blockchain. The validator where the rogue TP is working will constantly fail state validations (Merkle hashes will be different with rest of the network). Hence, the bigger the validator network, the more robust it is against such attacks.

### What does this error mean: ``processor | [... DEBUG executor] transaction processors registered for processor type cryptomoji: 0.1``?
* It means there is no transaction processor running for your transaction family.

### What does this error mean: ``processor | { AuthorizationException: Tried to get unauthorized address ...`` ?
* It means a the transaction processor tried to access (get/put) a value not in the list of inputs/outputs. This occurs when a client submits a transaction with an inaccurate list of inputs/outputs.
* Make sure the Sawtooth address is the correct length--the address is 70 hex characters, which represent a 35 byte address (including the 6 hex character or 3 byte Transaction Family prefix).

### What does this error mean: ``applicator->Apply errorState Get Authorization error. Check transaction inputs.``
* See the answer above.

### If you have a large file to store, is it best to just record the file hash and store the file offline?
* It depends on your use case. Storing data off-chain has a big downside.
* Although you can confirm it hasn't been tampered with with the on-chain hash, there is nothing stopping the file from disappearing.
* Also, how do you make sure everyone who needs the data can get to it?

### If I register a transaction processor to one validator, does the registration get transmitted to the other validators in a network?
* No. Your transaction processor must be deployed to all validators. All validators in a network must have the same set of transaction processors.

### How do I add a transaction processor?
* You just start it in for all the validator nodes. The TP needs to connect to ``tcp://localhost:4004`` or, if you are using Docker, ``tcp://validator:4004``

### How do I restrict what transaction processors are allowed?
* By default, any TP can be added to a node without special permission (other than network access). To restrict what TPs can be added to a validator, use ``sawset proposal create`` to set ``sawtooth.validator.transaction_families``.
For details, see ``Configuring the List of Transaction Families`` at https://sawtooth.hyperledger.org/docs/core/releases/latest/app_developers_guide/docker.html

### How do I add events to the transaction processor?
* In the TP code, call ``context.add_event()``.
* This adds a an application-specific event.
* In the client code (or other app for listening), subscribe to the event.
* [Read the details](https://sawtooth.hyperledger.org/docs/core/releases/latest/architecture/events_and_transactions_receipts.html#events)

### What initial Sawtooth events are available?
* Besides application-specific events, the Sawtooth default events are:
    * ``sawtooth/commit-block`` Committed block information: block ID, number, sate root hash, and previous block ID
    * ``sawtooth/state-delta`` All state changes that occurred for a block at a specific address

### How do I subscribe to Sawtooth events?
* [Read the documentation](https://sawtooth.hyperledger.org/docs/core/nightly/master/app_developers_guide/event_subscriptions.html)
* [Example in Python](https://github.com/danintel/sawtooth-cookiejar/blob/master/events/events_client.py)
* [Example in Javascript](https://github.com/hyperledger/sawtooth-supply-chain/blob/master/ledger_sync/subscriber/index.js)

### How do I handle forks while subscribing to Sawtooth events?
* If you get ``fork_detected: true`` in the ``state_changes`` object, you delete or undo events labeled with the blocks that have been removed from history. For example, if you added the events to a local database, remove the rows labeled with the removed blocks. Then apply events forward from the most recent common block.

### Why is the Apply method in the TP handler called twice?
* That is by design. It can be called more than twice. For that reason, the TP handler must be deterministic
(have the same output results given the same input).

### What does it mean to be deterministic?
* Deterministic means the output never varies, given the same input. That is,
   * serialization must be deterministic, meaning the encoding is always in the same order and always the same for the same data
   * timestamps cannot be generated by the TP as they chain (timestamps in a transaction from the client are OK as they don't change for a given transaction)
   * counters, likewise, generated by the TP are not allowed (but counters from the client are OK for a given transaction)

### Do Transaction Processors run off-chain or on-chain?
* Sawtooth TPs run off-chain, as a process (or processes).

### TP throws an exception of type ``InternalError``, but the ``Apply`` method gets stuck in an endless loop
* ``InternalError`` is supposed to be a transient error (some internal fault like 'out of memory' that is temporary), and may succeed if retried.
* The validator retries the transaction with the TP and results in a loop.
    * If the transaction is invalid, you probably want to raise an ``InvalidTransaction`` error instead.
    * Bottom line - internal errors are retried, and invalid transactions are not retried.

### Error trying to set some Sawtooth settings: ``Chain head is not set yet. Permit all``
* This error has been seen when the directory or file ownerships are wrong. Try setting ownership as follows: ``chown sawtooth:sawtooth /var/lib/sawtooth /var/lib/sawtooth/*`` .
* Then verify with ``ls -la /var/lib/sawtooth`` .
* This error has also been seen because the Settings TP has not been started. Start with ``settings-tp -vv`` .
* Another cause could be because there is no genesis block.

### Does the Transaction Processor know the current Transaction ID?
* Yes. It is available in the header.
* The transaction header_signature is the Transaction ID.

### Can I run two different Transaction Processors on the same Sawtooth Network?
* Yes, you can run any number of transaction families, for example, you can run the Seafood Supply Chain app and Bond Asset Settlement app on the same network.

### What happens if someone writes a fake Transaction Processor (with the same name, version, and address space) that can access and modify state data?
* The fake TP will cause the node to fork and it will be ignored by the rest of the network.

### Why is there no timestamp in a transaction header or block?
* Using timestamps in a distributed network is troublesome--mostly due to complex clock synchronization issues among peers. You could add a timestamp in your transaction family's transaction payload.
* Sawtooth stores a timestamp in the block if the network is setup to inject BlockInfo transactions using the BlockInfo Transaction Family (which is used for EVM compatibility). See: https://sawtooth.hyperledger.org/docs/core/releases/latest/transaction_family_specifications/blockinfo_transaction_family.html


### Does Sawtooth allow multiple digital signatures on a single transaction?
* In Sawtooth the "batch" is the atomic unit of change. This is a collection of one or more individually signed transactions. You could have multiple transactions, each signed by a different party, combined in one batch. This would have a similar effect to what you are talking about I think.
* You can also build whatever app logic you like. So you can require transactions from multiple parties before an action is taken.
* The individual transactions themselves have only one signer.

### What is the size limit for a Sawtooth transaction?
* There is no size limit, barring any memory and storage limits for your Sawtooth nodes.
* If you don't want to write a large transaction, you can reference some external source (and also save a checksum). The disadvantage of storing data externally is it's not replicated across nodes and may be lost.

### What does this message mean: ``Did not respond to the ping, removing transaction processor`` ?
* This is a message from the Hyperledger Sawtooth blockchain's Validator. A timeout occurred when the Validator was checking connections with all the registered transaction processors. If a transaction processor does not respond, it is removed from the list.
* Some possible causes: the transaction processor (TP) died. Check that the TP process is still running (check in the Docker container if you are running docker). Check network connectivity if the TP is on another host or another virtual machine. Check the message logs. Perhaps the TP is "frozen" or hanging or has a bug. Add logging messages (using LOGGER).

### What does this message mean: ``Block . . . rejected due to state root hash mismatch`` ?
* You have a transaction processor that implements some non-deterministic behavior, such as generating a random number in a calculation, or a timestamp, etc.

### What does this message mean: ``Have not received a chain head from peers.`` ?
* This message has been seen when a node is not running a needed transaction processor. A new node needs to run all the transaction processors required for all the supported transaction families in this Sawtooth blockchain network.

### How do I debug a transaction processor?
* One way is to add logging messages (using LOGGER) and sprinkle your code with debug messages, such as ``LOGGER.info("Action = %s.", action)`` in Python (or another language you use for the TP). Start the transaction processor with the ``-vv`` or ``-vvv`` flags and look for console output.

### What does this message mean: ``failing transaction ... since it isn't required in the configuration`` ?
* It means you set the ``sawtooth.validator.transaction_families`` setting with the Settings TP and did not include the TP name and version for the transaction that failed. The fix is to add the TP name and version to the setting.

### I noticed that TPs on various nodes do not process transactions in the same order. Why?
* There is no guarantee of sequencing in terms of how different transactions are submitted and executed by the TPs. When transactions read or modify the same portions of state, the validator enforces ordering correctness, even with parallel execution. That is because the validator's scheduler understands the ordering relationship and needs to apply each state transition to the context provided to the next transaction's execution.


# Sawtooth Validator

## What does the validator do?
* At a high-level, the Validator verifies the following:
   * Permission - Check the batch signing key against the allowed transactor permissions
   * Signature - Check for integrity of the data
   * Structure - Check structural composition of batches: duplicate transactions, extra transactions, etc.

# Is there a simple example on how to run Sawtooth
* See these instructions to install and use Sawtooth with Docker, Ubuntu Linux, or AWS:
https://sawtooth.hyperledger.org/docs/core/nightly/master/app_developers_guide/installing_sawtooth.html

### Is there an example for a multiple node Sawtooth Network?
* See these instructions for setting up a 5-node Sawtooth Network with PoET CFT Consensus using Docker:
https://sawtooth.hyperledger.org/docs/core/nightly/master/app_developers_guide/creating_sawtooth_network.html
* Here is a gist with brief instructions for a 2-node network:
https://gist.github.com/askmish/a23bde6f2e59e4256be8afe965a9166b
* The important part about configuring a multi-node network is
to create a genesis block only with the first validator. Do not create multiple genesis blocks with subsequent validators (that is do not re-run ``sawset genesis`` and ``sawadm genesis``).

### How do I add a node to a Sawtooth Network?
* See
https://sawtooth.hyperledger.org/docs/core/nightly/master/app_developers_guide/creating_sawtooth_network.html#ubuntu-add-a-node-to-the-single-node-environment

### How do I verify the Validator is running and reachable?
* Run the following command from the Validator Docker container or from where the Validator is running:
```
```

### What do I do if some of the Sawtooth Network nodes go offline?
* You can restart any failed nodes. They should rejoin the network and will then process all blocks that were added to the blockchain since the node went down. It will be busy during this initial phase, but will return to normal after that.

```
        curl http://localhost:8008/blocks
```
* This verifies the REST API is available.
* From the Client Docker container run this:

```
        curl http://rest-api:8008/blocks
```
* You should see a JSON response similar to this:
```
    {
      "data": [
        {
          "batches": [
            {
              "header": {
                "signer_public_key": . . .
```

### Do all validators need to run the same transaction processors?
* Yes. All validators must run all of the same transaction processors that are
on the network. If a validator receives a transaction that it does not have a
transaction processor for, the validator will wait until a transaction processor
connects that can handle that transaction. That validator would fall behind the
rest on the network while it waits. You can also limit which transactions are
accepted on the network with the ``sawtooth.validator.transaction_families``
setting. If that setting is not set, all transaction would be accepted.

### I set sawtooth.validator.transaction_families as follows (from the documentation) but it's ignored
* The sawtooth.validator.transaction_families setting is ignored using dev-mode consensus and does not need to be set.

### What is the difference between ``sawtooth-validator --peers {list}`` and ``sawtooth-validator --seeds {list}``?
* There are two peering modes in sawtooth: static and dynamic (use option ``--peering static`` or ``--peering dynamic`` depending on which mode is required). The static peering mode requires the ``--peers`` arg to connect to other peer validators. Whereas, in the dynamic peering mode the ``--peers`` if specified will be processed and then use ``--seeds`` for the initial connection to the validator network and to start topology build-out (discovery and connection to more peer validators).

### For static peering do I need to specify all validator nodes, or just some of them?
* For static, you need to specify all nodes. I recommend dynamic peering where you don't need to specify all of them, just a good sampling (with --seeds). The rest will be discovered. All dynamic peers have to specified by at least one other node (and preferably multiple nodes).

### What files does Sawtooth use?
* ``/var/lib/sawtooth/`` contains the blockchain, Merkle tree, and transaction receipts
* ``/var/log/sawtooth/`` contains log files
* ``~/.sawtooth/keys/`` contain one or more sets of user key pairs
* ``/etc/sawtooth/keys/`` contain the validator key pair
* ``/etc/sawtooth/policy/`` contains policy settings, if any
* ``/var/lib/sawtooth-raft/`` Optional Raft consensus-specific files.  Present only if you use Raft.  Directory can be changed with ``$SAWTOOTH_RAFT_HOME``
* If set, these files are placed under directory ``$SAWTOOTH_HOME`` (except files under your home directory, ``~`` ).

### Why does the validator create large 1TByte files?
* The large 1TByte files in ``/var/lib/sawtooth/`` are "sparse" files, implemented with LMDB (Lightning Memory-mapped Database). They are random-access files with mostly empty blocks. They do not actually consume 1Tbyte of storage.

### How do I backup a large sparse file?
* One method to backup it up is to use the ``tar -S`` option (sparse option). For example: ``tar cSf merkle-00.tar merkle-00.*`` . Some of the Linux file tools have similar options, such as ``cp --sparse``.
* For LMDB databases, the database should be backed up when it is quiet (no updates). If the database is "live", it's best to do a backup by dumping it to a file. That will avoid inconsistencies from backups during the middle of updates. Use ``mdb_dump`` from package ``lmdb-utils`` . For example,
``mdb_dump -n /var/lib/sawtooth/block-00.lmdb >block-00.lmdb.dump``
* Use ``mdb_load -n -f block-00.lmdb.dump`` to restore the database.

### What does ``lmdb.CorruptedError: mdb_put: MDB_CORRUPTED: Located page was wrong type`` mean?
* The LMDB database, which stores the blockchain, is corrupted. The blockchain is backed-up automatically with multiple nodes. There are no published recovery tools, but you could clean out the data on the failed machine and restart and then allow the chain to be rebuilt from its peers.

### What TCP ports does Sawtooth use?
* 4004 is used by the Validator component bus, which uses ZMQ. The validator listens to requests on this port from the REST API and from one or more transaction processors. This port can be closed to external hosts in a firewall configuration if all the transaction processors are on the same host as the validator (the usual case)
    * Port 4004 is sometimes exported to port 4040 in Sawtooth Docker containers for the validator.
* 8008 is used by the REST API, which connects the Client to the Validator. This port can be closed to external hosts in a firewall configuration if the client is always on the same host as a validator
* 8800 is used by the Validator network to communicate with other Validators. This port needs to be open to external hosts in a firewall configuration to communicate with peer validators
* 5050 is used by the consensus engine (such as PoET or Raft). This port should be closed to external hosts in a firewall configuration
* 3030 is used by the Seth TP (if you have Seth running). This port can be closed to external hosts in a firewall configuration if the client is always on the same host as a validator

### How do I create a Sawtooth Network?
* See *Creating a Sawtooth Network* at
https://sawtooth.hyperledger.org/docs/core/nightly/master/app_developers_guide/creating_sawtooth_network.html
* Create the genesis block only one time, on the first node, and configure one or more peer Validator nodes for each node.

### I have Sawtooth running with a single node. How do I add a node?
* You need to either start up the validator with information about the network peers using the ``sawtooth-validator --peers`` option or set ``seeds`` or ``peers`` in configuration file ``/etc/sawtooth/validator.toml``. Then restart the node.

### Can I run two validators on the same machine?
* Yes, but it is not recommended. You need to configure separate Sawtooth instances with different:
    * data, key, log, and policy directories (default values listed above).
    * If ``$SAWTOOTH_HOME`` is set, all these directories are under ``$SAWTOOTH_HOME``.
    * It's not recommended, but you can also can also change the directories in ``path.toml``.
* For more information, see
https://sawtooth.hyperledger.org/docs/core/releases/latest/sysadmin_guide/configuring_sawtooth/path_configuration_file.html
* REST API TCP port (default 8008). Change the ``rest-api.toml``. For details, see
https://sawtooth.hyperledger.org/docs/core/releases/latest/sysadmin_guide/configuring_sawtooth/rest_api_configuration_file.html
* Validator TCP ports (default of 8800 for the peer network and 4004 for the validator components). Change with the ``bind`` setting in ``validator.toml``.
* For details, see
https://sawtooth.hyperledger.org/docs/core/releases/latest/sysadmin_guide/configuring_sawtooth/validator_configuration_file.html
* Genesis block. This is important. As with validators on multiple machines (the usual case), it's important to create a genesis block only with the first validator. Do not create multiple genesis blocks with subsequent validators (that is do not run ``sawset genesis`` and ``sawadm genesis``)
* Instead, consider setting up separate virtual machines (such as with VirtualBox) for each validator. This ensures isolation of files and ports for each Validator.

### What TCP ports should I restrict or allow through a firewall?
* TCP Port 4004 is used for internal validator / transaction processor communications. Restrict from outside use
* TCP Port 8008 is used by the REST API for validator / client communications. Restrict from outside use if the client resides on the host
* TCP Port 8080 is used to communicate between validator nodes. Allow

### What is the validator parallel scheduler?
* The validator has two schedulers -- parallel and serial.
* The parallel scheduler gives a performance boost because it allows multiple transactions to be processed at the same time when the transaction inputs/outputs do not conflict.
* The scheduler is specified with the
``sawtooth-validator --scheduler {parallel,serial}`` option.
* The current default is ``serial``, but it may change to ``parallel`` in the future.
* For example:
``sawtooth-validator --scheduler parallel -vv`` .

### What are the verbosity levels of the various Sawtooth CLIs?
* ``-v`` means warning messages
* ``-vv`` means information + warning messages
* ``-vvv`` means debug + information + warning messages

### After a failed transaction, the validator stops processing further transactions. What can I do?
* You can run the validator in parallel processing mode.
* For a serial scheduler, a failed transaction will be retried and no further transactions can be processed until the blocked transaction is processed successfully. Parallel scheduling will cause non-dependent transactions to be scheduled irrespective of the failed transaction.

### How can I improve Sawtooth performance?
* First, for performance measurement or tuning, do not run the default "dev mode" consensus algorithm. Run another one, such as PoET SGX or PoET CFT. Dev mode is not for production use and excessive forks under heavy use degrades performance
* Run the validator in parallel mode, not serial mode
* Consider increasing the on-chain setting ``sawtooth.publisher.max_batches_per_block`` . Try a value of 200 batches per block to start with. This and other on-chain settings can be changed on-the-fly without impacting older blocks.
* Run multiple transaction processors per validator node for the same transaction family. This is especially useful for TPs written in Python
* Batch multiple transactions together as much as possible in a Batch of transaction or a BatchList of multiple transactions (or both)
* Write the transaction processor in a thread-friendly programming language such as Rust or C++, not Python. Python is an interpretive language and therefore slower. It also suffers from the Global Interpreter Lock (GIL), which locks executing multiple threads to one thread at-a-time
* When fully stabilized, substitute PoET consensus with Raft consensus. Raft is CFT instead of BFT, but it should perform better in exchange for lower fault tolerance
* As you make changes, measure the impact with a performance tool such as Hyperledger Caliper

### Is there any way to get real-time Sawtooth statistics?
* Yes. Sawtooth has Telegraf/InfluxDB/Grafana to gather and display metrics.
* Install the packages and follow these instructions:
https://sawtooth.hyperledger.org/docs/core/nightly/master/sysadmin_guide/grafana_configuration.html
* Here is a Sawtooth Grafana screenshot: https://twitter.com/liedenavilla/status/1042792583221653504

### What does this error mean: ``[... DEBUG client_handlers] Unable to find entry at address ...``?
* It means the address doesn't exist.
* I've seen this error when retrieving a value that should have been written, but was not written.
* The reason was because the transaction processor for the value was not running so the object at the address was never created.

### What does this error mean: ``sawtooth-validator[... ERROR cli] Cannot have a genesis_batch_file and an existing chain``?
* You tried to create a new genesis block when you did not need to (because there already is a genesis block). To solve, this remove file ``/var/lib/sawtooth/genesis.batch.file`` and restart ``sawtooth-validator`` .

### I get this warning when running a transaction processor: ``Max occupancy was not provided by transaction processor: ... Using default max occupancy: 10``
* Max occupancy is the number of transactions that a transaction processor can handle. By default it is set to 10, in this case if more than 10 transactions are supplied at once validator will wait until occupancy is available for the processor or is cancelled. This is introduced so that transaction processor is not overwhelmed with requests.
* You need to set the number of validators if it's over 10.
* For example, in ``/etc/sawtooth/validator.toml`` set ``maximum_peer_connectivity = 50``
* See https://sawtooth.hyperledger.org/docs/core/releases/latest/sysadmin_guide/configuring_sawtooth/validator_configuration_file.html
* You can also use the `sawtooth-validator --maximum-peer-connectivity` command line option.

### I start the validator, but it's stuck at this message: ``Waiting for transaction processor (sawtooth_settings, 1.0)``
* The Sawtooth Settings TP is mandatory for all Sawtooth nodes--even if you don't add or change any settings. You probably want to also start the TP for your desired application. To start the Settings TP, type: ``sudo -u sawtooth settings-tp -v``

### Can I change Sawtooth settings after genesis?
* Yes, but you are limited to using the rule that is currently set for changing settings. This is handled by the Settings TP.

### Why am I getting this validator message: ``Reject building on block 8c5ebbea: Validator is claiming blocks too frequently.``
* It is from the z-test, which is a defense-in-depth mechanism to catch validators that are publishing blocks with an improbable frequency. Unfortunately the defaults we chose for that statistical test aren't well suited for tiny networks (that feature is really intended for added security in large production networks).
* If you have only one validator, you are bound to fail the z-test eventually.
* Probably the best way to fix that in your test network is to restart it with some different z-test settings. This will effectively disable z-test: ``sawtooth.poet.ztest_minimum_win_count = 999999999``

### Why do I get a ``Block validation failed`` message from the validator?
* Usually block validation fails because of something non-deterministic in the transaction processor. This is usually because of the serialization method, which is usually because someone used JSON (use something like Protobufs or CBOR instead). Other common sources of non-determinism are relying on system time in the transaction processor logic.

### What does this error mean: ``Network communications between validators will not be authenticated or encrypted.``
* It means you did not configure your ``network_public_key`` and ``network_private_key`` in ``validator.toml``.

### How do I generate the ``network_public_key`` and ``network_private_key`` in ``validator.toml`` ?
* These are the ZMQ message keys used to securely communicate with other nodes.
* If you've installed sawtooth already, python3 and python3-zmq would have been already installed and available in your system.
* Here's an example to create the keypair in Python:
```
    import zmq
    (public, secret) = zmq.curve_keypair()
    print("network_public_key =", public.decode("utf-8"),
          "\nnetwork_private_key =", secret.decode("utf-8"))
```
* Also, if you can use a compiled binary tool:
```

   $ sudo apt-get install g++ libzmq3-dev
   $ wget https://raw.githubusercontent.com/zeromq/libzmq/master/tools/curve_keygen.cpp
   $ g++ curve_keygen.cpp -o curve_keygen -lzmq
   $ ./curve_keygen
```
* Copy the corresponding public key output to ``network_public_key`` and the private key output to ``network_private_key`` fields in ``validator.toml``

### What does this warning mean: ``Network key pair is not configured, Network communications between validators will not be authenticated or encrypted`` ?
* You did not configure the keypair for the network nodes.  For development purposes, that is OK.  For production, use create a network keypair and add to file `validator.toml`, as instructed in the question here about how to generate the ``network_public_key`` and ``network_private_key`` .

### I am seeing only one transaction per block in my blockchain. Why?
* The Sawtooth Validator combines transaction batches when possible. If you are using dev mode consensus, it is producing blocks as fast as possible, which will typically only contain one transaction. You can simulate what would happen on a real network by setting min and max block times for devmode. If you set min to 10 and max to 20, it will include many more transactions per block. You can also combine transactions from your client by submitting multiple transactions in a batch.

### What does ``Block publishing suspended until new chain head arrives`` mean?
* It means that a new block arrived and the receiving validator wants to stop creating the block it was working on until it finds the new chain head.
 
### After adding 100,000 blockchain state variables, I run out of memory. Why?
* Sawtooth stores the blockchain in a LMDB database at ``/var/lib/Sawtooth/block-00.lmdb`` . The LMDB database is a "sparse" file meaning no storage is allocated for the file until it is used (written to). The database should not run out of memory, as long as filesystem storage is available. The memory error could happen in Kubernetes or Docker or other virtual machine environments where there are no storage volumes mapped to the VM.

### What are the maximum number of blocks in a Sawtooth blockchain?
* There is no limit, other than the available storage for a node.

# Sawtooth Consensus Algorithms (including PoET)

### What consensus algorithms does Sawtooth support?
* dev-mode: Only suitable for testing TPs with single validator deployments.  Uses a simplified random-leader algorithm for development and testing.  Not for production use
* PoET CFT (also known as PoET Simulator): PoET with a simulated SGX environment. Provides CFT similar to Fabric and some other blockchains.  Requires poet-validator-registry TP. Runs on any processor (does not require Intel or SGX).  Has Crash Fault Tolerance and can be used for production networks if BFT is not required
* PoET SGX: Takes advantage of SGX in order to provide consensus with Byzantine Fault Tolerance (BFT), like PoW algorithms have, but at very low CPU usage. PoET SGX is the only algorithm that has hardware requirements (a processor supporting SGX)
* Raft: Consensus algorithm that elects a leader for a term of arbitrary time. Leader replaced if it times-out. Raft is faster than PoET, but is CFT, not BFT. Also Raft does not fork.  For Sawtooth Raft is new and still being stabilized.

### Will Sawtooth support more consensus algorithms in the future?
* Yes. With pluggable consensus, the idea is to have a meaningful set of consensus algorithms so the "best fit" can be applied to an application's use case.  Raft is a recent addition--still being stabilized. There is a PBFT prototype in the works.  Others are being planned.
* REMME.io has independently implemented Algorand Byzantine Agreement on Sawtooth.

### Where is Raft documented?
* https://sawtooth.hyperledger.org/docs/raft/nightly/master/
* To use, basically set ``sawtooth.consensus.algorithm`` to ``raft`` and
``sawtooth.consensus.raft.peers`` to a list of peer nodes (network public keys).

### Does the PBFT implementation follow the original paper?
* Yes, it follows the original 1999 Castro and Liskov paper without modifications or optimizations.

### Does the PoET CFT implement the same consensus algorithm as PoET SGX?
* Yes, they are same same consensus algorithm. The difference is the PoET CFT also simulates the enclave module, allowing PoET to run on non-SGX hardware.

### For PoET CFT (PoET Simulator), should I generate my own ``simulator_rk_pub.pem`` file or do I use the one in ``/etc/sawtooth/`` ?
* No, you use the one that is installed. It must match the private key that is in the PoET Simulator. The public key is needed to verify attestation verification reports from PoET.

### What is unpluggable consensus?
* Sawtooth supports unpluggable consensus, meaning you can change the consensus algorithm on the fly, at a block boundary.
* Changing consensus on the fly means it is done without stopping validators, flushing state, or starting over with a new genesis block.
* It is also called Dynamic Consensus.

### Can my Sawtooth network have validators with a mixture of PoET SGX and PoET CFT?
* No. You need to pick one consensus for all nodes.
* But you can change consensus after the Sawtooth network has started.

### Is PoET CFT suitable for production use?
* Yes.  It is for systems that do not have SGX and is intended for use in production.  Both PoET CFT and PoET SGX have tests to guard against bad actors, such as the "Z Test" to check a validator is not winning too frequently.
PoET CFT simulates the SGX environment and provides CFT (similar to Fabric and other blockchain software), which is good enough to go into production.
* That said, PoET SGX is preferred because of the additional SGX protections for generating the wait time.

### What cloud services offer SGX?
* SGX is available on IBM cloud and Alibaba.
* Early access was available on Microsoft Azure, but not now.

### Does PoET SGX function with SGX on cloud services?
* No. For PoET SGX to function, one also needs Platform Services (PSW), which is not available from any cloud provider.
* Instead, one can use PoET CFT, which is also supported.
* But other software software that requires SGX may be deployed on cloud services.

### I get this error during PoET SGX registration: "Machine requires update (probably BIOS) for SGX compliance."
* During EPID provisioning your computer is trying to get an anonymous credential from Intel. If that process is failing one possibility is that there's a network issue like a proxy. A second possibility is that there's some firmware out of date and so the protocol isn't doing what the backend expects it to. You can check for a firmware / BIOS update for that platform.
* SGX also needs to be enabled in the BIOS menu.

### Does Sawtooth require a certain processor to be deployed on a network?
* No. If you use PoET SGX consensus you need a processor that supports SGX.

### Does Sawtooth require SGX?
* No.  SGX is only needed if you use the hardened version of PoET, PoET SGX.
* We also have a version of PoET that just uses conventional software, PoET CFT, which runs on a Sawtooth network with any processor.

### How is PoET duration time computed?
* It is ``duration = random_float(0,1) * local_mean_wait_time``

### Why does PoET use exponentially-distributed random variable function instead of a uniform function?
* That is to minimize the number of "collisions" in the distribution of a given round of wait timers generated by the population, where "collision" means two or more timers that are near the minimum of the distribution and within some latency threshold.
* The distribution of the random function is shaped by a population estimate of the network, which is determined by examining the last N blocks.
* In an ideal world, you want a distribution where one and only one random wait time is around the desired inter block duration, and then there is a decent sized gap.

### Where is PoET 1.0 Specification?
* https://sawtooth.hyperledger.org/docs/core/releases/1.0/architecture/poet.html

### Where is the PoET SGX Enclave configuration file?
* It is at ``/etc/sawtooth/poet_enclave_sgx.toml`` .
* It is only for configuring PoET SGX Enclave, not the PoET CFT (PoET without SGX).
* A sample file is at
https://github.com/hyperledger/sawtooth-poet/blob/master/sgx/packaging/poet_enclave_sgx.toml.example
* The configuration is documented at
https://sawtooth.hyperledger.org/docs/core/releases/latest/sysadmin_guide/configuring_sawtooth/poet_sgx_enclave_configuration_file.html

### I run ``sudo -u sawtooth poet registration create . . .`` and get ``Permission denied: 'poet_genesis.batch'`` error
* Change to a sawtooth user-writable directory before running the command: ``cd /tmp``

### What does ``Consensus not ready to build candidate block`` mean?
* This message is usually an innocuous information message. It usually means that the validator isn't yet registered in the validator registry or that its previous registration has expired and it's waiting for the new one to commit.
* The message occurs after the block publisher polls the consensus interface asking if it is time to build the block. If not enough time has elapsed, it logs that message.
* However, if that message is rampant in the logs on all but one node, that might mean that none of them can register (they are deadlocked when launching a network). There's a few things that can cause that.
* Unlikely but worth mentioning: are you mapping volumes into the containers? If all the validators are trying to use the same data file that would be bad. That would not happen unless all the nodes are on the same host.
* More commonly, the defense-in-depth checks are too stringent during the initial launch. You can relax these parameters (see Settings_ in this FAQ) or, easier yet, relaunch the network.

### How do I change the Sawtooth consensus algorithm?
* Install the software package containing the consensus engine you wish to use on all nodes, if it is not already installed.
* Start any consensus-required TPs, if any, on all nodes (for example PoET requires the ``sawtooth_validator_registry`` TP).
* Use the ``sawset proposal create`` subcommand to modify ``sawtooth.consensus.algorithm`` (along with any consensus-required settings).  For an example, see https://sawtooth.hyperledger.org/docs/core/nightly/master/app_developers_guide/creating_sawtooth_network.html

* The initial default consensus algorithm is ``devmode``, which is not for production use.
* Here is an example that changes the consensus to Raft:
  ``sawset proposal create --url http://localhost:8008 --key /etc/sawtooth/keys/validator.priv  \
  sawtooth.consensus.algorithm=raft sawtooth.consensus.raft.peers=\
  '["0276f8fed116837eb7646f800e2dad6d13ad707055923e49df08f47a963547b631", \
  "035d8d519a200cdb8085c62d6fb9f2678cf71cbde738101d61c4c8c2e9f2919aa"]'``

### How do I change the consensus algorithm for a network that has forked?
* Bring the network down to one node with the preferred blocks and submit your consensus change proposal.  Bring in the other nodes, with any consensus-required TPs running (for example, PoET requires the Validator Registry TP).

### Where can I find information on the proposed PoET2 algorithm?
* PoET2 is different from PoET in that it supports SGX without relying on Intel Platform Services Enclave (PSE), making it suitable in cloud environments.
* PoET2 no longer saves anything across reboots (such as the clock, monotonic counters, or a saved ECDSA keypair).
* The PoET2 SGX enclave still generates a signed, random duration value.
* More details and changes are documented in the PoET2 RFC at
https://github.com/hyperledger/sawtooth-rfcs/pull/20/files
* A video presentation (2018-08-23) is at
https://drive.google.com/drive/folders/0B_NJV6eJXAA1VnFUakRzaG1raXc
(starting at 7:45)

### What is the Intel Platform Developers Kit for Blockchain - Ubuntu?
* The PDK is a small form factor computer with SGX with Ubuntu, Hyperledger Sawtooth, and development software pre-installed.  For information, see
https://designintools.intel.com/Intel_Platform_Developers_Kit_for_Blockchain_p/q6uidcbkcpdk.htm

### Where is the Consensus Engine API documented?
* At https://github.com/hyperledger/sawtooth-rfcs/pull/4
* See also the "Sawtooth Consensus Engines" video at 20180426-sawtooth-tech-forum.mp4, starting at 10:00,
in directory https://drive.google.com/drive/folders/0B_NJV6eJXAA1VnFUakRzaG1raXc

### What are the minimum number of nodes needed for PoET?
* PoET needs at least 3 nodes, but works best with at least 4 or 5 nodes. This is to avoid Z Test failures (a node winning too frequently).  In production, to keep a blockchain safe, more nodes are always better, regardless of the consensus. 10 nodes are good for internal testing. For production, have 2 nodes per identity.

### How should peer nodes be distributed?
* Blockchain achieves fault tolerance by having its state (data) completely duplicated among the peer nodes.  Best practice means distributing your nodes--geographically and organizationally.
* Distributing nodes on virtual machines sharing the same host does nothing to guard against hardware faults.
* Distributing nodes at the same site does not protect against site outages.

# Sawtooth Client

## What is a Sawtooth Client?
* It is an application that communicates with the Sawtooth Validator, usually using the REST API.  The application is Transaction Family-specific and may come in various forms, such as a CLI, BUI (browser/web app), GUI, or background daemon.  The client may be written in any language supported by the Sawtooth SDK.

## What languages does the Sawtooth Client SDK support?
* JavaScript, Python 3, and Rust.
* Others are in the process of being added: Java and C++.
* One can also interface directly to Sawtooth without a SDK.
* Multiple languages are supported as different languages are more suited for different problem spaces and developers tend to be more comfortable with some languages more than others.
* See this chart of Sawtooth SDK support:
https://sawtooth.hyperledger.org/docs/core/releases/latest/app_developers_guide/sdk_table.html
* For more information, see the Sawtooth SDK Reference at
https://sawtooth.hyperledger.org/docs/core/releases/latest/sdks.html

### Does Sawtooth have a .NET SDK?
* Yes, there is a Sawtooth SDK for .NET Core described here: https://tomislav.tech/2018-03-02-sawtooth-sdk-net-core/
* The source is here: https://github.com/hyperledger/sawtooth-sdk-dotnet

### When would you want to develop without the Sawtooth SDK?
* You should use the SDK whenever possible for your language. If your preferred development language does not have a SDK, or if the SDK is incomplete for something you need, then develop without a SDK.
* For details, see https://sawtooth.hyperledger.org/docs/core/releases/latest/app_developers_guide/no_sdk.html

### What does the client do to send a transaction?
* It encodes the TF-specific payload (which could be anything, but defined by the TF) in Base64,
signs the transaction using ECDSA with curve secp256k1, and generates a deterministic state address.

### What is the nonce used for in the transaction header?
* A nonce is a one-time use number (never repeated).  Typically a random number is used for a nonce.
* A nonce in this case guarantees against replay attacks by making transactions unique.

### What does this error mean: ``validator | [... DEBUG signature_verifier] transaction signature invalid for txn: ...``?
* The client submitted a transaction with an invalid signature.

### What are the various batch_statuses REST API result values?
* ``PENDING`` - batch validation has started on this validator. This ends when the batch is either committed or invalidated
* ``COMMITTED`` - batch is in the blockchain
* ``INVALID`` - batch has recently been invalidated by this validator and is still in the invalid batch cache
* ``UNKNOWN`` - batch is not in any of the above categories, it is not currently being validated by this validator, not in the blockchain, and not in this validator's invalid cache

### What does an INVALID batch status mean?
* It means the transaction batch was processed by the Transaction Processor, but the TP marked it as invalid. The INVALID batch information is not stored on the blockchain. Validators will keep a local cache of invalid batch info around for awhile (I think 10 minutes), so clients can query it, but that data is ephemeral.

### What does it mean if a batch status result remains PENDING?
* It means processing has not completed on the batch. If it stays that way, it means the transaction batch never reached the Transaction Processor.  The transaction remains in the validator queue waiting for the TP to appear online. The TP may have died or may have never started. Or the validator failed the PoET Z Test (z-tested out) because it was winning too frequently.

### Can I use partial address prefixes (say the 6-character prefix) in a transaction's input or output list?
* Yes.  You can use full addresses or partial addresses or empty (no address).  The full addresses are preferred as this allows the parallel scheduler to process non-conflicting transactions in parallel.

### How do I debug a Sawtooth client?
* Add debug messages (such as ``print("Action = {}".format(action))`` in Python).
* Start the REST API with the ``sawtooth-rest-api -vvv`` for the most verbosity.
* Set the trace parameter to true when calling method ``Batch``. In Python: ``batch_pb2.Batch(trace=True)`` .
This prints additional logging information in the Sawtooth REST API and Validator components.

### How do I delete or change a specific value in state?
* Use the ``delete_state`` in the SDK to delete a specific state variable.
* The data will remain in previously-created blocks (which are immutable), but will not be in the current blockchain state.

[Prev](sawtooth_faq.md) [Next](sawtooth_faq3.md)

© Copyright 2018, Intel Corporation.

© Portions Copyright 2018, Chainbelow Inc