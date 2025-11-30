#!/bin/bash

# CSV neu starten
echo "Distance,Etotal" > Distance.csv

for i in $(seq 0.10 0.1 2.00); do
    # Kopie der Template-Datei erstellen
    cp hydrogen_molecule_template.in hydrogen_molecule.in

    # DIST durch aktuellen Abstand ersetzen
    sed -i "s/DIST/$i/" hydrogen_molecule.in

    # SCF Rechnung starten
    pw.x < hydrogen_molecule.in > hydrogen_molecule.out

    # Energie aus output.xml extrahieren
    E=$(grep '!    total energy' hydrogen_molecule.out | awk '{print $5}')

    # In CSV schreiben
    echo "$i,$E" >> Distance.csv

    # Fortschritt ausgeben
    echo "Abstand $i Å -> Energie $E Ry"
done
