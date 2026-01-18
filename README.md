# VAS

**UPUTE**

1. Postaviti certifikat za XMPP poslužitelj na lokalnom serveru sa lozinkom *tajna*:

sudo prosodyctl cert generate localhost


2. Preuzeti SPADE biblioteku u željeno python okruženje, postaviti direktorij i pokrenuti SPADE:

uv init

uv add spade

source .venv/bin/activate

spade run


3. Prebaciti se u direktorij gdje se nalazi *sustav.py* datoteka i unjeti sljedeće naredbe za pokretanje:

chmod +x sustav.py

./sustav.py
