import time
import requests
from typing import Dict, Any, Optional

BASE_URL = "https://api.scryfall.com/cards/named"

def fetch_exact_print(name: str, set_code: str) -> Optional[Dict[str, Any]]:
    """ Fetches the exact print of a card including price"""

    time.sleep(0.55)  # Rate limiting to avoid hitting Scryfall's API too quickly

    response = requests.get(
        BASE_URL,
        params={"exact": name, "set": set_code}
        headers={"User-Agent": "MTGVaultApp/1.0", "Accept": "*/*"}
    )

    if response.status_code == 200:
        return response.json()
    return None

def fetch_base_metadata(name: str) -> Optional[Dict[str, Any]]:
    """ Fetches general card metadata (newest print). Ignores set-specific pricing."""
    
    time.sleep(0.55)  # Rate limiting to avoid hitting Scryfall's API too quickly

    response = requests.get(
        BASE_URL,
        params={"exact": name},
        headers={"User-Agent": "MTGVaultApp/1.0", "Accept": "*/*"}
    )

    if response.status_code == 200:
        return response.json()
    return None