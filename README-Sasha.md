# LINFO2142-TCPLS

## Commands 

Start the network : `sudo python3 network.py`

Get into a host from a terminal : `sudo mnexec -a [PID] bash` where `PID` is a host's PID.

In the mininet CLI :

 - List hosts and routers with their PIDs : `dump`
 - Get into a host : `h1 bash`
 - Clean network in case of crash : `sudo python3 -m ipmininet.clean`

Rapido : 
 - Start the server on host h1 :\
  `./rapido -c cert.pem -k key.pem h1 4443`
 - Start the client on host h2 :\
  `./rapido -s 100 -n localhost h1 4443`

 - Building rapido : 
    ```shell
    git submodule update --init
    cmake .
    make rapido
    make check
    ```
