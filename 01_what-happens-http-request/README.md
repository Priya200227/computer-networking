# What Really Happens When You Make an HTTP Request?

> **Learning note — Video 02, _Chai aur Computer Network_**  
> This note explains the end-to-end journey of a browser request, from application code to network transmission and back. It is a conceptual overview; later notes should expand DNS, TCP, IP, Ethernet, ARP, TLS, and HTTP individually.

## Why this topic matters

A request such as `fetch("https://api.example.com/profile")` looks like one line of JavaScript. In reality, several components cooperate:

- The browser and application code construct a request.
- DNS may resolve the hostname to one or more IP addresses.
- The operating system selects a route and a network interface.
- A transport protocol carries the application data.
- IP addresses identify the network-layer source and destination.
- A link-layer frame carries the packet across the current local link.
- Routers forward traffic between networks.
- The server receives the request, processes it, and sends a response.

Understanding this flow provides context for HTTP/HTTPS, DNS, IP addressing, TCP/UDP, ports, sockets, ARP, routing, TLS, cloud networking, APIs, and troubleshooting.

## The example

A browser running a React frontend on a laptop calls:

```javascript
const res = await fetch("https://api.example.com/profile");
```

Assume the service is hosted remotely and the browser uses HTTPS. The exact path depends on DNS answers, cached connections, proxies, VPNs, IPv4/IPv6, the server deployment, and the negotiated HTTP version.

### Workflow diagram from the video screenshots

The following images preserve the instructor's diagram as shown in your screenshots, in the order the workflow is built up during the video. The first image gives the high-level browser-to-server request and DNS mapping; the later images add the request bytes, TCP connection/segments, IP packet, link-layer frame, next-hop MAC address, transmission medium, and ARP.

> These are the original screenshots, not a newly simplified or corrected redraw. Some labels are intentionally discussed and qualified in the notes below.

**1. High-level request/response and DNS**

![1. High-level request/response and DNS](http_request_flow_assets/01-high-level-request-and-dns.png)

**2. HTTP request represented as bytes and sent through the OS networking stack**

![2. HTTP request represented as bytes and sent through the OS networking stack](http_request_flow_assets/02-http-request-bytes-and-tcp.png)

**3. Byte-sequence illustration in the diagram**

![3. Byte-sequence illustration in the diagram](http_request_flow_assets/03-byte-sequence-illustration.png)

**4. TCP handshake and segmentation illustration**

![4. TCP handshake and segmentation illustration](http_request_flow_assets/04-tcp-handshake-and-segments.png)

**5. TCP segment encapsulated in an IP packet**

![5. TCP segment encapsulated in an IP packet](http_request_flow_assets/05-tcp-segment-inside-ip-packet.png)

**6. Frame, source/destination addressing, and next-hop MAC**

![6. Frame, source/destination addressing, and next-hop MAC](http_request_flow_assets/06-frame-and-next-hop-mac.png)

**7. Transmission media, router, and ARP**

![7. Transmission media, router, and ARP](http_request_flow_assets/07-transmission-and-arp.png)

The screenshots show a teaching overview rather than a guaranteed packet-by-packet trace. A real request may reuse DNS results and existing connections, and the exact path depends on the network, deployment, and negotiated HTTP version.

## The journey, step by step

### 1. Application code requests a resource

The browser executes:

```javascript
const res = await fetch("https://api.example.com/profile");
```

`fetch()` is a browser API for making network requests. The URL identifies the scheme (`https`), hostname (`api.example.com`), and path (`/profile`). The default method is `GET` unless options specify another method.

The JavaScript code runs in the browser. It does not itself construct Ethernet frames or manually split the request into TCP segments.

### 2. DNS resolution finds an address

The browser or operating system needs an IP address for `api.example.com` unless a usable result is already cached or otherwise available. DNS can return IPv4 addresses (A records), IPv6 addresses (AAAA records), or other record types.

Important distinction:

- **Hostname:** a human-friendly name, such as `api.example.com`.
- **IP address:** a network-layer address used to route traffic.
- **DNS:** a distributed naming system that can map names to address records.

DNS does not necessarily return one fixed IP address forever. Results can change, and services may use multiple addresses, CDNs, load balancers, or other routing layers.

### 3. The operating system selects a route

The client determines how to reach the destination using its routing information. If the destination is outside the local subnet, the next hop is typically a default gateway/router.

