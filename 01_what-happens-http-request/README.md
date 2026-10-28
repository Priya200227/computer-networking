# What Really Happens When You Make an HTTP Request?

> **Section:** Computer Networking — [Chai aur Networking - 02](https://www.youtube.com/watch?v=_dCmQCiQmPE&list=PLd1s-PEC5Pio&index=2)
> **Purpose:** Build an end-to-end mental model of how a browser request travels from application code through the operating system and network, reaches a server, and returns a response.

## Overview

When frontend code calls an API, the request does not travel directly from JavaScript to the backend as a single object. The browser, operating system, transport protocol, IP layer, and local network each perform different jobs.

This section connects the concepts that appear throughout the networking course:

- HTTP requests and responses
- DNS name resolution
- TCP connections, ports, and segments
- The operating system's TCP/IP networking stack
- IP packets and IP addressing
- Link-layer frames and MAC addresses
- ARP and the default gateway
- Physical or wireless transmission

The workflow diagram below is the **complete diagram from my Video 02 notes**. It is kept as supplied so that it can be reviewed alongside the explanation and corrections in this README.

## Complete workflow diagram

![Complete HTTP request workflow from Video 02 notes](assests/http-request-workflow.png)

## 1. Start with an API call

A frontend might contain code such as:

```javascript
const res = await fetch("https://api.example.com/profile");
```

This asks the browser to make an HTTP request to the `/profile` resource on the host `api.example.com`. The call is asynchronous: `await` waits for the fetch operation to settle before the next line executes.

The browser handles the request on behalf of the JavaScript code. JavaScript does not manually construct Ethernet frames, calculate TCP sequence numbers, or transmit electrical/radio signals.

## 2. DNS: translate a hostname into an IP address

A hostname such as `api.example.com` is a human-friendly name. To connect to a server, the client needs an appropriate IP address.

The Domain Name System (DNS) provides records that help resolve names to addresses. A simplified view is:

```text
api.example.com
      |
      v
     DNS
      |
      v
an IP address (IPv4 and/or IPv6)
```

Important details:

- DNS resolution may be answered from browser, operating-system, or network caches; a new DNS query is not required for every request.
- A hostname can resolve to multiple addresses, and the result can vary by resolver, network, region, or configuration.
- The address returned for a public API may belong to a CDN, reverse proxy, or load balancer rather than directly to the application server.
- A private address such as `10.0.0.1` can be valid inside a private cloud network, but it is not a globally routable public Internet destination.

DNS resolves names; it does **not** carry the HTTP request itself.

## 3. HTTPS, HTTP, and the transport connection

The URL starts with `https://`, which means the browser is expected to use HTTP securely over TLS.

For the common combinations:

- **HTTP/1.1 and HTTP/2:** HTTP is carried over a TCP connection protected by TLS when using HTTPS.
- **HTTP/3:** HTTP is carried over QUIC, which uses UDP, with security integrated into QUIC.

Therefore, “HTTP always uses TCP” is not universally true. The negotiated HTTP version matters.

For an HTTPS connection using TCP, the client and server normally establish a TCP connection before application data is exchanged. TCP's three-way handshake is commonly described as:

1. Client sends `SYN`.
2. Server responds with `SYN-ACK`.
3. Client sends `ACK`.

TLS then establishes the secure session before HTTP data is exchanged, unless an existing connection/session can be reused or a supported protocol mechanism changes the setup sequence.

A new TCP handshake and TLS handshake do **not** necessarily happen for every `fetch()` call: browsers can reuse existing connections.

## 4. HTTP request: method, path, headers, and body

An HTTP request communicates what the client wants the server to do. A simplified conceptual request might be:

```http
GET /profile HTTP/1.1
Host: api.example.com
Authorization: Bearer <token>
Cookie: <cookie-value>
```

The actual headers depend on the browser, application, security policy, cookies, and server configuration. A `GET` request often has no body, but HTTP supports request bodies for methods and use cases that need them.

With HTTPS, the HTTP request is encrypted in transit after TLS is established. A normal packet capture on the network cannot simply read the HTTP headers and body as plaintext without access to the relevant decryption keys or an endpoint-level view.

## 5. The browser and operating system hand off network data

The browser prepares the request and uses operating-system networking facilities to send it. The operating system's networking stack handles transport and network-layer work, such as TCP/UDP and IP processing.

A useful conceptual sequence is:

```text
Frontend JavaScript
        |
        v
Browser networking implementation
        |
        v
Transport layer (TCP, or QUIC over UDP)
        |
        v
IP layer
        |
        v
Link layer / network interface
        |
        v
Wi-Fi or Ethernet network
```

This is a conceptual layer model, not a promise that every implementation uses exactly the same internal components or call sequence.

## 6. Ports: identify the application endpoint

IP addresses help identify a host/interface at the IP layer. Transport-layer port numbers help identify the relevant communication endpoint on that host.

For example, a server might accept HTTPS connections on port `443`. The client typically uses an **ephemeral source port** selected for the outbound connection.

Do not confuse:

- **Frontend development-server port:** for example, `3000`, where a local development server may listen.
- **Client source port:** the ephemeral port used by the browser's outbound network connection.
- **Server destination port:** often `443` for HTTPS.

These can be different. A diagram that labels `3000` as the source port is illustrating a possible setup, not a rule that the browser's connection must use port 3000.

## 7. Encapsulation: data, segment, packet, and frame

As data moves through the networking stack, each layer adds the information it needs. This is called **encapsulation**.

```text
Application data
      |
      v
TCP segment (TCP header + payload)
      |
      v
IP packet (IP header + payload)
      |
      v
Link-layer frame (link header/trailer + payload)
      |
      v
Signals transmitted over the network medium
```

Terminology matters:

- **HTTP message/data:** the application-level request or response.
- **TCP segment:** TCP header plus a portion of the byte stream.
- **IP packet** (often called an IP datagram): IP header plus its payload.
- **Link-layer frame:** local-network framing, such as an Ethernet frame or a Wi-Fi data frame.
- **Bits/signals:** the representation transmitted over a physical or radio medium.

These units are related but are **not interchangeable**.

TCP provides a reliable, ordered byte stream. An application write, HTTP message, TCP segment, IP packet, and link-layer frame do not necessarily map one-to-one. Segment count and size depend on factors such as path MTU, TCP behavior, congestion control, offloading, and implementation details. A diagram showing a fixed number of chunks is illustrative, not a general rule.

## 8. IP addresses and MAC addresses do different jobs

### IP address

An IP address is used for logical addressing and routing between IP networks. In a simplified client-to-server view, the source and destination IP addresses identify the IP endpoints for the packet. Network Address Translation (NAT), proxies, VPNs, and other mechanisms can alter what addresses are seen at different points.

### MAC address

A MAC address is used for delivery on a local link, such as an Ethernet or Wi-Fi network. It is not normally used by Internet routers as the end-to-end address of the remote server.

When a destination is outside the local subnet, the laptop generally sends the first frame to the **default gateway's MAC address**, not the remote server's MAC address. The IP packet is routed onward, and each routed link uses its own link-layer framing.

Consequently:

- The destination IP can represent a remote endpoint.
- The destination MAC in the laptop's first outbound frame usually represents the next hop (often the default gateway).
- The MAC header is replaced as the packet is forwarded across routed links; IP addresses usually remain the same end-to-end, except where mechanisms such as NAT or tunneling intervene.

## 9. ARP: resolve a local IPv4 next-hop address

Address Resolution Protocol (ARP) helps a device on an IPv4 local network discover the link-layer address associated with a local IPv4 address.

For example, if a laptop needs to send traffic through a default gateway at `192.168.1.1`, it may need to learn the gateway's MAC address. It can use an ARP request on the local link if the mapping is not already cached.

ARP does **not** discover the MAC address of an arbitrary remote Internet server across multiple routers. The laptop only needs the MAC address of the next hop on its local link.

For IPv6, the equivalent neighbor-resolution functionality is provided by **Neighbor Discovery**, not ARP.

## 10. Transmission and routing

The local network interface transmits data using the available link technology—for example, Wi-Fi radio signals or electrical/optical signaling over wired media.

If the destination is remote, routers forward IP packets between networks. At each link, the packet is carried inside the framing appropriate to that link. The remote server's network interface and operating system then process the incoming traffic and deliver it to the relevant transport endpoint and application.

The backend application handles the request and creates an HTTP response. The response travels back through the networking stack to the client, though its route need not be identical to the request's route.

## 11. The response returns to the frontend

A server might return a successful response, such as `200 OK`, along with data. That status is only an example: the server may instead return another 2xx response, a redirect, or an error status such as 4xx or 5xx.

With the Fetch API, an HTTP error status such as `404` or `500` does **not** usually cause `fetch()` to reject. Check `response.ok` or `response.status`:

```javascript
const response = await fetch("https://api.example.com/profile");

if (!response.ok) {
  throw new Error(`HTTP error: ${response.status}`);
}

const data = await response.json();
```

This example assumes the response body contains JSON. Production code should also consider network failures, timeouts/abort signals, authentication, and response validation.

## Corrections and precision notes for the diagram

The diagram is useful as an end-to-end overview. Treat its concrete values and some simplified labels as examples rather than universal rules:

| Diagram idea | More precise interpretation |
|---|---|
| `api.example.com → 10.0.0.1` | A possible private DNS mapping; public DNS may resolve to a public IP, CDN, or load balancer. `10.0.0.1` is a private IPv4 address. |
| Frontend port `3000` is the source port | Port 3000 may be the local development server's listening port. The browser's outbound connection normally uses an ephemeral source port. |
| Every request performs DNS resolution | Cached DNS results may be reused. |
| Every request requires a new TCP handshake | Existing connections may be reused. HTTP/3 uses QUIC over UDP rather than TCP. |
| HTTP headers are shown as bytes | With HTTPS, HTTP contents are encrypted on the network after TLS is established. |
| TCP creates a fixed number of chunks | TCP segments and sizes vary; application data boundaries do not map one-to-one to TCP segments. |
| TCP segment, IP packet, and frame are equivalent | They are different protocol-layer units created through encapsulation. |
| Laptop sends to the remote server's MAC address | The first frame usually targets the local next hop, such as the default gateway. |
| ARP finds any device's MAC address over the Internet | ARP resolves IPv4-to-link-layer mappings on the local link. IPv6 uses Neighbor Discovery. |
| Response is always `200 OK` | The server can return many status codes; check `response.ok` in Fetch API code. |

## Why this matters for data and AI engineering

This workflow appears in everyday engineering work:

- **Data pipelines:** clients connect to APIs, databases, object storage, and orchestration services.
- **Data engineering:** services communicate with warehouses, message brokers, compute clusters, and cloud storage.
- **AI applications:** a frontend or backend calls model APIs, embedding services, vector databases, and retrieval services.
- **Deployment and debugging:** DNS, ports, TLS certificates, firewall rules, routes, and connection timeouts are frequent sources of failures.
- **Distributed systems:** a request often crosses multiple services and network boundaries before a result is returned.

Understanding the layers makes it easier to diagnose whether a failure is in application logic, name resolution, connectivity, transport, TLS, routing, or the remote service.

## Quick self-check

Try answering these without looking back at the notes:

1. Why does a client need an IP address after it already has a hostname?
2. What is the difference between a TCP segment, an IP packet, and a link-layer frame?
3. Why does a laptop usually send a frame to the default gateway's MAC address for a remote destination?
4. What does a port number identify, and why might the browser's source port differ from the frontend development port?
5. Why is it inaccurate to say that every HTTP request creates a new TCP connection?
6. What changes when a request uses HTTPS rather than plain HTTP?
7. Why does ARP not resolve the MAC address of a remote Internet server?
8. What should frontend code check when `fetch()` receives an HTTP 404 or 500 response?

## References

These primary or authoritative references are useful for deeper study:

- [MDN — Overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview)
- [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html)
- [RFC 9293 — Transmission Control Protocol (TCP)](https://www.rfc-editor.org/rfc/rfc9293.html)
- [RFC 8446 — The Transport Layer Security (TLS) Protocol Version 1.3](https://www.rfc-editor.org/rfc/rfc8446.html)
- [RFC 9114 — HTTP/3](https://www.rfc-editor.org/rfc/rfc9114.html)
- [RFC 826 — An Ethernet Address Resolution Protocol (ARP)](https://www.rfc-editor.org/rfc/rfc826.html)
- [MDN — Using the Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
- [AWS — DNS concepts for Amazon VPC](https://docs.aws.amazon.com/vpc/latest/userguide/AmazonDNS-concepts.html)

---

**Learning note:** This page is a conceptual map of the request path. Later sections should study DNS, TCP/UDP, ports and sockets, IP addressing and routing, Ethernet/Wi-Fi, ARP, TLS, and HTTP versions individually.
