
from pathlib import Path
import argparse
import sys

# ============================================================
# COMPUTER NETWORKING REPOSITORY REORGANISATION
# Run from the repository root.
#
# Default: Dry run (no changes)
# Apply:   python reorganize_repo.py --apply
# ============================================================


ROOT = Path(__file__).resolve().parent


# ------------------------------------------------------------
# 1. Rename existing top-level modules
# ------------------------------------------------------------

MODULE_RENAMES = {
    "02-transport-layer": "03-transport-layer",
    "03-dns": "04-dns",
    "04-http-and-web": "05-http-and-web",
    "05-tls-and-security": "06-security",
}


# ------------------------------------------------------------
# 2. Move existing topic folders
# Paths are relative to the repository root.
# ------------------------------------------------------------

MOVES = {

    # NETWORK FUNDAMENTALS
    "01-network-fundamentals/network-architecture":
        "01-network-fundamentals/01-network-architecture",

    "01-network-fundamentals/08-osi_tcp_encapsulation":
        "01-network-fundamentals/02-network-models-and-encapsulation",

    "01-network-fundamentals/35-ethernet-switching":
        "01-network-fundamentals/03-ethernet-switching",


    # IP ADDRESSING AND ROUTING
    "01-network-fundamentals/02-network-host-cidr":
        "02-ip-addressing-and-routing/01-network-host-cidr",

    "01-network-fundamentals/03-ipv4-addressing":
        "02-ip-addressing-and-routing/02-ipv4-addressing",

    "01-network-fundamentals/04-subnet-masks":
        "02-ip-addressing-and-routing/03-subnet-masks",

    "01-network-fundamentals/05-default-gateway":
        "02-ip-addressing-and-routing/04-default-gateway",

    "01-network-fundamentals/06-mac-address":
        "02-ip-addressing-and-routing/05-mac-address",

    "01-network-fundamentals/07-arp":
        "02-ip-addressing-and-routing/06-arp",

    "01-network-fundamentals/09-routing-and-packet-travel":
        "02-ip-addressing-and-routing/07-routing-and-packet-travel",

    "01-network-fundamentals/10-icmp-ping-traceroute":
        "02-ip-addressing-and-routing/08-icmp-ping-traceroute",

    "01-network-fundamentals/30-nat":
        "02-ip-addressing-and-routing/09-nat",

    "01-network-fundamentals/31-ip-packet-anatomy":
        "02-ip-addressing-and-routing/10-ip-packet-anatomy",

    "01-network-fundamentals/32-dhcp":
        "02-ip-addressing-and-routing/11-dhcp",

    "01-network-fundamentals/33-ipv6":
        "02-ip-addressing-and-routing/12-ipv6",


    # PORTS AND SOCKETS
    "01-network-fundamentals/34-ports-and-sockets":
        "03-transport-layer/08-ports-and-sockets",


    # TRANSPORT LAYER
    "03-transport-layer/11-udp-transport":
        "03-transport-layer/01-udp-transport",

    "03-transport-layer/12-tcp-transport":
        "03-transport-layer/02-tcp-transport",

    "03-transport-layer/13-tcp-sequence-ack":
        "03-transport-layer/03-tcp-sequence-ack",

    "03-transport-layer/14-tcp-segment-anatomy":
        "03-transport-layer/04-tcp-segment-anatomy",

    "03-transport-layer/15-mtu-mss-pmtud":
        "03-transport-layer/05-mtu-mss-pmtud",

    "03-transport-layer/16-tcp-control-flow":
        "03-transport-layer/06-tcp-control-flow",

    "03-transport-layer/17-tcp-congestion-control":
        "03-transport-layer/07-tcp-congestion-control",


    # DNS
    "04-dns/18-how-dns-works":
        "04-dns/01-how-dns-works",

    "04-dns/19-major-dns-records":
        "04-dns/02-major-dns-records",


    # HTTP AND WEB
    "05-http-and-web/01-what-happens-http-request":
        "05-http-and-web/01-what-happens-http-request",

    "05-http-and-web/20-http-overview":
        "05-http-and-web/02-http-overview",

    "05-http-and-web/21-http-request-response-structure":
        "05-http-and-web/03-http-request-response-structure",

    "05-http-and-web/22-http1.1-connection-reuse-and-blocking-in-action":
        "05-http-and-web/04-http1.1-connection-reuse-and-blocking",

    "05-http-and-web/23-http2-multiplexing-streams-frames":
        "05-http-and-web/05-http2-multiplexing-streams-frames",

    "05-http-and-web/24-http2-binary-protocol":
        "05-http-and-web/06-http2-binary-protocol",

    "05-http-and-web/25-hpack-header-compression":
        "05-http-and-web/07-hpack-header-compression",

    "05-http-and-web/26-http2-head-line-blocking":
        "05-http-and-web/08-http2-head-of-line-blocking",

    "05-http-and-web/27-quic-protocol-overview":
        "05-http-and-web/09-quic-protocol-overview",

    "05-http-and-web/28-http-3":
        "05-http-and-web/10-http3",


    # TLS
    "06-security/29-tls":
        "06-security/01-tls",

    "06-security/tls-1.2-handshake":
        "06-security/01-tls/02-tls-1.2-handshake",


    # FIREWALLS
    "01-network-fundamentals/firewalls":
        "06-security/02-firewalls",


    # CLOUD NETWORKING
    "01-network-fundamentals/vpc-subnet-route-tables-igw":
        "07-cloud-networking/01-vpc-subnets-route-tables-igw",


    # APPLICATION TRAFFIC
    "01-network-fundamentals/proxies-and-reverse-proxies":
        "08-application-traffic-and-reliability/01-proxies-and-reverse-proxies",
}


