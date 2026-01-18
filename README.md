# UPUTE

1. Postaviti certifikat za XMPP poslužitelj na lokalnom serveru sa lozinkom *tajna*:<br />
+ sudo prosodyctl cert generate localhost<br /><br />

2. Preuzeti SPADE biblioteku u željeno python okruženje, postaviti direktorij i pokrenuti SPADE:<br />
+ uv init<br />
+ uv add spade<br />
+ source .venv/bin/activate<br />
+ spade run<br /><br />

3. Prebaciti se u direktorij gdje se nalazi *sustav.py* datoteka i unijeti sljedeće naredbe za pokretanje:<br />
+ chmod +x sustav.py<br />
+ ./sustav.py
