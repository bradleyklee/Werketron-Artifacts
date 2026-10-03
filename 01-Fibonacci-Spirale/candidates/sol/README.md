# Candidato Sol: spirale di Fibonacci nel terminale

Questa directory contiene il candidato indipendente per il Bead `LLM-ksk.2`,
transazione `factory-8a2929aec03d3072fa2ec88957bd58e5`. Il programma usa
soltanto la libreria standard di Python 3. La specifica congelata e il piano
sono copiati byte per byte come `SPEC.md` e `PLAN.json`; `bead.txt` conserva
la stampa del Bead disponibile al worker.

## Uso

```sh
python3 spirale_fibonacci.py 8
python3 spirale_fibonacci.py 8 --griglia
python3 spirale_fibonacci.py 8 --verifica
python3 verificatore.py
```

L'uscita predefinita è esclusivamente una tela Braille. `--griglia` produce
esclusivamente la tassellazione ASCII. `--verifica` controlla le proprietà
geometriche e di rendering e restituisce un messaggio in italiano. Il
verificatore separato controlla i casi da N=2 a N=11, gli argomenti della
riga di comando, l'occupazione unitaria del rettangolo, il contenimento degli
archi, la connessione raster e la conservazione del prefisso.

## Costruzione

I primi due quadrati sono adiacenti. I loro due archi hanno centro comune
`(1, 0)` e formano il semicerchio centrale. I quadrati seguenti vengono
aggiunti ciclicamente in basso, a sinistra, in alto e a destra. Per ogni
nuovo quadrato, il programma sceglie il centro tra i suoi vertici che rende
l'arco interno, continuo e tangente al precedente nello stesso verso. Tutti
i vertici e i raggi derivano da lati Fibonacci calcolati per ricorrenza.

La tassellazione rettangolare, la continuità e le tangenti sono proprietà
matematiche della costruzione: i due quadrati iniziali formano un rettangolo
`2 × 1`; a ogni passo il nuovo quadrato ha lato uguale al lato lungo del
rettangolo precedente, quindi il lato nuovo è la somma dei due precedenti,
`F(k+1) = F(k) + F(k-1)`. L'aggiunta esterna esclude sovrapposizioni.
I vettori radiali dei due archi alla giunzione coincidono in direzione
tangente secondo la stessa rotazione oraria di 90°, scelta fra i vertici del
nuovo quadrato. Il verificatore controlla computazionalmente queste proprietà
per i casi indicati. La resa Braille è una visualizzazione
raster approssimata degli archi circolari: i loro estremi e la connettività
sono conservati sulla griglia intera. La scelta estetica dei caratteri e
della risoluzione è una rappresentazione artistica, non una nuova relazione
matematica con la successione.

Una sola trasformazione globale sposta e, quando necessario, ruota di 90°
l'intera costruzione. Bordi e archi vengono rasterizzati con risoluzione
fissa di otto punti per unità geometrica. Il terminale deve supportare
Unicode Braille. La risoluzione non si riduce per N grandi; di conseguenza
l'uso di memoria e la dimensione dell'uscita crescono con l'area dei
rettangoli Fibonacci.

## Provenienza e limiti

La copia di `SPEC.md` ha SHA-256
`835f3957b162138ba88ccb1d8376de785958dd220c9941af15ad985fa23c3e6b`.
La copia di `PLAN.json` ha SHA-256
`e8a44c24797b0e80ae81a34b6325c1c222a14f85b175f7a66ec2c6f788aee59a`.
`inventory.json` contiene i digest dei file del candidato. Il worker non ha
ricevuto campi di accounting della transazione durante questa esecuzione;
il dispatcher e il manager devono preservare i dati grezzi effettivamente
registrati da STARCHART. Qui non sono stimati token, latenza o costi monetari.
Questo è un candidato da sottoporre a Quality e confronto, non un prodotto
canonico accettato.
