import re
from dataclasses import dataclass
from typing import Optional

@dataclass
class ParsedCardInput:
    quantity: int
    name: str
    set_code: Optional[str]
    is_proxy: bool
    location: str

# Matches: "1x Card Name (SET) [PROXY] @ Location"
# Handles missing quantity, set code, proxy tag, or location gracefully.
CARD_PATTERN = re.compile(
    r"^(?:(?P<qty>\d+)x?\s+)?"
    r"(?P<name>[^(\[@]+?)"
    r"(?:\s*\((?P<set>[a-zA-Z0-9]{3,5})\))?"
    r"(?:\s*\[(?P<proxy>PROXY)\])?"
    r"(?:\s*@\s*(?P<location>.+))?$",
    re.IGNORECASE
)

def parse_card_line(line: str) -> ParsedCardInput:
    cleaned = line.strip()
    match = CARD_PATTERN.match(cleaned)
    if not match:
        raise ValueError(f"Unable to parse card format: '{line}'")

    data = match.groupdict()
    return ParsedCardInput(
        quantity=int(data["qty"]) if data["qty"] else 1,
        name=data["name"].strip(),
        set_code=data["set"].upper() if data["set"] else None,
        is_proxy=bool(data["proxy"]),
        location=data["location"].strip() if data["location"] else "Unassigned"
    )
