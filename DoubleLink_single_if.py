from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

class DoubleLink(IPTopo):

    """
               10
              ____
            /      \    30
          H1        R1 ---- H2
            \ ____ /
               10

    """

    def build(self, *args, **kwargs):

        params30 = {"bw":5, "delay":"20ms"} # bw in Mbits
        params10 = {"bw":1, "delay":"20ms"}
        r1 = self.addRouter("r1")

        h1 = self.addHost("h1")
        h2 = self.addHost("h2")

        self.addLinks((h1, r1, params10), (h1, r1, params10), (r1, h2, params30))

        super().build(*args, **kwargs)

if __name__ == "__main__":
    net = IPNet(topo=DoubleLink())
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
