from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from topologies.spoon_topo import SpoonDouble
import numpy as np
import time
import os
import sys
import re

if __name__ == "__main__":

    transfert_size = 10

    handle_delay = 10
    top_delay = 10
    coef_bot_delay_start = 0.2
    coef_bot_delay_end_excluded = 3.1
    coef_bot_delay_step = 0.2

    ratios = np.arange(coef_bot_delay_start, coef_bot_delay_end_excluded, coef_bot_delay_step)
    n_ratios = len(ratios)

    bw_top = 5
    bw_bot = 5
    bw_handle = int((bw_bot+bw_top) * 2)
    n_iter = 2

    filename = "measurements/spoon_double_ratiodelay.txt"
    original_stdout = sys.stdout 
    with open(filename, 'w') as f:
        sys.stdout = f 
        print("Transfert size : {:f}, handle bandwidth : {:.10f} Mbits/sec, bandwidth of top link : {:.10f} Mbits/sec, bandwidth of bot link : {:.10f} Mbits/sec, handle delay : {:f} ms, top delay : {:f} ms, considered bot delay ratios relative to top delay : np.arange({:f}, {:f}, {:f}) iterations : {:d}".format(transfert_size, bw_handle, bw_top, bw_bot, handle_delay, top_delay, coef_bot_delay_start, coef_bot_delay_end_excluded, coef_bot_delay_step, n_iter))
        print("ratio iter total_transfert time goodput")
        sys.stdout = original_stdout 

    print("Transfert size : {:f}, handle bandwidth : {:.10f} Mbits/sec, bandwidth of top link : {:.10f} Mbits/sec, bandwidth of bot link : {:.10f} Mbits/sec, handle delay : {:f} ms, top delay : {:f} ms, considered bot delay ratios relative to top delay : np.arange({:f}, {:f}, {:f}) iterations : {:d}".format(transfert_size, bw_handle, bw_top, bw_bot, handle_delay, top_delay, coef_bot_delay_start, coef_bot_delay_end_excluded, coef_bot_delay_step, n_iter))
    print("ratio iter total_transfert time goodput")

    for i in ratios:

        bot_delay = i*top_delay

        net = IPNet(topo=SpoonDouble(2, bw_handle, [bw_top, bw_bot], delay_handle=handle_delay, delay_parallel=[top_delay, bot_delay]), use_v6=False)
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

            cmd_serv = "./rapido -c rsa/cert.pem -k rsa/key.pem -a {:s} {:s} 2142 >> measurements/spoon_double_ratiodelay_server.txt &".format(h2eth1, h2eth0)
            # ./rapido -c rsa/cert.pem -k rsa/key.pem -a 192.168.2.1 h2 2142
            # ./rapido -s 40 -n localhost h2 2142
            cmd_client = "./rapido -s {:d} -n localhost {:s} 2142".format(transfert_size, h2eth0)
            print("Waiting 15 sec for switches to boot")
            time.sleep(25)

            for j in range(0, n_iter):
                time.sleep(1)
                print("[iter "+str(j)+", ratio = "+str(i)+" top = "+str(bw_top)+", bot = "+str(bw_bot)+"] Launch rapido")

                net["h2"].cmd(cmd_serv) 

                time.sleep(1)

                net["h1"].cmd("echo '{:.3f} {:d} '$({:s}) >> {:s}".format(i, j, cmd_client, filename))

            # IPCLI(net)
                
        except Exception as e:
            print("error !" + str(e))
        finally:
            net.stop()