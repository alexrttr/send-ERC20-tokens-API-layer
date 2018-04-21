# Send ZEEW script

This project helps to send ZEEW tokens to ethereum address.
Please read this document carefully


### Prerequisites

This script requires docker-compose v1.20.1 and docker 17.05.0-ce or later versions. Ethereum chain data may take up to 10Gb of disk space. Also docker images and contatiners are also can take about 1..2 Gb of disk space.


### Installing

This script contains both testing and production configurations. Testing files start with "test" prefix in file names. The major difference between them is testing containers will mount a project foler directly into containers and will be watching for any chainges in Python files. The production config will copy the files inside containers, so any chainge requres a full rebuild of "worker" and "server" images.

A step by step instructions how to run the script.

Run run.sh script as shown below:

```
cd btceth_transfer
./run.sh
```

Stop script with the following command (after run.sh):

```
./stop.sh
```

Rebuild "worker" and "server" containers with the following command:

```
docker-compose rebuild
```


## Important environment variables in YAML files:

* RPC_PORT is a port server should open to receive send tokens requests
* ZEEW_TX_MINING_TIME is an integer value setting up how many minutes a typical transaction will take. It's used to delay reports
* ETH_RPC_PORT is an rpc port ethereum node listens on. Normally it shouln't be changed without a strong reason
* CONTRACT_ADDR is the address of ZEEW token holder contract
* ETH_HOST is a hostname of ethereum node
* RPC_PORT is a port server should open to receive send tokens requests
* INVESTMENT_HOST is an IP address of investment platform
* INVESTMENT_RPC_PORT is a port of json-rpc server on the investment platform receiving reports
- TIME_ZONE is a time zone of celery schedule, it should be set to server's time zone, celery delays tasks with it
- GAS_LIMIT is a max gas a particular transaction can use
- GAS_PRICE is a price of gas in gwei


## How to setup a geth container

In order to setup account the following steps are required:
* copy your keystore file into ethereum/keys/ethereum folder (ethereum/keys/test for test)
* echo your password into ethereum/keys/ethereum/password
* set "--unlock" key in docker-compose.yml to your account address (instead of index) if you have two or more addresses to test with. If you have only one address and your ethereum folder doesn't contain any files except for keystore, then default config should be able to figure out address on its own. If ethereum container reports "unable to unlock", set the address explicitly.
* make sure your ethereum folder is writable by root, run chmod or chown to allow root user to create files in it if needed, e.g. 
```
su -
chown root:root ethereum
cat ethereum/keys/ethereum/password
ls  ethereum/keys/ethereum/UTC*
```

Once the container is launched, wait about 30..40 hours for full sync with public network.


## How to communicate to the script

The script will open port 7080 on loopback interface. This port receives json-rpc requests. An example of such a request can be found in tests/send_tokens.sh script.

This script expects to be able connect to docker's bridge ip address and port 7081 to report back results of transaction.
A dummy listener can be found in tests/reports_listener.sh

## How to change smart contracts

In order to interact with smart contracts the script reads abi.json files in `contract` directory.  Addresses of smart contracts can be found in `*.yml` config files as both enviromnent variables and parameters to ethereum node.
