# Gravi
Programm zur Simulation der Planetenbewegung mittels RK4

zum starten des Programms:
-Python 3.8 installieren (https://www.python.org/downloads/)

-unter Gravi\env\pyenv.txt den home Path auf die Python installation setzen

-über Terminal Gravi\env\Scripts\activate ausführen (startet die virtuelle Umgebung zur verwarltung der Pakete)

-im Terminal im Ordner Gravi "python startSimulation.py" ausführen

Das Programm wurde als Python Modul umgesetzt. Um das Modul zu laden muss in der python Umgebung der Befehl "import gravSim" ausgeführt werden.
Um die eigentliche Simulation zu starten wird der Befehl gravSim.runSimulation() benutzt.
Alternativ kann aus eine Konsole heraus (z.B Windows cmd) der Befehl python startSimulation.py aufgerufen werden.

Es können unterschiedliche Objekte in das Programm geladen werden über die PlanetData.xlsx Datei. Standartmäßig wurde hier das Sonnensystem eingetragen.
Es ist dabei zu beachten, dass Abstände in astronomischen Einheiten und Massen in Erdmassen angegeben wurden.
Über die Config.txt Datei können allgemeine Einstellungen am Programm vorgenommen werden.
