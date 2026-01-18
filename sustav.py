#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import spade
from agentTekma import Tekma
from agentVjerojatnost import Vjerojatnost
from agentTecaj import Tecaj
from agentKorisnik import Korisnik


async def main():
    tekma = Tekma("tekma@localhost", "tajna")
    vjerojatnost = Vjerojatnost("vjerojatnost@localhost", "tajna")
    tecaj = Tecaj("tecaj@localhost", "tajna")
    korisnik = Korisnik("korisnik@localhost", "tajna")

    await tekma.start()
    await vjerojatnost.start()
    await tecaj.start()
    await korisnik.start()

    await spade.wait_until_finished(korisnik)
    await tekma.stop()
    await vjerojatnost.stop()
    await tecaj.stop()
    print("|Agenti zaustavljeni|")


if __name__ == "__main__":
    spade.run(main())
