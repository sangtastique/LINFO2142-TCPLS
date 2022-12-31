from ipmininet.ipnet import IPNet
from topologies.simple_one_link_topo import SimpOneLinkTopo
from ipmininet.cli import IPCLI
import time
import os
import sys
import numpy as np

n_iter = 30
transfert_size = 10
bw = 5
delay_from = 110
delay_to = 201
delay_step = 15

filename = "simple_link_different_delay.txt"

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

        cmd_server = "{:s} -c {:s} -k {:s} {:s} 2142 >> {:s} &".format(rapido_path, certif_path, key_path, h2ip, server_file)

        for j in range(0, n_iter):
            time.sleep(1)
            cmd_client = "echo '{:d} {:d} {:d} '$({:s} -s {:d} -n localhost {:s} 2142) >> {:s}".format(delay, bw, j, rapido_path, transfert_size, h2ip, client_file)
            
            print("["+str(delay)+"ms] Launch rapido")
            net["h2"].cmd(cmd_server)
            time.sleep(1)
            net["h1"].cmd(cmd_client)
            
        # IPCLI(net)
        
    finally:
        net.stop()