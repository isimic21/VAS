#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour


class Tekma(Agent):
    def stvoriTekme(self):
        timovi = [
            {"naziv": "Dinamo", "snaga": 0.7},
            {"naziv": "Belupo", "snaga": 0.8},
            {"naziv": "Lokomotiva", "snaga": 0.9},
            {"naziv": "Rijeka", "snaga": 0.75},
            {"naziv": "Hajduk", "snaga": 0.65},
            {"naziv": "Slaven", "snaga": 0.85},
        ]

        random.shuffle(timovi)
        tekme = []

        for i in range(0, len(timovi), 2):
            tekme.append({"id": i // 2 + 1, "home": timovi[i], "away": timovi[i + 1]})

        return tekme

    class stanjeTekma(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if not msg:
                return

            if msg.body == "GET":
                self.agent.tekme = self.agent.stvoriTekme()
                reply = msg.make_reply()
                reply.body = json.dumps(self.agent.tekme)
                await self.send(reply)

            elif msg.body.startswith("Simuliraj"):
                tekma_id = int(msg.body.split(":")[1])
                tekma = next(t for t in self.agent.tekme if t["id"] == tekma_id)

                HOME_prednost = 1.1
                AWAY_hendikep = 0.95

                HOME_rezultat = tekma["home"]["snaga"] * HOME_prednost * max(0.6, min(random.gauss(1, 0.25), 1.4))
                AWAY_rezultat = tekma["away"]["snaga"] * AWAY_hendikep * max(0.6, min(random.gauss(1, 0.25), 1.4))
                avg = (HOME_rezultat + AWAY_rezultat) / 2

                if abs(HOME_rezultat - AWAY_rezultat) / avg < 0.15:
                    pobjednik = "DRAW"
                elif HOME_rezultat > AWAY_rezultat:
                    pobjednik = "HOME"
                else:
                    pobjednik = "AWAY"

                reply = msg.make_reply()
                reply.body = json.dumps({"tekma_id": tekma_id, "pobjednik": pobjednik})
                await self.send(reply)

    async def setup(self):
        print("|Agent Tekma pokrenut|")
        self.tekme = []
        self.add_behaviour(self.stanjeTekma())
