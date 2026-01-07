import requests
from bs4 import BeautifulSoup

CRICBUZZ_URL = "https://www.cricbuzz.com/cricket-match/live-scores"
ESPN_API = "https://site.web.api.espn.com/apis/v2/sports/cricket/scoreboard"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
}


def scrape_cricbuzz():
    response = requests.get(CRICBUZZ_URL, headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    matches = []

    cards = soup.select("div.cb-mtch-lst.cb-col.cb-col-100.cb-tms-itm")

    for card in cards:
        title = card.select_one("h3.cb-lv-scr-mtch-hdr")
        status = card.select_one("span.cb-text-live, span.cb-text-complete")

        if title:
            matches.append({
                "name": title.get_text(strip=True),
                "type": "Live",
                "venue": "N/A",
                "status": status.get_text(strip=True) if status else "Live"
            })

    return matches


def scrape_espn():
    response = requests.get(ESPN_API, headers=HEADERS, timeout=10)
    response.raise_for_status()
    data = response.json()

    matches = []

    for event in data.get("events", []):
        name = event.get("name", "Unknown Match")
        status = event.get("status", {}).get("type", {}).get("description", "Live")

        matches.append({
            "name": name,
            "type": "Live",
            "venue": "N/A",
            "status": status
        })

    return matches


def get_live_matches():
    # Try Cricbuzz first
    try:
        matches = scrape_cricbuzz()
        if matches:
            return matches
    except Exception:
        pass

    # Fallback to ESPN
    try:
        matches = scrape_espn()
        if matches:
            return matches
    except Exception:
        pass

    # Absolute fallback (no crash)
    return [{
        "name": "Live matches temporarily unavailable",
        "type": "-",
        "venue": "-",
        "status": "Source sites blocked or no live games"
    }]
