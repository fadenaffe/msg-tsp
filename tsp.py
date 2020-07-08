#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#############################################################################################################
#
#           Author:         Marco Friedersdorf
#             Mail:         marco@friedersdorf.de
#
#     Last updated:         08.07.2020
#
#      Description:         Dies ist mein Beitrag zur Coding-Challenge von MSG, wie man sie auf
#                           https://www.get-in-it.de/coding-challenge (Stand 08.07.2020) finden kann.
#                           Im Grunde beschreibt es das Traveling Salesman Problem (TSP, auch Briefträgerproblem,
#                           Chinese Postman Problem, Route Inspection Problem, usw), in dem eine bestimmte Anzahl
#                           an Punkten (n) auf einer Karte "besucht" werden müssen, wobei Start- und Endpunkt immer
#                           fix sind. Für kleine Werte von n bietet sich eine Methode an, bei der alle möglichen
#                           Routen (p) ermittelt und deren Gesamtlänge berechnet werden. Da p aber mittels Fakultät
#                           berechnet wird, wird es mit jedem weiteren Faktor auch sehr schnell sehr groß. Es bietet
#                           sich daher als Alternative die "Nearest Neighbor"-Methode an. Hierbei wird eine Tabelle
#                           mit den Abständen aller Punkte zueinander benötigt, um damit, ausgehend vom Startpunkt,
#                           immer den kürzesten Abstand zum nächsten Punkt zu wählen. Diese Methode ist natürlich
#                           nicht die genauste, dafür aber bei größeren n sehr schnell.
#
#                           Und am Ende fährt der Salesman sicher lieber ein paar km mehr, als erstmal mehrere
#                           hundert Jahre auf die Ermittlung der perfekten Route zu warten.
#
#                           Es findet eine Ausgabe der Tabelle der Punkte und deren gerundeter Abstände zueinander
#                           auf dem Bildschirm statt. Außerdem wird eine Datei namens distances.csv ins
#                           Arbeitsverzeichnis gelegt, die die ungerundeten Werte enthält. Diese Werte sind natürlich
#                           auch die Berechnungsgrundlage.
#
#           Notes:          Das Script sollte auf einem UNIX-System mit Python 3 problemlos laufen und mittels
#                           'python tsp.py' im Verzeichnis aufrufbar sein.
#                           Ich habe darauf geachtet, nur Module zu benutzen, die in Python 3 enthalten sind, damit
#                           nichts nachinstalliert werden muss. Sicherlich gibt es Module, die das Problem lösen
#                           können, aber das sollte wohl nicht der Anspruch sein.
#                           Sollte es doch nicht auf Anhieb funktionieren, klappt es bestimmt mit dem Befehl
#                           'python3.6 tsp.py'.
#
#                           Aber ich rede hier ja mit Profis, das wird schon alles klappen.
#
#############################################################################################################


from math import sin, cos, sqrt, atan2, radians
import csv
import itertools
import time


def getdistance(pointa, pointb):
    R = 6371.0 ## Ungefährer Radius der Erde

    #Entfernungen zwsichen den Punkten berechnen
    dlon = radians(pointa["coords"][0]) - radians(pointb["coords"][0])
    dlat = radians(pointa["coords"][1]) - radians(pointb["coords"][1])

    # Entfernungen auf einem Sphaeroiden (Erde) berechnen nach Haversine
    a = sin(dlat / 2)**2 + cos(radians(pointa["coords"][1])) * cos(radians(pointb["coords"][1])) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

def printTableCell(maxlen, entry):
    ## Diese Methode reserviert eigentlich nur Platz für die Tabellenzellen der Bildschirmausgabe, damit alles gleichmäßig aussieht
    spacescount = maxlen - len(entry)
    newstring = ''
    for sp in range(0, spacescount):
        newstring = newstring + " "
    newstring = newstring + entry
    return newstring

