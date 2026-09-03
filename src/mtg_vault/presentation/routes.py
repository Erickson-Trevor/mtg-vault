from flask import Blueprint, jsonify, request
from mtg_vault.adapters.database import SessionLocal, CardRepository
from mtg_vault.services.vault_service import VaultService

vault_blueprint = Blueprint("vault", __name__)

@vault_blueprint.route("/ingest_card", methods=["POST"])
def ingest_cards():
    # 1. Parse the incoming HTTP request
    data = request.get_json()
    if not data or "line" not in data:
        return jsonify({"error": "Missing 'line' in JSON payload"}), 400

    # 2. Open a fresh database for this request
    session = SessionLocal()

    try:
        # 3. Instantiate the repository and service
        repository = CardRepository(session)
        service = VaultService(repository)

        # 4. Execute the ingestion logic
        saved_cards = service.ingest_card_line(data["line"])

        # 5. Format HTTP response
        return jsonify({
            "status": "success",
            "cards_added": len(saved_cards),
            "names": [card.name for card in saved_cards]
        }), 201