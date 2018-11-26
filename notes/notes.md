# Hyperledger Fabric 1.3
These notes are very crude. Please do not comment or ask questions on these.

## Compose New version 0.20
### Destroy old docker
```
docker kill $(docker ps -q)
docker rm $(docker ps -aq)
docker rmi $(docker images dev-* -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)
```
### Install Pre-requisites
```
curl -O https://hyperledger.github.io/composer/v0.19/prereqs-ubuntu.sh
chmod u+x prereqs-ubuntu.sh
./prereqs-ubuntu.sh
```

### Install Hyperledger Composer
```
npm install -g composer-rest-server@0.20
npm install -g composer-cli@0.20
npm install -g generator-hyperledger-composer@0.20
```

### Install Hyperledger Fabric 1.2 or 1.3+ 
```
mkdir fabric-dev-servers && cd fabric-dev-servers

curl -O https://raw.githubusercontent.com/hyperledger/composer-tools/master/packages/fabric-dev-servers/fabric-dev-servers.tar.gz
tar -xvf fabric-dev-servers.tar.gz

export FABRIC_VERSION=hlfv12
./downloadFabric.sh

./startFabric.sh
./createPeerAdminCard.sh
```

### Start a new project
```
yo hyperledger-composer:businessnetwork
* [ create a network called health-plan ]
cd health-plan
composer archive create -t dir -n .
composer network install --card PeerAdmin@hlfv1 --archiveFile health-plan@0.0.1.bna
composer network start --networkName health-plan --networkVersion 0.0.1 --networkAdmin admin --networkAdminEnrollSecret adminpw --card PeerAdmin@hlfv1 --file health-plan.card
composer card import --file health-plan.card
composer network ping --card admin@health-plan
composer-rest-server
* admin@health-plan
```

```
To restart the REST server using the same options, issue the following command:
   composer-rest-server -c admin@health-plan -n never -u true
```

## Start from Scratch (Docker or no docker)

```
# -- ubuntu
sudo apt-get -y install libssl-dev
```

```
# - macos
brew unlink openssl && brew link openssl --force
brew install openssl
export PATH="/usr/local/opt/openssl/bin:$PATH"' >> ~/.bash_profile
```

```
# - headers
export LDFLAGS="-L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I/usr/local/opt/openssl/include"

brew install softhsm

# - install
curl -O https://dist.opendnssec.org/source/softhsm-2.0.0.tar.gz
tar -xvf softhsm-2.0.0.tar.gz
cd softhsm-2.0.0
./configure --disable-non-paged-memory --disable-gost
make
sudo make install
```

```
sudo mkdir -p /var/lib/softhsm/tokens
sudo chmod 777 /var/lib/softhsm/tokens
softhsm2-util --init-token --slot 0 --label "ForComposer" --so-pin 1234 --pin 98765432
```

# Install Apache (Any Ubuntu 16.0.4 barebones EC Instance)

```
adduser devb
usermod -aG sudo devb
su - devb

apt update
apt-get install apache2
a2enmod ssl
a2enmod headers
a2enmod proxy_http
```

###### Note ~
```
# --- here is where the htmls are:
# ---  /var/www
sudo chmod -R 755 /var/www
```

### Install Node.JS 8.x
```
cd ~
curl -sL https://deb.nodesource.com/setup_8.x -o nodesource_setup.sh
bash nodesource_setup.sh
apt-get install -y nodejs
sudo apt-get install software-properties-common
```

##### Note ~ Install this git
```
curl -LkSs https://api.github.com/repos/devbnj/fabric-cloud/tarball -o fabric-cloud.tar.gz
tar -xvf fabric-cloud.tar.gz
```

### Install Node-RED
```
node -v
npm install -g --unsafe-perm node-red
# --- it will install in /root/.node-red/
```

### Install lets encrypt
```
sudo apt-get update
sudo apt-get autoclean

# --- ./certbot-auto
sudo apt-get install letsencrypt
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update
sudo apt-get install certbot 

# --- setup chainbelow.com
cd /etc/apache2/sites-available
nano 000-default.conf
systemctl restart apache2

certbot certonly --webroot -w /var/www/html/chainbelow -d www.chainbelow.com
# --- certs stored in /etc/letsencrypt
# --- /etc/letsencrypt/live/www.chainbelow.com/cert.pem
# --- /etc/letsencrypt/live/www.chainbelow.com/privkey.pem

apt-get install python-certbot-apache
certbot --apache -d chainbelow.com -d www.chainbelow.com
certbot renew --dry-run
systemctl restart apache2
```

## Install Go

