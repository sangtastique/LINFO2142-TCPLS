from ipmininet.ipnet import IPNet
from topologies.simple_one_link_topo import SimpOneLinkTopo
import time
import os
import sys

net = IPNet(topo=SimpOneLinkTopo(), use_v6=False)
try:
    net.start()
    time.sleep(1)

    net["h2"].cmd("rm measurements/simple_link_different_sizes_server_measurements.txt")
    net["h1"].cmd("rm measurements/simple_link_different_sizes_client_measurements.txt")

    for i in range(1, 21):
        time.sleep(1)
        # net["h2"].cmd("echo '["+str(i)+"MB]' >> measurements/simple_link_different_sizes_server_measurements.txt")
        # net["h1"].cmd("echo '["+str(i)+"MB]' >> measurements/simple_link_different_sizes_client_measurements.txt")
        print("["+str(i)+"MB] Launch rapido server")
        net["h2"].cmd("./rapido -c rsa/cert.pem -k rsa/key.pem "+ net["h2"].IP() +" 2142 >> measurements/simple_link_different_sizes_server_measurements.txt &")
        print("["+str(i)+"MB] Launch rapido client\n")
        net["h1"].cmd("./rapido -s "+str(i)+" -n localhost "+ net["h2"].IP() +" 2142 >> measurements/simple_link_different_sizes_client_measurements.txt")
        
    
finally:
    net.stop()