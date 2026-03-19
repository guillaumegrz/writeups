#!/usr/bin/env python3
"""
Auto README updater for guillaumegrz/writeups
Fetches data from HTB API, RootMe, and GitHub API
"""

import os
import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# ─── CONFIG ───────────────────────────────────────────────────────────────────
HTB_USER_ID     = os.environ.get("HTB_USER_ID", "3081565")
ROOTME_USERNAME = os.environ.get("ROOTME_USERNAME", "gr4z__")
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "guillaumegrz")
GITHUB_REPO     = os.environ.get("GITHUB_REPO", "writeups")
GITHUB_TOKEN    = os.environ.get("GITHUB_TOKEN", "")

HEADERS_GITHUB = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

HEADERS_HTB = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

# ─── HTB ──────────────────────────────────────────────────────────────────────
def get_htb_data():
    """Fetch HTB profile data via public API"""
    try:
        url = f"https://www.hackthebox.com/api/v4/user/profile/basic/{HTB_USER_ID}"
        r = requests.get(url, headers=HEADERS_HTB, timeout=10)
        if r.status_code == 200:
            data = r.json().get("profile", {})
            return {
                "name":           data.get("name", "N/A"),
                "rank":           data.get("rank", "N/A"),
                "points":         data.get("points", 0),
                "user_owns":      data.get("user_owns", 0),
                "system_owns":    data.get("system_owns", 0),
                "rank_text":      data.get("rankText", "N/A"),
            }
    except Exception as e:
        print(f"[HTB] Error: {e}")
    return None

def get_htb_activity():
    """Fetch recent HTB machine activity"""
    try:
        url = f"https://www.hackthebox.com/api/v4/user/profile/activity/{HTB_USER_ID}"
        r = requests.get(url, headers=HEADERS_HTB, timeout=10)
        if r.status_code == 200:
            activity = r.json().get("profile", {}).get("activity", [])
            # Get last machine solved
            for item in activity:
                if item.get("object_type") == "machine":
                    return {
                        "last_machine": item.get("name", "N/A"),
                        "last_machine_date": item.get("created_at", "")[:10]
                    }
    except Exception as e:
        print(f"[HTB Activity] Error: {e}")
    return {"last_machine": "N/A", "last_machine_date": "N/A"}

# ─── ROOTME ───────────────────────────────────────────────────────────────────
def get_rootme_data():
    """Scrape RootMe profile page"""
    try:
        url = f"https://www.root-me.org/{ROOTME_USERNAME}?lang=en"
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return None

        soup = BeautifulSoup(r.text, "html.parser")

        # Score global
        score = "N/A"
        score_tag = soup.find("span", class_="score")
        if score_tag:
            score = score_tag.text.strip()

        # Challenges par catégorie
        categories = {}
        for row in soup.select("table.stat tr"):
            cols = row.find_all("td")
            if len(cols) >= 2:
                cat_name = cols[0].text.strip()
                cat_score = cols[1].text.strip()
                if cat_name and cat_score:
                    categories[cat_name] = cat_score

        # Dernier challenge résolu
        last_challenge = "N/A"
        last_challenge_date = "N/A"
        activity_rows = soup.select("table.activite tr")
        for row in activity_rows[1:2]:  # First row after header
            cols = row.find_all("td")
            if len(cols) >= 2:
                last_challenge = cols[0].text.strip()
                last_challenge_date = cols[1].text.strip() if len(cols) > 1 else "N/A"

        return {
            "score": score,
            "categories": categories,
            "last_challenge": last_challenge,
            "last_challenge_date": last_challenge_date
        }

    except Exception as e:
        print(f"[RootMe] Error: {e}")
    return None

# ─── GITHUB ───────────────────────────────────────────────────────────────────
def get_latest_writeup():
    """Find the latest writeup pushed to the repo"""
    try:
        url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/commits"
        r = requests.get(url, headers=HEADERS_GITHUB, timeout=10)
        if r.status_code == 200:
            commits = r.json()
            for commit in commits:
                sha = commit["sha"]
                # Get files changed in this commit
                detail_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/commits/{sha}"
                dr = requests.get(detail_url, headers=HEADERS_GITHUB, timeout=10)
                if dr.status_code == 200:
                    files = dr.json().get("files", [])
                    for f in files:
                        filename = f.get("filename", "")
                        if filename.endswith(".md") and "README" not in filename:
                            # Extract machine name from path
                            parts = filename.split("/")
                            machine_name = parts[-2] if len(parts) > 1 else parts[-1].replace(".md", "")
                            date = commit["commit"]["author"]["date"][:10]
                            return {
                                "name": machine_name,
                                "path": filename,
                                "date": date,
                                "url": f"https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO}/blob/main/{filename}"
                            }
    except Exception as e:
        print(f"[GitHub] Error: {e}")
    return None

