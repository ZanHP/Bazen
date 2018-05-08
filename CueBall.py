from tkinter import *

k = 0.3 # trenje mize
dt0 = 0.5 # casovni interval
eps = 10 # toleranca pri upostevanju hitrosti
epsRob = 2 # toleranca pri upogibu roba, sicer problem pri zaznavanju odboja
B = 0.7 # upogib bande pri odboju vpliva na smeri odbite kugle

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
        self.spin = 0

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

    def drawDt(self, direction, energy, W, H):
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

        # dokler ima kugla nenicelno (vec od eps) hitrost, risemo nove crte, ki na koncu
        # predstavljajo potovanje bele
        while abs(self.vx) > eps or abs(self.vy) > eps:
            # ce ne dodamo energije, se hitrosti vx in vy zmanjsujeta zaradi trenja
            # (najbrz) po formuli v = v * (1 - k*dt)
            # to hitrost sprejmemo le, ce ni tako velika, da bi daljica pobegnila z mize
            # (to preverjamo kasneje)
            self.vx = self.vx*(1 - k * dt0) if abs(self.vx) > k * dt0 else 0
            self.vy = self.vy*(1 - k * dt0) if abs(self.vy) > k * dt0 else 0

            # nastavimo prvi krajisci daljice
            x0 = self.x
            y0 = self.y

            # mozni drugi krajisci, morda sta izven mize
            mx = x0 + self.vx * dt0
            my = y0 + self.vy * dt0

            # cas manjsamo, dokler nista drugi krajisci na mizi
            # Ker smo najprej poskusili s casom dt0 in pri tem dobili hitrost
            # po tem casu, moramo, ce zelimo daljico povleci do prejsnjega trenutka,
            # tudi primerno povacati hitrost.
            dt = dt0
            while not (self.R - epsRob <= mx <= W - self.R + epsRob) or \
                    not (self.R - epsRob <= my <= H - self.R + epsRob):
                dt = dt * 0.5
                self.vx = self.vx * (1 + k * dt)
                mx = x0 + self.vx * dt
                self.vy = self.vy * (1 + k * dt)
                my = y0 + self.vy * dt
            self.x = mx
            self.y = my

            # preverimo odboje
            # Ce se kugla odbija, obrnemo smer hitrosti,
            # to se pozna pri naslednjem koraku zanke.
            # Z 0<B<1 mnozimo tisto koordinato hitrosti, ki ne obrne smeri,
            # saj je tak odboj je bolj realen.
            if self.y <= self.R or H - self.y <= self.R:  # odboj zgoraj ali spodaj
                self.vy = - self.vy
                self.vx = self.vx * B * (1 + self.spin)
                self.spin += 3/800 * self.vx
            if self.x <= self.R or W - self.x <= self.R: # odboj levo ali desno
                self.vx = - self.vx
                self.vy = self.vy * B * (1 + self.spin)
                self.spin += 3/800 * self.vy
            print(self.spin)

            # narisemo
            self.lines.append(self.canvas.create_line(x0, y0, self.x, self.y))

        self.spin = 0