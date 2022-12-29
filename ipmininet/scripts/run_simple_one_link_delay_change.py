from ipmininet.ipnet import IPNet
from topologies.simple_one_link_topo import SimpOneLinkTopo
from ipmininet.cli import IPCLI
import time
import os
import sys
import numpy as np

n_iter = 30
transfert_size = 10
bw = 10
delay_from = 5
delay_to = 100
delay_step = 15

filename = "measurements/simple_link_different_delay.txt"

original_stdout = sys.stdout 
with open(filename, 'w') as f:
    sys.stdout = f 
    print("transfert size : {:.10f} MB, iterations : {:d}, delays : arange({:d}, {:d} ,{:d}), bw : {:d}".format(transfert_size, n_iter, delay_from, delay_to, delay_step, bw))
    print("delay bw iter total_transfert time goodput")
    sys.stdout = original_stdout

for delay in np.arange(delay_from, delay_to, delay_step):
    time.sleep(1)
    net = IPNet(topo=SimpOneLinkTopo(bw=bw, delay=delay), use_v6=False)

    try:
        net.start()

        time.sleep(1)

        h2ip = net["h2"].IP()

        cmd_server = "./rapido -c rsa/cert.pem -k rsa/key.pem {:s} 2142 >> measurements/simple_link_different_bw_server_measurements.txt &".format(h2ip)

        for j in range(0, n_iter):
            time.sleep(1)
            cmd_client = "echo '{:d} {:d} {:d} '$(./rapido -s {:d} -n localhost {:s} 2142) >> {:s}".format(delay, bw, j, transfert_size, h2ip, filename)
            
            print("["+str(delay)+"ms] Launch rapido")
            net["h2"].cmd(cmd_server)
            time.sleep(1)
            net["h1"].cmd(cmd_client)
            
        # IPCLI(net)
        
    finally:
        net.stop()