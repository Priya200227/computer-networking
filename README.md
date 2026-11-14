# Computer Networking - From Fundamentals to Protocol Internals

A structured, practical journey through computer networking - from understanding how devices communicate to exploring the internal mechanisms behind modern Internet protocols.

This repository contains **technical notes, diagrams, protocol breakdowns, practical examples, and learning resources** created while studying computer networking.

The goal is not just to memorize networking terminology, but to understand **how data travels across networks, how protocols work internally, and why networking decisions matter in real-world systems.**

---

## Learning Roadmap

The repository is organized into six subject-based modules.

| # | Module | Topics covered |
|---|---|---|
| 01 | [Network Fundamentals](./01-network-fundamentals/) | IPv4, subnetting, CIDR, MAC, ARP, gateways, routing, ICMP, NAT, IP packet anatomy |
| 02 | [Transport Layer](./02-transport-layer/) | UDP, TCP, sequence numbers, acknowledgements, TCP segments, MTU, MSS, flow control and congestion control |
| 03 | [DNS](./03-dns/) | How DNS works, DNS resolution, major DNS record types |
| 04 | [HTTP & Web](./04-http-and-web/) | HTTP fundamentals, request-response structure, HTTP/1.1, HTTP/2, multiplexing, HPACK, QUIC and HTTP/3 |
| 05 | [TLS & Security](./05-tls-and-security/) | TLS overview, certificates, TLS 1.2 handshake and TLS 1.3 handshake |
| 06 | [Packet Analysis](./06-packet-analysis/) | Practical packet inspection and Wireshark exercises - planned |

---

## What You'll Learn

### 01. Network Fundamentals

Understand how devices identify each other and communicate across networks.

- IPv4 addressing, network and host portions
- Subnet masks and CIDR notation
- Default gateways
- MAC addresses and ARP
- Routing and packet forwarding
- ICMP, ping and traceroute
- Network Address Translation (NAT)
- IPv4 packet structure and fragmentation

[Explore Network Fundamentals →](./01-network-fundamentals/)

### 02. Transport Layer

Understand how data is delivered between applications running on different devices.

- UDP and TCP
- TCP sequence and acknowledgement numbers
- TCP segment structure
- MTU, MSS and Path MTU Discovery
- TCP flow control
- TCP congestion control
- Reliable and ordered data delivery

[Explore Transport Layer →](./02-transport-layer/)

### 03. DNS

Understand how domain names are translated into IP addresses.

- DNS architecture and hierarchy
- Recursive and iterative resolution
- DNS caching
- Common DNS record types

[Explore DNS →](./03-dns/)

### 04. HTTP & Web

Explore how web applications communicate and how HTTP has evolved.

- HTTP fundamentals
- HTTP request and response structure
- HTTP/1.1 connection reuse and head-of-line blocking
- HTTP/2 binary framing and multiplexing
- HPACK header compression
- HTTP/2 head-of-line blocking
- QUIC protocol overview
- HTTP/3 and QUIC streams

[Explore HTTP & Web →](./04-http-and-web/)

### 05. TLS & Security

Understand how communication is protected over untrusted networks.

- TLS fundamentals
- Symmetric and asymmetric encryption
- Digital certificates and X.509
- Certificate authorities and chain of trust
- Certificate generation and verification
- TLS 1.2 handshake
- TLS 1.3 handshake

[Explore TLS & Security →](./05-tls-and-security/)

---

## How the Notes Are Structured

Each topic is designed to be useful as an independent learning resource.

Depending on the subject, a topic may include:

- **Concept explanations:** What the protocol or networking mechanism does.
- **Architecture and diagrams:** Visual representation of communication and packet flow.
- **Protocol internals:** Headers, fields, state transitions and important mechanisms.
- **Practical examples:** Scenarios that connect theory to real-world networking.
- **References:** Documentation, RFCs and other learning resources.

## Learning Resources & References

The notes are developed using a combination of structured video lessons, technical documentation and protocol specifications.

Some primary references include:

- [RFC Editor](https://www.rfc-editor.org/) — Internet protocol specifications.
- [IETF Datatracker](https://datatracker.ietf.org/) — Internet standards and working-group documents.
- [MDN Web Docs](https://developer.mozilla.org/) — HTTP and web technology documentation.
- [Wireshark Documentation](https://www.wireshark.org/docs/) — Packet analysis and protocol inspection.
- [Computer Networking — Chai aur Code](https://www.youtube.com/@chaiaurcode) — Video-based learning resource.

Relevant RFCs and documentation are linked within individual topic notes wherever applicable.

---

## Repository Structure

```text
computer-networking/
│
├── 01-network-fundamentals/
├── 02-transport-layer/
├── 03-dns/
├── 04-http-and-web/
├── 05-tls-and-security/
├── 06-packet-analysis/
│
└── README.md
```

Each module contains its own topic folders and supporting resources.

---

## Progress & Future Work

This is an evolving learning repository. Topics are added, reviewed and improved as the learning journey progresses.

**Upcoming focus:**
- Complete TLS 1.2 and TLS 1.3 handshake analysis.
- Build practical Wireshark packet-inspection exercises.
- Continue exploring networking concepts through packet-level examples.

---

## Why This Repository?

Networking is a foundational skill for understanding backend systems, distributed applications, cloud infrastructure and data engineering.

This repository is intended to serve as both a personal technical reference and a resource for anyone who wants to understand computer networking beyond surface-level definitions.

**Learn the concepts. Understand the protocols. Follow the packets.**

---

*Maintained as a continuously evolving computer networking learning project.*
