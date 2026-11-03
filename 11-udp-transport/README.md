# User Datagram Protocol (UDP)

> **Section:** Computer Networking — [Chai aur Networking](https://youtu.be/SjMw3nwAhuI?si=b5sY3gTxSDdbhS3h)
>
> **Learning objective:** Understand how UDP transports application messages with minimal protocol overhead, how ports identify application endpoints, how the eight-byte UDP header is structured, why applications choose UDP, and how to inspect UDP traffic—especially DNS queries—in Wireshark.

[← Back to Computer Networking Repository](https://github.com/Priya200227/computer-networking)

---

## Overview

The **User Datagram Protocol (UDP)** is a transport-layer protocol that lets applications send discrete messages called **datagrams** over IP. UDP has a small header and does not establish a transport connection before sending data.

UDP provides **best-effort delivery**. It does not guarantee that a datagram will arrive, arrive only once, or arrive in the same order in which it was sent. UDP itself does not provide retransmission, flow control, or congestion control. Applications and higher-level protocols must add the mechanisms they need.

UDP is useful when low overhead, low latency, message boundaries, or application-controlled behavior matter more than having TCP-like reliability built into the transport layer.

## Learning objectives

By the end of this section, you should be able to explain:

- UDP's role at OSI Layer 4 and its relationship with IP.
- What connectionless, best-effort, and message-oriented mean in practice.
- How UDP source and destination ports help deliver data to the right application endpoint.
- The four fields in a UDP header and why the minimum header is **8 bytes**.
- Why DNS commonly uses UDP but can also use TCP.
- How protocols such as QUIC can use UDP as a carrier while implementing additional transport features above it.
- How to identify UDP and DNS traffic in Wireshark.
- The trade-offs between UDP and TCP.

---

## 1. What is UDP?

UDP stands for **User Datagram Protocol**. It is associated with the transport layer (OSI Layer 4) and is identified by IP protocol number **17**.

A simplified view of sending data is:

```text
Application message
        |
        v
+---------------------------+
| UDP header (8 bytes)      |
+---------------------------+
| Application data          |
+---------------------------+
        |
        v
IP packet -> link-layer frame -> network
```

UDP adds source and destination ports, length, and checksum information to an application message. IP then carries the UDP datagram across the network.

### Connectionless does not mean “no application state”

UDP does not establish a transport connection with a three-way handshake before sending data. A sender can transmit a datagram to a destination IP address and port without first negotiating a UDP connection.

UDP itself maintains minimal per-communication state compared with TCP, but an application using UDP can still track peers, sessions, requests, acknowledgements, or keys. **QUIC**, for example, runs over UDP but implements connection-oriented behavior, encryption, loss recovery, streams, and congestion control above UDP.

## 2. Why use UDP?

UDP's main advantage is **minimal transport machinery**, not a guarantee that every UDP application is faster than every TCP application.

UDP avoids TCP's transport connection setup and does not automatically retransmit lost datagrams or wait to deliver later data behind missing earlier data. This can help with short request/response exchanges and real-time traffic where an old update may be less useful than the newest update.

### Common use cases

| Use case | Why UDP can fit | Important qualification |
|---|---|---|
| DNS lookups | A query and response can often be exchanged with low overhead | DNS can also use TCP; resolvers retry or change transport when needed |
| Real-time voice/video and WebRTC | Applications can prioritize timely media and manage loss/jitter themselves | Applications still need suitable congestion control and may use selective recovery |
| Online games | Frequent state updates may be more useful than delayed updates | Game protocols may add sequencing, acknowledgements, or reliability for selected messages |
| QUIC / HTTP/3 | QUIC uses UDP datagrams as its carrier | QUIC itself implements security, reliability mechanisms, and congestion control |
| VPNs and tunnels | UDP can carry encapsulated traffic with low transport overhead | Tunnel protocols must supply security and any required reliability/congestion behavior |
| RTP and related media protocols | Useful for time-sensitive media streams | UDP itself does not provide media timing, codecs, or loss recovery |

> **Key principle:** UDP gives applications a lightweight datagram service. It does not automatically make an application reliable, secure, or congestion-safe.

![UDP overview and use cases](assests/01-udp-overview-and-use-cases.png)

*This diagram summarizes UDP's transport-layer role, small header, lack of a transport handshake, and examples of applications that use it. “Fast but unreliable” compares built-in transport services; it is not a universal performance guarantee.*

![UDP use cases and message delivery](assests/02-udp-use-cases-and-message-delivery.png)

*The packet boxes illustrate discrete datagrams. Network delivery order is not guaranteed; a receiver may experience loss, duplication, or reordering. UDP itself does not restore missing messages.*

## 3. UDP versus TCP

| Property | UDP | TCP |
|---|---|---|
| Transport setup | No UDP handshake | Normally establishes a connection with a three-way handshake |
| Data model | Message/datagram-oriented | Reliable, ordered byte stream |
| Delivery guarantee | No guarantee from UDP itself | Provides reliable delivery while the connection remains viable |
| Ordering | Not guaranteed | Bytes are delivered to the application in order |
| Retransmission | Not built into UDP | Built in |
| Flow control | Not built into UDP | Built in |
| Congestion control | Not built into UDP | Built in |
| Header size | 8 bytes | Minimum 20 bytes, before options |
| Examples | DNS queries, real-time media, game traffic, QUIC's carrier | HTTP/1.1 and HTTP/2 commonly use TCP; email and file-transfer protocols also commonly use TCP |

**Do not conclude that UDP is always faster or TCP is always slower.** Performance depends on the application, network conditions, message sizes, congestion, and protocol design. QUIC shows that a protocol can use UDP while implementing reliability and congestion control above it.

## 4. UDP datagram structure

A UDP datagram consists of an **8-byte header** followed by application data. The header contains four fields, each 16 bits (2 bytes) long.

### Header layout

```text
  0               15 16              31
 +------------------+------------------+
 |    Source Port   | Destination Port |
 +------------------+------------------+
 |      Length      |     Checksum     |
 +------------------+------------------+
 |              Application Data       |
 +-------------------------------------+
```

| Field | Size | Purpose |
|---|---:|---|
| Source port | 16 bits / 2 bytes | Identifies the sending application endpoint when applicable; zero can be used if no source port is supplied |
| Destination port | 16 bits / 2 bytes | Identifies the destination application endpoint |
| Length | 16 bits / 2 bytes | Length of the complete UDP header plus data, in bytes; minimum value is 8 |
| Checksum | 16 bits / 2 bytes | Detects certain corruption and helps validate that the datagram matches the intended IP endpoints and protocol |

**Total UDP header size: 2 + 2 + 2 + 2 = 8 bytes.** The layout represents bits in the header, not a literal table of rows and columns in memory.

### Important field details

- **Ports are 16-bit values.** They help UDP deliver a received datagram to the correct socket/application endpoint. A port is not a physical connector and does not identify a process globally by itself; IP address and transport protocol also matter.
- **Length includes header and payload.** For example, 20 bytes of UDP data means a UDP length of 28 bytes.
- **Checksum is not encryption.** It is an integrity check, not cryptographic authentication, and does not protect against malicious modification.
- **IPv4 and IPv6 checksum rules differ.** In IPv4, a zero UDP checksum can indicate that no checksum was generated. In IPv6, UDP checksums are generally required, subject to narrowly defined exceptions.
- **The theoretical maximum length field is 65,535 bytes**, but practical payload size is constrained by IP packet size, path MTU, and fragmentation considerations. Avoid assuming very large datagrams will traverse the Internet intact.

![UDP datagram with ports](assests/04-udp-datagram-ports.png)

*The diagram shows a datagram sent from a source port to a destination port, with a reply using the reversed endpoint ports. The specific IP addresses and ports are illustrative.*

![UDP datagram header anatomy](assests/05-udp-datagram-header-anatomy.png)

*This diagram separates the four 16-bit header fields from application data. The UDP header is exactly 8 bytes; the payload size varies.*

## 5. How UDP ports work

IP addresses identify network-layer interfaces; transport-layer ports help identify application endpoints on a host.

For example, a client might send a DNS query from a temporary local port such as `55555` to a DNS server's UDP port `53`:

```text
Client: 192.168.1.10:55555
        |
        | UDP query
        v
DNS server: 8.8.8.8:53
```

The response typically comes from server port `53` to the client's original source port. The client port is usually dynamically selected and can vary. A port number does not guarantee that a service is running or reachable: firewalls, routing failures, host availability, and application state can all affect communication.

## 6. DNS over UDP and TCP

DNS commonly uses **UDP port 53** for ordinary queries because a query/response exchange can be lightweight. DNS also supports TCP port 53. TCP is used for operations such as zone transfers and may be used when a UDP response is truncated and the resolver retries over TCP.

### Simplified UDP DNS exchange

1. A client needs to resolve a name such as `example.com`.
2. The resolver sends a DNS query in a UDP datagram to a DNS server, usually destination port `53`.
3. The server sends a DNS response, typically to the client's source port.
4. If the response is not received, the resolver can time out and retry or try another server. **UDP itself does not retransmit the query.**

DNS messages contain a transaction ID that helps a resolver associate a response with a query. This ID is part of the DNS message, not a UDP header field.

![DNS built on UDP versus TCP](assests/03-dns-over-udp-vs-tcp.png)

*The left side illustrates a simple UDP query/response. The right side contrasts it with TCP connection setup and teardown. This is a conceptual illustration, not a universal packet count: exchanges depend on the response, transport, retries, and connection reuse. DNS over TCP does not necessarily create and close a new connection for every query.*

### Corrections to common simplifications

- DNS is **not UDP-only**; it supports both UDP and TCP.
- UDP has no built-in retransmission; DNS software handles timeout and retry behavior.
- TCP setup and teardown are not required for every DNS lookup; connections may be reused.
- Packet counts such as “2 trips” or “11 trips” are not protocol constants and should not be treated as universal measurements.

## 7. UDP, QUIC, and real-time communication

QUIC is a useful example of why “UDP is unreliable” does not mean “everything carried by UDP is unreliable.” QUIC sends packets inside UDP datagrams, but QUIC itself provides secure connections, streams, loss recovery, and congestion control. HTTP/3 uses QUIC.

```text
HTTP/3
   |
  QUIC  <- security, streams, loss recovery, congestion control
   |
  UDP   <- lightweight datagram transport
   |
   IP
```

Real-time applications may choose UDP because waiting to retransmit an old audio or game-state packet can be less useful than continuing with newer information. The application still needs to handle timing, loss, congestion, and any reliability it requires.

## 8. Inspect UDP traffic with Wireshark

Wireshark can show UDP headers, ports, lengths, checksums, and protocols carried in the payload.

### Basic workflow

1. Open Wireshark and select an interface you are authorized to capture.
2. Start a capture.
3. Generate traffic—for example, perform a DNS lookup.
4. Stop the capture.
5. Apply a display filter:
   - `udp` — show UDP packets.
   - `dns` — show packets Wireshark recognizes as DNS.
   - `udp.port == 53` — show UDP traffic using port 53.
   - `ip.addr == 8.8.8.8 && udp` — show UDP packets to or from that IPv4 address.
6. Select a packet and expand **User Datagram Protocol** in the packet-details pane.
7. Inspect source port, destination port, length, and checksum. If Wireshark decodes the payload as DNS, expand the DNS section too.

![Inspecting UDP traffic using Wireshark](assests/06-inspecting-udp-dns-traffic.png)

*The diagram illustrates a DNS request/response flow and UDP ports when querying a public DNS resolver. Addresses and example responses are illustrative; a live query may return different results.*


### Layer-by-layer analysis: DNS query and response

The following capture follows a DNS lookup for `github.com` using the resolver `8.8.8.8`. It shows how one DNS exchange is represented at the application, transport, network, and Ethernet layers.

![Wireshark DNS query and response analyzed across protocol layers](assests/07-wireshark-dns-query-response-layer-analysis.png)

#### 1. Generate and capture the DNS lookup

The example runs:

```bash
nslookup github.com 8.8.8.8
```

The command asks the DNS resolver at `8.8.8.8` to resolve `github.com`. In Wireshark, the screenshot narrows the displayed packets with:

```text
ip.dst == 8.8.8.8 or ip.src == 8.8.8.8
```

This is a **display filter**: it filters packets already captured. It is not a capture filter.

#### 2. Application layer — DNS message

At the application layer, Wireshark decodes the payload as DNS.

- The request is a DNS **standard query** for `github.com`.
- The response contains the matching DNS transaction and an answer record.
- The DNS transaction ID in the request and response is the same. This helps the requester associate the response with the outstanding query.
- The DNS message carries the query name, query type/class, and response information.

The DNS transaction ID is an application-layer correlation value. It is not the UDP source port and is not a TCP-style connection identifier.

#### 3. Transport layer — UDP

The packets use UDP destination port **53** at the resolver. In the example:

| Field | DNS query | DNS response |
|---|---:|---:|
| Source UDP port | 56470 (client's temporary port) | 53 |
| Destination UDP port | 53 | 56470 |
| UDP length | 36 bytes | 52 bytes |
| DNS message length | 28 bytes | 44 bytes |

The UDP length field includes both the 8-byte UDP header and the UDP payload:

```text
Query:    8-byte UDP header + 28-byte DNS message = 36 bytes
Response: 8-byte UDP header + 44-byte DNS message = 52 bytes
```

The response is larger in this capture because the DNS answer adds information beyond the original question. The UDP length is therefore different for the query and response.

**These byte counts are specific to the packets shown.** Other DNS queries and responses can have different lengths.

#### 4. Network layer — IPv4

The IP source and destination addresses reverse between the request and response:

| Field | DNS query | DNS response |
|---|---|---|
| Source IPv4 address | `192.168.1.7` | `8.8.8.8` |
| Destination IPv4 address | `8.8.8.8` | `192.168.1.7` |

The client sends the query to the resolver; the resolver sends the response back to the client. Other IPv4 fields, such as total length and header checksum, can also differ between the two packets.

#### 5. Data-link layer — Ethernet

The Ethernet source and destination MAC addresses also reverse between the outgoing query and incoming response on the captured local link.

MAC addresses are used for delivery on a local Ethernet/Wi-Fi link; IP addresses identify network-layer endpoints across routed networks. For an off-subnet destination, the MAC address visible at the client is typically the next-hop device's MAC—not the remote DNS server's physical MAC address.

#### 6. Correlating the request and response

To verify that the two packets belong to the same DNS exchange, compare:

- The DNS transaction ID — it should match for this query/response pair.
- The queried name and query type.
- The direction of the IP addresses.
- The reversed UDP port pair (client temporary port ↔ server port 53).
- The DNS message type/flags: query versus response.

A matching transaction ID alone is not universal proof that two packets belong together; use the DNS question and endpoint/port context as well. In the screenshot, the matching DNS transaction ID and corresponding query/answer provide evidence that the response belongs to the displayed request.

> **Layering takeaway:** The DNS message is carried inside UDP; UDP is carried inside IP; IP is carried inside an Ethernet frame on the local link. Each layer adds its own header. When the response returns, the endpoint addresses and ports are reversed, while the DNS transaction ID is retained to correlate the answer with the question.

### What to inspect

- Source and destination IP addresses.
- Source and destination UDP ports.
- UDP length and checksum status.
- Whether the payload is decoded as a DNS query or response.
- Whether a response corresponds to a query.
- Repeated queries that could indicate retries or a missing response.

**Capture responsibly:** inspect only traffic on systems and networks you own or are authorized to analyze. Packet captures may contain sensitive metadata or payloads.

## 9. Limits and common misconceptions

### “UDP is faster than TCP.”
Not automatically. UDP has less built-in transport machinery, but application behavior, congestion, packet loss, and protocol design determine performance.

### “UDP guarantees delivery because IP routes the packet.”
No. IP and UDP provide best-effort delivery. A datagram may be lost, duplicated, or reordered. UDP does not retransmit it.

### “UDP is always stateless.”
UDP itself has minimal transport state and no connection handshake. Applications using UDP can still maintain sessions. QUIC is one example.

### “UDP has no error checking.”
Incorrect. UDP has a checksum field. It detects certain accidental corruption; it does not provide encryption or cryptographic authentication.

### “DNS always uses UDP.”
Incorrect. DNS uses both UDP and TCP.

### “QUIC gets TCP reliability from UDP.”
Incorrect. UDP does not provide TCP's reliability. QUIC implements its own transport behavior on top of UDP.

### “The port number is part of the IP address.”
No. IP addresses belong to the network layer; UDP ports belong to the transport layer. Both help identify a network endpoint.

## Key takeaway

**UDP is a lightweight, connectionless transport protocol that sends independent datagrams with an 8-byte header.** It does not guarantee delivery, ordering, retransmission, or congestion control. Those trade-offs make UDP useful for applications that need low overhead or control their own transport behavior—but reliability and safe network behavior must be provided by the application or a higher-level protocol when required.

## References

- [RFC 768 — User Datagram Protocol](https://www.rfc-editor.org/rfc/rfc768.html) - UDP header format, fields, and best-effort delivery.
- [Wireshark User's Guide](https://www.wireshark.org/docs/wsug_html_chunked/) - capture and display-filter reference.
Video Reference:
- [Why UDP is the Unsung Hero of Fast Internet Protocols](https://youtu.be/SjMw3nwAhuI?si=WEjvm4xnMToTRCeA)
- [Unveiling the UDP Datagram: A Deep Dive into Its Structure](https://youtu.be/1mTI5X0pN6M?si=lT4WbaKw7teiSC_J)
- [How to Inspect UDP Traffic Using Wireshark](https://youtu.be/_JeDNQ22Wxk?si=pVr9epPz-U3-0O4v)
