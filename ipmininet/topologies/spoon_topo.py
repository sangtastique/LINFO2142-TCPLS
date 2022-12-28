from ipmininet.iptopo import IPTopo
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

class SpoonDouble(IPTopo):
    """
                  __________
                 /          \ 
        H1 ---- R1          H2
                 \__________/ 

        bw_parallel is expected to be [bw_top_link, bw_bot_link]
        delay_parallel is expected to be [delay_top_link, delay_bot_link]
    """
    def __init__( self, n_parallel, bw_handle, bw_parallel, delay_handle=None, delay_parallel=None, *args, **kwargs):
        
        self.switch_count = 0
        super().__init__(*args, **kwargs)

        r1 = self.addRouter("r1")

        h1 = self.addHost("h1")
        h2 = self.addHost("h2")

        # Add handle link
        if isinstance(delay_handle, str):
            h1r1 = self.addLink(h1, r1, bw=bw_handle, delay=delay_handle)
        else:
            h1r1 = self.addLink(h1, r1, bw=bw_handle)

        # Add parallel links
        if isinstance(delay_parallel, list):
            h2r1_1 = self.addLink(h2, r1, bw=bw_parallel[0], delay=delay_parallel[0])
            h2r1_2 = self.addLink(h2, r1, bw=bw_parallel[1], delay=delay_parallel[1])
        else:
            h2r1_1 = self.addLink(h2, r1, bw=bw_parallel[0])
            h2r1_2 = self.addLink(h2, r1, bw=bw_parallel[1])

    # We need at least 2ms of delay for accurate emulation
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
