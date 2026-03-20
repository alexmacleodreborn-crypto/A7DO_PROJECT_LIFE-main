#!/usr/bin/env python3
"""List all repositories for a GitHub account (with pagination)."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, Iterable, List, Optional


GITHUB_API = "https://api.github.com"


def _request_json(url: str, token: Optional[str]) -> List[Dict]:
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req) as response:
            payload = response.read().decode("utf-8")
            return json.loads(payload)
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"GitHub API request failed ({err.code}): {detail}") from err


def _iter_repositories(username: Optional[str], token: Optional[str], include_private: bool) -> Iterable[Dict]:
    page = 1
    per_page = 100

    while True:
        if include_private:
            endpoint = "/user/repos"
            query = {
                "affiliation": "owner",
                "sort": "full_name",
                "per_page": per_page,
                "page": page,
            }
        else:
            if not username:
                raise ValueError("username is required when include_private is False")
            endpoint = f"/users/{username}/repos"
            query = {
                "type": "owner",
                "sort": "full_name",
                "per_page": per_page,
                "page": page,
            }

        url = f"{GITHUB_API}{endpoint}?{urllib.parse.urlencode(query)}"
        batch = _request_json(url, token)

        if not batch:
            break

        for repo in batch:
            yield repo

        if len(batch) < per_page:
            break

        page += 1


def _normalize(repo: Dict) -> Dict[str, str]:
    return {
        "name": repo.get("name", ""),
        "full_name": repo.get("full_name", ""),
        "private": str(repo.get("private", False)).lower(),
        "visibility": repo.get("visibility", ""),
        "default_branch": repo.get("default_branch", ""),
        "html_url": repo.get("html_url", ""),
        "clone_url": repo.get("clone_url", ""),
        "ssh_url": repo.get("ssh_url", ""),
        "description": (repo.get("description") or "").replace("\n", " "),
    }


def _write_csv(repos: List[Dict[str, str]], output_path: Optional[str]) -> None:
    fields = [
        "name",
        "full_name",
        "private",
        "visibility",
        "default_branch",
        "html_url",
        "clone_url",
        "ssh_url",
        "description",
    ]

    fh = open(output_path, "w", newline="", encoding="utf-8") if output_path else sys.stdout
    try:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(repos)
    finally:
        if output_path:
            fh.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a full list of GitHub repositories for a user."
    )
    parser.add_argument(
        "username",
        nargs="?",
        help="GitHub username (required for public-only listing).",
    )
    parser.add_argument(
        "--private",
        action="store_true",
        help="Include private repositories for the authenticated user (requires GITHUB_TOKEN).",
    )
    parser.add_argument(
        "--token",
        default=os.getenv("GITHUB_TOKEN"),
        help="GitHub token. Defaults to GITHUB_TOKEN environment variable.",
    )
    parser.add_argument(
        "--output",
        help="Optional CSV output file. If omitted, CSV is printed to stdout.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.private and not args.token:
        print("Error: --private requires --token or GITHUB_TOKEN.", file=sys.stderr)
        return 2

    if not args.private and not args.username:
        print("Error: username is required when not using --private.", file=sys.stderr)
        return 2

    try:
        repos = [_normalize(r) for r in _iter_repositories(args.username, args.token, args.private)]
    except Exception as err:  # noqa: BLE001
        print(f"Error: {err}", file=sys.stderr)
        return 1

    _write_csv(repos, args.output)

    count_target = "authenticated user" if args.private else args.username
    print(f"\nExported {len(repos)} repositories for {count_target}.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
