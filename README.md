# UPUTE ZA POKRETANJE

1. Postaviti certifikat za XMPP poslužitelj na lokalnom serveru sa lozinkom *tajna*:
+ sudo prosodyctl cert generate localhost<br /><br /><br />

2. Preuzeti SPADE biblioteku u željeno python okruženje, postaviti direktorij i pokrenuti SPADE:
+ uv init<br />
+ uv add spade<br />
+ source .venv/bin/activate<br />
+ spade run<br /><br /><br />

3. Prebaciti se u direktorij gdje se nalazi *sustav.py* datoteka i unijeti sljedeće naredbe za pokretanje:
+ chmod +x sustav.py<br />
+ ./sustav.py
