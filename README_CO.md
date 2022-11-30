# LINFO2142-TCPLS

Run a example: sudo python3 -m ipmininet.examples --topo simple_ospf_network 

Launch rapido in mininet:
CLIENT (h1): h1 ./rapido -s 10 -n localhost h2 2142
SERVER (h2): ./rapido -c rsa/cert.pem -k rsa/key.pem h2 2142

Lancer perf3 pour mptcp (afin de comparer avec tcpls)
vagrant@vagrant:~/LINFO2142-TCPLS/iperf-mptcp/src$ ./iperf3 [options]

Launch iperf3-mptcp in mininet:
CLIENT (h1): h1 (cd ../iperf-mptcp/src && exec ./iperf3 -c h2 -m -n 10M - R)
SERVER (h2): (cd ../iperf-mptcp/src && exec ./iperf3 -s)

Launch iperf3 tcp in mininet:
CLIENT (h1): h1 (cd ../iperf-3.9/src && exec ./iperf3 -c h2 -n 10M - R)
SERVER (h2): (cd ../iperf-3.9/src && exec ./iperf3 -s)

ip mptcp (route)