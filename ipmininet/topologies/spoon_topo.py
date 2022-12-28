from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

class SpoonDouble(IPTopo):
    """
                  __________
                 /          \ 
        H1 ---- R1          H2
                 \__________/ 

    """
    def __init__( self, n_parallel, bw_handle, bw_parallel ):

        # Initialize topology
        IPTopo.__init__( self )

        # self.bw_handle = bw_handle
        # self.bw_parallel = bw_parallel
        r1 = self.addRouter("r1")

        h1 = self.addHost("h1")
        h2 = self.addHost("h2")

        # lr1r2 = self.addLink(r1, r2)
        # lr1r2[r1].addParams(ip=("2042:12::1/64", "10.12.0.1/24"))
        # lr1r2[r2].addParams(ip=("2042:12::2/64", "10.12.0.2/24"))

        h1r1 = self.addLink(h1, r1, bw=bw_handle)
        # h1r1[h1].addParams(ip="10.0.0.1")
        if(bw_parallel[0] != 0):
            h2r1_1 = self.addLink(h2, r1, bw=bw_parallel[0])
        if(bw_parallel[1] != 0):
            h2r1_2 = self.addLink(h2, r1, bw=bw_parallel[1])


    # def build(self, *args, **kwargs):

        # r1 = self.addRouter("r1")

        # h1 = self.addHost("h1")
        # h2 = self.addHost("h2")

        # # lr1r2 = self.addLink(r1, r2)
        # # lr1r2[r1].addParams(ip=("2042:12::1/64", "10.12.0.1/24"))
        # # lr1r2[r2].addParams(ip=("2042:12::2/64", "10.12.0.2/24"))

        # h1r1 = self.addLink(h1, r1, bw=self.bw_handle)
        # # h1r1[h1].addParams(ip="10.0.0.1")
        # self.addLink(h2, r1, bw=self.bw_parallel[0])
        # self.addLink(h2, r1, bw=self.bw_parallel[1])

        # super().build(*args, **kwargs)

if __name__ == "__main__":
    net = IPNet(topo=SpoonDouble(2, 20, [5, 5]), use_v6=False)
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
