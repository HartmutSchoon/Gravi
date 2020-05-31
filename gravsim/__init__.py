from . import interface
from . import physics
import numpy as np
import pandas as pd
import time


def runSimulation():
    #Hauptschleife der Simulation
    stepCounter=0
    elapsedTime=1
    #cnfg=myInterface.getCnfgCpy()
    #While-Schleife zum kontrolliertem Beenden des Programms
    while myInterface.requestExit == False:
        #While-Schleife um das Programm Pausieren zu können
        while myInterface.running == True and myInterface.requestExit == False:
            t=time.time()
            simTime=stepCounter*cnfg.dt
            #Abfragen um zu erkennen ob in diesem Durchlauf ein Frame gezeichnet werden soll.
            if stepCounter%cnfg.frameDrawingSkip == 0:
                #cnfg=myInterface.getCnfgCpy()
                myInterface.updateFrame(planets,cnfg)
                myInterface.updateTimeText(simTime)
                myInterface.updateFPSText(elapsedTime)

            #Abfragen um zu erkennen ob in diesem Durchlauf der Tracer aktualisiert werden soll.
            if stepCounter%cnfg.tracerSkip == 0:
                for planet in planets:
                    myInterface.drawTracer(planet,cnfg)

            #Abfragen um zu erkennen ob in diesem Durchlauf die Positionsdaten der Planeten
            #gespeichert werden soll.

            if stepCounter%cnfg.posSkip ==0 and stepCounter != 0:
                for planet in planets:
                    planet.storeData(cnfg)

            #Jeden Planeten seine nächste Position und Geschwindigkeit berechnen lassen
            for planet in planets:
                planet.makeStep(planets,cnfg)

            elapsedTime=time.time()-t
            stepCounter=stepCounter+1

        myInterface.updateFrame(planets,cnfg)

    #Am Ende des Programms immer nochmal alles im Buffer abspeichern.
    for planet in planets:
        planet.savePosBuffToFile()
        planet.dataFile.close()

def loadPlanets(cnfg):
    #Funktion um planeten Objekte zu Initialisieren und in die Liste "Planets" zu schreiben
    #die Werte zur erzeugung der Planeten werden aus der PlanetData Excel Datei entnommen
    planetData=pd.read_excel(cnfg.planetDataPath)
    planets=[]
    for i in range(planetData.shape[0]):
        dataRow=planetData.iloc[i]
        planet=physics.Planet(dataRow.Name,dataRow.Mass,dataRow.Radius,dataRow.PosX,dataRow.PosY,dataRow.VelX,dataRow.VelY,dataRow.Colour)
        planets.append(planet)
    return planets


class config:
    #Diese Klasse dient hauptsächlich der Strukturierung. In ihr sollen alle
    #zur Einstellung der Programms benötigten Werte gespeichert werden
    def __init__(self):
        self.gamma=self.loadValuesFromFile("gamma")
        self.dt = self.loadValuesFromFile("dt")
        self.physicWidth=self.loadValuesFromFile("physicWidth")

        self.posSkip=self.loadValuesFromFile("posSkip")
        self.posBuffMaxSize=self.loadValuesFromFile("posBuffMaxSize")

        self.cnvWidth=self.loadValuesFromFile("cnvWidth")
        self.frameDrawingSkip=self.loadValuesFromFile("frameDrawingSkip")
        self.tracerSkip=self.loadValuesFromFile("tracerSkip")
        self.tracerMaxPoints=self.loadValuesFromFile("tracerMaxPoints")

        self.planetDataPath=self.loadValuesFromFile("planetDataPath")

        #Umrechnungsfaktor um zwischen "realen" Koordinaten und Leinwand koordinaten zu wechseln
        self.transFak=self.cnvWidth/self.physicWidth

    def loadValuesFromFile(self,name):
        #Funktion zum Einlesen einer Konfigurationsdatei
        #Es wird in der "config.txt" Datei nach dem gesuchten Namen gesucht und
        #dann der dahinter stehende Wert ausgegeben
        configData=open("config.txt","r")
        for i in range(100):
            line=configData.readline()
            if (line.find("#")!=0):
                index=line.find("=")
                if index !=-1 :
                    nameInData=line[0:index]
                    if (name==nameInData and line[index+1]!="'"):
                        return float(line[index+1:])
                    elif (name==nameInData and line[index+1]=="'"):
                        return str(line[index+2:len(line)-2])

#Code wird ganz am anfang beim Import ausgführt:
cnfg=config()
planets=loadPlanets(cnfg)
myInterface=interface.Interface(planets,cnfg)
