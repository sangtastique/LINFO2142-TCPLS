# TCPLS : Performance evaluation

This repository contains a few scripts and results about a performance evaluation of TCPLS in the context of the LINFO2142 networking class at UCLouvain.

The project's structure is the following :

``` bash
LINFO2142-TCPLS
├───ipmininet
│   ├─── graphs        # Matplotlib graph scripts
│   ├─── measurements  # Measurement data
│   ├─── scripts       # Scripts to take measurements
│   │   └─── rsa       # Set of keys for TCPLS
│   └─── topologies    # IPMininet topologies
└─── rapido-edit.c     # Our modified rapido to take measurements
```

# Running the experiments

## Installation

All measurements happen inside the vagrant VM provided in [IPMininet's documentation](https://ipmininet.readthedocs.io/en/latest/install.html), so the first step is to download this VM.

### Building rapido



