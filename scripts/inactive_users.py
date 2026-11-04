"""List Okta users who have not signed in recently.

Reads OKTA_ORG_NAME, OKTA_BASE_URL and OKTA_API_TOKEN from the environment
(the same variables Terraform uses) and writes inactive_users.csv.
"""
import csv
import os
import sys
from datetime import datetime, timedelta, timezone

import requests

DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 30
BASE = f"https://{os.environ['OKTA_ORG_NAME']}.{os.environ['OKTA_BASE_URL']}"
HEADERS = {
    "Authorization": f"SSWS {os.environ['OKTA_API_TOKEN']}",
    "Accept": "application/json",
}


def all_users():
    """Yield every user, following Okta's Link-header pagination."""
    url = f"{BASE}/api/v1/users?limit=200"
    while url:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        yield from resp.json()
        url = resp.links.get("next", {}).get("url")


def main():
    cutoff = datetime.now(timezone.utc) - timedelta(days=DAYS)
    rows = []
    for user in all_users():
        last = user.get("lastLogin")
        last_dt = datetime.fromisoformat(last.replace("Z", "+00:00")) if last else None
        if last_dt is None or last_dt < cutoff:
            rows.append({
                "login": user["profile"]["login"],
                "status": user["status"],
                "department": user["profile"].get("department", ""),
                "last_login": last or "never",
            })
    with open("inactive_users.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["login", "status", "department", "last_login"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} users inactive for {DAYS}+ days -> inactive_users.csv")


if __name__ == "__main__":
    main()