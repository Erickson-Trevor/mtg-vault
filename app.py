import os
from flask import Flask
from mtg_vault.presentation.routes import vault_blueprint
from mtg_vault.adapters.database import init_db

# 1. Create the core Flask application
app = Flask(__name__)
# Use the enviornment variable, defaulting to sqlite if missing
db_url = os.getenv("DATABASE_URL", "sqlite:///decks.database")

# 2. Attach the Presentation Layer (Blueprint) to the core app
# Prepending "/api" means your endpoint becomes "http://127.0.0.1:5000/api/ingest"
app.register_blueprint(vault_blueprint, url_prefix="/api")

# 3. Generate the physical SQLite database file before starting
with app.app_context():
    init_db()

# 4. Start the local development server
if __name__ == "__main__":
    app.run(debug=True)