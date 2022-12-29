from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from topologies.ez_topo import MyEZTopo

net = IPNet(topo=MyEZTopo(), use_v6=False)
try:
    net.start()
    IPCLI(net)
finally:
    net.stop()