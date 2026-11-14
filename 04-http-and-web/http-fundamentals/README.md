# HTTP Fundamentals — Requests, Responses, Methods, Cookies & HTTPS

> [!NOTE]
> **Section:** Computer Networking — HTTP  
> **Learning objective:** Understand HTTP's client-server model, statelessness, URL structure, request and response semantics, methods, status codes, headers, cookies, sessions, and HTTPS.

[← Back to Computer Networking Repository](https://github.com/Priya200227/computer-networking)

---

## 1. What Is HTTP?

**HTTP (Hypertext Transfer Protocol)** is an application-layer protocol that defines how clients and servers communicate.

It specifies the rules for exchanging requests and responses, including:

- What action the client wants to perform.
- Which resource the client is requesting.
- What additional information accompanies the request.
- How the server communicates the result.
- How application data is represented and transferred.

HTTP is independent of the physical medium used to carry the data. The underlying network stack handles the delivery.

### Client–Server Architecture

HTTP communication follows a client-server model.

| Component | Responsibility | Examples |
|---|---|---|
| Client | Initiates requests and processes responses | Browser, mobile app, Postman |
| Server | Receives requests and provides responses | Web server, API server |

**Basic communication flow:**

```text
Client
  |
  | HTTP Request
  v
Server
  |
  | HTTP Response
  v
Client
```

The client initiates an HTTP request. The server processes it and returns an HTTP response.

### HTTP Is an Application-Layer Protocol

HTTP defines the application-level communication rules. It does not define how electrical signals, radio waves, or optical signals travel through the network.

For example:

```text
Application Layer  → HTTP
Transport Layer    → TCP / QUIC
Network Layer      → IP
Link Layer         → Ethernet / Wi-Fi
Physical Layer     → Electrical / Radio / Optical signals
```

The transport protocol depends on the HTTP version:

- HTTP/1.1 → commonly uses TCP.
- HTTP/2 → uses TCP.
- HTTP/3 → uses QUIC over UDP.

---

## 2. Why Is HTTP Stateless?

HTTP is designed as a **stateless protocol**.

This means that each request is treated as an independent request at the protocol level. HTTP does not automatically require the server to remember the context of previous requests.

Consider this example:

```text
Request 1:
Client → Server
Login request

Response 1:
Server → Client
Login successful

Request 2:
Client → Server
Request for user profile
```

HTTP itself does not automatically remember that Request 1 was a login request when processing Request 2.

### Why Statelessness Matters

**1. Scalability**

A stateless application can distribute requests across multiple server instances without requiring every instance to maintain the same in-memory client session.

```text
                 Load Balancer
                       |
             ---------------------
             |         |         |
          Server A  Server B  Server C
```

**2. Simpler request processing**

Each request carries the information needed to process it, rather than depending entirely on hidden conversational state stored in a particular server process.

**3. Easier horizontal scaling**

Additional server instances can be introduced behind a load balancer.

> [!IMPORTANT]
> Statelessness does not mean that servers cannot store user information.
>
> Applications can maintain state using databases, session stores, cookies, tokens, and other mechanisms. The distinction is that HTTP does not provide automatic session memory as part of its basic request-response model.

---

## 3. How Do Web Applications Remember Users?

If HTTP is stateless, how does a website remember that a user has logged in?

The answer involves mechanisms such as **cookies, sessions, and authentication tokens**.

### 3.1 Cookies

A cookie is a small piece of data that a server asks a browser to store.

The server sends a cookie using the `Set-Cookie` response header.

Example:

```http
HTTP/1.1 200 OK
Set-Cookie: session_id=abc123; Path=/; HttpOnly; Secure
```

The browser stores the cookie according to its attributes and applicable browser policies.

When making a subsequent matching request, the browser can send it back:

```http
GET /profile HTTP/1.1
Host: example.com
Cookie: session_id=abc123
```

The server can use the session identifier to look up the associated session information.

### 3.2 How a Session Works

A common server-side session workflow:

```text
1. User logs in
       |
       v
2. Browser sends credentials
       |
       v
3. Server validates credentials
       |
       v
4. Server creates a session
       |
       v
5. Server sends a session cookie
       |
       v
6. Browser stores the cookie
       |
       v
7. Browser sends cookie with later requests
       |
       v
8. Server validates the session
       |
       v
9. Requested resource is returned
```

The cookie often contains a session identifier, not the complete session data.

The actual session information may be stored on the server or in a shared session store.

### 3.3 Cookies vs. Sessions

| Cookie | Session |
|---|---|
| Stored by the browser | Commonly maintained on the server |
| Sent with matching requests | Looked up using a session identifier |
| Can contain an identifier or other permitted data | Can contain application-specific session state |
| Controlled by cookie attributes and browser policies | Controlled by application and server-side logic |

### 3.4 Cookies vs. JWT

A cookie is a browser storage and transport mechanism. A JWT is a token format.

They are not direct alternatives.

- A cookie can carry a session identifier.
- A cookie can also carry a JWT.
- A JWT can be sent using an `Authorization` header.

For example:

```http
Authorization: Bearer <access_token>
```

> [!NOTE]
> A JWT is not automatically secure simply because it is signed. Signing protects integrity, not confidentiality. A typical signed JWT payload is readable by anyone who obtains the token.

---

## 4. Cookie Security Attributes

Cookies can include attributes that help control how browsers store and send them.

Example:

```http
Set-Cookie: session_id=abc123;
            Path=/;
            HttpOnly;
            Secure;
            SameSite=Lax
```

| Attribute | Purpose |
|---|---|
| `HttpOnly` | Prevents JavaScript from accessing the cookie through browser cookie APIs |
| `Secure` | Restricts cookie transmission to secure connections, normally HTTPS |
| `SameSite` | Controls when cookies are sent in cross-site request contexts |
| `Path` | Restricts the request paths for which the cookie is sent |
| `Domain` | Controls the domain scope of the cookie |
| `Max-Age` | Specifies the cookie lifetime in seconds |
| `Expires` | Specifies an expiration date and time |

### Why Is HttpOnly Important?

JavaScript running in a page cannot read an `HttpOnly` cookie through `document.cookie`.

This helps reduce the risk of session-cookie theft through certain cross-site scripting (XSS) attacks.

However, `HttpOnly` does not prevent XSS itself. Malicious scripts may still perform actions using the user's authenticated browser session.

### Why Is Secure Important?

The `Secure` attribute instructs the browser to send the cookie only over secure connections.

This helps prevent the cookie from being transmitted over unencrypted HTTP.

> [!WARNING]
> Cookie attributes are security controls, not a complete security solution. Applications must also implement appropriate session expiration, access control, CSRF protections where applicable, and secure authentication practices.

---

## 5. URL Anatomy

A URL (Uniform Resource Locator) identifies the location of a resource and describes how it can be accessed.

Example:

```text
https://api.example.com:443/users/profile?id=101#details
```

### URL Components

| Component | Example | Purpose |
|---|---|---|
| Scheme | `https` | Identifies the access scheme |
| Host | `api.example.com` | Identifies the host |
| Port | `443` | Identifies the destination port |
| Path | `/users/profile` | Identifies the requested resource |
| Query | `?id=101` | Supplies additional parameters |
| Fragment | `#details` | Identifies a location within the resource |

A simplified structure:

```text
https://api.example.com:443/users/profile?id=101#details
  |           |          |       |             |       |
Scheme       Host       Port    Path         Query  Fragment
```

### URI vs. URL vs. URN

These terms are related but not identical.

| Term | Meaning |
|---|---|
| URI | Uniform Resource Identifier — identifies a resource |
| URL | Uniform Resource Locator — identifies a resource by describing how and where to access it |
| URN | Uniform Resource Name — identifies a resource by name within a namespace |

**Relationship:** A URL and a URN are both types of URI.

### Important: Do Not Put Sensitive Data in URLs

Query parameters can appear in:

- Browser history.
- Web server logs.
- Proxy logs.
- Analytics systems.
- Referrer information, depending on browser policies and request context.

Avoid putting passwords, session secrets, and sensitive tokens in URLs.

Use appropriate request headers or request bodies, along with HTTPS and proper access controls.

---

## 6. Anatomy of an HTTP Request

An HTTP request communicates what the client wants the server to do.

For HTTP/1.1, a request generally contains:

1. Request line.
2. Headers.
3. Empty line.
4. Optional message body.

Example:

```http
POST /api/v1/users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Accept: application/json
User-Agent: ExampleClient/1.0

{
  "name": "Priya",
  "email": "priya@example.com"
}
```

### 6.1 Request Line

```http
POST /api/v1/users HTTP/1.1
```

It contains three parts:

| Part | Value | Meaning |
|---|---|---|
| Method | `POST` | Action requested |
| Request target | `/api/v1/users` | Resource being requested |
| HTTP version | `HTTP/1.1` | Protocol version |

### 6.2 Request Headers

Headers provide additional information about the request.

Examples:

```http
Host: api.example.com
Content-Type: application/json
Accept: application/json
Authorization: Bearer <token>
User-Agent: ExampleClient/1.0
```

### 6.3 Empty Line

In HTTP/1.1, an empty line separates the header section from the optional message body.

### 6.4 Request Body

The body carries application data when required.

For example, a POST request may send JSON data:

```json
{
  "name": "Priya",
  "email": "priya@example.com"
}
```

A GET request typically does not use a request body. Clients and servers should not rely on GET request content having generally defined semantics.

> [!NOTE]
> This example shows HTTP/1.1 textual syntax. HTTP/2 and HTTP/3 represent HTTP semantics using their respective binary framing mechanisms rather than transmitting this exact textual request format.

---

## 7. Anatomy of an HTTP Response

An HTTP response communicates the result of a request.

An HTTP/1.1 response generally contains:

1. Status line.
2. Headers.
3. Empty line.
4. Optional message body.

Example:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 42
Cache-Control: no-store

{
  "message": "User created successfully"
}
```

### 7.1 Status Line

```http
HTTP/1.1 200 OK
```

It contains:

- HTTP version.
- Status code.
- Optional reason phrase.

### 7.2 Response Headers

Headers provide metadata about the response.

Examples:

```http
Content-Type: application/json
Content-Length: 42
Cache-Control: no-store
Set-Cookie: session_id=abc123; HttpOnly; Secure
```

### 7.3 Empty Line

Separates the response headers from the optional response body.

### 7.4 Response Body

Contains the returned representation, if one is included.

It may contain JSON, HTML, images, or other content.

---

## 8. HTTP Status Codes

HTTP status codes indicate the result of processing a request.

They are grouped into five categories.

| Category | Range | Meaning |
|---|---|---|
| 1xx | 100–199 | Informational |
| 2xx | 200–299 | Successful |
| 3xx | 300–399 | Redirection |
| 4xx | 400–499 | Client error |
| 5xx | 500–599 | Server error |

### Common Status Codes

| Code | Name | Meaning |
|---|---|---|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 202 | Accepted | Request accepted for processing, but processing may not be complete |
| 204 | No Content | Request succeeded; no response content is returned |
| 301 | Moved Permanently | Resource has a permanent redirect |
| 302 | Found | Temporary redirect |
| 304 | Not Modified | Cached representation can be reused |
| 400 | Bad Request | Request cannot be processed due to a client-side problem |
| 401 | Unauthorized | Valid authentication credentials are missing or not accepted |
| 403 | Forbidden | Server refuses the request |
| 404 | Not Found | Requested resource was not found |
| 405 | Method Not Allowed | Method is not supported for the target resource |
| 409 | Conflict | Request conflicts with the current resource state |
| 429 | Too Many Requests | Client has sent too many requests |
| 500 | Internal Server Error | Unexpected server-side failure |
| 502 | Bad Gateway | Gateway received an invalid response from an upstream server |
| 503 | Service Unavailable | Server is temporarily unable to handle the request |
| 504 | Gateway Timeout | Gateway did not receive a timely upstream response |

### 401 vs. 403

These two status codes are commonly confused.

**401 Unauthorized**

The request lacks valid authentication credentials.

Example:

```text
The user has not provided a valid login token.
```

**403 Forbidden**

The server understands the request but refuses to authorize it.

Example:

```text
The user is authenticated but does not have permission
to access the administrator dashboard.
```

> [!TIP]
> During debugging, first inspect the status-code category. It helps narrow down whether the issue is related to the request, authentication, authorization, redirection, or server processing.

---

## 9. HTTP Methods

HTTP methods describe the intended action for a request.

| Method | Purpose | Example |
|---|---|---|
| GET | Retrieve a resource | Fetch user details |
| POST | Submit data for processing or resource creation | Create an order |
| PUT | Create or replace the target resource's representation | Replace user details |
| PATCH | Apply a partial modification | Update only a user's city |
| DELETE | Remove a resource | Delete a user |
| HEAD | Retrieve response headers without the response content | Check resource metadata |
| OPTIONS | Discover communication options supported by a resource or server | Check supported methods |

### PUT vs. PATCH

Suppose a user resource contains:

```json
{
  "name": "Priya",
  "city": "Bangalore",
  "phone": "9876543210"
}
```

**PUT — Replace the resource representation**

A PUT request might send:

```json
{
  "name": "Priya Sharma",
  "city": "Hyderabad",
  "phone": "9876543210"
}
```

The target resource is replaced according to the server's PUT semantics.

**PATCH — Apply a partial modification**

A PATCH request might send:

```json
{
  "city": "Hyderabad"
}
```

Only the specified change is requested.

The exact behavior depends on the PATCH document format and server implementation.

---

## 10. Safe vs. Idempotent Methods

Two important HTTP method properties are **safety** and **idempotency**.

### 10.1 Safe Methods

A method is safe when the client is requesting a read-only operation.

The intended effect is not to change the server's resource state.

Examples:

- GET
- HEAD
- OPTIONS

### 10.2 Idempotent Methods

A method is idempotent when making the same request multiple times has the same intended effect on the server as making it once.

For example:

```text
PUT /users/101

Send the same replacement request once.
Send the same replacement request five times.

The intended resource state remains the same.
```

### Method Properties

| Method | Safe? | Idempotent? |
|---|---|---|
| GET | Yes | Yes |
| HEAD | Yes | Yes |
| OPTIONS | Yes | Yes |
| POST | No | No, generally |
| PUT | No | Yes |
| PATCH | No | Not guaranteed |
| DELETE | No | Yes |

### Why Does Idempotency Matter?

Consider a payment request:

```text
POST /payments
```

If the client retries the request because the network timed out, the server might process the payment again.

This is why payment systems often use **idempotency keys** to prevent duplicate processing.

> [!IMPORTANT]
> Idempotency describes the intended effect on server state, not whether every repeated response must be identical.
>
> For example, repeating DELETE may return `404 Not Found` after the first request succeeds, while the intended resource state remains unchanged.

---

## 11. Important HTTP Headers

HTTP headers carry metadata about requests and responses.

### 11.1 Content-Type

Indicates the media type of the message content.

Example:

```http
Content-Type: application/json
```

Other examples:

```http
Content-Type: text/html
Content-Type: application/xml
Content-Type: multipart/form-data
```

For file uploads, `multipart/form-data` is commonly used.

### 11.2 Accept

Indicates the media types the client is willing to receive.

Example:

```http
Accept: application/json
```

### Content-Type vs. Accept

| Header | Meaning |
|---|---|
| Content-Type | What format is being sent? |
| Accept | What format can the client receive? |

### 11.3 Cache-Control

Specifies caching directives for HTTP requests and responses.

Examples:

```http
Cache-Control: no-store
Cache-Control: no-cache
Cache-Control: max-age=3600
Cache-Control: private
Cache-Control: public
```

| Directive | Meaning |
|---|---|
| `no-store` | Do not store the response in a cache |
| `no-cache` | A stored response must be validated before reuse |
| `max-age=3600` | Response is fresh for 3600 seconds |
| `private` | Response is intended for a private cache |
| `public` | Response may be stored by shared caches, subject to other rules |

> [!IMPORTANT]
> `no-cache` does not mean the response cannot be stored. It means the stored response must be validated before reuse.
>
> `no-store` is the directive used when the response should not be stored by caches.

---

## 12. HTTP vs. HTTPS

HTTP communication can be transmitted without transport encryption.

HTTPS is HTTP communication protected using **TLS (Transport Layer Security)**.

```text
HTTP
 |
 | Application communication
 |
TCP (HTTP/1.1 or HTTP/2)
```

With HTTPS:

```text
HTTP
 |
TLS Encryption
 |
TCP (HTTP/1.1 or HTTP/2)
```

For HTTP/3, TLS 1.3 is integrated with QUIC rather than being layered over TCP.

### What Does TLS Provide?

**1. Confidentiality**

Encrypts application data so that network observers cannot normally read the protected HTTP contents.

**2. Integrity**

Helps detect unauthorized modification of data in transit.

**3. Authentication**

Allows the client to authenticate the server using its certificate and the TLS validation process.

### What Can a Network Observer See?

HTTPS protects the HTTP request and response contents, including paths, query strings, headers, and bodies.

However, HTTPS does not make every aspect of a connection invisible.

Depending on the network setup and TLS features, observers may still infer information such as:

- Destination IP address.
- Connection timing and traffic volume.
- Domain information in some connection setups.

DNS queries may also be visible unless protected separately. Encrypted ClientHello (ECH), where supported, can protect additional TLS handshake information.

> [!NOTE]
> HTTPS is not a separate replacement for HTTP semantics. It is HTTP communication protected by TLS.

---

## 13. HTTP Polling vs. WebSockets

HTTP follows a request-response model: the client initiates a request, and the server sends a response.

But how do applications display frequently changing information, such as live scores or notifications?

Two common approaches are polling and WebSockets.

### 13.1 Polling

The client periodically sends requests to check whether new information is available.

```text
Client                  Server
  |                        |
  |------ Request -------->|
  |<------ Response -------|
  |                        |
  |   Wait for interval    |
  |                        |
  |------ Request -------->|
  |<------ Response -------|
```

This is simple to implement, but can create unnecessary requests when no new data is available.

### 13.2 WebSockets

WebSockets provide a persistent, bidirectional communication channel.

After an opening handshake, both client and server can send messages independently.

```text
Client                  Server
  |                        |
  |--- Opening Handshake ->|
  |<------ Accepted -------|
  |                        |
  |<---- Server Message ---|
  |                        |
  |----- Client Message -->|
  |                        |
  |<---- Server Message ---|
```

### Polling vs. WebSockets

| Polling | WebSockets |
|---|---|
| Repeated HTTP requests | Persistent connection |
| Client periodically checks for updates | Both sides can send messages |
| Simple request-response model | Bidirectional communication |
| Can create repeated request overhead | Useful for frequent real-time updates |

> [!NOTE]
> WebSockets are not simply HTTP requests that remain open forever. They use an opening handshake and then switch to the WebSocket protocol. HTTP/1.1 commonly uses an Upgrade handshake; HTTP/2 and HTTP/3 support WebSockets through their respective extended CONNECT mechanisms.

---

## 14. Complete HTTP Concept Map

```text
HTTP
 |
 +-- Fundamentals
 |    +-- Protocol
 |    +-- Client-Server Architecture
 |    +-- Application Layer
 |    +-- Statelessness
 |
 +-- Resource Identification
 |    +-- URL
 |    +-- URI
 |    +-- URN
 |
 +-- Request and Response
 |    +-- Request Line
 |    +-- Headers
 |    +-- Body
 |    +-- Status Line
 |    +-- Status Codes
 |
 +-- HTTP Semantics
 |    +-- Methods
 |    +-- Safe Methods
 |    +-- Idempotency
 |
 +-- State Management
 |    +-- Cookies
 |    +-- Sessions
 |    +-- JWT
 |    +-- Cookie Security
 |
 +-- HTTP Headers
 |    +-- Content-Type
 |    +-- Accept
 |    +-- Cache-Control
 |
 +-- Security
 |    +-- HTTPS
 |    +-- TLS
 |
 +-- Real-Time Communication
      +-- Polling
      +-- WebSockets
```

---

## Key Takeaways

| Concept | What to remember |
|---|---|
| HTTP | Application-layer request-response protocol |
| Statelessness | HTTP does not inherently maintain client session state |
| URL | Identifies a resource and describes how to access it |
| Request | Communicates the client's intended operation |
| Response | Communicates the server's result |
| Status code | Indicates the outcome of request processing |
| HTTP methods | Define the intended action |
| Safe | Intended not to modify server resource state |
| Idempotent | Repetition has the same intended effect |
| Cookies | Small pieces of data stored by the browser |
| Sessions | Application mechanism for maintaining user state |
| Content-Type | Describes the message content format |
| Accept | Indicates acceptable response formats |
| Cache-Control | Controls caching behavior |
| HTTPS | HTTP protected using TLS |
| WebSockets | Persistent, bidirectional communication |

## References

- [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html)
- [RFC 9111 — HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111.html)
- [RFC 9112 — HTTP/1.1](https://www.rfc-editor.org/rfc/rfc9112.html)
- [RFC 9113 — HTTP/2](https://www.rfc-editor.org/rfc/rfc9113.html)
- [RFC 9114 — HTTP/3](https://www.rfc-editor.org/rfc/rfc9114.html)
- [RFC 8446 — TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446.html)
- [RFC 6265 — HTTP State Management Mechanism (Cookies)](https://www.rfc-editor.org/rfc/rfc6265.html)
- [RFC 6455 — The WebSocket Protocol](https://www.rfc-editor.org/rfc/rfc6455.html)

---

**Suggested next topics:** HTTP caching in depth, authentication and authorization, CORS, and API design.
