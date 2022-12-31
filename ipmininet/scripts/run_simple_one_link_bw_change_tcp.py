from ipmininet.ipnet import IPNet
from topologies.simple_one_link_topo import SimpOneLinkTopo
from ipmininet.cli import IPCLI
import time
import os
import sys
import numpy as np

n_iter = 15
transfert_size = 20
bw_from = 5
bw_to = 101
bw_step = 5

filename = "simple_link_different_bw_tcp.txt"

script_path = os.path.realpath(os.path.dirname(__file__))
root_path = os.path.dirname(os.path.dirname(script_path))
measurements_path = os.path.join(os.path.dirname(script_path), "measurements")

client_file = os.path.join(measurements_path, filename)
server_file = os.path.join(measurements_path, "server_{:s}".format(filename))

original_stdout = sys.stdout 
with open(client_file, 'w') as f:
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
        h1ip = net["h1"].IP()

        cmd_server = "iperf3 -s -1 &"

        for j in range(0, n_iter):
            time.sleep(1)

            net["h1"].cmd(cmd_server)

            cmd_client = "echo '{:d} {:d} '$(iperf3 -n {:d}M -c {:s} -f 'm' | tail -n 3 | grep 'receiver' | awk '{{ print $5,$3,$7 }}' | cut -d '-' --complement -f1) >> {:s}".format(bwdth, j, transfert_size, h1ip, client_file)

            print("["+str(bwdth)+"Mb] Launch rapido")
            time.sleep(1)
            net["h2"].cmd(cmd_client)
            
        
    finally:
        net.stop()