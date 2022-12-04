from ipmininet.ipnet import IPNet
from topologies.simple_one_link_topo import SimpOneLinkTopo
import time
import os
import sys
import numpy as np

bandwidth = 10
n_iter = 10

size_from = 2
size_to = 20
size_step = 2

filename = "measurements/simple_link_different_sizes.txt"

net = IPNet(topo=SimpOneLinkTopo(bw=bandwidth), use_v6=False)
try:
    net.start()
    time.sleep(1)

    original_stdout = sys.stdout 
    with open(filename, 'w') as f:
        sys.stdout = f 
        print("total bandwidth : {:.10f} Mbits/sec, iterations : {:d}, sizes : arange({:d}, {:d} ,{:d})".format(bandwidth, n_iter, size_from, size_to, size_step))
        print("file_size[MB] iter total_transfert time goodput")
        sys.stdout = original_stdout

    h2ip = net["h2"].IP()

    cmd_server = "./rapido -c rsa/cert.pem -k rsa/key.pem {:s} 2142 >> measurements/simple_link_different_sizes_server_measurements.txt &".format(h2ip)

    for i in np.arange(size_from, size_to, size_step):
        for j in range(0, n_iter):
            time.sleep(1)
            cmd_client = "echo '{:d} {:d} '$(./rapido -s {:d} -n localhost {:s} 2142) >> {:s}".format(i, j, i, h2ip, filename)
            
            print("["+str(i)+"MB] Launch rapido")
            net["h2"].cmd(cmd_server)
            time.sleep(1)
            net["h1"].cmd(cmd_client)
        
    
finally:
    net.stop()