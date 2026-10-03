#!/usr/bin/env python3
"""Disegna e verifica una spirale di Fibonacci terminale."""

from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass
from typing import Iterable

RISOLUZIONE = 8


@dataclass(frozen=True)
class Quadrato:
    lato: int
    x: int
    y: int

    def vertici(self) -> tuple[tuple[int, int], ...]:
        return ((self.x, self.y), (self.x + self.lato, self.y),
                (self.x + self.lato, self.y + self.lato),
                (self.x, self.y + self.lato))


@dataclass(frozen=True)
class Arco:
    centro: tuple[int, int]
    inizio: tuple[int, int]
    fine: tuple[int, int]
    verso: int
    lato: int

    def tangente(self, punto: tuple[int, int]) -> tuple[int, int]:
        dx = punto[0] - self.centro[0]
        dy = punto[1] - self.centro[1]
        segno_x = (dx > 0) - (dx < 0)
        segno_y = (dy > 0) - (dy < 0)
        return (-self.verso * segno_y, self.verso * segno_x)


def successione(n: int) -> list[int]:
    valori = [1, 1]
    while len(valori) < n:
        valori.append(valori[-1] + valori[-2])
    return valori[:n]


def costruisci(n: int) -> tuple[list[Quadrato], list[Arco]]:
    lati = successione(n)
    quadrati = [Quadrato(1, 0, 0), Quadrato(1, 1, 0)]
    sinistra, basso, destra, alto = 0, 0, 2, 1
    for indice, lato in enumerate(lati[2:], start=2):
        direzione = indice % 4
        if direzione == 2:  # sopra
            q = Quadrato(lato, sinistra, alto)
            alto += lato
        elif direzione == 3:  # a sinistra
            q = Quadrato(lato, sinistra - lato, basso)
            sinistra -= lato
        elif direzione == 0:  # sotto
            q = Quadrato(lato, sinistra, basso - lato)
            basso -= lato
        else:  # a destra
            q = Quadrato(lato, destra, basso)
            destra += lato
        quadrati.append(q)

    # I primi due quarti condividono il centro nell'angolo superiore comune.
    centro = (1, 1)
    archi = [Arco(centro, (0, 1), (1, 0), 1, 1),
             Arco(centro, (1, 0), (2, 1), 1, 1)]
    for q in quadrati[2:]:
        inizio = archi[-1].fine
        tangente_richiesta = archi[-1].tangente(inizio)
        vertici = q.vertici()
        candidati: list[Arco] = []
        for centro_candidato in vertici:
            if centro_candidato == inizio:
                continue
            dx, dy = inizio[0] - centro_candidato[0], inizio[1] - centro_candidato[1]
            if abs(dx) + abs(dy) != q.lato:
                continue
            for fine in vertici:
                fx, fy = fine[0] - centro_candidato[0], fine[1] - centro_candidato[1]
                if abs(fx) + abs(fy) != q.lato or dx * fx + dy * fy != 0:
                    continue
                for verso in (-1, 1):
                    arco = Arco(centro_candidato, inizio, fine, verso, q.lato)
                    if arco.tangente(inizio) == tangente_richiesta:
                        candidati.append(arco)
        if len(candidati) != 1:
            raise ValueError(f"impossibile scegliere l'arco del quadrato {len(archi) + 1}")
        archi.append(candidati[0])
    return quadrati, archi


