## Description

The Redmi router model RB03 with firmware version 1.0.57 is vulnerable to forged ICMP redirect message attacks. An attacker in the same WLAN as the victim can hijack the traffic between the victim and any remote server by sending out forged ICMP redirect messages.

See the paper[^icmp-redirect] for more details about the vulnerability.

[^icmp-redirect]: Feng, Xuewei, et al. "Man-in-the-middle attacks without rogue ap: When wpas meet icmp redirects." 2023 IEEE Symposium on Security and Privacy (SP). IEEE, 2023.

## CWE

CWE-940: Improper Verification of Source of a Communication Channel

## CVSS Score

`CVSS:4.0/AV:A/AC:L/AT:P/PR:L/UI:P/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N`

## Reproduction

Environment:

-   There are two hosts connecting to a Redmi RB03 router (AP) WiFi network.
-   One of the hosts is the attacker. It has the Scapy Python library installed.
-   The other host is the victim. It should be running Linux.
-   On the victim machine, `sysctl net.ipv4.conf.all.accept_redirects` and `sysctl net.ipv4.conf.<interface_name>.accept_redirects` are set to 1. (This is the default setting on Linux if no further configuration is provided.)

Reproduction steps:

1.  On the victim machine, run `ping 93.184.215.14` or visit <http://example.com> to see the normal responses before the attack. Run `ip route get 93.184.215.14` to see the normal routing.
2.  Before the attack, the attacker cannot sniff the ping/HTTP packets in step 1 thanks to the protection provided by WPA.
3.  On the attacker machine, run the [PoC script](./forge_redirect.py) to send the forged ICMP redirect messages through the AP to the victim.
4.  The victim machine will receive the forged ICMP redirect message in step 3. This can be confirmed in Wireshark.
5.  On the victim machine, run `ip route get 93.184.215.14` to see that the gateway has been changed to the attacker:
6.  On the victim machine, run `ping 93.184.215.14` or visit <http://example.com>.
7.  Now the attacker can sniff the packets sent by the victim to 93.184.215.14 in Wireshark, because they are forwarded to the attacker as the next-hop (gateway).

This only demonstrates the core steps to hijack the routing from the victim to the remote server and sniff outgoing packets. However, combined with other techniques, the attacker may completely hijack the traffic between the victim and the remote server and become a man-in-the-middle.

## Workaround

Before this vulnerability is fixed by the upstream, users may disable accepting ICMP redirect messages in the their hosts. On Linux, this is to set `sysctl net.ipv4.conf.all.accept_redirects` and `sysctl net.ipv4.conf.<interface_name>.accept_redirects` to 0.

## Credit

Yufan You, Ke Xu, Xuewei Feng, Qi Li, Yuxiang Yang