# ------------------------------------------------------------
# 3. Required module directories
# ------------------------------------------------------------

MODULES = [
    "01-network-fundamentals",
    "02-ip-addressing-and-routing",
    "03-transport-layer",
    "04-dns",
    "05-http-and-web",
    "06-security",
    "07-cloud-networking",
    "08-application-traffic-and-reliability",
]


# ------------------------------------------------------------
# 4. New topic folders and starter README content
# ------------------------------------------------------------

NEW_TOPICS = {

    "07-cloud-networking/02-security-groups": """# Security Groups

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
""",

    "08-application-traffic-and-reliability/02-load-balancers": """# Load Balancers

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
""",

    "08-application-traffic-and-reliability/03-connection-pooling": """# Connection Pooling

## Learning Objective

Understand why applications reuse database connections instead of
creating a new connection for every request.

## 1. What Is Connection Pooling?

Connection pooling maintains a reusable collection of established
connections that an application can borrow and return.

## 2. Key Concepts

- Database connections
- Connection creation overhead
- Pool size
- Connection checkout and return
- Idle connections
- Pool exhaustion
- Connection lifetime

## 3. Typical Request Flow

1. Application requests a connection from the pool.
2. Pool provides an available connection.
3. Application executes a query.
4. Application returns the connection to the pool.

## 4. Why It Matters

Explain performance, resource usage and database connection limits.

## References

- [SQLAlchemy Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html)
""",

    "08-application-traffic-and-reliability/04-timeouts-and-retries": """# Timeouts and Retries

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
"""
}


# ------------------------------------------------------------
# 5. Utility functions
# ------------------------------------------------------------

def log(message):
    print(message)


def move_folder(source, destination, dry_run):
    """Move a folder without overwriting an existing destination."""

    src = ROOT / source
    dst = ROOT / destination

    if not src.exists():
        return

    if dst.exists():
        log(f"  [CONFLICT] Destination already exists: {destination}")
        log("             Source was left untouched.")
        return

    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        src.rename(dst)

    log(f"  [MOVE] {source} -> {destination}")


def rename_module(source, destination, dry_run):
    """Rename a top-level module."""

    src = ROOT / source
    dst = ROOT / destination

    if not src.exists():
        return

    if dst.exists():
        log(f"  [CONFLICT] Module already exists: {destination}")
        return

    if not dry_run:
        src.rename(dst)

    log(f"  [RENAME] {source} -> {destination}")


def create_directory(relative_path, dry_run):
    """Create a directory if it does not exist."""

    path = ROOT / relative_path

    if path.exists():
        return

    if not dry_run:
        path.mkdir(parents=True, exist_ok=True)

    log(f"  [CREATE DIR] {relative_path}")


def create_readme(relative_path, content, dry_run):
    """Create a README only when one does not already exist."""

    path = ROOT / relative_path

    if path.exists():
        log(f"  [EXISTS] {relative_path}")
        return

    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.strip() + "\n", encoding="utf-8")

    log(f"  [CREATE README] {relative_path}")


# ------------------------------------------------------------
# 6. Main migration process
# ------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Reorganise the Computer Networking repository."
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply the migration. Without this flag, only preview changes."
    )

    args = parser.parse_args()
    dry_run = not args.apply

    if not (ROOT / ".git").exists():
        print("ERROR: This script must be saved in the root of your Git repository.")
        sys.exit(1)

    print("\n==========================================")
    print(" COMPUTER NETWORKING REPOSITORY MIGRATION")
    print("==========================================")

    print(f"\nRepository: {ROOT}")

    if dry_run:
        print("\nMODE: DRY RUN - No files will be changed.\n")
    else:
        print("\nMODE: APPLY - Changes will now be made.\n")

    # Step 1: Rename top-level modules
    print("\n[1/5] Renaming existing modules...")

    for source, destination in MODULE_RENAMES.items():
        rename_module(source, destination, dry_run)

    # Step 2: Move existing topic folders
    print("\n[2/5] Moving existing topic folders...")

    for source, destination in MOVES.items():
        move_folder(source, destination, dry_run)

    # Step 3: Create all module directories
    print("\n[3/5] Creating module directories...")

    for module in MODULES:
        create_directory(module, dry_run)

    # Step 4: Create the four new topic folders
    print("\n[4/5] Creating new topic folders and READMEs...")

    for folder, content in NEW_TOPICS.items():
        create_directory(folder, dry_run)
        create_readme(f"{folder}/README.md", content, dry_run)

    # Step 5: Create missing module README files
    print("\n[5/5] Checking module README files...")

    module_descriptions = {
        "02-ip-addressing-and-routing":
            "IP addressing, subnetting, gateways, routing and packet travel.",

        "07-cloud-networking":
            "Cloud networking concepts including VPCs, subnets, gateways and security controls.",

        "08-application-traffic-and-reliability":
            "Application traffic management, load balancing, connection pooling and timeouts."
    }

    for module, description in module_descriptions.items():
        content = f"""# {module.replace('-', ' ').title()}

> {description}

## Topics

Topic READMEs will be listed here as the module is developed.
"""
        create_readme(f"{module}/README.md", content, dry_run)

    print("\n==========================================")

    if dry_run:
        print("DRY RUN COMPLETE")
        print("No changes were made.")
        print("\nReview the proposed operations.")
        print("If everything looks correct, run:")
        print("\n    python reorganize_repo.py --apply")
    else:
        print("MIGRATION COMPLETE")
        print("\nReview the changes using:")
        print("\n    git status")
        print("\nCheck the README links and image paths before committing.")

    print("==========================================\n")


if __name__ == "__main__":
    main()
