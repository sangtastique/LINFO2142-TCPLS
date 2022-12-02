from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

class DoubleLink(IPTopo):
    """
                  __________
                 /          \ 
        H1 ---- R1          H2
                 \__________/ 

    """

    def build(self, *args, **kwargs):

        params20 = {"bw":20} # bw in Mbits/s
        params10 = {"bw":10}
        r1 = self.addRouter("r1")
        # r2 = self.addRouter("r2")
        # r3 = self.addRouter("r3")

        h1 = self.addHost("h1")
        h2 = self.addHost("h2")

        # self.addLinks((h1, r1, params20))
        # self.addLinks((r1, r2, params10), (r1, r3, params20))
        # self.addLinks((r2, h2, params10), (r3, h2, params20))
        # l1, l2, l3 = self.addLinks((h1, r1, params20), (h2, r1, params20), (h2, r1, params10))
        self.addLink(h1, r1, bw=60,)
        self.addLink(h2, r1, bw=30)
        self.addLink(h2, r1, bw=20)

        super().build(*args, **kwargs)

if __name__ == "__main__":
    net = IPNet(topo=DoubleLink(), use_v6=False)
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