```
sudo apt-get update
sudo apt-get -y upgrade
curl -O https://storage.googleapis.com/golang/go1.11.2.linux-amd64.tar.gz
sudo mv go /usr/local
sudo nano ~/.profile
# -- add to the end
export GOROOT=$HOME/go
export GOPATH=$HOME/work
export PATH=$PATH:$GOROOT/bin:$GOPATH/bin
export FABRIC_CFG_PATH=/home/devb/devbnj/fabric-cloud/hyperledger_fabric/root/config
# -- added
source ~/.profile
# -- test go
go version
```

##### Notes ~ For Production or Cloud Instance
```
Change the docker-compose.yaml file
You fill find in fabric-samples/basic-network
Add to each environment for every container
      - GODEBUG=netdns=go
      - FABRIC_LOGGING_SPEC=INFO
```

##### Notes ~ Rerunning Health-Plan on Fabric 1.3
```
composer network install --card PeerAdmin@hlfv1 --archiveFile health-plan@0.0.1.bna
composer network start --networkName health-plan --networkVersion 0.0.1 --networkAdmin admin --networkAdminEnrollSecret adminpw --card PeerAdmin@hlfv1 --file healthplan.card
composer network ping --card admin@health-plan

# --- Run composer on TLS
composer-rest-server -c admin@health-plan -n never -u true -d n -t true -e /etc/tigersof.pem -k /etc/tigerof.key
```

# Hyperledger Sawtooth 1.0.5

### Remove old Sawtooth Installation
```
sudo apt-get remove --purge sawtooth
sudo apt-get clean
sudo -u sawtooth rm -rf /var/lib/sawtooth/*
sudo rm /var/lib/dpkg/lock
```

## Install Fresh
```
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 8AA7AF1F1091A5FD
sudo add-apt-repository 'deb http://repo.sawtooth.me/ubuntu/1.0/stable xenial universe'

sudo apt update
sudo apt-get install -y sawtooth
sudo apt search sawtooth
sudo apt autoremove

# --- Alternatively
# sudo apt install aptitude
# aptitude install sawtooth python3-sawtooth-*
# aptitude search sawtooth
# sudo apt autoremove
```

### Viewing Console Output
To view the console output that you would see if you ran the components manually, run the following command:
```
sudo journalctl -f \
    -u sawtooth-validator \
    -u sawtooth-settings-tp \
    -u sawtooth-poet-validator-registry-tp \
    -u sawtooth-rest-api
```

#### Create Genesis Block
###### The first validator created in a new network must load a genesis block on creation to enable other validators to join the network. Prior to starting the first validator, run the following commands to generate a genesis block that the first validator can load:
```
sawtooth keygen
# --- it will generate dev.pub, devb.priv
sudo sawset genesis --key ~/.sawtooth/keys/devb.priv
# --- it will generate config-genesis.batch
sudo -u sawtooth sawadm genesis config-genesis.batch
# --- if required
sudo rm /var/lib/sawtooth/genesis.batch
# --- Start the validator:
sudo sawadm keygen
sudo -u sawtooth sawtooth-validator -vv
```

### Running sawtooth
Before starting the validator component you may need to generate the validator keypairs using the following command:

```
sudo sawadm keygen --force
### overwriting file: /etc/sawtooth/keys/validator.priv
### overwriting file: /etc/sawtooth/keys/validator.pub
```

##### Notes ~ 
```
## To start a component using systemd, run the following command where COMPONENT is one of:

* validator
* rest-api
* intkey-tp-python
* settings-tp
* xo-tp-python

### sudo systemctl start sawtooth-COMPONENT
sudo systemctl start sawtooth-validator
sudo systemctl status sawtooth-validator
### sawtooth-validator.service: Unit entered failed state.
### sawtooth-validator.service: Failed with result 'exit-code'.
sudo systemctl is-enabled sawtooth-validator
### disabled
sudo systemctl enable sawtooth-validator
### Created symlink from /etc/systemd/system/multi-user.target.wants/sawtooth-validator.service to /lib/systemd/system/sawtooth-validator.service.
### similarly start the rest-api
sudo systemctl status sawtooth-rest-api
sudo systemctl enable sawtooth-rest-api
### tcp://localhost:4004
```

#### Configuring Sawtooth
##### On Nov 22
##### When a Sawtooth component starts, it looks for a TOML configuration file in the config directory (config_dir). By default, configuration files are stored in /etc/sawtooth; see Path Configuration File for more information on the config directory location.
##### In addition, the Sawtooth log output can be configured with a log config file in TOML or YAML format. By default, Sawtooth stores error and debug log messages for each component in the log directory. For more information, see Log Configuration.

```
sudo rm -fr /var/lib/sawtooth/genesis.batch 
sudo sawadm keygen --force
sudo sawadm genesis
sudo sawtooth-validator -v --endpoint localhost:8800 &
sudo sawtooth-rest-api -v &
```

##### Test
```
curl http://localhost:8008/blocks
```

### Make changes to Apache Configuration
```
sudo nano /etc/apache2/sites-enabled/000-default.conf
sudo apachectl restart
```
