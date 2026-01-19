import requests
from bs4 import BeautifulSoup
import logging
import json
from src.config import load_config
from src.cache import get_cached_matches, cache_matches, is_cache_valid

CRICBUZZ_URL = "https://www.cricbuzz.com/cricket-match/live-scores"
ESPN_API = "https://site.web.api.espn.com/apis/v2/sports/cricket/scoreboard"

# Load configuration
config = load_config()
TIMEOUT = config.get("timeout", 10)
HEADERS = config.get("headers", {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
})

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def scrape_cricbuzz():
    try:
        logger.info(f"Attempting to fetch data from {CRICBUZZ_URL}")
        response = requests.get(CRICBUZZ_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        matches = []

        cards = soup.select("div.cb-mtch-lst.cb-col.cb-col-100.cb-tms-itm")
        
        if not cards:
            logger.warning("No match cards found on Cricbuzz page")
            return []

        for card in cards:
            title = card.select_one("h3.cb-lv-scr-mtch-hdr")
            status = card.select_one("span.cb-text-live, span.cb-text-complete")

            if title:
                match_data = {
                    "name": title.get_text(strip=True),
                    "type": "Live",
                    "venue": "N/A",
                    "status": status.get_text(strip=True) if status else "Live"
                }
                matches.append(match_data)
                logger.debug(f"Found match: {match_data['name']}")

        logger.info(f"Successfully scraped {len(matches)} matches from Cricbuzz")
        return matches
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error while fetching from Cricbuzz: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in scrape_cricbuzz: {str(e)}")
        return []


def scrape_espn():
    try:
        logger.info(f"Attempting to fetch data from {ESPN_API}")
        response = requests.get(ESPN_API, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()

        matches = []

        events = data.get("events", [])
        if not events:
            logger.warning("No events found in ESPN response")
            return []

        for event in events:
            name = event.get("name", "Unknown Match")
            status = event.get("status", {}).get("type", {}).get("description", "Live")

            match_data = {
                "name": name,
                "type": "Live",
                "venue": "N/A",
                "status": status
            }
            matches.append(match_data)
            logger.debug(f"Found match: {match_data['name']}")

        logger.info(f"Successfully scraped {len(matches)} matches from ESPN")
        return matches
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error while fetching from ESPN: {str(e)}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error in ESPN response: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in scrape_espn: {str(e)}")
        return []


def get_live_matches():
    logger.info("Starting to fetch live matches")
    
    # Check if we have valid cached data first
    cached_matches = get_cached_matches()
    if cached_matches is not None:
        logger.info("Using cached matches data")
        return cached_matches
    
    # Reload config in case it changed
    config = load_config()
    
    # Try Cricbuzz first if enabled
    if config.get("sources", {}).get("cricbuzz_enabled", True):
        matches = scrape_cricbuzz()
        if matches:
            logger.info(f"Returning {len(matches)} matches from Cricbuzz")
            cache_matches(matches)  # Cache the results
            return matches
        else:
            logger.info("No matches found from Cricbuzz, trying ESPN")
    else:
        logger.info("Cricbuzz source disabled by config, skipping")

    # Fallback to ESPN if enabled
    if config.get("sources", {}).get("espn_enabled", True):
        matches = scrape_espn()
        if matches:
            logger.info(f"Returning {len(matches)} matches from ESPN")
            cache_matches(matches)  # Cache the results
            return matches
    else:
        logger.info("ESPN source disabled by config, skipping")

    logger.info("No matches found from any enabled sources, returning fallback message")

    # Absolute fallback (no crash)
    fallback_match = {
        "name": "Live matches temporarily unavailable",
        "type": "-",
        "venue": "-",
        "status": "Source sites blocked or no live games"
    }
    fallback_result = [fallback_match]
    cache_matches(fallback_result)  # Cache the fallback result too
    logger.info(f"Returning fallback match: {fallback_match['name']}")
    return fallback_result