The browser's local address is not necessarily the address the remote server sees. A laptop commonly has a private address on its local network; a home or corporate gateway may use NAT, and the public-facing address may differ. VPNs, proxies, and cloud networks can change the path further.

### 4. A transport connection is established or reused

For HTTP/1.1 and HTTP/2, HTTP commonly runs over TCP. TCP provides a reliable, ordered byte stream and uses port numbers to identify communicating application endpoints.

A new TCP connection normally uses a three-way handshake:

1. Client sends `SYN`.
2. Server responds with `SYN-ACK`.
3. Client sends `ACK`.

A browser may reuse an existing connection, so a new handshake is not required for every request.

**Important modern exception:** HTTP/3 uses QUIC, which runs over UDP. Therefore, “HTTP always runs over TCP” is incorrect. For this example, assume HTTP/1.1 or HTTP/2 over TCP.

### 5. HTTPS protects the HTTP communication

For HTTPS over TCP, TLS is negotiated to provide encryption and integrity and to authenticate the server according to the client's certificate-validation rules.

The browser then sends HTTP data through the protected connection. On the network, observers generally cannot read the HTTP path, headers, or body from the encrypted TLS application data alone, although metadata such as IP addresses, ports, traffic timing, and sizes may remain observable.

Do not confuse these layers:

- **HTTP:** application-level request/response semantics.
- **TLS:** security for the connection.
- **TCP:** reliable transport for HTTP/1.1 and HTTP/2 in this example.
- **IP:** addressing and forwarding between networks.
- **Ethernet/Wi-Fi:** link-layer delivery on a local network.

### 6. Data is encapsulated as it moves down the stack

A useful simplified model is:

```text
Application data: HTTP request
          |
          v
Transport layer: TCP segment (TCP header + data)
          |
          v
Network layer: IP packet (IP header + TCP segment)
          |
          v
Link layer: frame (link header/trailer + IP packet)
          |
          v
Physical medium: electrical, optical, or radio signals
```

The terminology matters:

| Unit | Layer / context | What it contains |
|---|---|---|
| HTTP message/data | Application | Request or response semantics and content |
| TCP segment | Transport | TCP header plus a portion of the byte stream |
| IP packet (often called an IP datagram) | Internet/network | IP header plus transport-layer payload |
| Ethernet frame | Link | Link-layer header/trailer plus payload, commonly an IP packet |
| Bits/signals | Physical transmission | Encoded representation sent over a medium |

This is a simplified encapsulation model. Real implementations can include additional headers, tunnels, VLAN tags, IP fragmentation in some circumstances, and other details.

**A TCP segment is not the same thing as an IP packet, and neither is the same thing as an Ethernet frame.**

### 7. TCP does not divide every request into a fixed number of equal chunks

The video sketch shows sample hexadecimal bytes and “20 chunks.” Treat this only as an illustration that data is represented as bytes and may be carried across multiple segments.

It is not a general rule that every HTTP request becomes 20 chunks. Segment sizes depend on factors such as the amount of data, maximum segment size (MSS), path MTU, TCP implementation, congestion control, offloading, and current network conditions. Small requests may fit in one segment; larger data streams may span many segments. Application writes do not map one-to-one to TCP segments.

The hexadecimal sequence shown in a teaching diagram is illustrative; it should not be read as the actual bytes of the displayed request.

### 8. Ethernet addressing and ARP on the local link

For IPv4 over Ethernet, the client needs a link-layer destination address for the **next hop** on its local network.

- If the destination IP is on the same local subnet, the next hop is the destination host.
- If the destination is on another network, the next hop is usually the default gateway.

If the required mapping is not already in the ARP cache, ARP can discover the Ethernet MAC address associated with the next-hop IPv4 address on that local link.

**ARP does not discover the MAC address of a remote server across the internet.** MAC addresses are used for local-link delivery. As a packet crosses routers, each routed link uses its own link-layer framing; the Ethernet source and destination MAC addresses are replaced for each Ethernet hop, while the IP source and destination usually remain end-to-end, except where mechanisms such as NAT alter them.

ARP is for IPv4 address resolution. IPv6 uses Neighbor Discovery rather than ARP.

### 9. The server receives and handles the request

At the destination, the networking stack processes the received frames and packets and delivers the transport data to the appropriate socket. The server software handles the HTTP request and routes it to the application.

For example, the backend might handle:

```http
GET /profile HTTP/1.1
Host: api.example.com
Authorization: Bearer <token>
```

