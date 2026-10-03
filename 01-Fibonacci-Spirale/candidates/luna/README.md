# Candidato Luna: spirale di Fibonacci

Questo candidato realizza l'interfaccia definita in `input/SPEC.md` usando
soltanto Python 3 e la libreria standard. La geometria parte dai primi due
quadrati unitari e colloca ogni quadrato seguente sul lato successivo del
rettangolo. Ogni arco e un quarto di cerchio nel proprio quadrato. Il
verificatore controlla raggi, estremi, tangenti, rotazione, tassellazione,
connessione raster e proprieta di prefisso.

## Riproduzione

```sh
python3 spirale_fibonacci.py 8
python3 spirale_fibonacci.py 8 --griglia
python3 spirale_fibonacci.py 8 --verifica
python3 -m unittest discover -s . -v
```

La risoluzione e fissa a otto punti raster per unita. La tela grafica usa
solo celle Braille e deriva da una rasterizzazione globale condivisa da
bordi e archi. La modalita `--griglia` mostra i soli bordi ASCII.

## Ambito e limiti

La verifica geometrica e computazionale, non una dimostrazione formale. Il
test dei quadrati non sovrapposti insieme all'uguaglianza delle aree verifica
la tassellazione del rettangolo. Gli archi sono campionati sul reticolo con
passo angolare limitato a un punto circa; il programma non crea immagini o
usa coordinate finali codificate a mano. L'area della tela Braille cresce
esponenzialmente con N, quindi valori molto grandi richiedono molta memoria e
tempo.

Il worker ha ricevuto la SPEC congelata e il Bead `LLM-ksk.1`. Nessun record
grezzo di transazione o campo di accounting STARCHART era presente nel
workspace; `accounting.json` documenta questa lacuna senza stimare valori.
Il bundle pubblico completo, incluse ricevute e prompt originale, resta
compito del confronto manageriale.
