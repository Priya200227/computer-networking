# DNS — Major Resource Record Types

> **Learning objective:** Understand the purpose, structure, and practical use of the major DNS resource record types — A, AAAA, MX, CNAME, NS, TXT, and PTR — and how they support name resolution, mail routing, delegation, and reverse DNS.

[← Back to Computer Networking](https://github.com/Priya200227/computer-networking)

---

## 1. Overview

DNS stores information as **resource records (RRs)**. Not every record maps a domain name to an IP address: different record types publish different kinds of information.

- `A` maps a hostname to an IPv4 address.
- `AAAA` maps a hostname to an IPv6 address.
- `MX` identifies mail-exchange hostnames for a domain.
- `CNAME` aliases one hostname to another hostname.
- `NS` identifies authoritative name servers for a DNS zone and enables delegation.
- `TXT` publishes text data used by services, including email-authentication systems.
- `PTR` maps an IP address to a hostname in reverse DNS.

The examples use values from the supplied notes and are illustrative, not confirmation of a live domain's current DNS configuration.

## 2. Anatomy of a DNS resource record

A common textual representation is:

```text
NAME    TTL    CLASS    TYPE    RDATA
```

| Field | Meaning |
|---|---|
| `NAME` | Owner name — the domain or hostname to which the record belongs |
| `TTL` | Time to live, in seconds; controls how long a resolver may cache the record |
| `CLASS` | DNS class; `IN` means Internet |
| `TYPE` | Record type, such as `A`, `AAAA`, `MX`, or `TXT` |
| `RDATA` | Type-specific data/value |

Example:

```text
jyothipriya.in.  3600  IN  A  3.111.187.148
```

`jyothipriya.in.` is the owner name; `3600` is a one-hour TTL; `IN` is the Internet class; `A` identifies an IPv4 address record; and `3.111.187.148` is its RDATA.

**TTL is not the lifetime of a domain or server.** It is a caching duration. A resolver can reuse cached data until its TTL expires. If the authoritative record changes, cached answers may remain visible until their TTLs expire.

![DNS resource record fields](images/01-dns-resource-record-fields.png)

## 3. A record — IPv4 address

An `A` record maps a hostname to an IPv4 address.

```text
jyothipriya.in.  3600  IN  A  3.111.187.148
```

An `A` query asks: *What IPv4 address is associated with this hostname?*

A hostname can have multiple A records:

```text
jyothipriya.in.  3600  IN  A  3.111.187.148
jyothipriya.in.  3600  IN  A  3.111.187.149
```

Multiple addresses can support endpoint distribution, redundancy, or failover. But multiple A records alone do **not** guarantee health-aware load balancing or automatic failover. Resolver selection, client behaviour, caching, and service architecture all matter.

An A record stores a 32-bit IPv4 address, not an IPv6 address.

![DNS A record](images/02-a-record-ipv4.png)

## 4. AAAA record — IPv6 address

An `AAAA` record maps a hostname to an IPv6 address.

```text
jyothipriya.in.  3600  IN  AAAA  2606:4700:90d2:7cbc:c29e:8b4:5ff2:75c4
```

An `AAAA` query asks: *What IPv6 address is associated with this hostname?*

IPv6 addresses are 128 bits. A hostname can have multiple AAAA records and may publish both A and AAAA records. The client and network determine which address family is used; publishing an AAAA record does not guarantee that a client's network has working IPv6 connectivity.

![DNS AAAA record](images/03-aaaa-record-ipv6.png)

## 5. MX record — mail exchange

An `MX` record identifies the mail server hostname(s) responsible for receiving email for a domain.

```text
jyothipriya.in.  3600  IN  MX  10 smtp.secureserver.net.
```

MX RDATA contains a **preference value** and a **mail-exchanger hostname**.

### MX preference

A lower numeric preference is preferred:

```text
jyothipriya.in.  3600  IN  MX  10 smtp.secureserver.net.
jyothipriya.in.  3600  IN  MX  20 backup-mail-1.secureserver.net.
jyothipriya.in.  3600  IN  MX  50 backup-mail-2.secureserver.net.
```

A sending mail server normally tries the lowest-preference-number exchanger first. If it cannot deliver to that server, it may try another eligible MX target. Equal-preference MX records allow the sender to choose among equally preferred exchangers; this does not guarantee perfectly even distribution.

### MX records contain hostnames, not IP addresses

The sending mail server resolves the selected MX hostname to an address, typically using its A and/or AAAA records, before connecting.

MX records do **not** store emails. They tell sending mail systems where to attempt delivery. Mail transfer uses SMTP; DNS supplies the routing information. Server-to-server SMTP commonly uses TCP port 25.

![DNS MX record and mail-routing example](images/04-mx-record-mail-routing.png)

## 6. CNAME record — canonical name / alias

A `CNAME` record makes one hostname an alias of another hostname.

```text
blog.jyothipriya.in.  3600  IN  CNAME  hashnode.network.
```

This says `blog.jyothipriya.in` is an alias for `hashnode.network`. It does **not** directly map the alias to an IP address. The resolver follows the canonical target and obtains its address through A and/or AAAA records.

```text
blog.jyothipriya.in.  CNAME  hashnode.network.
hashnode.network.    A      1.2.3.4
```

The IP above is illustrative.

### Important CNAME constraint

A CNAME owner name generally cannot have other ordinary data records at the same name. For example, an A or MX record cannot normally coexist with a CNAME at the same owner name. This avoids ambiguity about what the alias represents. DNSSEC-related records have specific protocol rules, and some providers offer flattening/alias features that are not literal CNAME records.

A CNAME target must not create an alias loop; DNS resolution cannot follow a loop indefinitely.

![DNS CNAME record](images/05-cname-record-alias.png)

## 7. NS record — name server and delegation

An `NS` record identifies the authoritative name servers for a DNS zone.

```text
jyothipriya.in.  172800  IN  NS  dns1.p07.nsone.net.
jyothipriya.in.  172800  IN  NS  dns2.p07.nsone.net.
jyothipriya.in.  172800  IN  NS  dns3.p07.nsone.net.
jyothipriya.in.  172800  IN  NS  dns4.p07.nsone.net.
```

A zone commonly has multiple authoritative name servers for resilience and availability. NS records identify the servers; they do not contain the zone's A, MX, or TXT data.

### DNS delegation

A parent zone can delegate a child zone to another set of authoritative servers. For example, `jyothipriya.in` can delegate `api.jyothipriya.in`:

```text
; In the parent zone: jyothipriya.in
api.jyothipriya.in.  10000  IN  NS  r53-dns1.p07.aws.net.
api.jyothipriya.in.  10000  IN  NS  r53-dns2.p07.aws.net.
```

The resolver follows the delegation and asks the child zone's authoritative servers for records inside `api.jyothipriya.in`:

```text
api.jyothipriya.in.  3600  IN  A  19.20.21.22
```

**Delegation is not a CNAME.** Delegation directs resolution to another set of authoritative servers for a zone; CNAME aliases one hostname to another.

Some delegations require **glue records** in the parent zone: address records for delegated name servers that are needed to reach those servers without a circular dependency. Whether glue is needed depends on the name-server names and zone relationship.

![DNS NS record and delegation](images/06-ns-record-and-dns-delegation.png)

## 8. TXT record — text data and email authentication

A `TXT` record stores text strings associated with a DNS name.

```text
jyothipriya.in.  3600  IN  TXT  "v=spf1 include:secureserver.net -all"
```

TXT records support many services. Common email-authentication uses include:

- **SPF:** publishes a policy describing which sending hosts are authorized to send mail for a domain.
- **DKIM:** publishes public-key material used to verify DKIM signatures.
- **DMARC:** publishes a domain's policy and reporting preferences for handling mail that fails authentication/alignment checks.

TXT records are also used for domain ownership verification and other configuration. They do not directly route a browser to a web server.

### SPF and `-all`

In the illustrative policy:

```text
v=spf1 include:secureserver.net -all
```

- `v=spf1` identifies the SPF version.
- `include:secureserver.net` incorporates the SPF policy published by that domain.
- `-all` is the **Fail** qualifier for sources not matched by preceding mechanisms.

`-all` does not mean that one single SMTP server is authorized in every circumstance. The authorized set depends on the complete SPF evaluation, including the included domain's policy and other mechanisms.

SPF is evaluated by the receiving mail system using the connecting sender's IP and relevant envelope identity. SPF alone does not authenticate the visible From header or prove that a message is legitimate. DKIM and DMARC address other parts of email authentication.

**Correction to the supplied diagram:** the record type shown beside the SPF value is labelled `CNAME`; it should be `TXT`.

![DNS TXT record and SPF examples](images/07-txt-record-spf-and-email-authentication.png)

## 9. PTR record — reverse DNS

A `PTR` record is used for reverse DNS: it maps an IP address to a hostname.

- Forward lookup: hostname → IP (`A` or `AAAA`).
- Reverse lookup: IP → hostname (`PTR`).

Reverse DNS uses special namespaces:

- IPv4: `in-addr.arpa`
- IPv6: `ip6.arpa`

For IPv4, the address octets are reversed under `in-addr.arpa`. IPv6 reverse names are represented using reversed hexadecimal nibbles under `ip6.arpa`.

PTR records are commonly managed by whoever controls the IP address allocation — often an ISP, hosting provider, or cloud provider — rather than the owner of an unrelated forward DNS domain.

### PTR and email reputation

Receiving mail systems may check reverse DNS as one signal when evaluating a sending mail server. A missing or inconsistent PTR can affect trust or deliverability depending on receiver policy. It does not, by itself, stop a website from resolving or loading.

### Forward-confirmed reverse DNS (FCrDNS)

A common consistency check is:

1. Look up the sender IP's PTR and obtain a hostname.
2. Perform a forward A and/or AAAA lookup for that hostname.
3. Check whether the returned address set includes the original sender IP.

If it does, the relationship is forward-confirmed. This is useful validation, not cryptographic proof of identity. SPF, DKIM, DMARC, TLS, and other controls serve different purposes and may also be evaluated.

![PTR record and forward-confirmed reverse DNS](images/08-ptr-record-reverse-dns-and-fcrdns.png)

## 10. Compare the major record types

| Record | Main purpose | RDATA contains |
|---|---|---|
| `A` | Hostname to IPv4 | IPv4 address |
| `AAAA` | Hostname to IPv6 | IPv6 address |
| `MX` | Mail routing | Preference + mail-server hostname |
| `CNAME` | Hostname alias | Canonical target hostname |
| `NS` | Zone authority / delegation | Authoritative name-server hostname |
| `TXT` | Publish text for services | Text strings |
| `PTR` | Reverse DNS | Hostname |

## 11. Practical commands

Use `nslookup` (available on Windows, macOS, and Linux) or `dig` (commonly available on macOS/Linux and installable on Windows).

### `nslookup`

```bash
nslookup -type=A example.com
nslookup -type=AAAA example.com
nslookup -type=MX example.com
nslookup -type=NS example.com
nslookup -type=TXT example.com
nslookup -type=CNAME www.example.com
nslookup -type=PTR 8.8.8.8
```

### `dig`

```bash
dig example.com A
dig example.com AAAA
dig example.com MX
dig example.com NS
dig example.com TXT
dig www.example.com CNAME
dig -x 8.8.8.8
```

Useful options:

```bash
dig +short example.com A
dig +noall +answer example.com MX
dig +trace example.com A
```

`+trace` is useful for studying root, TLD, and authoritative referrals. Output can vary with DNS changes, resolver behaviour, and caching.

## 12. Common misconceptions

1. **Every DNS record maps a name to an IP.** False; MX, NS, TXT, CNAME, and PTR have different purposes.
2. **MX contains the mail server IP.** False; MX contains a hostname that is resolved separately.
3. **CNAME points directly to an IP.** False; it points to another hostname.
4. **NS records contain all DNS records.** False; they identify authoritative servers for a zone.
5. **A lower MX preference number means lower priority.** False; lower is preferred.
6. **Multiple A/AAAA records guarantee load balancing.** False; behaviour depends on resolvers, clients, and service architecture.
7. **PTR proves a sender is legitimate.** False; it is a DNS mapping, not cryptographic authentication.
8. **TXT is only for SPF.** False; it is also used for DKIM, DMARC, verification, and other services.
9. **TTL is how long a record exists at the authoritative server.** False; TTL controls caching.

## 13. Quick revision

- `A` → hostname to IPv4.
- `AAAA` → hostname to IPv6.
- `MX` → mail exchanger hostname plus preference.
- `CNAME` → alias hostname to canonical hostname.
- `NS` → authoritative name servers for a zone; supports delegation.
- `TXT` → text data interpreted by services and applications.
- `PTR` → IP address to hostname through reverse DNS.
- `TTL` → cache lifetime in seconds.
- `IN` → Internet DNS class.
- Lower MX preference number → more preferred mail exchanger.


## 15. References

- [RFC 1034 — Domain Names: Concepts and Facilities](https://www.rfc-editor.org/rfc/rfc1034)
- [RFC 1035 — Domain Names: Implementation and Specification](https://www.rfc-editor.org/rfc/rfc1035)
- [RFC 2181 — Clarifications to the DNS Specification](https://www.rfc-editor.org/rfc/rfc2181)
- [RFC 2308 — Negative Caching of DNS Queries](https://www.rfc-editor.org/rfc/rfc2308)
- [RFC 3596 — DNS Extensions to Support IP Version 6](https://www.rfc-editor.org/rfc/rfc3596)
- [RFC 5321 — Simple Mail Transfer Protocol](https://www.rfc-editor.org/rfc/rfc5321)
- [RFC 6376 — DomainKeys Identified Mail (DKIM)](https://www.rfc-editor.org/rfc/rfc6376)
- [RFC 7208 — Sender Policy Framework (SPF)](https://www.rfc-editor.org/rfc/rfc7208)
- [RFC 7489 — DMARC](https://www.rfc-editor.org/rfc/rfc7489)

