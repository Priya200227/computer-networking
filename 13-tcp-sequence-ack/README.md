# TCP Sequence Numbers and Acknowledgment Numbers

> **Learning objective:** Understand how TCP sequence numbers identify byte positions in a connection, how acknowledgment numbers report the next byte expected, and how these mechanisms support ordered delivery, duplicate detection, and retransmission.

[← Back to Computer Networking](https://github.com/Priya200227/computer-networking)

---

## 1. Overview

TCP provides a reliable, ordered byte stream. To keep that stream in order and detect missing or duplicate data, TCP assigns sequence numbers to bytes and uses acknowledgment numbers to report which bytes have been received.

- **Sequence Number (SEQ):** identifies the sequence-space position of the first data byte in a segment. When SYN is set, the field carries the Initial Sequence Number (ISN).
- **Acknowledgment Number (ACK):** when the ACK flag is set, identifies the next sequence number the sender of the ACK expects to receive. It cumulatively acknowledges all sequence-space positions before that value.

Both fields are 32 bits wide in the TCP header.

The authoritative definition is in [RFC 9293, Section 3.4 — Sequence Numbers](https://www.rfc-editor.org/rfc/rfc9293#section-3.4).

## 2. TCP sequence numbers

### 2.1 Every byte is numbered

TCP numbers the bytes (octets) in the byte stream, not merely the segments or packets.

A segment carrying data has a sequence number corresponding to its first data byte. The following bytes are numbered consecutively.

For illustration, suppose an application sends the ten-byte string `HELLOWORLD`, and the first data byte is assigned sequence number `1`:

| Byte | H | E | L | L | O | W | O | R | L | D |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Sequence number | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |

If TCP sends the first five bytes in one segment, that segment's sequence number is `1`. If it sends the remaining five bytes in another segment, that segment's sequence number is `6`.

The receiver uses these byte positions to place received data in the correct order, even if segments arrive out of order.

![TCP sequence numbers](images/01-tcp-sequence-numbers.png)

**Important:** This is an illustrative split. TCP does not promise that an application write becomes one segment or that segments have a fixed size. Actual segmentation depends on factors such as MSS, path MTU, TCP options, and implementation behavior.

### 2.2 The 32-bit sequence-number space

The TCP Sequence Number field is 32 bits wide. It represents:

\[
2^{32} = 4,294,967,296
\]

possible values, from `0` through:

\[
2^{32}-1 = 4,294,967,295
\]

`4,294,967,295` is the largest representable sequence-number value, not the total number of bytes a connection can transfer. Sequence numbers wrap around modulo \(2^{32}\) as data is transferred. They do not increase forever without returning to zero.

### 2.3 Initial Sequence Number (ISN) and SYN

Each endpoint independently chooses an Initial Sequence Number (ISN) for its direction of data flow during connection establishment.

In a normal three-way handshake:

1. Client sends `SYN` with sequence number `x`.
2. Server replies with `SYN + ACK`, using its own sequence number `y` and acknowledgment number `x + 1`.
3. Client sends `ACK` with acknowledgment number `y + 1`.

A SYN consumes one position in sequence space, even though it normally carries no application data. Therefore, if a client sends a SYN with sequence number `x`, its first data byte normally begins at `x + 1`.

The supplied diagram uses an initial sequence number of zero for illustration. Real TCP initial sequence numbers are selected by the TCP implementation and are not generally predictable or guaranteed to start at zero.

## 3. TCP acknowledgment numbers

An acknowledgment number communicates the **next sequence number expected** by the sender of that acknowledgment.

For example, if a receiver has successfully received bytes with sequence numbers `1` through `5`, the next byte it expects is byte `6`. It can therefore send:

```text
ACK = 6
```

This means all bytes before sequence number `6` have been received in order, and the receiver is currently expecting byte `6`.

TCP acknowledgments are generally **cumulative**. An ACK value of `6` acknowledges sequence-space positions before `6`; it does not mean “I received only segment number 6.”

![TCP acknowledgment numbers](images/02-tcp-acknowledgment-numbers.png)

### 3.1 Missing data and out-of-order arrival

Assume the sender transmits three consecutive data ranges:

| Segment | Sequence number | Data bytes |
|---|---:|---|
| 1 | 1 | `TCP` (bytes 1–3) |
| 2 | 4 | `HELLO` (bytes 4–8) |
| 3 | 9 | `WORLD` (bytes 9–13) |

Suppose segment 1 arrives, segment 2 is lost, and segment 3 arrives.

The receiver has bytes 1–3 and bytes 9–13, but it is still missing bytes 4–8. Its next expected sequence number remains `4`.

When later out-of-order data arrives, the receiver may send duplicate ACKs with acknowledgment number `4`. These tell the sender that the receiver is still waiting for the missing data beginning at byte 4.

The receiver may buffer out-of-order data, but TCP presents the application with the byte stream in order.

### 3.2 Duplicate ACKs

A **duplicate ACK** repeats an acknowledgment number already sent. It can indicate that the receiver is still missing data at that sequence position while later data is arriving.

Duplicate ACKs are useful signals for loss recovery. TCP congestion-control algorithms can use a series of duplicate ACKs to trigger **fast retransmit**, allowing a sender to retransmit a likely missing segment without waiting only for the retransmission timeout.

However:
- A duplicate ACK is not absolute proof that a segment was lost.
- Network reordering can also produce duplicate ACKs.
- Exact recovery behavior depends on the TCP implementation and algorithms in use.

See [RFC 5681, Section 3.2 — Fast Retransmit/Fast Recovery](https://www.rfc-editor.org/rfc/rfc5681#section-3.2).

## 4. How sequence and acknowledgment numbers work together

Sequence numbers identify the positions of transmitted bytes. Acknowledgment numbers report the next byte position expected by the receiver.

Together they help TCP:
- detect missing data,
- recognize duplicate data,
- reassemble data in the correct order,
- determine which transmitted data has been acknowledged,
- support retransmission and loss recovery.

![Sequence and acknowledgment numbers together](images/03-sequence-and-acknowledgment-together.png)

### Worked example

Suppose the client sends 10 bytes beginning at sequence number `1000`:

- First segment: bytes `1000`–`1004`.
- Second segment: bytes `1005`–`1009`.

If the receiver has received all ten bytes in order, it acknowledges:

\[
ACK = 1010
\]

Why `1010`? Because it is the next byte sequence number the receiver expects. The ACK cumulatively confirms receipt of all bytes before `1010`.

If the second segment arrives before the first, the receiver cannot advance its cumulative ACK beyond the missing byte range. It continues to acknowledge the first missing sequence number until the gap is filled, subject to TCP's receive and acknowledgment behavior.

## 5. SYN and FIN also consume sequence space

Sequence numbers do not count only application data bytes.

- **SYN** consumes one sequence-number position.
- **FIN** consumes one sequence-number position.
- **ACK** itself consumes no sequence-number space.

For example, if a SYN has sequence number `500`, the acknowledgment of that SYN is `501`. If a FIN is sent with sequence number `900` and no data in that segment, the peer acknowledges it with `901`.

This is why the first data byte after a SYN normally starts at `ISN + 1`, and why a FIN is also acknowledged by advancing the ACK number by one.

## 6. Common misconceptions and corrections

| Misconception | Correct explanation |
|---|---|
| TCP assigns one sequence number to each packet. | TCP numbers every data byte. A segment's sequence number identifies its first data byte (or its SYN when SYN is set). |
| The ACK number means the last byte received. | It means the **next byte expected**; it cumulatively acknowledges all earlier sequence-space positions. |
| Sequence numbers start at zero in every real connection. | The supplied diagram uses zero for illustration. Real endpoints choose ISNs; they are not generally zero. |
| The maximum sequence number means a connection can transfer only about 4 GB. | The 32-bit sequence space wraps modulo \(2^{32}\); it does not impose a 4 GB total-transfer limit. |
| Every duplicate ACK proves packet loss. | Duplicate ACKs can indicate a gap, but reordering can also cause them. |
| TCP always sends one ACK for every segment. | ACK behavior can be cumulative, delayed, or aggregated according to TCP behavior and implementation. |
| Segments always arrive in order. | IP networks can reorder or lose packets. TCP uses sequence numbers and recovery mechanisms to provide an ordered byte stream to the application. |

## 7. Quick revision

- TCP sequence numbers identify byte positions in a connection's byte stream.
- The Sequence Number field is 32 bits.
- The sequence-number space ranges from `0` to `4,294,967,295` and wraps modulo \(2^{32}\).
- The sequence number in a data segment identifies its first data byte.
- Each endpoint chooses an Initial Sequence Number during the handshake.
- SYN and FIN each consume one sequence-number position; ACK does not.
- The acknowledgment number is the next sequence number expected.
- TCP acknowledgments are cumulative.
- Duplicate ACKs can help TCP infer loss and perform fast retransmit.
- Sequence and acknowledgment numbers work together to support reliable, ordered delivery.

## 8. Self-check questions

1. Does TCP assign sequence numbers to segments or to bytes?
2. If a segment starts at sequence number `200` and carries 100 bytes, what sequence number does the next data byte use?
3. If a receiver has received bytes through sequence number `499`, what ACK number should it send next?
4. Why does a SYN with sequence number `x` lead to an acknowledgment of `x + 1`?
5. What does a duplicate ACK tell the sender?
6. Does a duplicate ACK always prove that a segment was lost?
7. Why does the TCP sequence-number space wrap around?
8. Do SYN, FIN, and ACK all consume sequence-number space?
9. Why can a receiver get later segments while still acknowledging an earlier sequence number?
10. How do sequence and acknowledgment numbers contribute to TCP reliability?

## 9. References

### Primary standards

- [RFC 9293 — Transmission Control Protocol (TCP)](https://www.rfc-editor.org/rfc/rfc9293) — TCP header fields, sequence numbers, cumulative acknowledgments, and connection behavior.
- [RFC 9293, Section 3.4 — Sequence Numbers](https://www.rfc-editor.org/rfc/rfc9293#section-3.4) — byte numbering, sequence-number space, SYN/FIN sequence-space behavior, and acknowledgment semantics.
- [RFC 5681, Section 3.2 — Fast Retransmit/Fast Recovery](https://www.rfc-editor.org/rfc/rfc5681#section-3.2) — duplicate ACKs and fast retransmit.
- [Wireshark User's Guide](https://www.wireshark.org/docs/wsug_html_chunked/) — inspecting TCP sequence and acknowledgment numbers in packet captures.

### Video reference

- [TCP Sequence Number and Acknowledgment Number](https://youtu.be/YryEKDfMXQw)

### Image notes

The three diagrams in `images/` are the supplied learning visuals. They are retained and embedded here. The explanations clarify the simplified examples and distinguish sequence-number values from byte counts and segment counts.

