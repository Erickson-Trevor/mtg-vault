def fetch_exact_print(name: str, set_code: str):
    """Fakes a successful Scryfall API response for offline testing."""
    return {
        "name": name,
        "id": "offline-mock-id-123",
        "mana_cost": "{2}{B}",
        "type_line": "Artifact",
        "prices": {"usd": "1.23"}
    }

def fetch_base_metadata(name: str):
    """Fakes a base metadata reponse for offline testing"""
    return fetch_exact_print(name, "MOCK")
