# Timeouts and Retries

## Learning Objective

Understand how timeouts and controlled retries prevent application
requests from waiting indefinitely.

## 1. What Is a Timeout?

A timeout defines how long an application waits for an operation
before treating it as unsuccessful.

## 2. Common Timeout Types

- Connection timeout
- Read timeout
- Write timeout
- Request timeout
- Database query timeout
- Connection pool acquisition timeout

## 3. Retries

Explain when applications retry failed requests and why retries
must be controlled.

## 4. Important Concepts

- Exponential backoff
- Retry limits
- Jitter
- Idempotency
- Retry storms
- Timeout budgets

## 5. Practical Example

Trace what happens when an application calls a slow external API.

## References

- [AWS Builders' Library: Timeouts, retries and backoff](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
