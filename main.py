from tkinter import *
import numpy as np
import math
from PIL import Image, ImageTk
from car import Car
import time

size_of_board = 500
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
Green_color = '#7BC043'

class Screen:

    def __init__(self):
        i = Image.open("./map.jpg")
        self.map = np.asarray(i)

        self.window = Tk()
        self.window.title('Car :D Connard')
        self.canvas = Canvas(self.window, width=size_of_board ,height=size_of_board)
        self.img =  ImageTk.PhotoImage(image=Image.fromarray(self.map, mode='RGB'))

        self.window.bind('<Button-1>', self.click)
        self.window.bind('<Button-3>', self.click2)
        self.on = False
        self.cars = []

        self.label = Label(text="")
        self.label.pack()

        

    def start(self):
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.img, anchor=NW)
        self.loop()
        self.window.mainloop()
    
    def display(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.img, anchor=NW)
        for car in self.cars:
            (x1, y1), (x2, y2) = car.polygon_points()
            # print(x1, y1, x2, y2)
            self.canvas.create_line(x1, y1, x2, y2, width=10)
        
    def click(self, event):
        self.cars[0].turn(math.pi / 8)
    def click2(self, event):
        self.cars[0].turn(-math.pi / 8)

    def add_car(self, car):
        self.cars.append(car)

    def loop(self):
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        self.window.after(1000//60, self.loop)
        self.cars[0].go()
        self.display()


screen = Screen()
screen.add_car(Car(230, 180, 0))
screen.display()
screen.start()