## Hier sind die Standorte
arrpoints = {
    1: {"standort": "Ismaning/München (Hauptsitz)", "coords" : (48.229035, 11.686153)},
    2: {"standort": "Berlin", "coords" : (52.580911, 13.293884)},
    3: {"standort": "Braunschweig", "coords" : (52.278748, 10.524797)},
    4: {"standort": "Bretten", "coords" : (49.032767, 8.698372)},
    5: {"standort": "Chemnitz", "coords" : (50.829383, 12.914737)},
    6: {"standort": "Düsseldorf", "coords" : (51.274774, 6.794912)},
    7: {"standort": "Essen", "coords" : (51.450577, 7.008871)},
    8: {"standort": "Frankfurt", "coords" : (50.136479, 8.570963)},
    9: {"standort": "Görlitz", "coords" : (51.145511, 14.970028)},
    10: {"standort": "Hamburg", "coords" : (53.557577, 9.986065)},
    11: {"standort": "Hannover", "coords" : (52.337987, 9.769706)},
    12: {"standort": "Ingolstadt", "coords" : (48.784417, 11.399106)},
    13: {"standort": "Köln/Hürth", "coords" : (50.886726, 6.913119)},
    14: {"standort": "Lingen (Ems)", "coords" : (52.519154, 7.322185)},
    15: {"standort": "Münster", "coords" : (51.969304, 7.61428)},
    16: {"standort": "Nürnberg", "coords" : (49.429596, 11.017404)},
    17: {"standort": "Passau", "coords" : (48.571989, 13.453256)},
    18: {"standort": "Schortens/Wilhelmshaven", "coords" : (53.537779, 7.936809)},
    19: {"standort": "St. Georgen", "coords" : (48.126258, 8.325873)},
    20: {"standort": "Stuttgart", "coords" : (48.694648, 9.161239)},
    21: {"standort": "Walldorf", "coords" : (49.295011, 8.649036)}

}
#############################################################################################################
##
## 1. Entfernungen zwischen allen Standorten ermitteln und ausgeben
##
#############################################################################################################

lenSpalte = 8 ## Gibt an, wie breit eine Spalte für die Bildschirmausgabe maximal sein darf


## Es wird ein Array distanceArr Arr gebildet mit dem Startort als key
## Jeder Key hat einen Tupel aus [Ziel] = [Entfernung] als Wert
## distanceArr = {Start1: {Ziel1 : Entfernung, Ziel2: Entferung, usw}, Start2: {Ziel1 : Entfernung, Ziel2: Entferung, usw}}
distanceArr = {}
for ids, start in enumerate(arrpoints):
    distanceArr[start] = {}
    for dest in arrpoints:
        distanceArr[start][dest] = getdistance(arrpoints[start], arrpoints[dest])


## Bildschirmausgabe der Entfernungen als Tabelle
## Zuerst aber den Kopf
print("        ", end="|")
for iid, i in enumerate(distanceArr.keys()):
    print(printTableCell(lenSpalte, str(i)), end = "|")
    if(iid == len(distanceArr.keys()) - 1):
        print(end="\n")

## Nun den Tabelleninhalt
for ids, start in enumerate(distanceArr):
    print(printTableCell(lenSpalte, str(start)), end="|")
    for dest in distanceArr[start]:
        print(printTableCell(lenSpalte, str(round(distanceArr[start][dest], 2))), end = "|")
    print(end="\n")


## Nun die Entfernung in eine csv schreiben
with open('distances.csv', 'w', newline='') as file:
    writer = csv.writer(file, distanceArr.keys())
    ## Ab hier wird der Tabellenkopf in die CSV geschrieben
    row = [""] ## Erste Spalte muss natürlich leer sein
    for standort in distanceArr.keys():
        row.append(arrpoints[standort]["standort"]) ## Ich übersetze die Nummern in die Namen der Standorte anhand des ursprünglichen Arrays
    writer.writerow(row)


    ## Ab hier schreibe ich den Tabelleninhalt in die CSV, ganz ähnlich wie bei der Ausgabe, nur mit Übersetzung der Nummern in die Namen der Standorte
    for ids, start in enumerate(distanceArr):
        row = [] ## Erstmal leeren
        row.append(arrpoints[start]["standort"]) ## Hier wird die erste Spalte befüllt
        ## Ab hier werden die Entfernungen eingefügt
        for dest in distanceArr[start]:
            row.append(distanceArr[start][dest])
        writer.writerow(row)



