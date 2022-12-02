from ipmininet.iptopo import IPTopo
from ipmininet.router.config import SSHd
from ipmininet.host.config import Named

class SimpOneLinkTopo(IPTopo):
    """

        H1 ---- R ---- H2

    """

    def build(self, *args, **kwargs):
        params = {"bw":10}
        r = self.addRouter("r")

        h1 = self.addHost("h1")
        h1.addDaemon(Named)
        h2 = self.addHost("h2")
        h2.addDaemon(Named)

        lh1r, lh2r = self.addLinks((h1, r, params), (h2, r, params)) # links between H1 and routers

        super().build(*args, **kwargs)
