from tkinter import *
import Ball as ball
import Cue as cue

W = 353
H = 480
D = 30 # širina roba

class Table():
    # cueX in cueY sta začetni koordinati bele
    def __init__(self, cueX, cueY, master):
        self.master = master

        self.lines = []

        # frame za mizo
        self.frame = Frame(self.master, width=W, height=H)
        self.frame.grid(row=0, column=0, rowspan=2)

        # frame za gumbe
        self.frameButtons = Frame(self.master, width=100, height=H)
        self.frameButtons.grid(row=0, column=1, rowspan=3)

        # miza z okvirjem vred
        self.cloth = Canvas(self.frame, bd=0, bg='brown', width=W, height=H)
        self.cloth.grid(row=0, column=0, rowspan=3)
        #self.cloth.create_polygon(D,D,W-D,D,W-D,H-D,D,H-D, fill='blue')


        # razred Table vsebuje objekte tipa Ball in Cue, ne pa njihovih podatkov
        self.cueBall = ball.Ball('white', cueX, cueY, self.cloth)
        self.cue = cue.Cue(cueX, cueY, self.cloth)

        self.line = self.cloth.create_line(0,0,0,0)

        self.strength = Scale(self.frameButtons, from_=0.1, to=100, length=200)
        self.strength.set(8)
        self.strength.grid(row=0, column=0)

        drawButton = Button(self.frameButtons, text="Draw!", command=lambda: self.draw_line())
        drawButton.grid(row=1, column=0)

        hitButton = Button(self.frameButtons, text="Hit!", command=lambda: self.cue.hit(self.strength.get()))
        hitButton.grid(row=2, column=0)

    def draw_line(self):
        (x, y) = self.cue.direction
        (x0, y0) = (self.cue.x0, self.cue.y0)

        # normiramo in razširimi smerni vektor glede na moč udarca
        N = 10 * self.strength.get() / (x**2 + y**2)**0.5
        x, y = N*x, N*y

        # pobrišemo vse črte
        for line in self.lines:
            self.cloth.after(5, self.cloth.delete, line)

        # možne točke odboja
        print(x,y,x0,y0)
        A = (x0 - y0 * x / y, 0) # zgoraj
        B = (W, y0 + (W - x0) * y / x) # desno
        C = (x0 + (H - y0)*x/y, H) # spodaj
        D = (0, y0 - x0*y/x) # levo

        if x>0 and y<0: # zgornji in desni rob
            if self.norma2(A) < self.norma2(B):
                self.lines.append(self.cloth.create_line(x0, y0, A[0], A[1]))
            else:
                self.lines.append(self.cloth.create_line(x0, y0, B[0], B[1]))

        if x>0 and y>0: # desni in spodnji rob
            if self.norma2(B) < self.norma2(C):
                self.lines.append(self.cloth.create_line(x0, y0, B[0], B[1]))
            else:
                self.lines.append(self.cloth.create_line(x0, y0, C[0], C[1]))

        if x<0 and y>0: # spodnji in levi rob
            if self.norma2(C) < self.norma2(D):
                self.lines.append(self.cloth.create_line(x0, y0, C[0], C[1]))
            else:
                self.lines.append(self.cloth.create_line(x0, y0, D[0], D[1]))

        if x<0 and y<0:
            if self.norma2(D) < self.norma2(A):
                self.lines.append(self.cloth.create_line(x0, y0, D[0], D[1]))
            else:
                self.lines.append(self.cloth.create_line(x0, y0, A[0], A[1]))

    def norma2(self, v):
        return v[0]**2 + v[1]**2

root = Tk()

bazen = Table(120, 200, root)

root.mainloop()