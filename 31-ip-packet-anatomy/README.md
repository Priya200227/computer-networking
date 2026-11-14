# IPv4 Packet Anatomy

>[!NOTE]
>**Section:** Computer Networking - [IP packet anatomy](https://youtu.be/UzWpKcMlaMg?si=9vVa5lKbaLSyhSF_)
>
>**Purpose:** Understand the structure of an IPv4 packet, the purpose of each IP header field, and how IPv4 handles packet fragmentation.

---

## 1. What is an IP Packet?

An **IP packet** (also called an IP datagram) is the data unit handled by the Internet Protocol at the Network Layer.

Its primary responsibility is to carry data from a source IP address to a destination IP address across networks.

An IPv4 packet consists of two main parts:

1. **IP Header** – Contains information required to route and process the packet.
2. **Payload** – Contains the data being carried, such as a TCP segment, UDP datagram, or ICMP message.

![IPv4 packet structure and header fields](assests/ipv4-packet-anatomy.png)

---

## 2. IPv4 Header Structure

An IPv4 header has a minimum size of **20 bytes** and a maximum size of **60 bytes**.

- Minimum header: 20 bytes (without options).
- Maximum header: 60 bytes (with options).
- The header consists of a fixed portion and an optional portion.

### IPv4 Header Fields

| Field | Size | Purpose |
|---|---:|---|
| Version | 4 bits | Identifies the IP version. For IPv4, the value is `4`. |
| IHL (Internet Header Length) | 4 bits | Specifies the header length in 32-bit words. Minimum value is `5` (20 bytes). |
| DSCP | 6 bits | Used for traffic classification and differentiated service treatment. |
| ECN | 2 bits | Supports explicit congestion notification. |
| Total Length | 16 bits | Specifies the total packet size, including header and payload. |
| Identification | 16 bits | Helps identify fragments belonging to the same original IPv4 datagram. |
| Flags | 3 bits | Controls or indicates fragmentation behaviour. |
| Fragment Offset | 13 bits | Indicates the fragment's position within the original datagram. |
| TTL (Time to Live) | 8 bits | Limits packet lifetime by hop count. Routers decrement it during forwarding. |
| Protocol | 8 bits | Identifies the encapsulated payload protocol, such as TCP, UDP, or ICMP. |
| Header Checksum | 16 bits | Detects errors in the IPv4 header. |
| Source Address | 32 bits | IPv4 address of the sender. |
| Destination Address | 32 bits | IPv4 address of the receiver. |
| Options + Padding | Variable | Optional control information and alignment padding. |

> [!IMPORTANT]
> The IPv4 header is at least 20 bytes. The IHL field specifies its length in units of 4 bytes, not directly in bytes.

### Important calculations

**IHL calculation**

`Header Length = IHL × 4 bytes`

Example:

- IHL = 5
- Header length = 5 × 4 = **20 bytes**

**Total Length**

`Total Length = IP Header Length + Payload Length`

The 16-bit Total Length field supports a maximum IPv4 packet size of **65,535 bytes**.

---

## 3. DSCP and ECN

The old IPv4 Type of Service (ToS) field was redefined. It is now commonly called the **Differentiated Services (DS) field**.

It contains:

- **DSCP (6 bits):** Used to classify traffic and support differentiated forwarding treatment.
- **ECN (2 bits):** Allows congestion information to be signalled without necessarily dropping packets.

For example, a network administrator may configure voice traffic to receive different treatment from bulk file downloads.

> [!NOTE]
> DSCP does not guarantee priority by itself. Actual packet treatment depends on the network's QoS configuration and policies.

Reference: [RFC 2474 – Definition of the Differentiated Services Field](https://datatracker.ietf.org/doc/html/rfc2474)

---

## 4. TTL (Time to Live)

TTL limits how many router hops an IPv4 packet can travel.

- The sender sets an initial TTL value.
- Each router forwarding the packet decreases TTL by at least 1.
- When TTL reaches 0, the router discards the packet and normally sends an ICMP Time Exceeded message.

**Why is TTL needed?**

It prevents packets from circulating indefinitely due to routing loops.

TTL is also used by tools such as `traceroute` to discover the route packets take through a network.

---

## 5. Protocol Field

The Protocol field identifies which protocol is carried inside the IPv4 payload.

| Protocol | Protocol Number |
|---|---:|
| ICMP | 1 |
| TCP | 6 |
| UDP | 17 |

For example, if the Protocol field contains `6`, the receiving system knows that the IPv4 payload should be processed as TCP.

Reference: [IANA – Protocol Numbers](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml)

---

## 6. IPv4 Fragmentation

Fragmentation occurs when an IPv4 packet is larger than the Maximum Transmission Unit (MTU) of a network link and fragmentation is permitted.

The original datagram is divided into smaller fragments. Each fragment receives its own IPv4 header.

### Fields involved in fragmentation

Three important IPv4 header fields help with fragmentation and reassembly:

1. **Identification:** Fragments of the same original datagram share the same Identification value.
2. **Flags:** Indicates fragmentation-related information.
3. **Fragment Offset:** Indicates where the fragment's payload belongs in the original datagram.

### IPv4 Flags

The Flags field contains 3 bits:

| Flag | Meaning |
|---|---|
| Reserved | Must be zero. |
| DF (Don't Fragment) | If set to `1`, the packet must not be fragmented by routers. |
| MF (More Fragments) | Set to `1` when more fragments follow; set to `0` for the final fragment or an unfragmented packet. |

### Fragment Offset

The Fragment Offset is measured in units of **8 bytes**.

`Fragment Offset = Payload starting position / 8`

For example:

- A fragment begins at byte 0 → offset = 0.
- A fragment begins at byte 400 → offset = 400 / 8 = 50.
- A fragment begins at byte 800 → offset = 800 / 8 = 100.

### Example: Fragmenting a packet

Suppose an original IP datagram has 1,200 bytes of payload and is divided into three fragments, each carrying 400 bytes of payload.

| Fragment | Payload size | Fragment Offset | MF |
|---|---:|---:|---:|
| Fragment 1 | 400 bytes | 0 | 1 |
| Fragment 2 | 400 bytes | 50 | 1 |
| Fragment 3 | 400 bytes | 100 | 0 |

All three fragments have the same Identification value because they belong to the same original datagram.

Each fragment has its own IP header. The destination uses the Identification, Fragment Offset, and MF flag to help reassemble the original datagram.

> [!IMPORTANT]
> If DF = 1, a router cannot fragment the packet. If the packet is too large for the outgoing link, the router drops it and normally sends an ICMP Destination Unreachable message indicating that fragmentation is needed.

### Header Checksum

The IPv4 Header Checksum validates the IPv4 header only, not the payload.

Because fields such as TTL change during forwarding, routers must update the header checksum when modifying the header.

---

## 7. Key Takeaways

- An IPv4 packet consists of a header and a payload.
- IPv4 header size ranges from 20 to 60 bytes.
- IHL specifies header length in 4-byte units.
- Total Length includes both the header and payload.
- DSCP supports traffic classification; ECN supports congestion notification.
- TTL prevents packets from circulating indefinitely.
- Protocol identifies the payload protocol, such as TCP, UDP, or ICMP.
- Identification, Flags, and Fragment Offset support IPv4 fragmentation and reassembly.
- Fragment Offset is measured in 8-byte units.
- IPv4 Header Checksum covers only the header.

---

## References

1. [RFC 791 – Internet Protocol (IPv4)](https://datatracker.ietf.org/doc/html/rfc791)
2. [RFC 790 - Assigned Numbers (Page - 6)](https://datatracker.ietf.org/doc/html/rfc790)
3. [RFC 2474 – Differentiated Services Field](https://datatracker.ietf.org/doc/html/rfc2474)
4. [IANA – Protocol Numbers](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml)

---

[⬅️ Back to Computer Networking](../README.md)
