# Creol Cartesi Prototype

This project contains current code being used to test the Descartes SDK, documented in https://cartesi.io/docs/, by verifying web3 eth signatures coming from Creol's IoT devices

## Getting Started

### 1. Requirements

- docker
- docker-compose
- node 12.x
- yarn
- truffle

### 2. Environment

Download and run the Descartes SDK Environment ready-to-use artifact by executing:

```
wget https://github.com/cartesi/descartes-tutorials/releases/download/v0.2.0/descartes-env-0.2.0.tar.gz
tar -xzvf descartes-env-0.2.0.tar.gz
```
Then, start it up by running:

```
cd descartes-env
docker-compose up
```

### 3. Cartesi Playground

Clone this project and use the cartesi/playground Docker image, making sure to map the current directory:

```
docker run -it --rm \
  -e USER=$(id -u -n) \
  -e GROUP=$(id -g -n) \
  -e UID=$(id -u) \
  -e GID=$(id -g) \
  -v `pwd`:/home/$(id -u -n) \
  -w /home/$(id -u -n) \
  cartesi/playground:0.3.0 /bin/bash
```
  
Pack the web3test folder into a custom filesystem, for usage within the Cartesi Machine.
This way you can load it into the machine to run the check.
Still inside the playground, use the genext2fs tool to generate the file-system with those contents:

```
genext2fs -b 1024 -d web3test web3test.ext2
```
### 4. Building the Python3 Web3py Buildroot

0. Init the submodule ```machine-emulator-sdk``` and enter it and enter the ```fs``` folder.

To build the capable buildroot that is able to run the python script, you will have to enable the following packages within

```
make config
```
They are as follows ( * indicates a selection)
```bash
Target Packages
    ->Interpreters/Languages
        -> * python3
            -> Core Modules
                -> * bz2
                -> * readline
                -> * ssl
                -> * unicode
                -> * sqlite
                -> * xml
                -> * xz
                -> * zlib
            -> External Modules
                -> * python-pip
```

Hit exit, and do not build the buildroot when prompted.

Verify that the cartesi-buildroot-config file has the modules enabled.

Then run and wait for it to finish

```
make
```
 
#### 4.1 Enabling web3py in the Cartesi Buildroot

To be able to run custom python packages within the Cartesi Buildroot, cross compilation of the environment must be added to the system.

0. Run the buildroot itself
    ```javascript
    make run-as-root
    ```

1. Update the packages and install venv
    ```javascript
    apt update
    apt install python3-pip python3-venv
    ```
2. Install Python cross compiler environment
    ```
    pip3 install crossenv
    ```
3. Setup virtual python environment 
    ```javascript
    cd /opt/riscv/rootfs
    python3 -m crossenv buildroot/work/staging/usr/bin/python3.8 venv
    //activate environment
    . venv/bin/activate
    ```
4. Build cython and install web3
    ```javascript
    // build cython
    build-pip3 install cython 
    // build web3
    pip3 install web3
    ```
5. Finally close the venv
    ```javascript
    deactivate
    ```
6. Lastly, build the ext2 file and copy it to the shared folder, then exit 
    ```javascript
    genext2fs -f -i 512 -b 65536 -d cross python-web3.ext2
    cp python-web3.ext2 /opt/cartesi/rootfs
    exit
    ```

#### Running the cross compiled Web3py Cartesi Machine

1. Change directories to the emulator and activate the path variables
    ```javascript
    cd sdk/emulator
    eval $(make env)
    ```
2. Change to ```src``` directory and copy the ext2 fs for use in the machine.

    ```javascript
    cd src
    cp ../../fs/python-web3.ext2 .
    cp ../../../web3test.ext2 .
    
    ```
   

#### Running the Web3 Computation Interactively

Execute the following command within the ```src``` directory to run the web3 signature check in an interactive cartesi machine:
```javascript
docker run -it --rm \
  -e USER=$(id -u -n) \
  -e GROUP=$(id -g -n) \
  -e UID=$(id -u) \
  -e GID=$(id -g) \
  -v `pwd`:/home/$(id -u -n) \
  -w /home/$(id -u -n) \
  cartesi/playground:0.3.0 /bin/bash

cartesi-machine --flash-drive="label:root,filename:rootfs.ext2" --flash-drive="label:python-web3,filename:python-web3.ext2" --flash-drive="label:web3test,filename:web3test.ext2" -i /bin/sh
```

Once inside the interactive Cartesi Machine, run the following 3 commands
```javascript
export PATH=/mnt/python-web3/bin:$PATH
cd /mnt/web3test
python3 web3test.py
```
And the Output should resemble

```javascript
Running in interactive mode!

         .
        / \
      /    \
\---/---\  /----\
 \       X       \
  \----/  \---/---\
       \    / CARTESI
        \ /   MACHINE
         '

cartesi-machine:/ # export PATH=/mnt/python-web3/bin:$PATH
export PATH=/mnt/python-web3/bin:$PATH
cartesi-machine:/ # cd /mnt/web3test
cd /mnt/web3test
cartesi-machine:/mnt/web3test # python3 web3test.py
python3 web3test.py
Signed Local Transaction Hash is:

0xd8f64a42b57be0d565f385378db2f6bf324ce14a594afc05de90436e9ce01f60
Loading "Transmitted Thread Txn"...
Txn loaded:...
Comparing local transaction sign against transmitted transaction...
Success! Matching hashes, this txn was signed from within the network

```

## Running on real ARM IoT Devices

To be able to run this example on an ARM device, you will need to build all the docker images on the ARM device yourself. Until a final stable ARM release is published from the Cartesi team. We are actively working on this to help move things forward.

The intent of this demo is to show that calculations can be done on Creol IoT devices. With the express purpose of working towards the final output being that ThREDLeader devices verify transactions signed by other nodes in the network before broadcasting them onchain.

The diagram below indicates the proposed architecture that was explored in the Cartesi dApp grant program.

![Creol-Cartesi-Diagram](https://github.com/creol-io/creol-cartesi-prototype/blob/main/creol-cartesi-diagram.PNG "Creol Cartesi Diagram")

The design is that devices in the Thread Mesh network sign transactions themselves and submit the data that was signed and the signed transaction to the ThRED Leader to verify it came from within the network using Cartesi for the check before pushing the transaction to the RPC node to propagate to the network.

Creol CreezyPi devices would sign transactions themselves and then send them via 802.15.4 Thread to the Thread leader to run a check. When it receives it over Thread, it would trigger the Cartesi Machine to verify that the message came from within the pre auth'd network. 1 can either share a single key or each device can have it's own key.

