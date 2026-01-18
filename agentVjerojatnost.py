#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour


class Vjerojatnost(Agent):
    class stanjeVjerojatnost(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if not msg:
                return

            tekme = json.loads(msg.body)
            vjerojatnosti = {}

            HOME_prednost = 1.1
            AWAY_hendikep = 0.95

            for tekma in tekme:
                rezultati = {"HOME": 0, "AWAY": 0, "DRAW": 0}

                for _ in range(500):
                    HOME_rezultat = tekma["home"]["snaga"] * HOME_prednost * max(0.6, min(random.gauss(1, 0.25), 1.4))
                    AWAY_rezultat = tekma["away"]["snaga"] * AWAY_hendikep * max(0.6, min(random.gauss(1, 0.25), 1.4))
                    avg = (HOME_rezultat + AWAY_rezultat) / 2

                    if abs(HOME_rezultat - AWAY_rezultat) / avg < 0.15:
                        rezultati["DRAW"] += 1
                    elif HOME_rezultat > AWAY_rezultat:
                        rezultati["HOME"] += 1
                    else:
                        rezultati["AWAY"] += 1

                ukupno = sum(rezultati.values()) + 3
                vjerojatnosti[tekma["id"]] = {
                    "HOME": round((rezultati["HOME"] + 1) / ukupno, 2),
                    "AWAY": round((rezultati["AWAY"] + 1) / ukupno, 2),
                    "DRAW": round((rezultati["DRAW"] + 1) / ukupno, 2),
                }

            reply = msg.make_reply()
            reply.body = json.dumps(vjerojatnosti)
            await self.send(reply)

    async def setup(self):
        print("|Agent Vjerojatnost pokrenut|")
        self.add_behaviour(self.stanjeVjerojatnost())
