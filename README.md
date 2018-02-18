# powerDogReader

usage:

RRD Files generieren an hand der Liste allStrings und allGraphValues

**solarGraph.py --create**

Daten vom FTP Verzeichnis in die RRD abfüllen (z.B. alle 10 Minuten mit einem while loop im Script)

**solarGraph.py --update**

Grafiken Rendern (immer nach dem abfüllen der Daten im selben Script server.sh)

**solarGraph.py --render**

Webseite

index.php lädt die Bilder alle 30 Sekunden

**get.py** (deprecated, holt den neuesten Wert aus dem FTP Verzeichnis)

**python get.py --path /home/toni --file B2_A2_S2 --value pac**


Erste Resultate:
![First Results](https://raw.githubusercontent.com/braindef/powerDogReader/master/firstResults.png "First Results")
