from tkinter import *

D = 20 # odmik od bele
d = 8 # dolžina palice

class Cue():
    # x0 in y0 predstavljata koordinati bele
    def __init__(self, x0, y0, canvas):
        self.x0 = x0
        self.y0 = y0

        # potrebujemo za smerni vektor udarca
        self.x = 100
        self.y = 100

        # normiramo šele, ko je poklicana funkcija hit
        self.direction = (self.x0 - self.x, self.y0 - self.y)

        self.canvas = canvas

        # narišemo palico
        self.id = canvas.create_line(x0+D,y0+D, x0+2*D,y0+2*D, width=3)

        self.canvas.bind("<B1-Motion>", self.move)
        self.canvas.bind("<ButtonRelease-3>", self.move2)

    def move(self, event):
        (x, y) = (event.x, event.y)
        # N = D/norma
        N = D/((x - self.x0) ** 2 + (y - self.y0) ** 2) ** 0.5
        if N <= 1:
            x_0 = self.x0
            y_0 = self.y0
            x0, y0 = x_0 + N * (x-x_0), y_0 + N * (y-y_0)
            x, y = x_0 + d*N * (x - x_0), y_0 + d*N * (y - y_0)
            self.x, self.y = x, y
            self.canvas.coords(self.id, x0,y0, x,y)
            self.direction = (self.x0 - self.x, self.y0 - self.y)

    def move2(self, event):
        (x0, y0) = (event.x, event.y)
        self.x0 = x0
        self.y0 = y0
        self.canvas.coords(self.id, x0+D,y0+D, x0+2*d,y0+2*d)
        self.direction = (self.x0 - self.x, self.y0 - self.y)

    def hit(self, strength):
        N = D / ((self.x - self.x0) ** 2 + (self.y - self.y0) ** 2) ** 0.5
        print(strength, N)
