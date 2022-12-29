from ipmininet.ipnet import IPNet
from topologies.simple_one_link_topo import SimpOneLinkTopo
from ipmininet.cli import IPCLI
import time
import os
import sys
import numpy as np

n_iter = 10
transfert_size = 10
bw_from = 2
bw_to = 20
bw_step = 2

filename = "measurements/simple_link_different_bw.txt"

original_stdout = sys.stdout 

script_path = os.path.realpath(os.path.dirname(__file__))
root_path = os.path.dirname(os.path.dirname(script_path))
rapido_path = os.path.join(root_path, "rapido_edit", "rapido-edit")

with open(filename, 'w') as f:
    sys.stdout = f 
    print("transfert size : {:.10f} MB, iterations : {:d}, max bandwidths : arange({:d}, {:d} ,{:d})".format(transfert_size, n_iter, bw_from, bw_to, bw_step))
    print("max_bw iter total_transfert time goodput")
    sys.stdout = original_stdout

for bwdth in np.arange(bw_from, bw_to, bw_step):
    time.sleep(1)
    net = IPNet(topo=SimpOneLinkTopo(bw=bwdth), use_v6=False)

    try:
        net.start()

        time.sleep(1)

        h2ip = net["h2"].IP()

        cmd_server = "{:s} -c rsa/cert.pem -k rsa/key.pem {:s} 2142 >> measurements/simple_link_different_bw_server_measurements.txt &".format(rapido_path, h2ip)

        for j in range(0, n_iter):
            time.sleep(1)
            cmd_client = "echo '{:d} {:d} '$({:s} -s {:d} -n localhost {:s} 2142) >> {:s}".format(bwdth, j, rapido_path, transfert_size, h2ip, filename)
            
            print("["+str(bwdth)+"MB] Launch rapido")
            net["h2"].cmd(cmd_server)
            time.sleep(1)
            net["h1"].cmd(cmd_client)
            
        # IPCLI(net)
        
    finally:
        net.stop()