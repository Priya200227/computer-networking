# Load Balancers

## Learning Objective

Understand how load balancers distribute incoming application
traffic across multiple backend servers.

## 1. What Is a Load Balancer?

A load balancer distributes requests across multiple backend targets
to improve availability, scalability and resource utilisation.

## 2. Key Concepts

- Frontend listener
- Backend targets
- Health checks
- Traffic distribution
- Layer 4 vs Layer 7 load balancing
- Application Load Balancer vs Network Load Balancer

## 3. How It Works

1. A client sends a request.
2. The load balancer receives it.
3. It selects a healthy backend target.
4. The backend processes the request.
5. The response returns to the client.

## 4. Load Balancer vs Reverse Proxy

Explain how these concepts overlap and where their responsibilities
differ.

## References

- [AWS Elastic Load Balancing](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html)
