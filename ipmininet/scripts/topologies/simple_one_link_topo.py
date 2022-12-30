from ipmininet.iptopo import IPTopo
from ipmininet.router.config import SSHd
from ipmininet.host.config import Named
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

class SimpOneLinkTopo(IPTopo):
    """

        H1 ---- R ---- H2

    """
    def __init__( self, bw=10, delay=None, *args, **kwargs):
        self.switch_count = 0
        super().__init__(*args, **kwargs)

        if(delay==None):
            params = {"bw":bw}
        else:
            params = {"bw":bw, "delay":"{:d}ms".format(delay)}

        r = self.addRouter("r1")

        h1 = self.addHost("h1")
        h2 = self.addHost("h2")

        lh1r, lh2r = self.addLinks((h1, r, params), (h2, r, params))

    # def addLink(self, node1, node2, delay="2ms", bw=None,
    #             max_queue_size=None, **opts):
    #     src_delay = None
    #     dst_delay = None
    #     opts1 = dict(opts)
    #     if "params2" in opts1:
    #         opts1.pop("params2")
    #     try:
    #         src_delay = opts.get("params1", {}).pop("delay")
    #     except KeyError:
    #         pass
    #     opts2 = dict(opts)
    #     if "params1" in opts2:
    #         opts2.pop("params1")
    #     try:
    #         dst_delay = opts.get("params2", {}).pop("delay")
    #     except KeyError:
    #         pass

    #     src_delay = src_delay if src_delay else delay
    #     dst_delay = dst_delay if dst_delay else delay

    #     # node1 -> switch
    #     default_params1 = {"bw": bw}
    #     default_params1.update(opts.get("params1", {}))
    #     opts1["params1"] = default_params1

    #     # node2 -> switch
    #     default_params2 = {"bw": bw}
    #     default_params2.update(opts.get("params2", {}))
    #     opts2["params2"] = default_params2

    #     # switch -> node1
    #     opts1["params2"] = {"delay": dst_delay,
    #                         "max_queue_size": max_queue_size}
    #     # switch -> node2
    #     opts2["params1"] = {"delay": src_delay,
    #                         "max_queue_size": max_queue_size}

    #     # Netem queues will mess with shaping
    #     # Therefore, we put them on an intermediary switch
    #     self.switch_count += 1
    #     s = "s%d" % self.switch_count
    #     self.addSwitch(s)
    #     return super().addLink(node1, s, **opts1), \
    #            super().addLink(s, node2, **opts2)


    # # def build(self, *args, **kwargs):
    # #     params = {"bw":10}
    # #     r = self.addRouter("r")

    # #     h1 = self.addHost("h1")
    # #     h1.addDaemon(Named)
    # #     h2 = self.addHost("h2")
    # #     h2.addDaemon(Named)

    # #     lh1r, lh2r = self.addLinks((h1, r, params), (h2, r, params)) # links between H1 and routers

    # #     super().build(*args, **kwargs)

if __name__ == "__main__":
    net = IPNet(topo=SimpOneLinkTopo(bw=10, use_v6=False))
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