This is an illustrative HTTP/1.1 request shape. With HTTPS, the HTTP content is carried inside TLS records on the network; with HTTP/2, the protocol representation uses frames rather than the HTTP/1.1 textual format.

The application may authenticate the user, read a database, call another service, and construct a response.

### 10. The response returns to the client

The server sends an HTTP response, such as:

```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
{
  "name": "Example User"
}
```

The status and body above are illustrative. The response travels back through the network, is processed by the browser's networking stack, and becomes available to JavaScript through the `Response` object. `fetch()` does not automatically throw an exception for HTTP error statuses such as 404 or 500; application code should check `res.ok` or `res.status`.

```javascript
const res = await fetch("https://api.example.com/profile");

if (!res.ok) {
  throw new Error(`HTTP error: ${res.status}`);
}

const data = await res.json();
console.log(data);
```

## Corrections and caveats from the video sketch

The instructor's diagram is useful as a high-level orientation. The following details should not be copied literally into technical notes.

| Sketch / simplification | More accurate understanding |
|---|---|
| Frontend source is `127.0.0.1:3000` and backend destination is `10.0.0.1:443` | `127.0.0.1` is a loopback address: it refers to the local machine, not a remote laptop address visible to an EC2 server. A browser request to a remote server uses the client's actual network path and source address as seen at each hop. |
| `10.0.0.1` is shown as the public API's DNS answer | `10.0.0.1` is in a private IPv4 range. It can be valid inside a private network/VPC, but it is not globally routable over the public internet. A public API hostname may resolve to a public address, CDN, load balancer, or other endpoint; private DNS can return private addresses within an appropriate network. |
| Source port is `3000` | Port 3000 may be the local development server's listening port for the frontend. A browser's outbound connection normally uses a client-side ephemeral source port; it is not generally the frontend server's listening port. |
| HTTPS request bytes are shown as readable HTTP headers and arbitrary hex | With HTTPS, HTTP content is protected by TLS on the network. A packet capture without appropriate decryption keys generally does not reveal the HTTP headers/body as plaintext. |
| HTTP is based on TCP | This is true for HTTP/1.1 and HTTP/2 in common deployments, but HTTP/3 uses QUIC over UDP. |
| TCP always splits data into a fixed number of chunks | Segment sizes and counts vary. TCP presents a byte stream, not application-defined message boundaries. |
| One frame contains the original source MAC and final server MAC | Ethernet MAC addresses are local-link addresses. A router normally replaces link-layer headers on the next link; the frame's destination MAC is the next hop, not a remote internet server's MAC. |
| ARP maps any IP anywhere to its MAC address | ARP resolves IPv4-to-link-layer mappings on a local link. For a remote destination, the client normally resolves the default gateway's local MAC address. |
| HTTP response `200 OK` is guaranteed | `200 OK` is only an example of a successful HTTP response. The actual status depends on the server and operation. |

### A note about the example's IP addresses

The screenshot combines a local loopback address (`127.0.0.1`) with a private IPv4 address (`10.0.0.1`) to illustrate source and destination fields. That is fine as a rough teaching sketch, but it should not be interpreted as a literal packet path from a laptop on the public internet to a public EC2 API.

For a real deployment, use the actual address and routing information of the environment. An EC2 instance's public and private DNS behavior depends on its networking configuration; AWS documents these details in its official DNS documentation.

## The most important mental model

Remember the responsibility of each layer:

- **Application / HTTP:** What request is being made?
- **DNS:** What address or service endpoint does this name resolve to?
- **Transport / TCP or QUIC:** How is application data carried between endpoints?
- **IP:** How are packets addressed and forwarded between networks?
- **Link layer / Ethernet or Wi-Fi:** How does the packet cross the current local link?
- **Physical layer:** What signals carry the bits?

These are conceptual responsibilities, not a claim that every protocol maps perfectly to one layer in every model.

## How this connects to data engineering and AI engineering

This flow is directly relevant when you:

- Ingest data from APIs using Python.
- Connect applications to remote databases.
- Deploy a FastAPI model-inference service.
- Connect a RAG application to a vector database and an LLM provider.
- Debug DNS, TLS, timeout, firewall, and connection errors.
- Run containers and services in a cloud VPC.
- Diagnose latency and throughput problems in distributed systems.

For troubleshooting, distinguish these classes of failure:

