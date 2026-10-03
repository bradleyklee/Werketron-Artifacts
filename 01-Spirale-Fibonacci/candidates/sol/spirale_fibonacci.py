#!/usr/bin/env python3
"""Costruzione geometrica e rappresentazione terminale della spirale di Fibonacci."""

import sys
from dataclasses import dataclass
from math import cos, pi, sin


RISOLUZIONE = 8
DIREZIONI = ((0, -1), (1, 0), (0, 1), (-1, 0))
PUNTI_CARDINALI = ((1, 0), (0, 1), (-1, 0), (0, -1))
PUNTI_BRAILLE = ((0, 0, 0), (0, 1, 1), (0, 2, 2), (1, 0, 3),
                 (1, 1, 4), (1, 2, 5), (0, 3, 6), (1, 3, 7))


@dataclass(frozen=True)
class Quadrato:
    lato: int
    x: int
    y: int

    @property
    def vertici(self):
        return ((self.x, self.y), (self.x + self.lato, self.y),
                (self.x + self.lato, self.y + self.lato),
                (self.x, self.y + self.lato))


@dataclass(frozen=True)
class Arco:
    centro: tuple
    raggio: int
    quadrante: int
    inizio: tuple
    fine: tuple


@dataclass(frozen=True)
class Trasformazione:
    minimo_x: int
    minimo_y: int
    massimo_x: int
    massimo_y: int
    ruotata: bool

    @property
    def larghezza(self):
        return (self.massimo_y - self.minimo_y if self.ruotata
                else self.massimo_x - self.minimo_x)

    @property
    def altezza(self):
        return (self.massimo_x - self.minimo_x if self.ruotata
                else self.massimo_y - self.minimo_y)

    def applica(self, x, y, scala):
        if self.ruotata:
            return (round((y - self.minimo_y) * scala),
                    round((x - self.minimo_x) * scala))
        return (round((x - self.minimo_x) * scala),
                round((self.massimo_y - y) * scala))


def fibonacci(n):
    valori = [1, 1]
    while len(valori) < n:
        valori.append(valori[-1] + valori[-2])
    return valori


def tangente(quadrante):
    return DIREZIONI[quadrante]


def arco_successivo(quadrato, inizio, direzione):
    """Trova il quarto di cerchio interno al quadrato e tangente al precedente."""
    candidati = []
    for centro in quadrato.vertici:
        for quadrante, (dx, dy) in enumerate(PUNTI_CARDINALI):
            if (centro[0] + dx * quadrato.lato,
                    centro[1] + dy * quadrato.lato) != inizio:
                continue
            if tangente(quadrante) != direzione:
                continue
            dx_f, dy_f = PUNTI_CARDINALI[(quadrante - 1) % 4]
            fine = (centro[0] + dx_f * quadrato.lato,
                    centro[1] + dy_f * quadrato.lato)
            if fine in quadrato.vertici:
                candidati.append(Arco(centro, quadrato.lato,
                                      quadrante, inizio, fine))
    if len(candidati) != 1:
        raise ValueError("Il quadrato non determina un arco tangente unico")
    return candidati[0]


def costruisci(n):
    if n < 2:
        raise ValueError("N deve essere almeno 2")
    lati = fibonacci(n)
    quadrati = [Quadrato(1, 0, 0), Quadrato(1, 1, 0)]
    # Il centro comune produce il semicerchio nei due quadrati unitari.
    archi = [Arco((1, 0), 1, 2, (0, 0), (1, 1))]
    archi.append(arco_successivo(quadrati[1], archi[-1].fine,
                                 tangente((archi[-1].quadrante - 1) % 4)))
    estremi = [0, 0, 2, 1]
    for indice in range(2, n):
        lato = lati[indice]
        direzione = indice % 4  # giù, sinistra, su, destra
        minimo_x, minimo_y, massimo_x, massimo_y = estremi
        if direzione == 2:
            quadrato = Quadrato(lato, minimo_x, minimo_y - lato)
            minimo_y -= lato
        elif direzione == 3:
            quadrato = Quadrato(lato, minimo_x - lato, minimo_y)
            minimo_x -= lato
        elif direzione == 0:
            quadrato = Quadrato(lato, minimo_x, massimo_y)
            massimo_y += lato
        else:
            quadrato = Quadrato(lato, massimo_x, minimo_y)
            massimo_x += lato
        quadrati.append(quadrato)
        precedente = archi[-1]
        archi.append(arco_successivo(quadrato, precedente.fine,
                                     tangente((precedente.quadrante - 1) % 4)))
        estremi = [minimo_x, minimo_y, massimo_x, massimo_y]
    return quadrati, archi


