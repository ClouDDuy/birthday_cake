import tkinter as tk
import turtle

screen = turtle.Screen()
screen.bgcolor("#f6d2ff")
screen.setup(width=1.0, height=1.0)
screen.title("Button")

t = turtle.Turtle()
t.penup()
t.goto(0,0)
t.write("Klick", align="center", font=("arial", 20, "bold"))

def on_button_click():
    t.clear()
    t.write("Ich wurde geklickt", align="center", font=("arial", 20, "bold"))

canvas = screen.getcanvas()
root = canvas.winfo_toplevel()
my_button = tk.Button(root, text = "Fick mich", command = on_button_click)

canvas.create_window(0, -200, window=my_button)

screen.mainloop()