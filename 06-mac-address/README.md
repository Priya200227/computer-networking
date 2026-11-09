# MAC Addresses: Structure, Purpose, and IP vs. MAC

> [!NOTE]
> **Section:** Computer Networking  - [Chai aur Networking](https://youtu.be/jKWlJPpkp9o?si=OfX5f-Y3lhJOMpIT)
**Learning objective:** Understand what a MAC address identifies, how it is structured, how it differs from an IP address, and how both are used in local-network communication.

[← Back to Computer Networking Repository](https://github.com/Priya200227/computer-networking)

---

## 1. Network Interfaces

A **network interface** is the connection point through which a device communicates with a network.

Examples:
- Wi-Fi
- Ethernet
- Virtual network interfaces

A device can have multiple network interfaces, and each interface can have its own MAC address.

![Network interface and MAC address](assests/01-network-interface-and-mac-address.png)

**Key point:** A MAC address identifies a network interface on a local link, not necessarily the entire physical device.

## 2. What Is a MAC Address?

A **Media Access Control (MAC) address** is a link-layer address used to identify a network interface for communication over a local network, such as Ethernet or Wi-Fi.

A common MAC address is **48 bits (6 bytes)** long and is written as six hexadecimal groups.

Example:

```text
50:C2:E8:94:52:7F
```

Each hexadecimal group represents one byte (8 bits).

### Why Is It Needed?

When devices communicate over a local network, the sender needs a destination MAC address to deliver the network frame to the appropriate interface.

For IPv4 networks, **ARP** helps discover the MAC address associated with a local IPv4 next hop.

## 3. Structure of a MAC Address

A conventional 48-bit MAC address contains six bytes:

```text
50:C2:E8:94:52:7F
```

- Total length: 48 bits
- Number of bytes: 6
- Each hexadecimal digit: 4 bits
- Each pair of hexadecimal digits: 1 byte

### OUI and Interface-Specific Portion

A commonly used representation divides the address into two parts:

```text
50:C2:E8 : 94:52:7F
└── OUI ──┘ └ Interface-specific portion ┘
```

- **First 24 bits:** Commonly associated with an organization through an OUI (Organizationally Unique Identifier).
- **Remaining 24 bits:** Used to distinguish addresses within that allocation.

![MAC address structure](assests/02-mac-address-structure.png)

**Note:** This is the conventional allocation model. Locally administered and randomized MAC addresses may not identify a device manufacturer.

## 4. IP Address vs. MAC Address

IP addresses and MAC addresses serve different purposes in networking.

| Feature | IP Address | MAC Address |
|---|---|---|
| Layer | Network layer (Layer 3) | Data-link layer (Layer 2) |
| Purpose | Identifies an IP destination and supports routing | Delivers frames over a local link |
| Size | IPv4: 32 bits; IPv6: 128 bits | Commonly 48 bits |
| Example | `192.168.1.10` | `50:C2:E8:94:52:7F` |
| Scope | Used across routed networks | Used on the current local link |
| Can change? | Yes | Yes |

### Simple Mental Model

- **IP address:** Where should the packet go?
- **MAC address:** Which interface should receive the frame on this local link?

A router uses IP addressing to forward packets between networks. It uses link-layer addressing to deliver frames to the next hop.

## 5. How IP and MAC Addresses Work Together

Consider a laptop with IP address `192.168.1.4/24` communicating with another device.

### Case A: Destination on the Same Subnet

Destination IP: `192.168.1.2`

1. The laptop checks whether the destination belongs to its local subnet.
2. It determines that both devices are on the same subnet.
3. It needs the destination device's MAC address.
4. If the address is not already cached, it uses **ARP** to discover it.
5. The laptop sends the frame directly over the local network.

### Case B: Destination on a Different Subnet

Destination IP: `192.168.2.4`

1. The laptop determines that the destination is outside its local subnet.
2. It selects a route, typically through its default gateway.
3. It uses ARP to discover the gateway's MAC address if necessary.
4. It sends the frame to the gateway's MAC address.
5. The router forwards the packet toward the destination network.

**Important:** The IP packet's destination remains `192.168.2.4` during ordinary routing, while the frame's MAC addresses change at each routed link.

![IP vs MAC and ARP](assests/03-ip-vs-mac-and-arp.png)

## 6. Where ARP Fits In

**Address Resolution Protocol (ARP)** discovers the MAC address associated with an IPv4 address on the local network.

Example:

```text
Known:  IPv4 address = 192.168.1.2
Need:   Corresponding MAC address

ARP:    Who has 192.168.1.2?

Reply:  The device responds with its MAC address.
```

The mapping may then be stored temporarily in the ARP cache.

**Remember:**
- ARP resolves IPv4 addresses to link-layer addresses on the local link.
- For remote destinations, a host resolves the MAC address of its next hop, usually the default gateway.
- IPv6 uses Neighbor Discovery Protocol (NDP), not ARP.

## 7. Practical Commands

Use these commands to inspect network interfaces and addresses.

**Windows**

```powershell
ipconfig /all
getmac /v
arp -a
```

**Linux**

```bash
ip addr
ip link
ip neigh
```

**macOS**

```bash
ifconfig
arp -a
```

These commands help you inspect:
- Network interfaces
- IP addresses
- MAC addresses
- Neighbor and ARP cache entries

---

## References

- [What Is a MAC Address? Understanding Its Structure and Purpose](https://youtu.be/jKWlJPpkp9o?si=OfX5f-Y3lhJOMpIT)
- [IP vs MAC Addresses](https://youtu.be/sMDYh-II22Q?si=v8xHmElJn6yng7PP)

---
**Next:** [ARP](../07-arp/README.md)
