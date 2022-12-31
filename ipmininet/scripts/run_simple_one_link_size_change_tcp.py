from ipmininet.ipnet import IPNet
from topologies.simple_one_link_topo import SimpOneLinkTopo
from ipmininet.cli import IPCLI
import time
import os
import sys
import numpy as np

bandwidth = 10
n_iter = 15

size_from = 2
size_to = 21
size_step = 2

filename = "simple_link_different_sizes_tcp.txt"

script_path = os.path.realpath(os.path.dirname(__file__))
root_path = os.path.dirname(os.path.dirname(script_path))
rapido_path = os.path.join(root_path, "rapido_edit", "rapido-edit")
measurements_path = os.path.join(os.path.dirname(script_path), "measurements")

certif_path = os.path.join(script_path, "rsa", "cert.pem")
key_path = os.path.join(script_path, "rsa", "key.pem")

client_file = os.path.join(measurements_path, filename)
server_file = os.path.join(measurements_path, "server_{:s}".format(filename))

original_stdout = sys.stdout 
with open(client_file, 'w') as f:
    sys.stdout = f 
    print("total bandwidth : {:.10f} Mbits/sec, iterations : {:d}, sizes : arange({:d}, {:d} ,{:d})".format(bandwidth, n_iter, size_from, size_to, size_step))
    print("file_size[MB] iter time total_transfert goodput")
    sys.stdout = original_stdout

net = IPNet(topo=SimpOneLinkTopo(bw=bandwidth), use_v6=False)
try:
    net.start()

    time.sleep(1)    

    h2ip = net["h2"].IP()
    h1ip = net["h1"].IP()

    cmd_server = "iperf3 -s -1 &"
    net["h2"].cmd(cmd_server)

    for i in np.arange(size_from, size_to, size_step):
        for j in range(0, n_iter):
            time.sleep(1)
            net["h1"].cmd(cmd_server)

            cmd_client = "echo '{:d} {:d} '$(iperf3 -n {:d}M -c {:s} -f 'm' | tail -n 3 | grep 'receiver' | awk '{{ print $3,$5,$7 }}' | cut -d '-' --complement -f1) >> {:s}".format(i, j, i, h1ip, client_file)
            
            print("["+str(i)+"MB] Launch rapido")
            
            time.sleep(1)
            net["h2"].cmd(cmd_client)
        
    # IPCLI(net)
    
finally:
    net.stop()