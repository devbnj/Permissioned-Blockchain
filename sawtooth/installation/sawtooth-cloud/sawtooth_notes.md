# Sawtooth Notes

## Install – 10%
* Install Sawtooth packages

    * Installation
    * Follow the instructions to [run on Ubuntu](https://sawtooth.hyperledger.org/docs/core/releases/latest/appdevelopersguide/ubuntu.html)
    * For specific apps, you can run without docker by manually running commands in a Dockerfile as follows:
        * Install Sawtooth on an Ubuntu following the instructions in the *Sawtooth Applications Developer's Guide*
```
            # -- if you have an earlier installation or even a failed installation
            $ sudo rm /var/lib/dpkg/lock
            # -- on with the Sawtooth installation
            $ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 8AA7AF1F1091A5FD
            $ sudo add-apt-repository 'deb http://repo.sawtooth.me/ubuntu/1.0/stable xenial universe'
            # -- ensure your instance is upto date with the suggested repository
            $ sudo apt update
            $ sudo apt-get install -y sawtooth
            # -- clean up
            $ sudo apt autoremove
```

* Start component services
        
```
            $ sudo systemctl [start|stop|restart|enable] sawtooth-validator.service
            $ sudo systemctl [start|stop|restart|enable] sawtooth-rest-api.service
            $ sudo systemctl [start|stop|restart|enable] sawtooth-settings-tp.service
            $ sudo systemctl [start|stop|restart|enable] sawtooth-poet-validator-registry-tp.service
```

* Generate keys

```
            $ sawtooth keygen
            # -- response
            # -- creating key directory: /home/devb/.sawtooth/keys
            # -- private key
            # -- writing file: /home/devb/.sawtooth/keys/devb.priv
            # -- public certificate
            # -- writing file: /home/devb/.sawtooth/keys/devb.pub
```
   * Install required packages listed under the RUN line in the Dockerfile for each container
   * Install your application's transaction processor and client.
   * Make sure your client app connects to the REST API at http://localhost:8008 instead of http://rest-api:8008
   * Make sure your transaction processor connects to tcp://localhost:4004 instead of tcp://validator:4004
* Register validator
* Configure peering 
   * Start the Validator, REST API, and Settings TP:
```
            sudo -u sawtooth sawtooth-validator -vv &
            sudo -u sawtooth sawtooth-rest-api -vvv &
            sudo -u sawtooth settings-tp -vv &
``` 
   * Start your application-specific transaction processor(s). See the CMD line in the Dockerfile for your TP
   * Start your application client (see CMD in your client Dockerfile)
* Verify install and fix if necessary
   * Make sure your client app connects to the REST API at http://localhost:8008 instead of http://rest-api:8008
   * Make sure your transaction processor connects to tcp://localhost:4004 instead of tcp://validator:4004
* Connect transaction processor to validator
* Create genesis block
   * Create the Genesis Block. See Guide in previous step
```
            $ sudo sawset genesis --key ~/.sawtooth/keys/devb.priv
            # -- response
            # -- Generated config-genesis.batch
```
* Verify system meets hardware requirements

## Configuration – 25%
```
            $ cd /etc/sawtooth
            $ sudo cp cli.toml.example cli.toml
            $ sudo cp path.toml.example path.toml
            $ sudo cp rest_api.toml.example rest_api.toml
            $ sudo cp log_config.toml.example log_config.toml
            $ sudo cp settings.toml.example settings.toml
            $ sudo cp validator.toml.example validator.toml
            $ sudo cp xo.toml.example xo.toml
```
* Configure validator peering and network
```
            
            # --- Network
            bind = [ “endpoint”, “endpoint” ]. Sets the network and component endpoints. 
            Default network bind interface: tcp://127.0.0.1:8800. 
            Default component bind interface: tcp://127.0.0.1:4004. 
            Each string has the format {option}:{endpoint}, where {option} is either 
            network or component. 
            For example: bind = ["network:tcp://127.0.0.1:8800","component:tcp://127.0.0.1:4004"]. 
            
            # --- Peering
            peering = "static | dynamic" . Static peering attempts to peer only with the 
            candidates provided with the peers option. Dynamic peering first 
            processes any static peers, starts topology buildouts, 
            then uses the URLs specified by the seeds option for the initial 
            connection to the validator network.
            
            # --- Endpoint
            endpoint = "URL" . Sets the advertised network endpoint URL. Default: tcp://127.0.0.1:8800. 
            
            # --- Seeds (Dynamic)
            seeds = [URI] . (Dynamic peering only.) Specifies the URI or URIs 
            for the initial connection to the validator network. 
            Example: seeds = ["tcp://127.0.0.1:8801"].
            
            # --- Peers (Static)
            peers = [“URL“] . Specifies a static list of peers to attempt to connect to.
            
            # --- Scheduler
            scheduler = 'serial | parallel'
            
            # --- Public and Private Keys
            network_public_key = "" and network_private_key = "". 
            Specifies the curve ZMQ key pair used to create a secured network based 
            on side-band sharing of a single network key pair to all participating nodes.
            
            # --- Metrics
            opentsdb_url = “value“ . Sets the host and port for Open TSDB database. Default: none.
            opentsdb_db = “name“ . Sets the name of the Open TSDB database. Default: none.
            opentsdb_username = username . Sets the username for the Open TSDB database. Default: none.
            opentsdb_password = password . Sets the password for the Open TSDB database. Default: none.
            network = "trust | challenge" . Specifies the type of authorization that 
            must be performed for the different type of authorization roles on the 
            network: trust or challenge. Default - trust.
            
            # --- Authorization type
            role = "policy" . The role names specified in this config file must match the 
            roles stored in state for transactor permissioning. 
            For example: ``transactor`` ``transactor.transaction_signer`` 
            ``transactor.transaction_signer.[tp_name]`` and ``transactor.batch_signer`` . 
            For policy, specify a policy file in policy_dir (by default, /etc/sawtooth/). 
            Each policy file contains permit and deny rules for the transactors. 
            See Off-Chain Transactor Permissioning.
            
            # --- Min and Max Peer connectivity
            minimum_peer_connectivity = min | default 3
            maximum_peer_connectivity = max | default 10
```
* Configure consensus
    * PoET Enclave - Read https://sawtooth.hyperledger.org/docs/core/releases/latest/sysadmin_guide/configure_sgx.html
```
            # spid
            spid = ‘string‘. Specifies the Service Provider ID (SPID), which is 
            linked to the key pair used to authenticate with 
            the attestation service. 
            # ias
            ias_url = ‘URL‘ . Specifies the URL of the 
            Intel Attestation Service (IAS) server. 
            # cert
            spid_cert_file = ‘/full/path/to/certificate.pem‘. Identifies 
            the PEM-encoded certificate file that was submitted to Intel 
            in order to obtain a SPID
```    

* Configure logging
    * The validator log config file should be named log_config.toml. Each transaction processor can define its own config file. The name of this file is determined by the author. The transaction processors included in the Python SDK use the following naming convention: [TransactionFamilyName]_log_config.toml
```
            version = 1
            disable_existing_loggers = false

            [formatters.simple]
            format = "[%(asctime)s.%(msecs)03d [%(threadName)s] %(module)s %(levelname)s] %(message)s"
            datefmt = "%H:%M:%S"
            
            [handlers.interconnect]
            level = "DEBUG"
            formatter = "simple"
            class = "logging.FileHandler"
            filename = "path/filename.log"
            
            [loggers."sawtooth_validator.networking.interconnect"]
            level = "DEBUG"
            propagate = true
            handlers = [ "interconnect"]
```    
* Configure REST API
```
            # --- connect to validator
            connect = "URL" . Identifies the URL of a running validator. 
            Default: tcp://localhost:4004. For example: 
                connect = "tcp://localhost:4004"

            # --- timeout 
            timeout = value . Specifies the time, in seconds, to wait for a 
            validator response. Default: 300. For example:
                timeout = 900

            # --- size
            client_max_size = value . Specifies the size, in bytes, that the REST 
            API will accept for the body of requests. If the body is larger a 413: 
            Request Entity Too Large will be returned Default: 10485760 
            (or 10 MB). For example:
                client_max_size = 10485760

            # --- metrics
            opentsdb_url = “value“ . Sets the host and port for Open TSDB database.
            opentsdb_db = “name“ . Sets the name of the Open TSDB database. Default: none.
            opentsdb_username = username . Sets the username for the Open TSDB database. Default: none.
            opentsdb_password = password . Sets the password for the Open TSDB database. Default: none.
```
* Configure layer 3 network ports/firewall
* Configure metrics
* Configure transaction processor endpoint
    * Settings TP and XO TP - generally
```
            connect = “URL“ . Identifies the URL of a running validator. 
            Default: tcp://localhost:4004. 
```
* Configure systemd services
* Choose parallel / sync scheduler
* Configure storage paths
```
            # --- The path.toml configuration changes the Sawtooth data_dir directory. 
            key_dir = path . Directory path to use when loading key files
            data_dir = path . Directory path for storing data files 
                such as the block store
            log_dir = path . Directory path to use to write log files 
                (by default, an error log and a debug log; see Log Configuration).

            policy_dir = path
            # --- If SAWTOOTH_HOME is set, conf_dir = SAWTOOTH_HOME/etc/
            # --- If SAWTOOTH_HOME is not set, conf_dir = /etc/sawtooth
```
* Configure Sawtooth CLI
```
            # --- The REST API URL
            url = "http://localhost:8008"
```

## Permissioning, Identity Management, and Security – 20%
* Identify network ID / system / peer ID
    * A running protected network needs a mechanism for limiting which transactors are allowed to submit batches and transactions to the validators. There are two different methods for defining the transactors a validator will accept.
    * The first method is configuring a validator to only accept batches and transactions from predefined transactors that are loaded from a local validator config file. Once the validator is configured the list of allowed transactors is immutable while the validator is running. 
    * The second method uses the identity namespace which will allow for network-wide updates and agreement on allowed transactors. The allowed transactors are checked when a batch is received from a client, received from a peer, and when a block is validated.
    * When using both on-chain and off-chain configuration, the validator only accepts transactions and batches from a client if both configurations agree it should be accepted. If a batch is received from a peer, only on-chain configuration is checked.
```
            # --- Off-Chain Transactor Permissioning - validator.toml
            [permissions]
            ROLE = POLICY_NAME
            # --- policy file
            PERMIT_KEY [key | *] * - allow all
            DENY_KEY [key | *] 

            # --- On-Chain Transactor Permissioning
            The Identity Namespace stores roles as key-value pairs, 
            where the key is a role name and the value is a policy. 

            transactor.SUB_ROLE = POLICY_NAME
            
            To configure on-chain roles, the signer of identity transactions needs to 
            have their public key set in the Setting “sawtooth.identity.allowed_keys”. 
            
            $ sawset proposal create sawtooth.identity.allowed_keys=
            02b2be336a6ada8f96881cd55fd848c10386d99d0a05e1778d2fc1c60c2783c2f4
            
            $ sawtooth identity policy create ...
            $ sawtooth identity role create ...
            
            # ---- Example
            # ---- Permits all 
            
            $ sawtooth identity policy create policy_1 "PERMIT_KEY *"
            $ sawtooth identity role create transactor policy_1
```
* Permission a transaction processor
* Policy management
    * **Transactor Roles** - The following are the identity roles that are used to control which transactors are allowed to sign transactions and batches on the system.
    * ``default``: When evaluating role permissions, if the role has not been set, the default policy will be used. The policy can be changed to meet the network’s requirements after initial start-up by submitting a new policy with the name default. If the default policy has not been explicitly set, the default is “PERMIT_KEY *”.
    * ``transactor``: The top level role for controlling who can sign transactions and batches on the system will be transactor. This role shall be used when the allowed transactors for transactions and batches are the same. Any transactor whose public key is in the policy will be allowed to sign transactions and batches, unless a more specific sub-role disallows their public key.
    * ``transactor.transaction_signer``: If a transaction is received that is signed by a transactor who is not permitted by the policy, the batch containing the transaction will be dropped.
    * ``transactor.transaction_signer.[tp_name]``: If a transaction is received for a specific transaction family that is signed by a transactor who is not permitted by the policy, the batch containing the transaction will be dropped.
    * ``transactor.batch_signer``: If a batch is received that is signed by a transactor who is not permitted by the policy, that batch will be dropped.

* Validator registration
    * One of the permissioning requirements is that the validator network be able to limit the nodes that are able to connect to it. The permissioning rules determine the roles a connection is able to play on the network. The roles control the types of messages that can be sent and received over a given connection. 
    * Validators are able to determine whether messages delivered to them should be handled or dropped based on a set of role and identities stored within the Identity namespace. Each requester will be identified by the public key derived from their identity signing key. Permission verifiers examine incoming messages against the policy and the current configuration and either permit, drop, or respond with an error. In certain cases, the connection will be forcibly closed – for example: if a node is not allowed to connect to the validator network.
    * This on-chain approach allows the whole network to change its policies at the same time while the network is live, instead of relying on a startup configuration.
    * The Identity namespace stores roles as key-value pairs, where the key is a role name and the value is a policy. Validator network permissioning roles use the following pattern:
    ``network[.SUB_ROLE] = POLICY_NAME``
    where network is the name of the role to be used for validator network permissioning. 
* System permissions
    * Network Roles - The following is the suggested high-level role for on-chain validator network permissioning.
    * ``network`` - If a validator receives a peer request from a node whose public key is not permitted by the policy, the message will be dropped, an AuthorizationViolation will be returned, and the connection will be closed. This role is checked by the permission verifier when the following messages are received:
        * GossipMessage
        * GetPeersRequest
        * PeerRegisterRequest
        * PeerUnregisterRequest
        * GossipBlockRequest
        * GossipBlockResponse
        * GossipBatchByBatchIdRequest
        * GossipBatchByTransactionIdRequest
        * GossipBatchResponse
        * GossipPeersRequest
        * GossipPeersResponse
    * ``network.consensus`` - If a validator receives a GossipMessage that contains a new block published by a node whose public key is not permitted by the policy, the message will be dropped, an ``AuthorizationViolation`` will be returned, and the connection will be closed.
* Configure validator local policy file
* Validator key permissioning
```
    # --- allow or deny nodes (validators) to join the network
    Public - YES | NO
    Consortium - YES | NO
    Private - YES | NO
```
* Role management: transactor roles
* Role management: network roles
* Configure transactor permissions

* Secure connections between components
* Use a proxy server to authorize the REST API
    * As a lightweight shim on top of internal communications, requests sent to the Hyperledger Sawtooth REST API are simply passed on to the validator, without any sort of authorization. While this is in keeping with the public nature of blockchains, that behavior may not be desirable in every use case. Rather than internally implementing one authorization scheme or another, the REST API is designed to work well behind a proxy server, allowing any available authorization scheme to be implemented externally.
    * “X-Forwarded” Headers - Although they aren’t part of any standard, the various X-Forwarded headers are a very common way of communicating useful information about a proxy. There are three of these headers that the REST API may look for when building links.

| header	        | description	                            | example           |
|-------------------|-------------------------------------------|-------------------|
|X-Forwarded-Host	|The domain name of the proxy server.	    | hyperledger.org   |
|X-Forwarded-Proto	|The protocol/scheme used to make request.	| https             |
|X-Forwarded-Path	|An uncommon header implemented specially   | /sawtooth         |
|                   |by the REST API to handle extra path       |                   |
|                   |information. Only necessary if the proxy   |                   |
|                   |endpoints do not map directly to the       |                   |
|                   |REST API endpoints (“hyperledger.org/      |                   |
|                   |sawtooth/blocks”->“localhost:8008/blocks”).|                   |

    * There are three keys in particular the REST API will look for when building response links:

|key|description|example|
|---|---|---|
|host|The domain name of the proxy server.|host=hyperledger.org|
|proto|The protocol/scheme used to make request.|proto=https|
|path|An non-standard key header used to handle extra path information. Only necessary if the proxy endpoints do not map directly to the REST API endpoints (i.e. “hyperledger.org/sawtooth/blocks” -> “localhost:8008/blocks”).	|path=”/sawtooth”|

    * Install Apache
```
            $ apt-get update
            $ apt-get install -y apache2
            $ a2enmod ssl
            $ a2enmod headers
            $ a2enmod proxy_http

            $ sudo nano /etc/apache2/sites-enabled/000-default.conf
```

```
            <VirtualHost *:443>
                ServerName sawtooth
                ServerAdmin sawtooth@sawtooth
                DocumentRoot /var/www/html

                SSLEngine on
                SSLCertificateFile /tmp/.ssl.crt
                SSLCertificateKeyFile /tmp/.ssl.key
                RequestHeader set X-Forwarded-Proto "https"

                <Location>
                    Options Indexes FollowSymLinks
                    AllowOverride None
                    AuthType Basic
                    AuthName "Enter password"
                    AuthUserFile "/tmp/.password"
                    Require user sawtooth
                    Require all denied
                </Location>
            </VirtualHost>
            ProxyPass /sawtooth http://localhost:8008
            ProxyPassReverse /sawtooth http://localhost:8008
            RequestHeader set X-Forwarded-Path "/sawtooth"
```

```
            $ apachectl start
            $ apachectl restart

            # -- Start a validator, and the REST API.
            $ sawadm keygen
            $ sawadm genesis
            $ sawtooth-validator -v --endpoint localhost:8800
            $ sawtooth-rest-api -v

            # --- Test
            $ curl http://localhost:8008/blocks
            $ curl https://localhost/sawtooth/blocks --insecure
            $ curl https://localhost/sawtooth/blocks --insecure -u sawtooth:sawtooth
```

* Securing connecting between validators
* Manage validator keys and secrets

|Network Scenario|Capabilities|
|---|---|
|Public Network|1. Allow all batch signers to submit batches 2. Allow all transaction signers to submit transactions 3. Allow all nodes to join the validator network|
|Consortium Network|1. Allow all batch signers to submit batches 2. Allow all transaction signers to submit transactions 3. Allow only specific nodes to join the validator network 4. Allow only specific nodes to participate in consensus 5. Support policy-based transactor permissioning|
|Private Network|1. Allow only specific batch signers to submit batches 2. Allow only specific transaction signers to submit transactions 3. Allow only specific nodes to join the validator network 4. Allow only specific nodes to participate in consensus 5. Restrict the type of transactions transactors can sign 6. Restrict address space access to a limited set of transactors 7. Support policy-based transactor permissioning|

* Read more on validator peering and secrets - https://sawtooth.hyperledger.org/docs/core/releases/latest/sysadmin_guide/configuring_sawtooth/validator_configuration_file.html

## Lifecycle – 25%
* Create new network
    * Validator Start-up Process - Creating a Genesis Block - The first validator created in a new network must load a genesis block on creation to enable other validators to join the network. Prior to starting the first validator, run the following commands to generate a genesis block that the first validator can load:
    ```
            $ sawtooth keygen --key-dir ~/sawtooth
            $ sawset genesis --key ~/sawtooth.priv
            $ sawadm genesis config-genesis.batch
    ```
    * Vagrant SSH -  To initially launch, for example, two txnvalidator instances and have the logging level set to DEBUG, execute the following:
    ```
    $ ./bin/launcher --count 2 --log-level DEBUG
    # --- Retrieving the Status of the Validator Network
    
    # Execute the status command to get information about the 
    running txnvalidator instances.
    launcher_cli.py> status

    # Adding a validator
    launcher_cli.py> launch
    # it will give an id

    # Kill a validator
    launcher_cli.py> kill 2 [id]

    # Tear down a vvalidator network
    launcher_cli.py> exit

    ```

* Joining an existing network
    * Validator Network - The network layer is responsible for communication between validators in a Sawtooth network, including performing initial connectivity, peer discovery, and message handling. Upon startup, validator instances begin listening on a specified interface and port for incoming connections. Upon connection and peering, validators exchange messages with each other based on the rules of a gossip or epidemic [1] protocol.
    * A primary design goal is to keep the network layer as self-contained as possible. For example, the network layer should not need knowledge of the payload of application messages, nor should it need application-layer provided data to connect to peers or to build out the connectivity of the network. Conversely, the application should not need to understand implementation details of the network in order to send and receive messages.
    * The choice of 0MQ provides considerable flexibility in both available connectivity patterns and the underlying capabilities of the transport layer (IPv4, IPv6, etc.). Intel has adopted the 0MQ Asynchronous Client/Server Pattern [2] which consists of a 0MQ ROUTER socket on the server side which listens on a provided endpoint, with a number of connected 0MQ DEALER sockets as the connected clients. The 0MQ guide describes the features of this pattern as follows:
        * Clients connect to the server and send requests.
        * For each request, the server sends 0 or more replies.
        * Clients can send multiple requests without waiting for a reply.
        * Servers can send multiple replies without waiting for new requests.
    * States - Sawtooth has defined three states related to the connection between any two validator nodes:
        * Unconnected
        * Connected - A connection is a required prerequisite for peering.
        * Peered - A bidirectional relationship that forms the base case for application level message passing (gossip).
    * See Above
* Remove validator node from the network
    * See Above
* Rejoin network after network failure
* Restart validator after crash or maintenance
* Restart components after crash or maintenance
* Add new transaction processor
* Changing consensus mode
* Change network configuration
* Update Sawtooth software
* Update transaction processor version

## Troubleshooting – 20%
* Troubleshoot network communication
* Troubleshoot REST API
* Troubleshoot consensus
* Troubleshoot transaction processor
* Identify and resolve chain fork
* Fix validator
* Enable Sawtooth monitoring
* Monitor network topology
* Troubleshoot deployment
* Troubleshoot resource constraints