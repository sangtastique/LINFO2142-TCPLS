from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from topologies.spoon_topo import SpoonDouble
import numpy as np
import time
import os
import sys
import re

if __name__ == "__main__":

    transfert_size = 30

    ratio_start = 0.5
    ratio_end_excluded = 0.6
    ratio_step = 0.1
    ratios = np.arange(ratio_start, ratio_end_excluded, ratio_step)
    n_ratios = len(ratios)

    sum_bw = 10
    bw_handle = int(sum_bw * 2)
    n_iter = 2

    print("handle bandwidth : {:.10f} Mbits/sec, total bandwidth of parallel links : {:.10f} Mbits/sec, considered rations : np.arange({:f}, {:f}, {:f}) iterations : {:d}".format(bw_handle, sum_bw, ratio_start, ratio_end_excluded, ratio_step, n_iter))
    print("ratio iter goodput")

    for i in ratios:

        bw_top = i*sum_bw
        bw_bot = (1-i)*sum_bw

        net = IPNet(topo=SpoonDouble(2, bw_handle, [bw_top, bw_bot]), use_v6=False)
        try:
            net.start()
            time.sleep(1)

            h2eth0 = net["h2"].intf(intf="h2-eth0").ip
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

            cmd_serv = "./rapido -c rsa/cert.pem -k rsa/key.pem -a {:s} {:s} 2142 >> measurements/spoon_double_ratiobw_server.txt &".format(h2eth1, h2eth0)
            # ./rapido -c rsa/cert.pem -k rsa/key.pem -a 192.168.2.1 h2 2142
            # ./rapido -s 40 -n localhost h2 2142
            cmd_client = "./rapido -s {:d} -n localhost {:s} 2142".format(transfert_size, h2eth0)

            for j in range(0, n_iter):

                print("[iter "+str(j)+", ratio = "+str(i)+" top = "+str(bw_top)+", bot = "+str(bw_bot)+"] Launch rapido")

                net["h2"].cmd(cmd_serv) 

                time.sleep(1)

                net["h1"].cmd("echo '{:.3f} {:d} '$({:s}) >> measurements/spoon_double_ratiobw_client.txt".format(i, j, cmd_client))

            # IPCLI(net)
                
        except Exception as e:
            print("error !" + str(e))
        finally:
            net.stop()