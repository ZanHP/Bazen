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

        self.frame = Frame(self.master, width=W + 2*D, height=H + 2*D)
        self.frame.grid(row=0, column=0, rowspan=2)

        self.cloth = Canvas(self.frame,bg='brown', width=W, height=H)
        self.cloth.create_polygon(D,D,W-D,D,W-D,H-D,D,H-D, fill='blue')
        self.cloth.grid(row=0, column=0, rowspan=2)

        # razred Table vsebuje objekte tipa Ball in Cue, ne pa njihovih podatkov
        self.cueBall = ball.Ball('white', cueX, cueY, self.cloth)
        self.cue = cue.Cue(cueX, cueY, self.cloth)

        self.line = self.cloth.create_line(0,0,0,0)

        self.strength = Scale(master, from_=0.1, to=100, length=200)
        self.strength.grid(row=0, column=1)

        drawButton = Button(master, text="Draw!", command=lambda: self.draw_line())
        drawButton.grid(row=1, column=1)

        hitButton = Button(master, text="Hit!", command=lambda: self.cue.hit(self.strength.get()))
        hitButton.grid(row=1, column=1)

    def draw_line(self):
        (x, y) = self.cue.direction
        (cueX, cueY) = (self.cue.x0, self.cue.y0)
        N = 10 * self.strength.get() / (x**2 + y**2)**0.5
        self.cloth.after(5, self.cloth.delete, self.line)
        self.line = self.cloth.create_line(cueX, cueY, cueX + N*x, cueY + N*y)

root = Tk()

bazen = Table(120, 200, root)

root.mainloop()