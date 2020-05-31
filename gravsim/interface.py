import tkinter as tk
import mpmath as mp

class Interface:
    #Diese Klasse dient dem erstellen eines Programmfensters und der grafischen
    #anzeige der Positionen der Planeten
    def __init__(self,planets,cnfg):
        #Kopie der Konfigurationklasse
        #self.cnfgCpy=cnfg
        #Hauptfenster
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.requestExit)

        #Leinwand
        self.cnvFrame=tk.Frame(self.root)
        self.canvas = tk.Canvas(self.cnvFrame,bg="white", width=cnfg.cnvWidth,height=cnfg.cnvWidth)
        self.cnvFrame.pack()
        self.canvas.pack()

        #Textbox zur Zeitangabe
        self.textTimeID=self.canvas.create_text((10,10),anchor="nw")
        self.textFPSID=self.canvas.create_text((cnfg.cnvWidth-10,10),anchor="ne")

        #Hilfsachsen
        self.drawAxis(cnfg)
        self.drawPlanets(planets,cnfg)

        #Knöpfe
        self.buttonFrame=tk.Frame(self.root)
        self.runButton=tk.Button(self.buttonFrame,text="Run",command=self.switchRunning)
        #self.zoomInButton=tk.Button(self.buttonFrame,text="Zoom In",command=self.zoomIn)
        #self.zoomOutButton=tk.Button(self.buttonFrame,text="Zoom Out",command=self.zoomOut)
        self.exitButton=tk.Button(self.buttonFrame,text="Exit",command=self.requestExit)

        self.buttonFrame.pack()
        self.runButton.pack(side="left")
        #self.zoomInButton.pack(side="left")
        #self.zoomOutButton.pack(side="left")
        self.exitButton.pack(side="left")

        #Variablen zum anhalten oder beenden des Programms
        self.running=False
        self.requestExit=False

        self.root.update()

    #def setCnfgCpy(self,cnfg):
        #self.cnfgCpy=cnfg

    #def getCnfgCpy(self):
        #return self.cnfgCpy

    #def zoomIn(self):
    #self.cnfgCpy.physicWidth=self.cnfgCpy.physicWidth-0.1*self.cnfgCpy.physicWidth
    #    self.cnfgCpy.transFak=self.cnfgCpy.cnvWidth/self.cnfgCpy.physicWidth

    #def zoomOut(self):
        #self.cnfgCpy.physicWidth=self.cnfgCpy.physicWidth-0.1*self.cnfgCpy.physicWidth
        #self.cnfgCpy.transFak=self.cnfgCpy.cnvWidth/self.cnfgCpy.physicWidth

    def requestExit(self):
        #Funktion um Beenden Variable zu setzen
        self.requestExit=True

    def switchRunning(self):
        #Funktion um zwischen pausiertem und laufendem Programm zu Wechseln
        if self.running==True:
            self.running=False
            self.runButton.configure(text="Run")
            self.root.update()
        elif self.running==False:
            self.running=True
            self.runButton.configure(text="Pause")
            self.root.update()

    def transformLength(self,cnfg,length):
        #Funktion um Längen von physikalischen zu Leinwandkoordinaten zu tranformieren
        return length*cnfg.transFak

    def transformPosition(self,cnfg,pos):
        #Funktion um physikalische Positionen in Leinwandkoordinaten zu transformieren
        #Das Koordinatensystem der Leinwand startet in dessen oberen linken Ecke.
        #Die X-Achse verläuft dann von links nach rechts und die Y-Achse von oben nach unten.
        #Der Ursprung des physikalische Koordinatensystem liegt im Zentrum der Leinwand.
        #Dessen X Achse läuft von links nach rechts und dessen Y-Achse von unten nach oben.
        b=cnfg.cnvWidth/2
        b=cnfg.cnvWidth/2
        pixPosX=int(round(cnfg.transFak*pos[0]+b))
        pixPosY=int(round(-cnfg.transFak*pos[1]+b))
        return (pixPosX,pixPosY)

    def transformToBoxCoords(self,planet,cnfg):
        #Funktion um aus physikalischen Positionsdaten Box-Koordinaten im Leinwandkoordinatensystem
        #zu erzeugen. Positionen von Objekten(hier die Ovale) auf der Leinwand werden dabei durch ein
        #einhüllendes Rechteck angegeben
        pixPos=self.transformPosition(cnfg,planet.pos)
        pixRadius=self.transformLength(cnfg,planet.radius)

        x0=pixPos[0]-pixRadius
        y0=pixPos[1]-pixRadius
        x1=pixPos[0]+pixRadius
        y1=pixPos[1]+pixRadius

        return (x0,y0,x1,y1)


    def drawAxis(self,cnfg):
        #Zeichnet zwei Hilflinien zur verdeutlichung des physikalischen Koordinatensystems.
        self.canvas.create_line(0,cnfg.cnvWidth/2,cnfg.cnvWidth,cnfg.cnvWidth/2)
        self.canvas.create_line(cnfg.cnvWidth/2,0,cnfg.cnvWidth/2,cnfg.cnvWidth)

    def drawTracer(self,planet,cnfg):
        #Funktion um Bahnspuren zu zeichnen
        if len(planet.tracerBuffer)<cnfg.tracerMaxPoints:
            planet.tracerBuffer.append(self.transformPosition(cnfg,(planet.pos[0],planet.pos[1])))
            if(len(planet.tracerBuffer)>1):
                self.canvas.delete(planet.tracerID)
                planet.tracerID=self.canvas.create_line(planet.tracerBuffer)
        else:
            planet.tracerBuffer=planet.tracerBuffer[1:]
            planet.tracerBuffer.append(self.transformPosition(cnfg,(planet.pos[0],planet.pos[1])))
            if(len(planet.tracerBuffer)>1):
                self.canvas.delete(planet.tracerID)
                planet.tracerID=self.canvas.create_line(planet.tracerBuffer)


    def drawPlanets(self,planets,cnfg):
        #Funktion um Kreise(Planeten) auf Leinwand zu zeichnen. Wird nur bei initialisierung aufgerufen.
        #Danach werden Kreise nicht neu erzeugt sondern nur noch bewegt
        for planet in planets:
            boxCoords=self.transformToBoxCoords(planet,cnfg)
            planet.cnvOvalID=self.canvas.create_oval(boxCoords[0],boxCoords[1],boxCoords[2],boxCoords[3],fill=planet.colour)
            planet.cnvTextID=self.canvas.create_text(boxCoords[2],boxCoords[3],text=planet.name,anchor="nw")

    def updateFrame(self,planets,cnfg):
        #Funktion um Alle Planeten neu einzuzeichnen
        for planet in planets:
            currentCoords=self.canvas.coords(planet.cnvOvalID)
            planetBoxCoords = self.transformToBoxCoords(planet,cnfg)
            dx=planetBoxCoords[0]-currentCoords[0]
            dy=planetBoxCoords[1]-currentCoords[1]
            pixRadius=self.transformLength(cnfg,planet.radius)

            self.canvas.move(planet.cnvOvalID,dx,dy)
            self.canvas.move(planet.cnvTextID,dx,dy)
            self.canvas.update()


    def updateTimeText(self,simTime):
        simTimeYears=simTime/(365*24*60*60)
        self.canvas.itemconfig(self.textTimeID,text=["{:.2f}".format(simTimeYears)+"y"])

    def updateFPSText(self,elapsedTime):
        fps=1/elapsedTime
        self.canvas.itemconfig(self.textFPSID,text=["{:.2f}".format(fps)+"FPS"])
