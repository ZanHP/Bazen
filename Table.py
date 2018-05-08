from tkinter import *
import CueBall as ball
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
        self.cueBall = ball.CueBall('white', 8, cueX, cueY, 0, 0, self.cloth)
        self.cue = cue.Cue(cueX, cueY, self.cloth)

        self.energy = Scale(self.frameButtons, from_=0.1, to=800, length=200)
        self.energy.set(200)
        self.energy.grid(row=0, column=0)

        # seznam vseh narisanih črt
        self.lines = []

        drawButton = Button(self.frameButtons, text="Draw!",
                            command=lambda: self.draw_line(self.cue.direction))
        drawButton.grid(row=1, column=0)

        hitButton = Button(self.frameButtons, text="Hit!", command=lambda: self.cue.hit(self.energy.get()))
        hitButton.grid(row=2, column=0)

        # control ima isto funkcijo kot gumb draw
        self.master.bind("<Control_L>", lambda x: self.draw_line(self.cue.direction))
        self.master.focus_set()


        #self.updater()

    def updater(self):
        self.draw_line(self.cue.direction)
        self.master.after(100, self.updater)

    def draw_line(self, v):
        # v0 - začetna točka
        # v - smerni vektor
        N = self.norma2(v)**0.5
        v = (v[0]/N, v[1]/N)
        # podamo se W in H, da ni treba cesa importati
        self.cueBall.drawDt(v, self.energy.get(), W, H)

    def norma2(self, v):
        return v[0]**2 + v[1]**2


root = Tk()

bazen = Table(120, 200, root)

root.mainloop()