| Symptom | Areas to investigate first |
|---|---|
| Hostname cannot be resolved | DNS configuration, hostname, resolver |
| Connection refused | Destination address/port, whether the service is listening, firewall behavior |
| Connection timeout | Routing, firewall/security rules, unreachable or overloaded service, network path |
| TLS certificate error | Certificate validity, hostname match, trust chain, system clock |
| HTTP 401 / 403 | Authentication, authorization, application policy |
| HTTP 404 | URL path, routing, resource existence |
| HTTP 429 | Rate limits and retry policy |
| HTTP 5xx | Server or upstream dependency, logs, capacity |
| Slow response | Network latency, server processing, database or upstream latency, payload size |

These are starting points, not definitive diagnoses. Similar symptoms can have different causes, and status codes alone do not prove where a failure occurred.

## Key terms

- **Client:** The program initiating a request.
- **Server:** The software that receives requests and provides responses.
- **DNS:** A distributed system for resolving names and storing related records.
- **IP address:** A network-layer address.
- **Port:** A transport-layer identifier for an application endpoint.
- **Socket:** An operating-system communication endpoint; exact semantics depend on the API and protocol.
- **TCP:** A connection-oriented transport protocol providing a reliable, ordered byte stream.
- **TLS:** A protocol for securing communication, including confidentiality and integrity.
- **Packet:** Commonly used for an IP packet, though usage varies by context.
- **Frame:** A link-layer protocol data unit.
- **MAC address:** A link-layer address used for delivery on a local network technology.
- **ARP:** Address Resolution Protocol, used to resolve IPv4 addresses to link-layer addresses on a local link.
- **Default gateway:** The router a host typically uses to reach destinations outside its directly connected network.
- **Encapsulation:** Wrapping data with protocol-specific headers (and sometimes trailers) as it moves down the networking stack.

## Quick self-check

1. Why is `127.0.0.1` not the remote server's view of a laptop's address?
2. Why does a client usually resolve the gateway's MAC address rather than a remote server's MAC?
3. What is the difference between a TCP segment, an IP packet, and an Ethernet frame?
4. Why might a browser not perform a DNS lookup or TCP handshake for every request?
5. What changes when HTTPS is used instead of plain HTTP?
6. Why is “HTTP always uses TCP” inaccurate?
7. Why can a request fail before the server returns any HTTP status code?
8. Why is `200 OK` not proof that the returned business data is correct?

## Reliable references

Prefer standards and official documentation when checking protocol details.

1. **MDN — Overview of HTTP**  
   https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview  
   Explains HTTP's client-server model, its place in the protocol stack, connection handling, and HTTP evolution.

2. **IETF RFC 9110 — HTTP Semantics**  
   https://www.rfc-editor.org/rfc/rfc9110.html  
   The HTTP semantics specification, including methods, status codes, fields, and message semantics.

3. **IETF RFC 9293 — Transmission Control Protocol (TCP)**  
   https://www.rfc-editor.org/rfc/rfc9293.html  
   The TCP specification.

4. **IETF RFC 826 — An Ethernet Address Resolution Protocol (ARP)**  
   https://www.rfc-editor.org/rfc/rfc826.html  
   The original ARP specification and its role in mapping protocol addresses to local hardware addresses.

5. **IETF RFC 8446 — The Transport Layer Security (TLS) Protocol Version 1.3**  
   https://www.rfc-editor.org/rfc/rfc8446.html  
   Defines TLS 1.3.

6. **IETF RFC 9114 — HTTP/3**  
   https://www.rfc-editor.org/rfc/rfc9114.html  
   Defines HTTP/3, which uses QUIC.

7. **AWS — Understanding Amazon DNS**  
   https://docs.aws.amazon.com/vpc/latest/userguide/AmazonDNS-concepts.html  
   Explains AWS DNS behavior, including EC2 hostname resolution.

8. **AWS — EC2 Hostname Types**  
   https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/hostname-types.html  
   Describes private and public hostname behavior.

9. **Cloudflare Learning Center — What is a packet?**  
   https://www.cloudflare.com/learning/network-layer/what-is-a-packet/  
   A beginner-friendly explanation of packets and network communication.

---

## Summary

An HTTP request is not simply sent directly from JavaScript to a server. Application code creates the request; name resolution and routing help locate the destination; transport and security protocols carry the communication; IP packets are forwarded across networks; link-layer frames carry packets over individual links; and the server processes the request and returns a response.

The exact sequence varies with cached DNS, reused connections, proxies, the negotiated HTTP version, and the deployment architecture. Keep the layers distinct, and use this overview as the map for the deeper topics that follow.

