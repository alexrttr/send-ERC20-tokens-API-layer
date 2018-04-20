# Send ZEEW script

This project helps to send ZEEW tokens to ethereum address.


### Prerequisites

This script requires docker-compose v1.20.1 and docker 17.05.0-ce or later versions. Ethereum chain data may take up to 80Gb of disk space. Also docker images and contatiners are also can take about 1..2 Gb of disk space.


### Installing

This script contains both testing and production configurations. Testing files start with "test" prefix in file names. The major difference between them is testing containers will mount a project foler directly into containers and will be watching for any chainges in Python files. The production config will copy the files inside containers, so any chainge requres a full rebuild of "worker" and "server" images.

A step by step instructions how to run the script.

Run run.sh script as shown below:

```
cd btceth_transfer
./run.sh
```

Stop script with the following command:

```
./stop.sh
```

Rebuild "worker" and "server" containers with the following command:

```
docker-compose rebuild
```


## Important environment variables in YAML files:

* RPC_PORT is a port server should open to receive send tokens requests.
* ZEEW_TX_MINING_TIME is an integer value setting up how many minutes a typical transaction will take. It's used to delay reports.
* ETH_RPC_PORT is an rpc port ethereum node listens on. Normally it shouln't be changed without a strong reason.
* CONTRACT_ADDR is the address of ZEEW token holder contract
* ETH_HOST is a hostname of ethereum node
* INVESTMENT_HOST is an IP address of investment platform
* INVESTMENT_RPC_PORT is a port of json-rpc server on the investment platform receiving reports
- TIME_ZONE is a time zone of celery schedule, it should be set to server's time zone, celery delays tasks with it


## How to setup a geth container

In order to setup account the following steps are required:
* copy your keystore file into ethereum/keystore folder
* echo your password into ethereum/keystore/password
* set "--unlock" key in docker-compose.yml to your account address (instead of index) if you have two or more addresses to test with. If you have only one address and your ethereum folder doesn't contain any files except for keystore, then default config should be able to figure out address on its own. If ethereum container reports "unable to unlock", set the address explicitly.
* make sure your ethereum folder is writable by root, run chmod or chown to allow root user to create files in it, e.g. 
```
su -
chown root:root ethereum
cat ethereum/keystore password
```

Once the container is launched, waits for full sync with public ethereum network.

* RPC_PORT is a port server should open to receive send tokens requests.

## How to communicate to the script

The script will open port 7080 on the loopback interface. This port receives json-rpc requests. An example of such a request can be found in tests/rpc_caller.sh script.

This script expects to be able connect to localhost port 7081 to report back results of transaction.

## How to change smart contracts

In order to interact with smart contracts the script reads abi.json files in `contract` directory.  Addresses of smart contracts can be found in `*.yml` config files as both enviromnent variables and parameters to ethereum node.
