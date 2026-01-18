#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import asyncio
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message


class stanjeKorisnik(FSMBehaviour):
    async def on_start(self):
        print("\nDobro došli~")

    async def on_end(self):
        print("\nHvala na korištenju!")
        await self.agent.stop()


class Depozit(State):
    async def run(self):
        loop = asyncio.get_event_loop()
        novac = float(await loop.run_in_executor(None, input, "Depozit: "))
        self.agent.saldo = novac
        self.set_next_state("CekajTekme")

class CekajTekme(State):
    async def run(self):
        msg = Message(to="tekma@localhost", body="GET")
        await self.send(msg)
        self.set_next_state("UzmiTekme")

class UzmiTekme(State):
    async def run(self):
        msg = await self.receive(timeout=10)
        if msg:
            self.agent.tekme = json.loads(msg.body)
            self.set_next_state("CekajVjerojatnosti")

class CekajVjerojatnosti(State):
    async def run(self):
        msg = Message(to="vjerojatnost@localhost")
        msg.body = json.dumps(self.agent.tekme)
        await self.send(msg)
        self.set_next_state("UzmiVjerojatnosti")

class UzmiVjerojatnosti(State):
    async def run(self):
        msg = await self.receive(timeout=10)
        if msg:
            self.agent.vjerojatnosti = json.loads(msg.body)
            self.set_next_state("CekajTecaj")

class CekajTecaj(State):
    async def run(self):
        msg = Message(to="tecaj@localhost")
        msg.body = json.dumps(self.agent.vjerojatnosti)
        await self.send(msg)
        self.set_next_state("UzmiTecaj")

class UzmiTecaj(State):
    async def run(self):
        msg = await self.receive(timeout=10)
        if msg:
            self.agent.tecaj = json.loads(msg.body)
            self.set_next_state("Izbornik")

class Izbornik(State):
    async def run(self):
        print("\nTrenutno dostupne tekme:")
        for tekma in self.agent.tekme:
            tekma_id = str(tekma["id"])
            print(f'\nTekma {tekma_id}: {tekma["home"]["naziv"]} (HOME) vs {tekma["away"]["naziv"]} (AWAY)')
            for rezultat in ["HOME", "DRAW", "AWAY"]:
                t = self.agent.tecaj[tekma_id][rezultat]
                print(f"{rezultat}: Tečaj {t:.2f} | Vjerojatnost {(1/t*100):.0f}%")

        print(f"\nSaldo: {self.agent.saldo}")
        self.set_next_state("Kladenje")

class Kladenje(State):
    async def run(self):
        loop = asyncio.get_event_loop()
        self.agent.ulog_tekma = int(await loop.run_in_executor(None, input, "\nID tekme: "))
        self.agent.ulog_pobjednik = (await loop.run_in_executor(None, input, "Pobjednik (HOME/AWAY/DRAW): ")).upper()
        ulog = float(await loop.run_in_executor(None, input, "Uplata: "))

        if ulog > self.agent.saldo:
            print("Nedovoljan saldo.")
            self.set_next_state("Kladenje")
            return

        self.agent.ulog = ulog
        self.agent.saldo -= ulog
        self.agent.saldo = round(self.agent.saldo, 2)
        self.set_next_state("Simuliraj")

class Simuliraj(State):
    async def run(self):
        msg = Message(to="tekma@localhost")
        msg.body = f"Simuliraj:{self.agent.ulog_tekma}"
        await self.send(msg)
        self.set_next_state("UzmiRezultat")

class UzmiRezultat(State):
    async def run(self):
        msg = await self.receive(timeout=10)
        if msg:
            rezultat = json.loads(msg.body)
            pobjednik = rezultat["pobjednik"]
            print(f"\nRezultat: {pobjednik}")

            if pobjednik == self.agent.ulog_pobjednik:
                t = self.agent.tecaj[str(self.agent.ulog_tekma)][self.agent.ulog_pobjednik]
                dobitak = round(self.agent.ulog * t, 2)
                self.agent.saldo += dobitak
                self.agent.saldo = round(self.agent.saldo, 2)
                profit = round(dobitak - self.agent.ulog, 2)
                print(f"Pobjeda! Osvojio si: {profit}")
            else:
                print("Izgubio si okladu :[")

            print(f"Saldo: {self.agent.saldo}")
            self.set_next_state("Nastavak")

class Nastavak(State):
    async def run(self):
        loop = asyncio.get_event_loop()
        if self.agent.saldo <= 0:
            izbor = await loop.run_in_executor(None, input, "\nSaldo pao na 0. Dodati jos novca? (y/n): ")
            if izbor == "y":
                self.set_next_state("Depozit")
            else:
                self.set_next_state("Kraj")
            return

        izbor = await loop.run_in_executor(None, input, "\nNastaviti? (y/n): ")
        if izbor == "y":
            self.set_next_state("CekajTekme")
        else:
            self.set_next_state("Kraj")

class Kraj(State):
    async def run(self):
        print(f"\nKonacni saldo: {self.agent.saldo}")


class Korisnik(Agent):
    async def setup(self):
        self.saldo = 0
        fsm = stanjeKorisnik()

        fsm.add_state("Depozit", Depozit(), initial=True)
        fsm.add_state("CekajTekme", CekajTekme())
        fsm.add_state("UzmiTekme", UzmiTekme())
        fsm.add_state("CekajVjerojatnosti", CekajVjerojatnosti())
        fsm.add_state("UzmiVjerojatnosti", UzmiVjerojatnosti())
        fsm.add_state("CekajTecaj", CekajTecaj())
        fsm.add_state("UzmiTecaj", UzmiTecaj())
        fsm.add_state("Izbornik", Izbornik())
        fsm.add_state("Kladenje", Kladenje())
        fsm.add_state("Simuliraj", Simuliraj())
        fsm.add_state("UzmiRezultat", UzmiRezultat())
        fsm.add_state("Nastavak", Nastavak())
        fsm.add_state("Kraj", Kraj())

        fsm.add_transition("Depozit", "CekajTekme")
        fsm.add_transition("CekajTekme", "UzmiTekme")
        fsm.add_transition("UzmiTekme", "CekajVjerojatnosti")
        fsm.add_transition("CekajVjerojatnosti", "UzmiVjerojatnosti")
        fsm.add_transition("UzmiVjerojatnosti", "CekajTecaj")
        fsm.add_transition("CekajTecaj", "UzmiTecaj")
        fsm.add_transition("UzmiTecaj", "Izbornik")
        fsm.add_transition("Izbornik", "Kladenje")
        fsm.add_transition("Kladenje", "Simuliraj")
        fsm.add_transition("Kladenje", "Kladenje")
        fsm.add_transition("Simuliraj", "UzmiRezultat")
        fsm.add_transition("UzmiRezultat", "Nastavak")
        fsm.add_transition("Nastavak", "CekajTekme")
        fsm.add_transition("Nastavak", "Depozit")
        fsm.add_transition("Nastavak", "Kraj")

        print("|Agent Korisnik pokrenut|")
        self.add_behaviour(fsm)
