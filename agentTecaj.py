#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour


class Tecaj(Agent):
    class stanjeTecaj(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                vjerojatnosti = json.loads(msg.body)
                tecaj = {}

                for tekma_id, vjerojatnost in vjerojatnosti.items():
                    tecaj[tekma_id] = {}
                    for rezultat, v in vjerojatnost.items():
                        tecaj[tekma_id][rezultat] = round(1 / (v * 1.05), 2)

                reply = msg.make_reply()
                reply.body = json.dumps(tecaj)
                await self.send(reply)

    async def setup(self):
        print("|Agent Tecaj pokrenut|")
        self.add_behaviour(self.stanjeTecaj())
