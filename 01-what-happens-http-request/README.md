# What Really Happens When You Make an HTTP Request?

> [!NOTE]
> **Section:** Computer Networking — [Chai aur Networking](https://youtube.com)
> 
> **Purpose:** Build an end-to-end mental model of how a browser request travels from application code through the operating system and network, reaches a server, and returns a response.

[← Back to Computer Networking Repository](https://github.com) 

---

## Overview

When an application makes an HTTP request, several networking components work together to deliver it to a server and return the response. This video introduces the overall journey from a frontend API call through DNS lookup and the operating system's networking stack, to transport and network addressing, local-network delivery, and transmission to the backend.

The diagram below brings these pieces together. It is an **overview**, not a detailed explanation of every protocol; each concept will be covered in its own topic.

## Complete Workflow Diagram

![Complete HTTP request workflow from Video 02 notes](assests/http-request-network-encapsulation-flow.png)

## Workflow at a Glance

### 🌐 1. Application Layer
1. **Frontend API call:** The browser starts an HTTP request, for example, through JavaScript's `fetch()` function.
2. **DNS lookup:** The domain hostname is resolved into an IP address so the client can identify the destination server.

### 📦 2. Transport & Operating System
3. **Transport layer:** The request uses an appropriate transport protocol — `TCP` for HTTP/1.1 and HTTP/2, or `QUIC` over `UDP` for HTTP/3.
4. **Operating-system networking stack:** The browser works with the OS networking stack to prepare and transmit the data.
5. **Encapsulation and addressing:** Application data is encapsulated with transport-layer information (such as source and destination ports), IP addressing information, and local-link framing information.

### 📡 3. Network & Link-Layer Delivery
6. **Local-network delivery:** The device prepares a frame for transmission over the local network. <mark>**ARP**</mark> helps resolve an IPv4 address to a MAC address when the next-hop MAC address is not already known.
7. **Routing and server processing:** Routers forward packets across networks towards the destination. The server receives the data, processes the request through its networking stack, and passes it to the backend application.

### 🔄 4. Response
8. **HTTP response:** The backend generates a response, which travels back through the network to the client, where the browser processes it.

---

> [!NOTE]
> **Accuracy note:** The concrete addresses, ports, byte values, and chunk count in the diagram are illustrative. In real networks, DNS answers and routes vary; client source ports are usually ephemeral; connections may be reused; and the number and size of TCP segments are not fixed. With HTTPS, HTTP content is encrypted in transit after TLS is established. The exact transport also depends on the HTTP version.

## Key Takeaway

An HTTP request is not sent directly from frontend code to a backend as one indivisible object. Browser networking, the operating system, transport protocols, IP routing, and local-link delivery each contribute to moving the request across the network.

These are the building blocks for the next topics. DNS, TCP/UDP, ports, IP addressing, routing, MAC addresses, ARP, TLS, and HTTP versions will be explored separately rather than explained in depth here.

---
**Next:** [Network-Host-CIDR](../02-network-host-cidr/)
