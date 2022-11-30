from ipmininet.iptopo import IPTopo

class MyEZTopo(IPTopo):
    """
            ______ R1 _____
          /                 \ 
         /                   \ 
        H1                   H2
         \                   /
          \ ______ R2 _____ /

    """

    def build(self, *args, **kwargs):
        params = {"bw":10}
        r1 = self.addRouter("r1")
        r2 = self.addRouter("r2")

        h1 = self.addHost("h1")
        h2 = self.addHost("h2")

        lh1r1, lh1r2 = self.addLinks((h1, r1, params), (h1, r2, params)) # links between H1 and routers
        lh2r1, lh2r2 = self.addLinks((h2, r1, params), (h2, r2, params)) # links between H2 and routers

        super().build(*args, **kwargs)
