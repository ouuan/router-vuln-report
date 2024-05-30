## Description

The Redmi router model RB03 with firmware version 1.0.57 is vulnerable to TCP DoS or hijacking attacks. An attacker in the same WLAN as the victim can disconnect or hijack the traffic between the victim and any remote server by sending out forged TCP RST messages to evict NAT mappings in the router.

See the paper[^nat-rst] for more details about the vulnerability.

[^nat-rst]: Yang, Yuxiang, et al. "Exploiting Sequence Number Leakage: TCP Hijacking in NAT-Enabled Wi-Fi Networks." Network and Distributed System Security (NDSS) Symposium. 2024.

## CWE

CWE-940: Improper Verification of Source of a Communication Channel

## CVSS Score

`CVSS:4.0/AV:A/AC:L/AT:P/PR:L/UI:P/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N`

## Reproduction

Environment:

-   There are two hosts connecting to a Redmi RB03 router (AP) WiFi network.
-   One of the hosts is the attacker. It has the Scapy Python library installed.
-   The other host is the victim. It has netcat installed.
-   There is another remote server. It has netcat installed.

Here netcat is used to better illustrate the attack, but it is not required in a real attack.

Reproduction steps:

1.  On the remote server, run `nc -l -p 80`.
2.  On the victim machine, run `nc <remote server IP> -p 50005` to connect to the remote server with port 50005. (Here a fixed port is used, but it can be probed by the attacker in a real attach.)
3.  Now the remote server and the victim can send messages to each other.
4.  On the attacker machine, run the [PoC script](./forge_rst.py) to send out forged TCP RST messages to the AP.
5.  Wait a few seconds, and then the victim and the remote server are disconnected from each other in both directions. Netcat will exit when trying to send more messages.

This only demonstrates the core steps to disconnect the victim from the remote server. However, combined with other techniques, the attacker may hijack the traffic between the victim and the remote server and become a man-in-the-middle.

## Credit

Yufan You, Ke Xu, Yuxiang Yang, Qi Li, Xuewei Feng
