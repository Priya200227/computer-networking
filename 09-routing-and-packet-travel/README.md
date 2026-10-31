# Routing and How Packets Travel Across Networks

**Video reference:** [How Routing Determines Your Data's Journey Across Networks](https://youtu.be/GBhaNXK-ows?si=MQEk14etHW1qwOwW)

## Learning objectives

By the end of this section, you should be able to explain how hosts decide whether a destination is local or remote, how ARP resolves a local IPv4 next hop, how switches forward Ethernet frames, how routers forward IP packets, why MAC addresses change at routed hops, and how these principles apply to a simplified Internet-to-AWS example.

## Contents

1. [Core idea](#1-core-idea)
2. [Routing overview](#2-routing-overview)
3. [Devices and tables](#3-devices-and-tables)
4. [Scenario A — A to D on the same subnet](#4-scenario-a--a-to-d-on-the-same-subnet)
5. [Scenario B — C to X on another subnet](#5-scenario-b--c-to-x-on-another-subnet)
6. [Scenario C — C to a remote AWS EC2 instance](#6-scenario-c--c-to-a-remote-aws-ec2-instance)
7. [What changes at each hop?](#7-what-changes-at-each-hop)
8. [Important corrections and nuances](#8-important-corrections-and-nuances)
9. [Troubleshooting checklist](#9-troubleshooting-checklist)
10. [Quick revision](#10-quick-revision)
11. [Self-check questions](#11-self-check-questions)
12. [Reliable references](#12-reliable-references)

---

## 1. Core idea

**Routing selects the next hop and outgoing interface for an IP packet so it can move toward its destination network.** A router usually does not calculate the entire end-to-end path for each packet. It makes a local forwarding decision using its routing/forwarding information.

| Function | Question answered | Typical mechanism/device |
|---|---|---|
| Address resolution | Which link-layer address reaches this local next hop? | ARP for IPv4 on Ethernet |
| Switching | Which local port should receive this frame? | Ethernet switch and MAC address table |
| Routing/forwarding | Which interface or next hop should receive this IP packet? | IP router and forwarding table |

A host uses its IP address and subnet prefix/mask to decide whether a destination is on-link. If the destination is local, the host sends a frame to the destination host's MAC address. If it is off-link, the host sends the frame to its configured default gateway's MAC address. The IP packet remains addressed to the final destination IP unless a function such as NAT changes it.

## 2. Routing overview

![Routing overview across a LAN, router, Internet hops, and an AWS network](images/01-routing-overview.png)

The overview contains:
- **Network 1:** hosts A, B, C and D connected through a switch. Example IP addresses include `10.0.0.2`, `10.0.0.3`, `10.0.0.4`, and `10.0.0.5`.
- **Router:** connects Network 1 (`10.0.0.1`) and Network 2 (`192.168.1.1`).
- **Network 2:** includes host X (`192.168.1.5`).
- **Internet/cloud path:** shows the concept of forwarding through multiple routers toward a remote AWS-hosted destination.

All addresses and devices are illustrative. This is a learning diagram, not a real routing table or a literal map of the Internet or AWS infrastructure.

## 3. Devices and tables

### 3.1 Ethernet switch

A typical Layer 2 switch learns source-MAC-to-port mappings and uses its MAC address table to forward known unicast frames to the appropriate port. If a destination MAC is unknown, it generally floods the frame within the VLAN (except the incoming port). Broadcast frames are also flooded within the VLAN.

A normal Ethernet switch does not choose Internet routes based on the destination IP address. Its ordinary Layer 2 forwarding decision uses the destination MAC address.

### 3.2 Router and routing table

A router connects IP networks. For a packet that must be forwarded, it examines the destination IP and uses its forwarding information to select an outgoing interface and, where necessary, a next-hop IP address. When multiple routes match, IP routers use the **longest matching prefix**.

Illustrative route-table entries might look like this:

| Destination prefix | Target | Meaning |
|---|---|---|
| `10.0.0.0/24` | Connected interface | Network 1 is directly connected |
| `192.168.1.0/24` | Connected interface | Network 2 is directly connected |
| `0.0.0.0/0` | Upstream next hop | Default route if no more-specific route matches |

These are examples only, not the exact configuration shown in the image.

### 3.3 Default gateway

A default gateway is the first-hop router a host uses for off-link destinations when no more-specific route applies. A host normally needs a suitable IP address, subnet prefix/mask, and default gateway to communicate outside its local subnet.

### 3.4 ARP — Address Resolution Protocol

ARP discovers the link-layer address associated with an IPv4 address on the local link. Devices cache learned mappings in an ARP cache/table.

**Critical distinction:** ARP does not discover a remote Internet server's MAC address. ARP requests are local-link broadcasts and are not forwarded by routers as ordinary routed traffic. For an off-subnet destination, a host usually ARPs for the default gateway's MAC address. The router may then use ARP on its own outgoing Ethernet link to resolve the next hop there.

ARP is for IPv4. IPv6 uses Neighbor Discovery (NDP), not ARP.

## 4. Scenario A — A to D on the same subnet

![Scenario A: A sends to D on the same local network and uses ARP if needed](images/02-same-network-arp-a-to-d.png)

Example addresses in the diagram:
- A: `10.0.0.3`
- D: `10.0.0.5`
- B: `10.0.0.2`
- C: `10.0.0.4`

Assume A's subnet prefix says D is on the same subnet.

1. **A checks the destination IP.** A compares `10.0.0.5` with its own subnet and determines D is on-link.
2. **A checks its ARP cache.** If it has a valid mapping for `10.0.0.5`, it can use it. Otherwise, A broadcasts an ARP request asking which device owns that IP.
3. **D replies.** D provides its MAC address; A caches the mapping.
4. **A builds a frame.** Ethernet source MAC = A's MAC; Ethernet destination MAC = D's MAC. The encapsulated IP packet has source IP `10.0.0.3` and destination IP `10.0.0.5`.
5. **The switch forwards the frame.** It uses its MAC address table to select D's port.
6. **D receives the frame.** D processes the Ethernet frame, then the IP packet and its payload.

| Field | Value/meaning |
|---|---|
| IP source | `10.0.0.3` (A) |
| IP destination | `10.0.0.5` (D) |
| Ethernet source MAC | A's MAC |
| Ethernet destination MAC | D's MAC |

The default gateway is not part of the ordinary forwarding path for this same-subnet exchange. ARP is skipped if A already has a usable cache entry.

## 5. Scenario B — C to X on another subnet

![Scenario B: C sends to X on a different subnet through the default gateway](images/03-cross-network-arp-c-to-x.png)

Example addresses:
- C in Network 1: `10.0.0.4`
- Router's Network 1 interface: `10.0.0.1`
- Router's Network 2 interface: `192.168.1.1`
- X in Network 2: `192.168.1.5`

1. **C checks X's IP.** Using its subnet mask/prefix, C determines that `192.168.1.5` is off-link.
2. **C chooses its default gateway.** It sends the packet toward `10.0.0.1`.
3. **C resolves the gateway MAC.** If necessary, C ARPs for `10.0.0.1`—not for X's MAC across Network 1.
4. **C sends the first-hop frame.** Ethernet destination MAC = router's Network 1 MAC. The IP source and destination remain `10.0.0.4` and `192.168.1.5` in this no-NAT example.
5. **The router receives the frame.** It removes the incoming link-layer framing and examines the IP packet.
6. **The router looks up the destination.** Its forwarding table indicates that Network 2 is directly connected (assuming the example topology).
7. **The router resolves X's MAC if needed.** It uses ARP on Network 2 for `192.168.1.5`, unless a valid cache entry already exists.
8. **The router creates a new frame.** Ethernet source MAC = router's Network 2 interface MAC; Ethernet destination MAC = X's MAC.
9. **X receives the packet.** X processes the frame and the enclosed IP packet.

### Why do MAC addresses change but IP addresses usually do not?

MAC addresses deliver frames over a single local link. A router terminates the incoming link-layer frame and creates a new frame for the outgoing link. Therefore, link-layer source and destination addresses are local to each link.

IP source and destination addresses normally identify the end hosts across routed networks. Ordinary routing does not replace them at each hop. However, routers decrement IPv4 TTL and update the IPv4 header checksum. NAT and other middleboxes can also change IP addresses or transport ports.

| Link | Ethernet source MAC | Ethernet destination MAC | IP source | IP destination |
|---|---|---|---|---|
| C → router on Network 1 | C's MAC | Router's Network 1 MAC | `10.0.0.4` | `192.168.1.5` |
| Router → X on Network 2 | Router's Network 2 MAC | X's MAC | `10.0.0.4` | `192.168.1.5` |

The actual hexadecimal MAC addresses are not supplied in the diagrams; the names above are conceptual.

## 6. Scenario C — C to a remote AWS EC2 instance

![Scenario C: C sends toward a remote AWS EC2 instance through Internet routers](images/04-internet-and-aws-ec2-routing.png)

This is a simplified illustration of a local host sending traffic through an upstream network and multiple Internet routers toward a remote cloud-hosted destination. Addresses such as `2.3.4.5` and `3.4.5.6` are examples in the diagram, not real AWS configuration details.

1. **C determines the destination is off-link.** It sends the first frame to its default gateway.
2. **C resolves the local gateway.** It uses a cached ARP mapping or ARPs for the router's local interface.
3. **The edge router forwards upstream.** It consults its forwarding table and selects a next hop. If NAT is configured, the edge device may translate the private source IP to a public IP and may translate transport ports as well.
4. **Upstream routers forward the packet.** Each router uses its own forwarding information. The actual path depends on routing policies, topology, and current network conditions.
5. **Link-layer framing is rebuilt at each routed Ethernet hop.** A remote server's MAC address is not carried end-to-end over the Internet.
6. **The packet travels through multiple networks.** The diagram's intermediate routers are conceptual placeholders, not named or guaranteed Internet devices.
7. **The destination cloud network receives the traffic.** Cloud routing and network controls determine how the packet reaches the intended virtual network and instance interface.
8. **The final link delivers the frame to the destination interface.** IP addresses remain the same unless a NAT or other middlebox changes them.

### How this relates to AWS

In Amazon VPC, route tables map destination prefixes to targets. A public subnet can have a default IPv4 route (`0.0.0.0/0`) pointing to an Internet Gateway. A private subnet commonly uses a NAT Gateway or another configured egress path when instances need outbound IPv4 Internet access.

An Internet Gateway route alone does not make every instance reachable. Public addressing, subnet routing, security groups, network ACLs, host configuration, and other controls matter. AWS networking is virtualized and managed; this diagram is not an exact representation of AWS's internal network.

## 7. What changes at each hop?

For ordinary routed IPv4 traffic **without NAT**:

- **Ethernet frame:** removed on ingress and rebuilt for the outgoing link. MAC addresses change from one Ethernet hop to the next.
- **IP source and destination:** generally remain the same end-to-end.
- **IPv4 TTL:** decremented by every router that forwards the packet. When TTL reaches zero, the packet is discarded; an ICMP Time Exceeded message may be generated.
- **IPv4 header checksum:** updated when the IPv4 header changes, including TTL.
- **NAT:** can change source and/or destination IP addresses and often transport ports.
- **Middleboxes:** firewalls, proxies, load balancers, and tunnels can inspect, modify, or encapsulate traffic according to their roles.

| Field | Same-subnet A → D | Routed C → X | Internet path with NAT |
|---|---|---|---|
| Ethernet MAC addresses | A MAC → D MAC | Rebuilt at router | Rebuilt on each Ethernet hop |
| IP source/destination | A IP → D IP | Usually C IP → X IP | May change at NAT boundaries |
| IPv4 TTL | No router decrement if no router is traversed | Decremented by each router | Decremented by each forwarding router |
| ARP | Local LAN only | Used on each Ethernet link as needed | Not end-to-end; local next hops are resolved per link |

## 8. Important corrections and nuances

1. **ARP resolves a local next hop.** For a remote destination, the host normally ARPs for its default gateway, not the remote host's MAC.
2. **Routers do not forward the same Ethernet frame unchanged.** They process the IP packet and create new link-layer framing for the outgoing interface.
3. **“IP addresses never change” is too absolute.** They usually remain unchanged during ordinary routing, but NAT, proxies, and tunnels can change or encapsulate addressing. IPv4 TTL changes at each routed hop.
4. **Routers do not need to discover the complete route for every packet.** Routing protocols/configuration populate routing information; forwarding uses the resulting table.
5. **Switching is more than reading a destination MAC.** Switches learn source MAC-to-port mappings and forward using their MAC table. Unknown-unicast and broadcast handling depends on VLAN and switch configuration.
6. **The subnet mask/prefix matters.** Similar-looking IP addresses do not by themselves prove that hosts are on the same subnet.
7. **NAT and routing are different functions.** Routing selects a next hop; NAT translates address/port information. A device can perform both.
8. **The return path may differ.** Internet routing can be asymmetric; successful request delivery does not by itself guarantee a working response path.
9. **AWS is not one ordinary LAN behind a single router.** VPC routes, gateways, virtual interfaces, security controls, and managed infrastructure all matter.
10. **ARP caches are dynamic.** A host does not need a permanent entry for every device on its subnet; entries can be learned, refreshed, and expire.

## 9. Troubleshooting checklist

1. Is the host's IP address and subnet prefix/mask correct?
2. Does the destination fall inside or outside the local subnet?
3. If off-link, is the default gateway configured and reachable?
4. Can the host resolve the local destination MAC or next-hop MAC?
5. Are switch ports, VLANs, and link state correct?
6. Does the router have a matching route, and is the next hop reachable?
7. Is there a return route from the destination network?
8. Could a firewall, security group, network ACL, or host firewall block the traffic?
9. If NAT is expected, are translation and return mappings correct?
10. Could an MTU issue or another network error prevent delivery?

Useful commands include `ipconfig` on Windows; `ip addr`, `ip route`, and `ip neigh` on Linux; `arp -a`; `ping`; `tracert` on Windows; and `traceroute` or `tracepath` on Linux (availability varies). Interpret results carefully: ICMP may be filtered, so a failed ping does not prove that every application protocol is unreachable.

## 10. Quick revision

| Term | Remember this |
|---|---|
| Routing | Selects the next hop/interface for an IP packet |
| Forwarding table | Used for per-packet forwarding decisions |
| Longest-prefix match | Prefer the matching route with the most specific prefix |
| Default gateway | First-hop router for off-link destinations |
| ARP | Resolves IPv4 addresses to link-layer addresses on a local link |
| MAC address | Link-layer address used to deliver a frame over a local segment |
| IP address | Network-layer address used to route packets across networks |
| Switch | Forwards Layer 2 frames using MAC learning and forwarding information |
| Router | Forwards IP packets between networks and rebuilds link-layer framing |
| NAT | Translates IP addresses and often transport ports |
| TTL | Limits the number of IPv4 router hops |
| AWS VPC route table | Maps destination prefixes to targets such as local routes and gateways |

## 11. Self-check questions

Answer these without looking at the notes:

1. If A and D are on the same subnet, why can A send directly to D without using the default gateway?
2. When C sends to X on another subnet, which MAC does C need first: X's or the local router's?
3. What does ARP resolve, and why does it not find an Internet server's MAC?
4. Which device uses a MAC address table, and which uses an IP forwarding table?
5. Why does a router create a new frame when forwarding a packet?
6. Which fields normally remain the same end-to-end, and which change at each routed Ethernet hop?
7. What happens to IPv4 TTL at a router?
8. How can NAT make the statement “the IP source never changes” incorrect?
9. Why does the destination network need a route back for a request/response exchange?
10. Why is the AWS diagram a conceptual example rather than an exact topology?

## 12. Reliable references

These are primary standards and official cloud documentation, selected to avoid unverified or random sources.

1. **RFC 1812 — Requirements for IP Version 4 Routers (RFC Editor).** Router behavior, forwarding, route tables, next-hop selection, TTL, and link-layer framing.  
   https://www.rfc-editor.org/rfc/rfc1812.html

2. **RFC 826 — An Ethernet Address Resolution Protocol (RFC Editor).** ARP and mapping protocol addresses to Ethernet addresses on a local network.  
   https://www.rfc-editor.org/rfc/rfc826.html

3. **RFC 1122 — Requirements for Internet Hosts: Communication Layers (RFC Editor).** Internet host requirements and the TCP/IP protocol layers.  
   https://www.rfc-editor.org/rfc/rfc1122.html

4. **Amazon VPC — Configure route tables (official AWS documentation).** Destination prefixes, route targets, and VPC traffic paths.  
   https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html

5. **Amazon VPC — Enable internet access using an Internet Gateway (official AWS documentation).** Internet Gateway routing, public subnet requirements, public IPv4 addressing, and IPv4 NAT behavior.  
   https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html

6. **Reference video:**  
   https://youtu.be/GBhaNXK-ows?si=MQEk14etHW1qwOwW

---

## Key takeaway

**The IP destination tells routers where the packet ultimately needs to go; the link-layer destination MAC tells the current local network where to deliver the next frame.** A host uses ARP to find the local next hop on IPv4 Ethernet, switches forward frames within a LAN, and routers forward IP packets between networks while rebuilding link-layer framing for each outgoing link. NAT and cloud networking can add address translation and policy controls.