def count_writeups():
    """Count total writeups in the repo"""
    try:
        url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/git/trees/main?recursive=1"
        r = requests.get(url, headers=HEADERS_GITHUB, timeout=10)
        if r.status_code == 200:
            tree = r.json().get("tree", [])
            count = sum(
                1 for f in tree
                if f["path"].endswith(".md")
                and "README" not in f["path"]
                and "TEMPLATE" not in f["path"]
            )
            return count
    except Exception as e:
        print(f"[GitHub count] Error: {e}")
    return 0

# ─── README BUILDER ───────────────────────────────────────────────────────────
def build_readme(htb, htb_activity, rootme, latest_writeup, writeup_count):
    """Build the README content"""

    updated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # HTB section
    if htb:
        htb_section = f"""### 🟢 HackTheBox
| Stat | Value |
|------|-------|
| 🎯 Rank | {htb.get('rank_text', 'N/A')} |
| ⭐ Points | {htb.get('points', 0)} |
| 🖥️ User Owns | {htb.get('user_owns', 0)} |
| 💀 System Owns | {htb.get('system_owns', 0)} |
| 🔴 Last Machine | {htb_activity.get('last_machine', 'N/A')} ({htb_activity.get('last_machine_date', 'N/A')}) |

[→ View HTB Profile](https://app.hackthebox.com/users/{HTB_USER_ID})"""
    else:
        htb_section = "### 🟢 HackTheBox\n*Could not fetch data*"

    # RootMe section
    if rootme:
        cats = rootme.get("categories", {})
        forensics_line = ""
        network_line = ""
        for cat, score in cats.items():
            cat_lower = cat.lower()
            if "forensic" in cat_lower:
                forensics_line = f"| 🔬 Forensics | {score} |"
            if "network" in cat_lower or "réseau" in cat_lower:
                network_line = f"| 🌐 Network | {score} |"

        rootme_section = f"""### 🔴 Root-Me
| Stat | Value |
|------|-------|
| 🏆 Score | {rootme.get('score', 'N/A')} |
{forensics_line}
{network_line}
| 📌 Last Challenge | {rootme.get('last_challenge', 'N/A')} ({rootme.get('last_challenge_date', 'N/A')}) |

[→ View RootMe Profile](https://www.root-me.org/{ROOTME_USERNAME})"""
    else:
        rootme_section = "### 🔴 Root-Me\n*Could not fetch data*"

    # Latest writeup section
    if latest_writeup:
        writeup_section = f"""### 📝 Latest Writeup
**[{latest_writeup['name']}]({latest_writeup['url']})** — {latest_writeup['date']}

Total writeups published : **{writeup_count}**"""
    else:
        writeup_section = f"### 📝 Writeups\nTotal published : **{writeup_count}**"

    readme = f"""# Guillaume Grazioli — Offensive Security

🇫🇷 Software engineering background | Now fully focused on **offensive cybersecurity**  
🇬🇧 French / Spanish / English  
📍 Available from May 2025 — France / Spain / Remote

---

## 🛠️ Current Stack

```
Forensics    Volatility 2/3 · strings · binwalk · Autopsy
Cracking     John the Ripper · Hashcat
Network      Wireshark · tcpdump · nmap · netcat
Web          Burp Suite · sqlmap · manual testing
OS           Kali Linux · Ubuntu · Windows
CTF          RootMe · HackTheBox
```

---

## 📊 Progress

{htb_section}

{rootme_section}

{writeup_section}

---

## 📂 Writeups Repository

| Platform | Path |
|----------|------|
| HackTheBox Starting Point | [hackthebox/starting-point/](hackthebox/starting-point/) |
| HackTheBox Machines | [hackthebox/](hackthebox/) |
| RootMe | [rootme/](rootme/) |

---

*Last updated : {updated_at} by GitHub Actions*
"""
    return readme

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    print("Fetching HTB data...")
    htb = get_htb_data()
    htb_activity = get_htb_activity()
    print(f"HTB: {htb}")

    print("Fetching RootMe data...")
    rootme = get_rootme_data()
    print(f"RootMe score: {rootme.get('score') if rootme else 'N/A'}")

    print("Fetching latest writeup...")
    latest_writeup = get_latest_writeup()
    writeup_count = count_writeups()
    print(f"Latest writeup: {latest_writeup}")
    print(f"Total writeups: {writeup_count}")

    print("Building README...")
    readme_content = build_readme(htb, htb_activity, rootme, latest_writeup, writeup_count)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("README.md updated successfully.")

if __name__ == "__main__":
    main()
