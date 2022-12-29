# TCPLS : Performance evaluation

This repository contains a few scripts and results about a performance evaluation of TCPLS in the context of the LINFO2142 networking class at UCLouvain.

The project's structure is the following :

``` bash
LINFO2142-TCPLS
├─── deps                # Dependencies (rapido git submodule)
├─── ipmininet
│   ├─── graphs          # Matplotlib graph scripts
│   ├─── measurements    # Measurement data
│   └─── scripts         # Scripts to take measurements
│       └─── rsa         # Set of keys for TCPLS
│       └─── topologies  # IPMininet topologies
├─── rapido_edit         # Edited C code, binary and helper script
└─── README.md           # <-- You're here :)
```

# Running the experiments

## Installation

All measurements happen inside the vagrant VM provided in [IPMininet's documentation](https://ipmininet.readthedocs.io/en/latest/install.html), so the first step is to download and run this VM. Clone this repository inside it or in a shared folder.

### Building rapido

The [rapido repository](https://github.com/mpiraux/rapido) is included in this one as a git submodule. Before trying to build rapido make sure you have the required dependencies :
```bash
sudo apt-get install libgoogle-perftools-dev

sudo apt-get install faketime libscope-guard-perl libtest-tcp-perl
```
After that you can build with our (lightly) modified `rapido.c` by running the `get_rapido.sh` script :
```
./rapido_edit/get_rapido.sh
``` 
This script will update rapido's git submodule, compile the binary and move it to the `rapido_edit` folder. All scripts expect the binary to be in this folder under the name `rapido-edit`.

## Running a script

Finally you can run our experiments on you own machine :
```bash
sudo python3 ipmininet/scripts/run_[end of script name here]
```

## Running an IPMininet topology
Before running a topology don't forget to clean : `sudo python3 -m ipmininet.clean`
You can also run one of our topologies and get the mininet CLI :
```
sudo python3 ipmininet/scripts/topologies/[topology name]
```
Once there you can open a shell on a host :
```bash
mininet> h1 bash           # Open a shell in host 1 from mininet's CLI

mininet> dump              # Get IPs and PIDs of nodes
sudo mnexec -a [PID] bash  # Open a shell from another non-mininet shell
```

When you have access to hosts you can run the rapido executable :
```bash
# Start the rapido server on h2
./rapido -c rsa/cert.pem -k rsa/key.pem h2 4443
# Start the client on h1
./rapido -s 20 -n localhost h2 4443
```
TCPLS can use multiple paths in a single session, to do so the server must advertise more than a single address. You can give an additional address to the server with the `-a [IP]` option.

When the server host has two interfaces you have to make sure to configure it such that it will not use only one interface as global gateway :
```bash
ip rule add from [IP SECOND INTERFACE] table 1
ip route add [SUBNET SECOND INTERFACE] dev [SECOND INTERFACE NAME] scope link table 1
ip route add default via [IP SECOND INTERFACE LINK] dev [SECOND INTERFACE NAME] table 1
```
For example if we are on host h2, its second interface is called `h2-eth1` and has IP `192.168.2.1` with subnet `192.168.2.1` we would do :
```bash
ip rule add from 192.168.2.1 table 1
ip route add 192.168.2.1 dev h2-eth1 scope link table 1
ip route add default via 192.168.2.2 dev h2-eth1 table 1
```
This adds a rule that applies on traffic we send from IP `192.168.2.1`, the rule says to use table 1 and table 1 has a default gateway that will go through the interface `h2-eth1`.


