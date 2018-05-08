from tkinter import *

k = 0.3 # trenje mize
dt = 1 # casovni interval

class CueBall():
    def __init__(self, barva, R, x, y, vx, vy, canvas):
        self.R = R

        # polozaj
        self.x0 = x
        self.y0 = y

        # polozaj za risanje crte
        self.x = x
        self.y = y

        # hitrost za risanje crte
        self.vx = vx
        self.vy = vy

        self.canvas = canvas
        self.id = self.canvas.create_oval(self.x - self.R, self.y - self.R, self.x + self.R, self.y + self.R, fill=barva)

        self.lines = []

        # belo premikamo z desnim klikom
        self.canvas.bind("<B3-Motion>", self.moveMouse)

    def moveMouse(self, event):
        (x, y) = (event.x, event.y)
        self.x = x
        self.y = y
        self.x0 = x
        self.y0 = y
        self.canvas.coords(self.id, self.x - self.R, self.y - self.R, self.x + self.R, self.y + self.R)

    def drawDt(self, direction, energy=0):
        # energy - energija, ki jo kugla sprejme. Ce smo v trenutku, ki ni prvi
        # po udarcu, je dodana energija enaka 0
        # direction - smer, v kateri se energija manifestira (normiran vektor)
        x, y = direction[0], direction[1]

        # nastavimo koordinate bele nazaj na te, kjer bela res je
        self.x, self.y = self.x0, self.y0

        print("x,y: ", x, y)

        # pobrisemo stare crte
        for line in self.lines:
            self.canvas.after(1, self.canvas.delete, line)

        if energy > 0:
            # (x, y) lezi na enotski kroznici, torej
            # x = cos(fi), y = sin(fi),
            # zato lahko energijo pretvorimo v hitrost takole:
            self.vx = energy * x
            self.vy = energy * y

        # dokler ima kugla pozitivno hitrost, podaljsujemo crto
        while self.vx != 0 or self.vy != 0:
            print("vx,vy: ", self.vx, self.vy)
            # ce ne dodamo energije, se hitrosti vx in vy zmanjsujeta zaradi trenja
            sx, sy = self.sign(self.vx), self.sign(self.vy)
            self.vx = sx*(abs(self.vx)*(1 - k * dt)) if abs(self.vx) > k * dt else 0
            self.vy = sy*(abs(self.vy)*(1 - k * dt)) if abs(self.vy) > k * dt else 0
            self.drawDtHelp()

    def drawDtHelp(self):
        print("risem")
        x0 = self.x
        y0 = self.y
        self.x = x0 + self.vx * dt
        self.y = y0 + self.vy * dt
        self.lines.append(self.canvas.create_line(x0,y0, self.x,self.y))

    def sign(self, x):
        if x < 0:
            return -1
        if x > 0:
            return 1