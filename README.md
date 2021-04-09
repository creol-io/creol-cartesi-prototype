# Creol Cartesi Prototype

This project contains current code being used to test the Descartes SDK, documented in https://cartesi.io/docs/, by verifying web3 eth signatures coming from Creol's IoT devices

## Getting Started

### Requirements

- docker
- docker-compose
- node 12.x
- yarn
- truffle

### Environment

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

### Cartesi Playground

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

Still within the playground, execute the following command to run the web3 signature check in a cartesi machine:
To note: The custom rootfs for this is prebuilt as it requires heavy customization to get running. The signature passed to the file is pre signed for the purposes of this repo. Future releases will be able to accept any signed message from any device for checking
```
cartesi-machine \
  --flash-drive="label:web3test,filename:web3test.ext2" \
  --flash-drive="label:root,filename:rootfs.ext2" \
  --flash-drive="label:output,length:1<<12,filename:output.raw,shared" \
  -- $'cd /mnt/web3test ; ./runweb3test.sh > $(flashdrive output)'
```

The result of the signature check will be stored in the output.raw file.


## Running on real ARM IoT Devices

To be able to run this example on an ARM device, you will need to build all the docker images on the ARM device yourself. Until a final stable ARM release is published from the Cartesi team. We are actively working on this to help move things forward.

The intent of this demo is to show that calculations can be done on Creol IoT devices. With the express purpose of working towards the final output being that ThREDLeader devices verify transactions signed by other nodes in the network before broadcasting them onchain.

The diagram below indicates the proposed architecture that was explored in the Cartesi dApp grant program.

![Creol-Cartesi-Diagram](https://github.com/creol-io/creol-cartesi-prototype/blob/main/creol-cartesi-diagram.PNG "Creol Cartesi Diagram")

The design is that devices in the Thread Mesh network sign transactions themselves and submit the data that was signed and the signed transaction to the ThRED Leader to verify it came from within the network using Cartesi for the check before pushing the transaction to the RPC node to propagate to the network.
