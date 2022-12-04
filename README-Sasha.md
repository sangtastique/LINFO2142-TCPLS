# LINFO2142-TCPLS

## Commands 

Start the network : `sudo python3 network.py`

Get into a host from a terminal : `sudo mnexec -a [PID] bash` where `PID` is a host's PID.

In the mininet CLI :

 - List hosts and routers with their PIDs : `dump`
 - Get into a host : `h1 bash`
 - Clean network in case of crash : `sudo python3 -m ipmininet.clean`
./rapido -c cert.pem -k key.pem h1 4443
Rapido : 
 - Start the server on host h1 :\
  `./rapido -c rsa/cert.pem -k rsa/key.pem -a 192.168.2.2 h2 4443`
  `./rapido -c rsa/cert.pem -k rsa/key.pem h2 4443`
  `./rapido -c rsa/cert.pem -k rsa/key.pem 192.168.1.1 4443`
 - Start the client on host h2 :\
  `./rapido -s 20 -n localhost h2 4443`

 - Building rapido : 
    ```shell
    git submodule update --init
    cmake .
    make rapido
    make check
    ```
   Moving the binary : `cp rapido ../LINFO2142-TCPLS/`

 - iperf : h2 server
   ```
   h2 iperf -s -p 2002 &
   h1 iperf -c h2 -p 2002
   ```

ip rule add from 192.168.2.2 table 1
ip route add 192.168.2.0/24 dev h2-eth1 scope link table 1
ip route add default via 192.168.2.1 dev h2-eth1 table 1

ip rule add from 192.168.2.1 table 1
ip route add 192.168.2.0/24 dev h2-eth1 scope link table 1
ip route add default via 192.168.2.2 dev h2-eth1 table 1

./rapido -c rsa/cert.pem -k rsa/key.pem -a 192.168.2.1 h2 4443

ip rule del  from 192.168.2.2 table 1
