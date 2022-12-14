from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from topologies.spoon_topo import SpoonDouble
import numpy as np
import time
import os
import sys
import re

if __name__ == "__main__":

    transfert_size = 20

    ratio_start = 0
    ratio_end_excluded = 1.01
    ratio_step = 0.1
    ratios = np.arange(ratio_start, ratio_end_excluded, ratio_step)
    n_ratios = len(ratios)

    sum_bw = 10
    bw_handle = int(sum_bw * 1.1)
    n_iter = 15

    filename = "spoon_double_ratiobw.txt"

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
        print("handle bandwidth : {:.10f} Mbits/sec, total bandwidth of parallel links : {:.10f} Mbits/sec, considered rations : np.arange({:f}, {:f}, {:f}) iterations : {:d}".format(bw_handle, sum_bw, ratio_start, ratio_end_excluded, ratio_step, n_iter))
        print("ratio iter total_transfert time goodput")
        sys.stdout = original_stdout 

    print("handle bandwidth : {:.10f} Mbits/sec, total bandwidth of parallel links : {:.10f} Mbits/sec, considered ratios : np.arange({:f}, {:f}, {:f}) iterations : {:d}".format(bw_handle, sum_bw, ratio_start, ratio_end_excluded, ratio_step, n_iter))
    print("ratio iter total_transfert time goodput")

    for i in ratios:

        bw_top = i*sum_bw
        bw_bot = (1-i)*sum_bw

        net = IPNet(topo=SpoonDouble(2, bw_handle, [bw_top, bw_bot]), use_v6=False)
        try:
            net.start()
            time.sleep(1)
            h2eth0 = net["h2"].intf(intf="h2-eth0").ip
            if(not (bw_top == 0 or bw_bot == 0)):
                h2eth1 = net["h2"].intf(intf="h2-eth1").ip

                h2eth1_split = re.findall("\d+", h2eth1)

                # to make router's interface address
                last_r1h2eth1 = '1'
                if(h2eth1_split[3] == '1'):
                    last_r1h2eth1 = '2'

                cmd_rule_add = "ip rule add from " + h2eth1 + " table 1"
                cmd_route_add = "ip route add "+h2eth1_split[0]+"."+h2eth1_split[1]+"."+h2eth1_split[2]+".0/24 dev h2-eth1 scope link table 1"
                cmd_route_default = "ip route add default via "+h2eth1_split[0]+"."+h2eth1_split[1]+"."+h2eth1_split[2]+"."+last_r1h2eth1+" dev h2-eth1 table 1"

                net["h2"].cmd(cmd_rule_add)
                net["h2"].cmd(cmd_route_add)
                net["h2"].cmd(cmd_route_default)

                cmd_serv = "{:s} -c {:s} -k {:s} -a {:s} {:s} 2142 >> {:s} &".format(rapido_path, certif_path, key_path, h2eth1, h2eth0, server_file)
                # ./rapido -c rsa/cert.pem -k rsa/key.pem -a 192.168.2.1 h2 2142
                # ./rapido -s 40 -n localhost h2 2142
                cmd_client = "{:s} -s {:d} -n localhost {:s} 2142".format(rapido_path, transfert_size, h2eth0)
            else:
                # There's only one link !!
                cmd_serv = "./rapido -c rsa/cert.pem -k rsa/key.pem {:s} 2142 >> measurements/spoon_double_ratiobw_server.txt &".format( h2eth0)

                cmd_client = "./rapido -s {:d} -n localhost {:s} 2142".format(transfert_size, h2eth0)

            for j in range(0, n_iter):
                time.sleep(1)
                print("[iter "+str(j)+", ratio = "+str(i)+" top = "+str(bw_top)+", bot = "+str(bw_bot)+"] Launch rapido")

                net["h2"].cmd(cmd_serv) 

                time.sleep(1)

                net["h1"].cmd("echo '{:.3f} {:d} '$({:s}) >> {:s}".format(i, j, cmd_client, client_file))

            # IPCLI(net)
                
        except Exception as e:
            print("error !" + str(e))
        finally:
            net.stop()