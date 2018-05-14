from tkinter import *

k = 0.3 # trenje mize
kF = 0.003 # vpliv mize na forback in forbacka na hitrost
dt0 = 0.5 # casovni interval
eps = 2 # toleranca pri upostevanju hitrosti
epsRob = 2 # toleranca pri upogibu roba, sicer problem pri zaznavanju odboja
B = 0.7 # upogib bande pri odboju vpliva na smeri odbite kugle
rot = 0.025 # vpliv bande na povacanje rotacije odbite kugle

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

        # rotacija, ce vec od 0, se vrti v levo
        self.english = 0

        # rotacija naprej in nazaj
        self.forback = 0

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

    def drawDt(self, direction, energy, forback, W, H, d, rVogal):
        print("draw")
        # energy - energija, ki jo kugla sprejme. Ce smo v trenutku, ki ni prvi
        # po udarcu, je dodana energija enaka 0
        # direction - smer, v kateri se energija manifestira (normiran vektor)
        x, y = direction[0], direction[1]

        # nastavimo koordinate bele nazaj na te, kjer bela res je
        self.x, self.y = self.x0, self.y0

        # pobrisemo stare crte
        for line in self.lines:
            self.canvas.after(1, self.canvas.delete, line)

        if energy > 0:
            # (x, y) lezi na enotski kroznici, torej
            # x = cos(fi), y = sin(fi),
            # zato lahko energijo pretvorimo v hitrost takole:
            self.vx = energy * x
            self.vy = energy * y
        self.forback = forback

        # dokler ima kugla nenicelno (vec od eps) hitrost, risemo nove crte, ki na koncu
        # predstavljajo potovanje bele
        while abs(self.vx) > eps or abs(self.vy) > eps:
            # ce ne dodamo energije, se hitrosti vx in vy zmanjsujeta zaradi trenja
            # (najbrz) po formuli v = v * (1 - k*dt)
            # to hitrost sprejmemo le, ce ni tako velika, da bi daljica pobegnila z mize
            # (to preverjamo kasneje)
            self.vx = self.vx*(1 - k * dt0) if abs(self.vx) - k * dt0 > 0 else 0
            self.vy = self.vy*(1 - k * dt0) if abs(self.vy) - k * dt0 > 0 else 0

            # nastavimo prvi krajisci daljice
            x0 = self.x
            y0 = self.y

            # mozni drugi krajisci, morda sta izven mize
            mx = x0 + self.vx * dt0
            my = y0 + self.vy * dt0

            # cas manjsamo, dokler nista drugi krajisci na mizi
            # Ker smo najprej poskusili s casom dt0 in pri tem dobili hitrost
            # po tem casu, moramo, ce zelimo daljico povleci do prejsnjega trenutka,
            # tudi primerno povecati hitrost.
            dt = dt0
            while not (self.R - epsRob <= mx <= W - self.R + epsRob) or \
                    not (self.R - epsRob <= my <= H - self.R + epsRob):
                dt = dt * 0.5
                self.vx = self.vx * (1 + k * dt)
                mx = x0 + self.vx * dt
                self.vy = self.vy * (1 + k * dt)
                my = y0 + self.vy * dt

            # preden dokoncno dolocimo drugi krajisci, moramo upostevati se forback
            # hitrost
            v = (self.vx**2 + self.vy**2)**0.5
            # rotacijo forback povecamo, ce velja, da je manj od v/self.R
            # ustrezno zmanjsamo hitrost
            # TODO razmisliti koliko se res zmanjsa/poveca hitrost
            print("v1: ",v)
            if self.forback < v/self.R:
                self.forback += v/self.R * kF * dt
                self.vx += self.vx * self.forback * kF * dt
                self.vy += self.vy * self.forback * kF * dt
                print(self.forback)
                print("v2: ", v)
            # sicer jo zmanjsamo in povecamo hitrost
            elif self.forback > v/self.R:
                self.forback -= v / self.R * kF * dt
                self.vx += self.vx * self.forback * kF * dt
                self.vy += self.vy * self.forback * kF * dt
                print(self.forback)
                print("v2: ", v)

            # dolocimo drugi krajisci
            self.x = x0 + self.vx * dt
            self.y = y0 + self.vy * dt

            #N = self.vx**2 + self.vy**2
            #print("00:vx,vy", self.vx, self.vy)

            # preverimo odboje
            # Ce se kugla odbija, obrnemo smer hitrosti,
            # to se pozna pri naslednjem koraku zanke.
            # Z 0<B<1 mnozimo tisto koordinato hitrosti, ki ne obrne smeri,
            # tak odboj je potem bolj realen.
            # Privzamemo, da se pri vsakem odboju forback iznici.
            if self.y <= self.R:  # odboj zgoraj
                self.vy = - self.vy
                if self.vx < 0:
                    self.vx = self.vx * B * (1 - self.english)
                    self.english += rot * self.vx
                else:
                    self.vx = self.vx * B * (1 + self.english)
                    self.english += rot * self.vx
                self.forback = 0

            if H - self.y <= self.R: # odboj spodaj
                self.vy = - self.vy
                if self.vx < 0:
                    self.vx = self.vx * B * (1 + self.english)
                    self.english -= rot * self.vx
                else:
                    self.vx = self.vx * B * (1 - self.english)
                    self.english -= rot * self.vx
                self.forback = 0

            if self.x <= self.R: # odboj levo
                self.vx = - self.vx
                if self.vy < 0:
                    self.vy = self.vy * B * (1 + self.english)
                    self.english -= rot * self.vy
                else:
                    self.vy = self.vy * B * (1 - self.english)
                    self.english -= rot * self.vy
                self.forback = 0

            if W - self.x <= self.R: # odboj desno
                self.vx = - self.vx
                if self.vy < 0:
                    self.vy = self.vy * B * (1 - self.english)
                    self.english += rot * self.vy
                else:
                    self.vy = self.vy * B * (1 + self.english)
                    self.english += rot * self.vy
                self.forback = 0

            # narisemo
            self.lines.append(self.canvas.create_line(x0, y0, self.x, self.y))

            if self.checkPot(self.x, self.y, W, H, d, rVogal):
                print("Pot!")
                break

        self.english = 0
        self.forback = 0
        print("DONE")

    def checkPot(self, x, y, W, H, d, rVogal):
        # preveri, ali je kugla padla v vogalno luknjo,
        # ce je, potem vrne True in odbijanje se ustavi
        # levo zgoraj
        if (x + d)**2 + (y + d)**2 < rVogal**2:
            return True

        # desno zgoraj
        if (x-(W + d))**2 + (y + d)**2 < rVogal**2:
            return True

        # desno spodaj
        if (x-(W + d))**2 + (y - (H + d))**2 < rVogal**2:
            return True

        # levo spodaj
        if (x + d)**2 + (y - (H + d))**2 < rVogal**2:
            return True

        return False