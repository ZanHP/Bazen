from tkinter import *

R = 8
class Ball():
    def __init__(self, barva, x, y, canvas):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.id = self.canvas.create_oval(self.x - R, self.y - R, self.x + R, self.y + R, fill=barva)
        # belo premikamo z desnim klikom
        self.canvas.bind("<B3-Motion>", self.move)

    def move(self, event):
        (x, y) = (event.x, event.y)
        self.x = x
        self.y = y
        self.canvas.coords(self.id, self.x - R, self.y - R, self.x + R, self.y + R)

    # def moveButton(self, x, y):
    #     self.x = x
    #     self.y = y
    #     self.canvas.coords(self.id, self.x - R, self.y - R, self.x + R, self.y + R)