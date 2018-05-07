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



        self.strength = Scale(self.frameButtons, from_=0.1, to=800, length=200)
        self.strength.set(8)
        self.strength.grid(row=0, column=0)

        # seznam vseh narisanih črt
        self.lines = []

        drawButton = Button(self.frameButtons, text="Draw!",
                            command=lambda: self.draw_line((self.cueBall.x, self.cueBall.y), self.cue.direction, False))
        drawButton.grid(row=1, column=0)

        hitButton = Button(self.frameButtons, text="Hit!", command=lambda: self.cue.hit(self.strength.get()))
        hitButton.grid(row=2, column=0)

        #self.updater()

    def updater(self):
        self.draw_line()
        self.master.after(50, self.updater)

    def draw_line(self, v0, v, reflection):
        # v0 - začetna točka
        # v - smerni vektor
        # reflection - True, če je odboj, sicer False
        (x0, y0) = v0
        (x, y) = v

        # normiramo smerni vektor
        N = 1 / (x**2 + y**2)**0.5
        x, y = N*x, N*y

        # pobrišemo vse črte, če risanje ni odboj
        if not reflection:
            for line in self.lines:
                self.cloth.after(5, self.cloth.delete, line)

        # možne točke odboja
        A = (x0 - y0 * x / y, 0) if y != 0 else (x0, 0) # zgoraj
        B = (W, y0 + (W - x0) * y / x) if x != 0 else (W, y0) # desno
        C = (x0 + (H - y0) * x / y, H) if y != 0 else (x0, H) # spodaj
        D = (0, y0 - x0 * y / x) if x != 0 else (0, y0) # levo

        str = self.strength

        if x>=0 and y<=0: # zgornji in desni rob
            if self.norma2(A) < self.norma2(B):
                print(self.norma2(A), (str.get())**2)
                if self.norma2(A) < (str.get())**2:
                    # če je razdalja do roba manjša od moči udarca
                    # oz. preostale hitrosti
                    self.lines.append(self.cloth.create_line(x0, y0, A[0], A[1]))
                    str.set(str.get() - self.norma2(A)**0.5)
                    print(str.get())
                    self.reflect(A, (x, y))
                else:
                    # če je razdalja do roba večja od moči
                    x1, y1 = x0 + str.get()*x, y0 + str.get()*y
                    print(x0,y0,x1,y1)
                    self.lines.append(self.cloth.create_line(x0, y0, x1, y1))

            else:
                self.lines.append(self.cloth.create_line(x0, y0, B[0], B[1]))
                self.reflect(B, (x,y))

        if x>=0 and y>=0: # desni in spodnji rob
            if self.norma2(B) <= self.norma2(C):
                self.lines.append(self.cloth.create_line(x0, y0, B[0], B[1]))
            else:
                self.lines.append(self.cloth.create_line(x0, y0, C[0], C[1]))

        if x<=0 and y>=0: # spodnji in levi rob
            if self.norma2(C) <= self.norma2(D):
                self.lines.append(self.cloth.create_line(x0, y0, C[0], C[1]))
            else:
                self.lines.append(self.cloth.create_line(x0, y0, D[0], D[1]))

        if x<=0 and y<=0:
            if self.norma2(D) <= self.norma2(A):
                self.lines.append(self.cloth.create_line(x0, y0, D[0], D[1]))
            else:
                self.lines.append(self.cloth.create_line(x0, y0, A[0], A[1]))

    def reflect(self, v0, v):
        # v0 - točka odboja
        # v - smerni vektor pred obdbojem
        x0, y0 = v0
        x, y = v
        if x0>0 and y0==0: # odboj zgoraj
            y = -y
            self.draw_line((x0,y0), (x,y), True)

    def norma2(self, v):
        return v[0]**2 + v[1]**2


root = Tk()

bazen = Table(120, 200, root)

root.mainloop()