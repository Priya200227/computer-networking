#!/usr/bin/env python3
"""
Restructure the computer-networking Git repository into topic-based modules.

Usage:
  python restructure_repo.py             # dry run; makes no changes
  python restructure_repo.py --apply     # move folders and rewrite local Markdown links

Run this from the repository root. Commit/stash existing work first.
The script uses `git mv`, preserves each topic folder (including its images),
and updates relative Markdown links after moving folders.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

ROOT = Path.cwd()

MODULES = {
    "01-network-fundamentals": [
        "02-network-host-cidr",
        "03-ipv4-addressing",
        "04-subnet-masks",
        "05-default-gateway",
        "06-mac-address",
        "07-arp",
        "08-osi_tcp_encapsulation",
        "09-routing-and-packet-travel",
        "10-icmp-ping-traceroute",
        "30-nat",
        "31-ip-packet-anatomy",
    ],
    "02-transport-layer": [
        "11-udp-transport",
        "12-tcp-transport",
        "13-tcp-sequence-ack",
        "14-tcp-segment-anatomy",
        "15-mtu-mss-pmtud",
        "16-tcp-control-flow",
        "17-tcp-congestion-control",
    ],
    "03-dns": [
        "18-how-dns-works",
        "19-major-dns-records",
    ],
    "04-http-and-web": [
        "01-what-happens-http-request",
        "20-http-overview",
        "21-http-request-response-structure",
        "22-http1.1-connection-reuse-and-blocking-in-",
        "23-http-2-multiplexing-streams-frames",
        "24-http-2-binary-protocol",
        "25-hpack-header-compression",
        "26-http-2-head-line-blocking",
        "27-quic-protocol-overview",
        "28-http-3",
    ],
    "05-tls-and-security": [
        "29-tls",
    ],
    "06-packet-analysis": [],
}

# A standalone fundamentals folder is retained as a subtopic; its contents
# are not merged or deleted automatically.
EXTRA_MOVES = {
    "http-fundamentals": "04-http-and-web/http-fundamentals",
}

MODULE_DESCRIPTIONS = {
    "01-network-fundamentals": "IPv4 addressing, subnetting, local communication, routing, NAT and IP packet structure.",
    "02-transport-layer": "UDP, TCP, ports, reliability, flow control, congestion control and MTU.",
    "03-dns": "DNS resolution, hierarchy, caching and resource records.",
    "04-http-and-web": "HTTP request/response behaviour, HTTP versions, multiplexing, compression and QUIC.",
    "05-tls-and-security": "TLS, certificates and secure connection establishment.",
    "06-packet-analysis": "Practical packet inspection and protocol analysis with Wireshark.",
}

LINK_RE = re.compile(r'(!?\[[^\]]*\]\()([^)]+)(\))')


def run_git(args: list[str], dry_run: bool) -> None:
    cmd = ["git", *args]
    print("$", " ".join(cmd))
    if not dry_run:
        subprocess.run(cmd, cwd=ROOT, check=True)


def discover_source(prefix: str) -> str | None:
    exact = ROOT / prefix
    if exact.is_dir():
        return prefix
    matches = sorted(
        p.name for p in ROOT.iterdir()
        if p.is_dir() and p.name.startswith(prefix)
    )
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise RuntimeError(
            f"More than one folder matches {prefix!r}: {matches}. "
            "Edit the mapping at the top of this script to choose the correct folder."
        )
    return None


def build_mapping() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for module, entries in MODULES.items():
        for entry in entries:
            actual = discover_source(entry)
            if actual:
                mapping[actual] = f"{module}/{actual}"
            elif entry.startswith("22-"):
                print(
                    "WARNING: Could not find the HTTP/1.1 folder beginning "
                    f"with {entry!r}; add its exact name to MODULES."
                )
            else:
                print(f"WARNING: Folder not found; skipping: {entry}")
    for source, destination in EXTRA_MOVES.items():
        if (ROOT / source).is_dir():
            mapping[source] = destination
        else:
            print(f"INFO: Optional folder not present; skipping: {source}")
    return mapping


def check_git_state(dry_run: bool) -> None:
    if not (ROOT / ".git").exists():
        raise RuntimeError("Run this script from the root of your Git repository.")
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=ROOT, capture_output=True, text=True, check=True
    )
    if result.stdout.strip():
        print(result.stdout)
        raise RuntimeError(
            "Your working tree has uncommitted changes. Commit or stash them "
            "before restructuring so the moves and link edits are easy to review."
        )


def destination_path(old_target: Path, mapping: dict[str, str]) -> Path:
    """Translate a repository-relative target using the folder move map."""
    try:
        rel = old_target.relative_to(ROOT)
    except ValueError:
        return old_target
    parts = rel.parts
    if not parts:
        return old_target
    moved = mapping.get(parts[0])
    if not moved:
        return old_target
    return ROOT.joinpath(moved, *parts[1:])


def old_location_for_moved_file(new_file: Path, mapping: dict[str, str]) -> Path:
    """Recover a moved Markdown file's original path for resolving old links."""
    rel = new_file.relative_to(ROOT)
    for old_top, new_top in mapping.items():
        new_parts = PurePosixPath(new_top).parts
        rel_parts = rel.parts
        if rel_parts[:len(new_parts)] == new_parts:
            suffix = rel_parts[len(new_parts):]
            return ROOT / old_top / Path(*suffix)
    return new_file


