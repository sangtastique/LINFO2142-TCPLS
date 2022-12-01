from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

class DoubleLink(IPTopo):

    def build(self, *args, **kwargs):

        params20 = {"bw":20} # bw in Mbits
        params10 = {"bw":10}
        r1 = self.addRouter("r1")

        h1 = self.addHost("h1")
        h2 = self.addHost("h2")

        self.addLinks((h1, r1, params10), (h1, r1, params10), (h2, r1, params20))

        super().build(*args, **kwargs)

if __name__ == "__main__":
    net = IPNet(topo=DoubleLink())
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
