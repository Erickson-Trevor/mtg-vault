from mtg_vault.services.parser import parse_card_line
from mtg_vault.adapters.scryfall import fetch_exact_print, fetch_base_metadata
from mtg_vault.domain.models import VaultCard
from mtg_vault.adapters.database import CardRepository

class VaultService:
    """Orchestrates parsing, API fetching, and database storage."""

    def __init__(self, repository: CardRepository):
        self.repository = repository

    def ingest_card_line(self, line: str) -> list[VaultCard]:

        # 1. Parse the input line to extract card details.
        parsed_data = parse_card_line(line)

        #2. Fetch Scryfall data based on whether the card is a proxy or has a set code.
        price = 0.0
        api_data = None

        if parsed_data.is_proxy or not parsed_data.set_code:
            api_data = fetch_base_metadata(parsed_data.name)
        else:
            api_data = fetch_exact_print(parsed_data.name, parsed_data.set_code)

            #Grab the price if available, otherwise default to 0.0.
            if api_data and api_data.get("prices") and api_data["prices"].get("usd"):
                price = float(api_data["prices"]["usd"])


        # Extract metadata, fall back to parsed name if API fails.
        name = api_data.get("name", parsed_data.name) if api_data else parsed_data.name
        scryfall_id = api_data.get("id") if api_data else None
        mana_cost = api_data.get("mana_cost") if api_data else None
        type_line = api_data.get("type_line") if api_data else None

        # 3. Create and save domain objects based on quanity.
        saved_cards = []
        for _ in range(parsed_data.quantity):
            card = VaultCard(
                name = name,
                set_code = parsed_data.set_code,
                scryfall_id = scryfall_id,
                mana_cost = mana_cost,
                type_line = type_line,
                physical_location = parsed_data.location,
                is_proxy = parsed_data.is_proxy,
                usd_price = price
            )
            saved_cards.append(self.repository.save(card))

        return saved_cards