# msg-tsp
           Author:         Marco Friedersdorf
             Mail:         marco@friedersdorf.de

     Last updated:         08.07.2020

      Description:         Dies ist mein Beitrag zur Coding-Challenge von MSG, wie man sie auf
                           https://www.get-in-it.de/coding-challenge (Stand 08.07.2020) finden kann.
                           Im Grunde beschreibt es das Traveling Salesman Problem (TSP, auch Briefträgerproblem,
                           Chinese Postman Problem, Route Inspection Problem, usw), in dem eine bestimmte Anzahl
                           an Punkten (n) auf einer Karte "besucht" werden müssen, wobei Start- und Endpunkt immer
                           fix sind. Für kleine Werte von n bietet sich eine Methode an, bei der alle möglichen
                           Routen (p) ermittelt und deren Gesamtlänge berechnet werden. Da p aber mittels Fakultät
                           berechnet wird, wird es mit jedem weiteren Faktor auch sehr schnell sehr groß. Es bietet
                           sich daher als Alternative die "Nearest Neighbor"-Methode an. Hierbei wird eine Tabelle
                           mit den Abständen aller Punkte zueinander benötigt, um damit, ausgehend vom Startpunkt,
                           immer den kürzesten Abstand zum nächsten Punkt zu wählen. Diese Methode ist natürlich
                           nicht die genauste, dafür aber bei größeren n sehr schnell.

                           Und am Ende fährt der Salesman sicher lieber ein paar km mehr, als erstmal mehrere
                           hundert Jahre auf die Ermittlung der perfekten Route zu warten.

                           Es findet eine Ausgabe der Tabelle der Punkte und deren gerundeter Abstände zueinander
                           auf dem Bildschirm statt. Außerdem wird eine Datei namens distances.csv ins
                           Arbeitsverzeichnis gelegt, die die ungerundeten Werte enthält. Diese Werte sind natürlich
                           auch die Berechnungsgrundlage.

           Notes:          Das Script sollte auf einem UNIX-System mit Python 3 problemlos laufen und mittels
                           'python tsp.py' im Verzeichnis aufrufbar sein.
                           Ich habe darauf geachtet, nur Module zu benutzen, die in Python 3 enthalten sind, damit
                           nichts nachinstalliert werden muss. Sicherlich gibt es Module, die das Problem lösen
                           können, aber das sollte wohl nicht der Anspruch sein.
                           Sollte es doch nicht auf Anhieb funktionieren, klappt es bestimmt mit dem Befehl
                           'python3.6 tsp.py'.

                           Aber ich rede hier ja mit Profis, das wird schon alles klappen.