def rewrite_link_target(target: str, old_md: Path, new_md: Path,
                         mapping: dict[str, str]) -> str:
    target = target.strip()
    # Leave external URLs, mail links, anchors and protocol-relative URLs alone.
    if (not target or target.startswith(("#", "https://", "http://", "mailto:",
                                         "tel:", "//", "data:"))):
        return target

    # Preserve optional Markdown title text: path "title".
    match = re.match(r'^(\S+)(\s+.+)?$', target)
    if not match:
        return target
    raw_path, title = match.group(1), match.group(2) or ""

    # Do not rewrite absolute site paths.
    if raw_path.startswith("/"):
        return target

    path_part, sep, fragment = raw_path.partition("#")
    path_part, qsep, query = path_part.partition("?")
    decoded = unquote(path_part)
    if not decoded:
        return target

    old_target = (old_md.parent / Path(decoded)).resolve()
    translated = destination_path(old_target, mapping)

    # If the target is unaffected, keep the authored link unchanged.
    if translated == old_target:
        return target

    relative = os.path.relpath(translated, new_md.parent)
    relative = relative.replace(os.sep, "/")
    if not relative.startswith("."):
        relative = "./" + relative

    suffix = (("?" + query) if qsep else "") + (("#" + fragment) if sep else "")
    return relative + suffix + title


def rewrite_markdown_links(mapping: dict[str, str], dry_run: bool) -> None:
    changed_count = 0
    for md in ROOT.rglob("*.md"):
        if ".git" in md.parts:
            continue
        new_md = md
        old_md = old_location_for_moved_file(new_md, mapping)
        original = md.read_text(encoding="utf-8")

        def replace(match: re.Match[str]) -> str:
            prefix, target, suffix = match.groups()
            updated = rewrite_link_target(target, old_md, new_md, mapping)
            return prefix + updated + suffix

        updated_text = LINK_RE.sub(replace, original)
        if updated_text != original:
            changed_count += 1
            print(f"UPDATE links: {md.relative_to(ROOT)}")
            if not dry_run:
                md.write_text(updated_text, encoding="utf-8")
    print(f"Markdown files needing link updates: {changed_count}")


def create_module_readmes(dry_run: bool) -> None:
    for module, description in MODULE_DESCRIPTIONS.items():
        module_dir = ROOT / module
        topic_dirs = sorted(
            p for p in module_dir.iterdir()
            if p.is_dir() and (p / "README.md").exists()
        ) if module_dir.exists() else []
        lines = [
            f"# {module[3:].replace('-', ' ').title()}",
            "",
            f"> {description}",
            "",
            "[⬅️ Back to Computer Networking](../README.md)",
            "",
            "## Topics",
            "",
        ]
        if topic_dirs:
            for topic in topic_dirs:
                title = topic.name.split("-", 1)[-1].replace("-", " ").replace("_", " ").title()
                lines.append(f"- [{title}](./{topic.name}/README.md)")
        else:
            lines.append("_Practical exercises and notes will be added here._")
        lines.extend(["", ""])
        path = module_dir / "README.md"
        content = "\n".join(lines)
        if path.exists():
            print(f"KEEP existing module README: {path.relative_to(ROOT)}")
        else:
            print(f"CREATE module README: {path.relative_to(ROOT)}")
            if not dry_run:
                module_dir.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply", action="store_true",
        help="perform moves and link updates; without this flag, only preview"
    )
    args = parser.parse_args()
    dry_run = not args.apply

    try:
        check_git_state(dry_run)
        mapping = build_mapping()
        if not mapping:
            raise RuntimeError("No source folders were found. Check the repository root.")

        print("\nPlanned folder moves:")
        for old, new in mapping.items():
            print(f"  {old}/  ->  {new}/")

        # Detect destination collisions before making any changes.
        for old, new in mapping.items():
            destination = ROOT / new
            if destination.exists():
                raise RuntimeError(
                    f"Destination already exists: {new}. "
                    f"Resolve this manually before moving {old}."
                )

        if dry_run:
            print("\nDRY RUN ONLY — no files have been changed.")
            print("Review the mapping, then run: python restructure_repo.py --apply")
            return 0

        for module in MODULES:
            (ROOT / module).mkdir(parents=True, exist_ok=True)

        # git mv each complete topic directory, including images/assets.
        for old, new in mapping.items():
            run_git(["mv", old, new], dry_run=False)

        rewrite_markdown_links(mapping, dry_run=False)
        create_module_readmes(dry_run=False)

        print("\nRestructuring complete.")
        print("Next: inspect `git status`, search for broken links, preview every README,")
        print("then commit the changes. The root README is intentionally not overwritten.")
        return 0

    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