def verifica(n: int) -> list[str]:
    quadrati, archi = costruisci(n)
    lati = successione(n)
    assert [q.lato for q in quadrati] == lati
    assert len({(q.x, q.y, q.lato) for q in quadrati}) == n
    rett = (min(q.x for q in quadrati), min(q.y for q in quadrati),
            max(q.x + q.lato for q in quadrati),
            max(q.y + q.lato for q in quadrati))
    lati_rettangolo = successione(n + 1)[-2:]
    assert sorted((rett[2] - rett[0], rett[3] - rett[1])) == sorted(lati_rettangolo)
    assert sum(q.lato * q.lato for q in quadrati) == (rett[2] - rett[0]) * (rett[3] - rett[1])
    for i, q in enumerate(quadrati):
        for altro in quadrati[i + 1:]:
            assert (q.x + q.lato <= altro.x or altro.x + altro.lato <= q.x
                    or q.y + q.lato <= altro.y or altro.y + altro.lato <= q.y)
    for i, (q, a) in enumerate(zip(quadrati, archi)):
        assert a.lato == q.lato
        assert (a.inizio in q.vertici()) and (a.fine in q.vertici())
        assert sum((a.inizio[k] - a.centro[k]) ** 2 for k in (0, 1)) == q.lato ** 2
        assert sum((a.fine[k] - a.centro[k]) ** 2 for k in (0, 1)) == q.lato ** 2
        for passo in range(33):
            t = math.atan2(a.inizio[1] - a.centro[1], a.inizio[0] - a.centro[0]) + a.verso * math.pi * passo / 64
            x = a.centro[0] + a.lato * math.cos(t)
            y = a.centro[1] + a.lato * math.sin(t)
            assert q.x - 1e-9 <= x <= q.x + q.lato + 1e-9
            assert q.y - 1e-9 <= y <= q.y + q.lato + 1e-9
        if i:
            assert archi[i - 1].fine == a.inizio
            assert archi[i - 1].tangente(a.inizio) == a.tangente(a.inizio)
        assert connessi(rasterizza_arco(a))
        if i:
            assert set(rasterizza_arco(archi[i - 1])) & set(rasterizza_arco(a))
    assert len({a.verso for a in archi}) == 1
    if n < 80:
        quadrati_successivi, archi_successivi = costruisci(n + 1)
        assert quadrati_successivi[:n] == quadrati
        assert archi_successivi[:n] == archi
    punti = rasterizza(quadrati, archi)
    assert punti
    assert connessi(punti)
    larghezza = max(x for x, _ in punti) - min(x for x, _ in punti) + 1
    altezza = max(y for _, y in punti) - min(y for _, y in punti) + 1
    assert larghezza > 0 and altezza > 0
    assert len({x for x, _ in punti}) == larghezza
    assert len({y for _, y in punti}) == altezza
    return [f"N={n}: {n} quadrati, {n} archi; rettangolo {rett[2]-rett[0]}x{rett[3]-rett[1]}; raster {larghezza}x{altezza}."]


def rasterizza(quadrati: list[Quadrato], archi: list[Arco]) -> set[tuple[int, int]]:
    scala = RISOLUZIONE
    punti: set[tuple[int, int]] = set()
    for q in quadrati:
        x0, y0 = q.x * scala, q.y * scala
        x1, y1 = (q.x + q.lato) * scala, (q.y + q.lato) * scala
        punti.update((x, y0) for x in range(x0, x1 + 1))
        punti.update((x, y1) for x in range(x0, x1 + 1))
        punti.update((x0, y) for y in range(y0, y1 + 1))
        punti.update((x1, y) for y in range(y0, y1 + 1))
    for a in archi:
        punti.update(rasterizza_arco(a, scala))
    # Una sola rotazione globale, seguita da una sola traslazione globale.
    x0, y0 = min(x for x, _ in punti), min(y for _, y in punti)
    x1, y1 = max(x for x, _ in punti), max(y for _, y in punti)
    if y1 - y0 > x1 - x0:
        punti = {(-y, x) for x, y in punti}
    x0, y0 = min(x for x, _ in punti), min(y for _, y in punti)
    return {(x - x0, y - y0) for x, y in punti}


