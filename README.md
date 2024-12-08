# Schere, Stein, Papier

Schere, Stein, Papier ist ein beliebtes Spiel. Zwei Spieler wählen eines der Symbole (Schere, Stein oder Papier) und zeigen dieses bei Aufruf gleichzeitig an. Jedes Symbol ist einem anderen Symbol überlegen. Wählen beide dasselbe Symbol, kommt es zu einem Unentschieden. Das Spiel wird in diesem Fall wiederholt. 

 

Für jedes gewonnene Spiel erhält der Gewinner einen Punkt. Nach einer vorher festlegbaren Bedingung z.B. (Beste aus 3; Erste mit 5; Anzahl Spiele; …) gewinnt ein Spieler die Runde.
## Varianten 

### Klassische Regeln

```
Schere schneidet Papier,
Papier umwickelt Stein,
Stein schlägt Schere,
```

### Regeln mit Spock und Echse

```
Schere schneidet Papier, 
Papier umwickelt Stein, 
Stein zerquetscht Echse, 
Echse vergiftet Spock, 
Spock zertrümmert Schere, 
Schere köpft Echse, 
Echse frisst Papier, 
Papier widerlegt Spock, 
Spock verdampft Stein, 
Stein schlägt Schere
```
 

### Erweiterung der Regeln

Die Regeln können beliebig erweitert werden. Hierzu kann in `rules` (oder woanders)
eine Datei beschreiben welches Symbol/Objekt welchem überlegen ist. Beispiel dafür sind 
die beiden varianten oben.

```
python main.py --rules PATH-TO-RULES
```

## Code ausführen
Das Spiel nutzt nur die Python Standardbibliothek, daher sind keine weiteren packages nötig. Python Version >=3.12 empfohlen.
Es sind drei verschiedene Gewinnbedingungen implementiert:
Best-out-of-X (Standard mit Wert 3), Anzahl an Spielen und Anzahl an Gewinnen.

Das Spiel kann jederzeit bei Eingabeaufforderung mit dem Befehl `exit` beendet werden (außer es ist ein Symbol im Spiel), wahlweise mit `ctrl + c`.

Spiel wird gestartet mit `python main.py`.


```
usage: main.py [-h] [--extended | --rules RULES] [--bestoutof BESTOUTOF | --numgames NUMGAMES | --numberofwins NUMBEROFWINS]

Schere, Stein, Papier (& Erweiterungen)

options:
  -h, --help            show this help message and exit
  --extended            Erweiterte Regeln mit Spock und Echse.
  --rules RULES         Dateipfad für eigen erstellte Regeln.
  --bestoutof BESTOUTOF
                        Gewinnkondition: Mehrzahl der BESTOUTOF Spiele gewonnen (Standard=3).
  --numgames NUMGAMES   Das Spiel hört nach NUMGAMES Spielen auf.
  --numberofwins NUMBEROFWINS
                        Das Spiel hört nach NUMBEROFWINS Gewinnen auf.

```