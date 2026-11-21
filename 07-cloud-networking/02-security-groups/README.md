# Security Groups

## Learning Objective

Understand how cloud Security Groups control inbound and outbound
network traffic to cloud resources.

## 1. What Is a Security Group?

A Security Group is a virtual, stateful network security control
associated with cloud resources.

## 2. Key Concepts

- Inbound rules
- Outbound rules
- Allowed protocols and ports
- Source and destination
- Stateful traffic filtering
- Security Group references

## 3. Security Groups vs Network ACLs

| Feature | Security Group | Network ACL |
|---|---|---|
| Stateful | Yes | No |
| Rule actions | Allow | Allow and deny |
| Applied to | Resource network interfaces | Subnets |
| Return traffic | Automatically allowed for tracked connections | Must be explicitly allowed |

## 4. Practical Example

Document how a web server can accept HTTPS traffic while a database
only accepts connections from the application server.

## References

- [AWS Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)
- [AWS Network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html)