def rasterizza_arco(a: Arco, scala: int = RISOLUZIONE) -> set[tuple[int, int]]:
    cx, cy = a.centro[0] * scala, a.centro[1] * scala
    sx, sy = (a.inizio[0] - a.centro[0]) * scala, (a.inizio[1] - a.centro[1]) * scala
    angolo = math.atan2(sy, sx)
    passi = max(2, math.ceil(math.pi * a.lato * scala / 2))
    punti = set()
    for i in range(passi + 1):
        t = angolo + a.verso * (math.pi / 2) * i / passi
        punti.add((cx + round(a.lato * scala * math.cos(t)),
                   cy + round(a.lato * scala * math.sin(t))))
    punti.add((a.inizio[0] * scala, a.inizio[1] * scala))
    punti.add((a.fine[0] * scala, a.fine[1] * scala))
    return punti


def connessi(punti: set[tuple[int, int]]) -> bool:
    da_visitare = [next(iter(punti))]
    visitati = {da_visitare[0]}
    while da_visitare:
        x, y = da_visitare.pop()
        for vicino in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1),
                       (x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)):
            if vicino in punti and vicino not in visitati:
                visitati.add(vicino)
                da_visitare.append(vicino)
    return len(visitati) == len(punti)


def griglia(quadrati: list[Quadrato]) -> str:
    x0, y0 = min(q.x for q in quadrati), min(q.y for q in quadrati)
    x1 = max(q.x + q.lato for q in quadrati)
    y1 = max(q.y + q.lato for q in quadrati)
    righe = []
    for y in range(y1, y0 - 1, -1):
        riga = []
        for x in range(x0, x1 + 1):
            bordo = any(x in (q.x, q.x + q.lato) and q.y <= y <= q.y + q.lato
                        or y in (q.y, q.y + q.lato) and q.x <= x <= q.x + q.lato
                        for q in quadrati)
            riga.append("+" if bordo else " ")
        righe.append("".join(riga).rstrip())
    return "\n".join(righe)


def braille(punti: set[tuple[int, int]]) -> str:
    x1, y1 = max(x for x, _ in punti), max(y for _, y in punti)
    larg, alt = (x1 + 1 + 1) // 2, (y1 + 1 + 3) // 4
    bit = {(0, 0): 0, (0, 1): 1, (0, 2): 2, (1, 0): 3,
           (1, 1): 4, (1, 2): 5, (0, 3): 6, (1, 3): 7}
    righe = []
    for cy in range(alt - 1, -1, -1):
        chars = []
        for cx in range(larg):
            valore = 0
            for (dx, dy), indice in bit.items():
                if (cx * 2 + dx, cy * 4 + dy) in punti:
                    valore |= 1 << indice
            chars.append(chr(0x2800 + valore))
        righe.append("".join(chars))
    return "\n".join(righe)


def main(argv: Iterable[str] | None = None) -> int:
    class Parser(argparse.ArgumentParser):
        def format_usage(self) -> str:
            return super().format_usage().replace("usage:", "uso:", 1)

        def error(self, message: str) -> None:
            self.print_usage(sys.stderr)
            self.exit(2, "errore: opzioni o valori non validi\n")

    parser = Parser(description="Disegna una spirale di Fibonacci terminale.", add_help=False)
    parser.add_argument("N", type=int, nargs="?", help="numero di quadrati (almeno 2)")
    parser.add_argument("--griglia", action="store_true", help="mostra la tassellazione ASCII")
    parser.add_argument("--verifica", action="store_true", help="verifica la costruzione")
    parser.add_argument("-h", "--aiuto", action="store_true", help="mostra questo aiuto in italiano")
    args = parser.parse_args(argv)
    if args.aiuto:
        print("Uso: python3 spirale_fibonacci.py N [--griglia | --verifica]")
        print("N deve essere almeno 2. Senza opzioni viene mostrata la tela Braille.")
        return 0
    if args.N is None:
        parser.error("manca il numero N")
    if args.N < 2:
        print("Errore: N deve essere almeno 2.", file=sys.stderr)
        return 2
    try:
        quadrati, archi = costruisci(args.N)
        if args.verifica:
            print("\n".join(verifica(args.N)))
        elif args.griglia:
            print(griglia(quadrati))
        else:
            print(braille(rasterizza(quadrati, archi)))
    except (AssertionError, ValueError) as errore:
        print(f"Errore di verifica: {errore}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
