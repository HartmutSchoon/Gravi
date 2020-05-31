import numpy as np
import mpmath as mp

class Planet:
    #In dieser Klasse sollen Planeten definiert werden. Hauptsächlich wird hier die
    #momentane Position und geschwindigkeit, sowie die Masse des Planetens und sein Name
    #abgespeichert. In der Planeten Klasse ist ebenfalls der Runge-Kutta Algoritmus
    #implementiert. Idee war: die Planeten sehen ihre Umgebung und verändern sich selbst
    #nach den physikalischen vorgaben
    def __init__(self,name,mass,radius,posX,posY,velX,velY,colour):
        self.name=name
        self.mass=mass
        self.radius=radius
        self.colour=colour
        self.pos=np.array([posX,posY])
        self.posBuffer=self.pos
        self.posBuffer=self.posBuffer[:,np.newaxis]
        self.vel=np.array([velX,velY])

        #Speicherort für grafische Zwecke
        self.cnvOvalID=[]
        self.cnvTextID=[]
        self.tracerID=[]
        self.tracerBuffer=[]

        #Speicherpfad zur Exportierung der Daten
        self.dataFile = open(".\Data\ "+self.name+".txt","w+")

        #mp.dps=100
    def nextPos(self,cnfg):
        #funktion um nächste Position zu erhalten bei jetziger Position und jetziger Geschwindigkeit
        newPosX=self.pos[0]+self.vel[0]*cnfg.dt
        newPosY=self.pos[1]+self.vel[1]*cnfg.dt
        return np.array([newPosX,newPosY])

    def calcDeltaPos(self,planet,cnfg,v):
        #Funktion um Abstand in X und Y Dimension zu erhalten bei variabler! Geschwindigkeit
        #dazu gilt dx=x_andererPlanet-x_dieserPlanet
        # => dx=x_andererPlanet-(x_dieserPlanetimNächstenSchritt-v*dt)
        newPos=self.nextPos(cnfg)
        dX=planet.pos[0]-newPos[0]+v[0]*cnfg.dt
        dY=planet.pos[1]-newPos[1]+v[1]*cnfg.dt
        return np.array([dX,dY])

    def getAcceleration(self,planet,cnfg,v):
        #Funktion um die Beschleunigung des Planetens zu errechnen, welche anderer Planet auf diesen auswirkt
        #Muss abhängig von v sein für RK4
        deltaPos=self.calcDeltaPos(planet,cnfg,v)
        r=mp.sqrt(deltaPos[0]*deltaPos[0]+deltaPos[1]*deltaPos[1])
        acceleration=cnfg.gamma*planet.mass/(r*r) #Gesamtbeschleunigung
        aX=acceleration*deltaPos[0]/r #Beschleunigung in X-Richtung
        aY=acceleration*deltaPos[1]/r #Beschleunigung in Y-Richtung
        return np.array([aX,aY])

    def sumAcceleration(self,planets,cnfg,v):
        #Funktion getAcceleration betrachtet nur einen Planet. Diese Funktion addiert alle
        #durch andere Planeten erzeugte Beschleunigungen auf.
        acc=np.array([0,0])
        for planet in planets:
            if(self.name != planet.name):
                acc=acc+self.getAcceleration(planet,cnfg,v)
        return acc

    def rk4_Main(self,planets,cnfg):
        #RK4-Algorithmus zur Berechnung der Geschwindigkeit des Planeten in nächstem Zeitschritt
        velNow=self.vel
        k1=self.sumAcceleration(planets,cnfg,velNow)
        k2=self.sumAcceleration(planets,cnfg,velNow+cnfg.dt/2*k1)
        k3=self.sumAcceleration(planets,cnfg,velNow+cnfg.dt/2*k2)
        k4=self.sumAcceleration(planets,cnfg,velNow+cnfg.dt*k3)
        nextVel=velNow+cnfg.dt*1/6*(k1+2*k2+2*k3+k4)
        return nextVel

    def makeStep(self,planets,cnfg):
        #Hauptfunktion um einen neuen Schritt zu machen. Die nächste Position wird
        #durch Euler Verfahren anhand der jetzigen Position und Geschwindigkeit ermittelt.
        #Die nächste Geschwindigkeit wird mit dem RK-4 verfahren ermittelt.

        newPos=self.nextPos(cnfg)
        newVel=self.rk4_Main(planets,cnfg)
        self.pos=newPos
        self.vel=newVel

    def storeData(self,cnfg):
        #Funktion welche Positionsdaten in einen Buffer schiebt und das Exportieren
        #der Datein bei vollem Buffer einleited
        if (self.posBuffer.shape[1]<cnfg.posBuffMaxSize):
            self.posBuffer=np.append(self.posBuffer,self.pos[:,np.newaxis],axis=1)
        else:
            self.savePosBuffToFile()

    def savePosBuffToFile(self):
        #Exportierung der Datein im Buffer in Text Datei
        np.savetxt(self.dataFile,np.transpose(self.posBuffer))
        self.posBuffer=self.pos[:,np.newaxis]