def trasformazione(quadrati):
    minimo_x = min(q.x for q in quadrati)
    minimo_y = min(q.y for q in quadrati)
    massimo_x = max(q.x + q.lato for q in quadrati)
    massimo_y = max(q.y + q.lato for q in quadrati)
    return Trasformazione(minimo_x, minimo_y, massimo_x, massimo_y,
                          massimo_y - minimo_y > massimo_x - minimo_x)


def segmento(primo, ultimo):
    """Rasterizzazione intera continua di Bresenham, estremi inclusi."""
    x, y = primo
    fine_x, fine_y = ultimo
    passo_x = 1 if x < fine_x else -1
    passo_y = 1 if y < fine_y else -1
    delta_x = abs(fine_x - x)
    delta_y = -abs(fine_y - y)
    errore = delta_x + delta_y
    punti = []
    while True:
        punti.append((x, y))
        if (x, y) == ultimo:
            return punti
        doppio = 2 * errore
        if doppio >= delta_y:
            errore += delta_y
            x += passo_x
        if doppio <= delta_x:
            errore += delta_x
            y += passo_y


def punti_arco(arco, orientamento, scala=RISOLUZIONE):
    campioni = max(4, arco.raggio * scala * 4)
    percorso = []
    for indice in range(campioni + 1):
        angolo = (arco.quadrante - indice / campioni) * pi / 2
        x = arco.centro[0] + arco.raggio * cos(angolo)
        y = arco.centro[1] + arco.raggio * sin(angolo)
        punto = orientamento.applica(x, y, scala)
        if percorso and punto != percorso[-1]:
            percorso.extend(segmento(percorso[-1], punto)[1:])
        elif not percorso:
            percorso.append(punto)
    return percorso


def punti_bordi(quadrati, orientamento, scala=RISOLUZIONE):
    punti = set()
    for quadrato in quadrati:
        vertici = [orientamento.applica(*punto, scala)
                   for punto in quadrato.vertici]
        for indice in range(4):
            punti.update(segmento(vertici[indice], vertici[(indice + 1) % 4]))
    return punti


def punti_spirale(archi, orientamento, scala=RISOLUZIONE):
    percorsi = [punti_arco(arco, orientamento, scala) for arco in archi]
    return percorsi


def tela_braille(punti, orientamento, scala=RISOLUZIONE):
    larghezza = (orientamento.larghezza * scala + 2) // 2
    altezza = (orientamento.altezza * scala + 4) // 4
    righe = [[0] * larghezza for _ in range(altezza)]
    for x, y in punti:
        colonna, riga = x // 2, y // 4
        dx, dy = x % 2, y % 4
        indice = next(numero for px, py, numero in PUNTI_BRAILLE
                      if (px, py) == (dx, dy))
        righe[riga][colonna] |= 1 << indice
    return [''.join(chr(0x2800 + valore) for valore in riga)
            for riga in righe]


def disegna(quadrati, archi):
    orientamento = trasformazione(quadrati)
    bordi = punti_bordi(quadrati, orientamento)
    percorsi = punti_spirale(archi, orientamento)
    punti = bordi | {punto for percorso in percorsi for punto in percorso}
    return tela_braille(punti, orientamento)


def griglia(quadrati):
    orientamento = trasformazione(quadrati)
    larghezza = 2 * orientamento.larghezza + 1
    altezza = 2 * orientamento.altezza + 1
    tela = [[' '] * larghezza for _ in range(altezza)]
    for quadrato in quadrati:
        vertici = [orientamento.applica(*punto, 2)
                   for punto in quadrato.vertici]
        for indice in range(4):
            primo = vertici[indice]
            ultimo = vertici[(indice + 1) % 4]
            for x, y in segmento(primo, ultimo):
                tela[y][x] = '-' if primo[1] == ultimo[1] else '|'
    for quadrato in quadrati:
        vertici = [orientamento.applica(*punto, 2)
                   for punto in quadrato.vertici]
        for x, y in vertici:
            tela[y][x] = '+'
    return [''.join(riga) for riga in tela]


def controlla(condizione, messaggio):
    if not condizione:
        raise ValueError(messaggio)