## Noch ein paar hilfreiche Ausgaben
print()
print("rounded values in km - for precise values see file distances.csv")
print()
print("legend: ")

for standort in arrpoints:
    print(standort, "-", arrpoints[standort]["standort"])
print()

#############################################################################################################
##
## 2. Ermittlung der kürzesten Route mit allen Standorten
##
#############################################################################################################

##Den Startpunkt kurz zwischenspeichern
startpoint = arrpoints[1]

## Erstmal alle möglichen Routen ermitteln, dazu aber den Hauptsitz erstmal entfernen
del arrpoints[1]


## Hier wird die Anzahl aller möglichen Routen berechnet
sum = 1
for x in range(len(arrpoints)):
    sum = (x+1) * sum

print("There are", sum, "possible routes with", startpoint["standort"], "as start and end and I computed", end=" ")


## Ab hier werden die Entfernungen aller möglichen Routen berechnet und verglichen, um das TSP zu lösen
shortestdistance = 0
counter = 0
nearest_neighbor = False
starttime = time.time()
for permut in itertools.permutations(arrpoints, len(arrpoints)):
    counter = counter + 1

    ## der Ganze If-Block schaut nach, wie lange die ersten 100000 Routen berechnet wurden und stellt eine Prognose auf
    ## wie lange die Berechnung des Rests dauern würde. Dauert es länger als eine halbe Stunde, wird abgebrochen und die
    ## Nearest Neighbor Methode gewählt. Das ist meist der Fall bei ca. mehr als 12 Standorten (auf dem Entwicklungssystem)
    if counter == 100000:
        endttime = time.time()
        prognose = endttime - starttime
        print (counter, "of them in about", round(prognose, 4), "milliseconds.")
        print("Computing all would therefore take about", round(sum/counter * prognose / (1000 * 60 * 60 * 24 * 7 * 52), 2), "years.")
        if sum/counter * prognose > 1800000:
            print("Since the computing time is longer than 30 mins, I'm switching to the \"nearest neighbor\"-method.")
            nearest_neighbor = True
            break
        else:
            print("Since it's less then 30 minutes I keep computing.")
    start = 1
    temp_distance = 0

    ## Hier werden die Entfernungen aufaddiert
    for dest in permut:
        temp_distance = temp_distance + distanceArr[start][dest]
        start = dest
    temp_distance = temp_distance + distanceArr[start][1]
    ## Und falls die ermittelte Entfernung kleiner ist, als die vorherige (oder falls diev vorherige 0 ist)
    ## Ist das unsere neuste kürzste Distanz
    if temp_distance < shortestdistance or shortestdistance == 0:
        shortestdistance =  temp_distance
        route = permut


if nearest_neighbor == True:
    ## Die "Nearest Neighbor"-Methode ermittelt aus der Tabelle mit den Distanzen ausgehend vom Sartpunkt aus immer die kürzste Distanz.
    ## Es ist nicht perfekt, aber sehr brauchbar
    print() ## Leerzeile schadet nie
    start = 1
    route = [1]
    shortestdistance = 0

    for d in range(len(arrpoints)):
        temp_distance = 0
        temp_dest = 0
        for dest in distanceArr[start]:
            if (temp_distance == 0 or distanceArr[start][dest] < temp_distance) and dest not in route:
                temp_distance = distanceArr[start][dest]
                temp_dest = dest

        shortestdistance = shortestdistance + temp_distance
        start = temp_dest
        route.append(temp_dest)

    ## Und zurück nach Hause
    shortestdistance = shortestdistance + distanceArr[start][1]
    route.append(1)



print("Shortest distance is", shortestdistance, "km via: ")

count = 0
## Hier kommt die Ausgabe mit Übersetzung der Nummern in die Namen der Standorte
## der erste if-elif-else-Block hübscht das alles ein bisschen auf
for point in route:
    count = count + 1
    if count % 5 == 0:
        endstring = "  ---->  \n"
    elif count == len(route):
        endstring = "\n"
    else: endstring = "  ---->  "

    if point == 1:
        print(startpoint["standort"], end = endstring)
    else:
        print(arrpoints[point]["standort"], end = endstring)
print()
