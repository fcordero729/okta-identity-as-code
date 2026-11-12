"""Compare Okta's SCIM app assignments with the accounts in the app.

Reads OKTA_ORG_NAME, OKTA_BASE_URL, OKTA_API_TOKEN, SCIM_BASE_URL and SCIM_TOKEN
from the environment and writes scim_reconcile.csv. Read-only on both sides.
"""
import csv
import os

import requests

APP_LABEL = "SCIM Playground"
OKTA = f"https://{os.environ['OKTA_ORG_NAME']}.{os.environ['OKTA_BASE_URL']}"
OKTA_HEADERS = {"Authorization": f"SSWS {os.environ['OKTA_API_TOKEN']}", "Accept": "application/json"}
SCIM = os.environ["SCIM_BASE_URL"].rstrip("/")
SCIM_HEADERS = {"Authorization": f"Bearer {os.environ['SCIM_TOKEN']}", "Accept": "application/scim+json"}


def okta_pages(url):
    """Yield every item, following Okta's Link-header pagination."""
    while url:
        resp = requests.get(url, headers=OKTA_HEADERS, timeout=30)
        resp.raise_for_status()
        yield from resp.json()
        url = resp.links.get("next", {}).get("url")


def okta_app_users():
    apps = list(okta_pages(f"{OKTA}/api/v1/apps?q={APP_LABEL}"))
    app_id = next(a["id"] for a in apps if a["label"] == APP_LABEL)
    return {
        u["credentials"]["userName"].lower(): u["status"]
        for u in okta_pages(f"{OKTA}/api/v1/apps/{app_id}/users?limit=200")
    }


def scim_users():
    """Return every SCIM user, following startIndex/count pagination."""
    start, users = 1, {}
    while True:
        resp = requests.get(f"{SCIM}/Users", headers=SCIM_HEADERS,
                            params={"startIndex": start, "count": 100}, timeout=30)
        resp.raise_for_status()
        body = resp.json()
        for u in body.get("Resources", []):
            users[u["userName"].lower()] = u.get("active", True)
        start += body.get("itemsPerPage", 0) or 100
        if start > body.get("totalResults", 0):
            return users


def main():
    okta, app = okta_app_users(), scim_users()
    rows = []
    for name in sorted(set(okta) | set(app)):
        if name not in okta:
            finding = "ORPHAN: in app, not assigned in Okta"
        elif name not in app:
            finding = "MISSING: assigned in Okta, no app account"
        else:
            finding = "ok"
        rows.append({"userName": name, "okta_status": okta.get(name, ""),
                     "app_active": app.get(name, ""), "finding": finding})
    with open("scim_reconcile.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["userName", "okta_status", "app_active", "finding"])
        writer.writeheader()
        writer.writerows(rows)
    issues = sum(r["finding"] != "ok" for r in rows)
    print(f"{len(rows)} accounts compared, {issues} findings -> scim_reconcile.csv")


if __name__ == "__main__":
    main()