def verifica(n):
    quadrati, archi = costruisci(n)
    lati = fibonacci(n + 1)
    controlla([q.lato for q in quadrati] == lati[:n], "Lati non Fibonacci")
    for indice, primo in enumerate(quadrati):
        for secondo in quadrati[indice + 1:]:
            sovrapposizione_x = max(primo.x, secondo.x) < min(primo.x + primo.lato, secondo.x + secondo.lato)
            sovrapposizione_y = max(primo.y, secondo.y) < min(primo.y + primo.lato, secondo.y + secondo.lato)
            controlla(not (sovrapposizione_x and sovrapposizione_y), "Quadrati sovrapposti")
    orientamento = trasformazione(quadrati)
    larghezze = sorted((orientamento.massimo_x - orientamento.minimo_x,
                        orientamento.massimo_y - orientamento.minimo_y))
    controlla(larghezze == sorted((lati[n - 1], lati[n])) and
             sum(q.lato ** 2 for q in quadrati) == larghezze[0] * larghezze[1],
             "Unione non rettangolare Fibonacci")
    controlla(archi[0].centro == archi[1].centro and
             archi[0].fine == archi[1].inizio, "Semicerchio centrale errato")
    for indice, (quadrato, arco) in enumerate(zip(quadrati, archi)):
        controlla(arco.raggio == quadrato.lato and arco.centro in quadrato.vertici and
                 arco.inizio in quadrato.vertici and arco.fine in quadrato.vertici,
                 "Arco fuori dal quadrato o raggio errato")
        if indice:
            precedente = archi[indice - 1]
            comuni = {precedente.inizio, precedente.fine} & {arco.inizio, arco.fine}
            controlla(precedente.fine == arco.inizio and comuni == {arco.inizio},
                     "Estremi degli archi non unici")
            controlla(tangente((precedente.quadrante - 1) % 4) == tangente(arco.quadrante),
                     "Tangenti diverse")
    # Entrambi gli insiemi passano lo stesso oggetto di trasformazione globale.
    bordi = punti_bordi(quadrati, orientamento)
    percorsi = punti_spirale(archi, orientamento)
    for indice, percorso in enumerate(percorsi):
        controlla(bool(percorso), "Arco raster vuoto")
        controlla(percorso[0] == orientamento.applica(*archi[indice].inizio, RISOLUZIONE) and
                 percorso[-1] == orientamento.applica(*archi[indice].fine, RISOLUZIONE),
                 "Estremi raster errati")
        controlla(all(max(abs(a[0] - b[0]), abs(a[1] - b[1])) <= 1
                     for a, b in zip(percorso, percorso[1:])), "Arco raster disconnesso")
        if indice:
            controlla(percorsi[indice - 1][-1] == percorso[0], "Giunzione raster disconnessa")
    righe = tela_braille(bordi | {p for percorso in percorsi for p in percorso}, orientamento)
    controlla(len({len(riga) for riga in righe}) == 1, "Righe di larghezza diversa")
    controlla(all(0x2800 <= ord(c) <= 0x28ff for r in righe for c in r),
             "Caratteri non Braille")
    controlla(any(c != '\u2800' for c in righe[0]) and
             any(c != '\u2800' for c in righe[-1]) and
             any(r[0] != '\u2800' for r in righe) and
             any(r[-1] != '\u2800' for r in righe),
             "Margine esterno vuoto")
    altri_quadrati, altri_archi = costruisci(n + 1)
    controlla(quadrati == altri_quadrati[:n] and archi == altri_archi[:n],
             "Prefisso geometrico non conservato")
    return len(quadrati), len(righe), len(righe[0])


def principale():
    argomenti = sys.argv[1:]
    if len(argomenti) not in (1, 2) or (len(argomenti) == 2 and
                                        argomenti[1] not in ('--griglia', '--verifica')):
        errore_interfaccia('argomenti non validi')
    try:
        n = int(argomenti[0])
    except ValueError:
        errore_interfaccia('N deve essere un numero intero')
    if n < 2:
        errore_interfaccia('N deve essere almeno 2')
    modo = argomenti[1] if len(argomenti) == 2 else ''
    if modo == '--verifica':
        try:
            numero, righe, colonne = verifica(n)
        except ValueError as errore:
            print(f'Verifica fallita: {errore}', file=sys.stderr)
            raise SystemExit(1) from errore
        print(f'Verifica superata: {numero} quadrati; tela {righe} righe × {colonne} colonne.')
        return
    quadrati, archi = costruisci(n)
    print('\n'.join(griglia(quadrati) if modo == '--griglia' else disegna(quadrati, archi)))


def errore_interfaccia(messaggio):
    print(f'Errore: {messaggio}', file=sys.stderr)
    print('Uso: python3 spirale_fibonacci.py N [--griglia | --verifica]',
          file=sys.stderr)
    raise SystemExit(2)


if __name__ == '__main__':
    principale()
