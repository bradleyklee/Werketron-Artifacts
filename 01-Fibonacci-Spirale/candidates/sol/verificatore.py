#!/usr/bin/env python3
"""Controlli riproducibili e indipendenti per la spirale terminale."""

import subprocess
import sys
from math import cos, pi, sin
from pathlib import Path

import spirale_fibonacci as prodotto


def richiedi(condizione, messaggio):
    if not condizione:
        raise AssertionError(messaggio)


def verifica_occupazione(quadrati):
    minimo_x = min(q.x for q in quadrati)
    minimo_y = min(q.y for q in quadrati)
    massimo_x = max(q.x + q.lato for q in quadrati)
    massimo_y = max(q.y + q.lato for q in quadrati)
    celle = {}
    for quadrato in quadrati:
        for x in range(quadrato.x, quadrato.x + quadrato.lato):
            for y in range(quadrato.y, quadrato.y + quadrato.lato):
                celle[x, y] = celle.get((x, y), 0) + 1
    atteso = {(x, y) for x in range(minimo_x, massimo_x)
              for y in range(minimo_y, massimo_y)}
    richiedi(set(celle) == atteso and all(numero == 1 for numero in celle.values()),
             'Tassellazione incompleta o sovrapposta')


def verifica_archi(quadrati, archi):
    richiedi(archi[0].centro == archi[1].centro, 'Semicerchio centrale assente')
    for indice, (quadrato, arco) in enumerate(zip(quadrati, archi)):
        richiedi(arco.raggio == quadrato.lato, 'Raggio diverso dal lato')
        for frazione in range(101):
            angolo = (arco.quadrante - frazione / 100) * pi / 2
            x = arco.centro[0] + arco.raggio * cos(angolo)
            y = arco.centro[1] + arco.raggio * sin(angolo)
            tolleranza = 1e-10
            richiedi(quadrato.x - tolleranza <= x <= quadrato.x + quadrato.lato + tolleranza and
                     quadrato.y - tolleranza <= y <= quadrato.y + quadrato.lato + tolleranza,
                     'Arco esterno al quadrato')
        if indice:
            prima = archi[indice - 1]
            comuni = {prima.inizio, prima.fine} & {arco.inizio, arco.fine}
            richiedi(prima.fine == arco.inizio and comuni == {arco.inizio},
                     'Giunzione non unica')
            richiedi((prima.quadrante - 1) % 4 == arco.quadrante,
                     'Tangente o verso non coincidente')


def verifica_raster(quadrati, archi):
    orientamento = prodotto.trasformazione(quadrati)
    bordi = prodotto.punti_bordi(quadrati, orientamento)
    percorsi = prodotto.punti_spirale(archi, orientamento)
    punti = bordi | set().union(*(set(percorso) for percorso in percorsi))
    massimo_x = orientamento.larghezza * prodotto.RISOLUZIONE
    massimo_y = orientamento.altezza * prodotto.RISOLUZIONE
    richiedi(all(0 <= x <= massimo_x and 0 <= y <= massimo_y for x, y in punti),
             'Raster fuori dal rettangolo')
    for indice, percorso in enumerate(percorsi):
        richiedi(all(max(abs(x - xx), abs(y - yy)) <= 1
                     for (x, y), (xx, yy) in zip(percorso, percorso[1:])),
                 'Arco raster disconnesso')
        if indice:
            richiedi(percorsi[indice - 1][-1] == percorso[0],
                     'Giunzione raster disconnessa')
    righe = prodotto.tela_braille(punti, orientamento)
    richiedi(len({len(riga) for riga in righe}) == 1, 'Larghezze diseguali')
    richiedi(all(0x2800 <= ord(c) <= 0x28ff for r in righe for c in r),
             'Tela non esclusivamente Braille')
    richiedi(all(any(c != '\u2800' for c in riga) for riga in (righe[0], righe[-1])) and
             all(any(riga[indice] != '\u2800' for riga in righe) for indice in (0, -1)),
             'Margine esterno vuoto')
    richiedi(all(len(riga) == 2 * orientamento.larghezza + 1
                 for riga in prodotto.griglia(quadrati)), 'Griglia incoerente')
    richiedi(all(carattere in '+-| ' for riga in prodotto.griglia(quadrati)
                 for carattere in riga), 'Griglia non ASCII')
    return len(righe), len(righe[0])


def verifica_interfaccia():
    programma = Path(__file__).with_name('spirale_fibonacci.py')
    for n in (2, 5):
        for opzione in ('', '--griglia', '--verifica'):
            argomenti = [sys.executable, str(programma), str(n)]
            if opzione:
                argomenti.append(opzione)
            esito = subprocess.run(argomenti, capture_output=True, text=True, check=True)
            richiedi(bool(esito.stdout.strip()) and not esito.stderr,
                     'Interfaccia senza risultato valido')
    for argomenti in (('1',), ('due',), ('2', '--griglia', '--verifica')):
        esito = subprocess.run([sys.executable, str(programma), *argomenti],
                               capture_output=True, text=True)
        richiedi(esito.returncode != 0, 'Argomento invalido accettato')


def principale():
    for n in range(2, 12):
        quadrati, archi = prodotto.costruisci(n)
        verifica_occupazione(quadrati)
        verifica_archi(quadrati, archi)
        righe, colonne = verifica_raster(quadrati, archi)
        richiedi(prodotto.verifica(n) == (n, righe, colonne),
                 'Verifica integrata incoerente')
        quadrati_seguenti, archi_seguenti = prodotto.costruisci(n + 1)
        richiedi(quadrati_seguenti[:n] == quadrati and archi_seguenti[:n] == archi,
                 'Prefisso non stabile')
        print(f'N={n}: occupazione, archi, raster e prefisso verificati; '
              f'tela {righe} × {colonne}.')
    verifica_interfaccia()
    print('Interfaccia e casi invalidi verificati.')


if __name__ == '__main__':
    principale()
