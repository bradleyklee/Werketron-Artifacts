# Spirale di Fibonacci terminale parametrica

## OBIETTIVO

Scrivere un programma Python 3 deterministico che, dato N >= 2, costruisca
e visualizzi nel terminale la spirale di Fibonacci ottenuta dai primi N
quadrati della successione.

Tutto il codice, i commenti e l'output devono essere in italiano.

## INTERFACCIA

```text
python3 spirale_fibonacci.py N
python3 spirale_fibonacci.py N --griglia
python3 spirale_fibonacci.py N --verifica
```

Usare soltanto la libreria standard.
Nessuna rete, casualità, generazione di immagini o libreria grafica.

## GEOMETRIA

Usare:

```text
F1 = 1
F2 = 1
Fk = F(k-1) + F(k-2)
```

Partire da due quadrati unitari adiacenti.

Per k >= 3 aggiungere un quadrato di lato Fk al rettangolo esistente,
ruotando di 90 gradi la direzione di aggiunta a ogni passo.

Dopo ogni passo, l'unione dei quadrati deve essere un rettangolo i cui lati
sono due numeri di Fibonacci consecutivi.

Ogni quadrato contribuisce un quarto di circonferenza di raggio uguale al
proprio lato.

I primi due quarti di circonferenza devono formare insieme il semicerchio
centrale della costruzione.

Ogni arco successivo deve essere scelto dalla geometria del proprio
quadrato in modo che:

- inizi esattamente dove termina l'arco precedente;
- abbia la stessa tangente nel punto di giunzione;
- mantenga un unico verso di rotazione;
- rimanga interamente nel proprio quadrato.

La spirale deve quindi derivare dai quadrati. Non calcolare una spirale
logaritmica indipendente.

## RENDERING

Usare un unico reticolo di coordinate intere per quadrati, bordi e archi.

Usare una risoluzione fissa sufficiente a rendere chiaramente leggibili
anche i quadrati di lato 1; non ridurre automaticamente la risoluzione al
crescere di N.

Rasterizzare bordi e archi sullo stesso reticolo e applicare loro una sola
trasformazione globale.

Se il rettangolo finale è più alto che largo, ruotare l'intera costruzione
di 90 gradi prima del rendering.

Non normalizzare o traslare separatamente bordi e spirale.

La tela deve coincidere con il minimo rettangolo raster necessario:
nessuna riga o colonna esterna completamente vuota.

Convertire la tela in Unicode Braille U+2800...U+28FF.

Ogni cella Braille rappresenta 2 × 4 punti raster.

Anche le celle vuote della tela devono essere U+2800.

Non mescolare ASCII, box-drawing e Braille nella tela grafica.

## --GRIGLIA

Mostrare soltanto la tassellazione dei quadrati mediante ASCII.

La griglia ASCII e il rendering Braille devono derivare dalle stesse
coordinate matematiche.

## --VERIFICA

Verificare almeno che:

- i lati siano F1...FN;
- i quadrati non si sovrappongano;
- la loro unione sia il rettangolo Fibonacci atteso;
- ogni arco abbia raggio uguale al lato del proprio quadrato;
- archi consecutivi condividano esattamente un estremo;
- le tangenti coincidano alle giunzioni;
- gli archi rasterizzati siano connessi;
- bordi e spirale usino esattamente la stessa trasformazione globale;
- tutte le righe della tela abbiano la stessa larghezza;
- non esistano righe o colonne esterne completamente vuote;
- la tela grafica contenga soltanto caratteri Braille;
- la costruzione per N+1 conservi esattamente come prefisso geometrico
  la costruzione per N.

## ACCETTAZIONE

Il programma deve funzionare per valori crescenti di N senza coordinate,
immagini o layout finali specifici codificati a mano.

Passando da N a N+1 deve essere aggiunto soltanto il successivo quadrato di
Fibonacci e il relativo quarto di circonferenza.

L'obiettivo è ricostruire algoritmicamente la famiglia completa delle
spirali di Fibonacci terminali, non riprodurre un'immagine di riferimento.

## CONFRONTO CONTROLLATO DEI MODELLI

Eseguire due tentativi indipendenti a partire dall'identica versione congelata
di questa specifica: uno con il worker Luna corrente e uno con il worker Sol
corrente. Ogni tentativo deve usare una transazione distinta e un'area di
output distinta. Un tentativo non può leggere o modificare l'implementazione
dell'altro.

Confrontare almeno:

- conformità funzionale e geometrica alla specifica;
- correttezza delle verifiche e qualità della spiegazione;
- interventi umani e cicli di REWORK;
- latenza, invocazioni e token di input, output e cache quando tali valori
  sono effettivamente registrati dal sistema;
- limiti o campi mancanti che impediscono un confronto economico attendibile.

Non stimare costi monetari senza una tabella prezzi esplicita, datata e
separata dai dati grezzi. La Quality indipendente e il manager determinano
l'accettazione; nessuno dei due tentativi è canonico per il solo fatto di
essere più economico o più veloce.

## PACCHETTO PUBBLICO CON RICEVUTE

Consegnare una directory di distribuzione autonoma e comprensibile senza
accesso al repository operativo. Deve contenere almeno:

- il prompt originale e questa specifica congelata;
- le stampe grezze complete dei Bead pertinenti;
- un'esportazione immutata delle transazioni pertinenti, inclusi stato,
  eventi, risultati worker, review, pubblicazioni e accounting disponibili;
- il prodotto finale e un verificatore riproducibile;
- note in linguaggio ordinario sul processo, sulle decisioni e sui REWORK;
- un manifesto machine-readable che colleghi prompt, SPEC, Bead, transazioni,
  modelli, commit, release, artefatti e digest SHA-256.

Separare chiaramente dati grezzi, spiegazioni e artefatti derivati. Classificare
ogni relazione dichiarata con la successione di Fibonacci come dimostrata
matematicamente, verificata computazionalmente, interpretata artisticamente o
metaforica. Il pacchetto deve permettere a un revisore, umano o AI
avversariale, di inventariare i file, ripetere i controlli e contestare ogni
affermazione senza fidarsi della narrazione del progetto.
