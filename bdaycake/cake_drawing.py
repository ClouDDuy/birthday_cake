import turtle
import pyaudio
import random
import numpy as np
import tkinter as tk
import pygame

# Audioeinstellungen
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD = 10000

# Klicken
CLICK_RADIUS = 20

# Mikrofonabfrage
p = pyaudio.PyAudio()
stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = CHUNK)


# Bildschirmeinstellungen
screen = turtle.Screen()
screen.bgcolor("#f6d2ff")
screen.setup(width = 1.0, height = 1.0)
screen.title("Happy birthday emi <3")
screen.tracer(0)

t = turtle.Turtle()
t.speed(0)
t.hideturtle()
t.penup()

# Knopf
canvas = screen.getcanvas()
root = canvas.winfo_toplevel()
vid_button = tk.Button(root, text="Click me")

flame_colors = ["orange", "#ffcc00", "red"]
all_blown_out = False
mic_active = False
all_lit = False
fire_started = False

# Sound
pygame.mixer.init()
click_sound = pygame.mixer.Sound("lighter.mp3")
burn_sound = pygame.mixer.Sound("fire.mp3")
hbd_sound = pygame.mixer.Sound("happybday.mp3")

def draw_rect(x, y, width, height, color):
    t.penup()
    t.goto(x, y)
    t.setheading(0)
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)
    t.end_fill()
    t.penup()

def animate_flame(candle):
    if all_blown_out or not candle["lit"]:
        return

    flame_turtle = candle["flame_t"]
    x, y = candle["x"], candle["y"]
    
    flame_turtle.clear()

    size = random.uniform(4, 8)
    color = random.choice(flame_colors)
    wobble = random.uniform(-2, 2)

    flame_turtle.goto(x + wobble, y)
    flame_turtle.setheading(0)
    flame_turtle.fillcolor(color)
    flame_turtle.begin_fill()
    flame_turtle.circle(size)
    flame_turtle.end_fill()

    screen.update()
    screen.ontimer(lambda:animate_flame(candle), 120)

def light_me():
    t.penup()
    t.goto(0, 250)
    t.color("#000000")
    t.write("Light me", align="center", font=("Georgia", 36, "bold"))
    t.color("black")

def blow_me():
    t.penup()
    t.goto(0, 250)
    t.color("#000000")
    t.write("Blow me", align="center", font=("Georgia", 36, "bold"))
    t.color("black")

def on_button_click():
    ""

def create_bttn():
    canvas.create_window(0, 350, window = vid_button, command = on_button_click)

def draw_bday():
    t.penup()
    t.goto(0, 250)
    t.color("#f6d2ff")
    t.write("Happy Birthday", align="center", font=("Georgia", 36, "bold"))
    t.goto(0, 200)
    t.write("Emilia", align="center", font=("Georgia", 36, "bold"))
    t.color("black")
    hbd_sound.play()
    create_bttn()

def extinguish_candles():
    global all_blown_out
    all_blown_out = True

    burn_sound.stop()

    screen.bgcolor("Black")
    for candle in candles:
        candle["flame_t"].clear()

    draw_bday()
    screen.update()

def is_sound():
    if all_blown_out or not mic_active:
        return

    data = stream.read(CHUNK, exception_on_overflow=False)
    audio_data = np.frombuffer(data, dtype = np.int16)
    rms = np.sqrt(np.mean(audio_data.astype(np.float64)**2))

    if rms > THRESHOLD:
        extinguish_candles()
        stream.stop_stream()
        stream.close()
        p.terminate()
        return

    screen.ontimer(is_sound, 100)

def try_light_candle(x, y):
    global mic_active, all_lit, fire_started

    if all_blown_out:
        return

    if not all_lit:
        click_sound.play()

    for candle in candles:
        if candle["lit"]:
            continue
        dx = x - candle["x"]
        dy = y - candle["y"]
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance <= CLICK_RADIUS:
            candle["lit"] = True
            animate_flame(candle)
            if not fire_started:
                fire_started = True
                burn_sound.play(loops = -1)
            break

    if all (c["lit"] for c in candles) and not mic_active:
        blow_me()
        mic_active = True
        is_sound()
        all_lit = True


#cakelayer
cake_x = -150
cake_y = -200
cake_width_bottom = 300
cake_height = 80

cake_current_x = cake_x
cake_current_y = cake_y
cake_current_width = cake_width_bottom

#icinglayer
ici_x = -150
ici_y = -120
ici_width_bottom = 300
ici_height = 10

ici_current_x = ici_x
ici_current_y = ici_y
ici_current_width = ici_width_bottom

#candles
can_x = -80
can_y = 60
can_width_bottom = 10
can_height = 50

can_current_x = can_x

#candletip
tip_x = -75
tip_y = 110
tip_width_bottom = 1
tip_height = 5

tip_current_x = tip_x

candles = []

for i in range(3):
    draw_rect(cake_current_x, cake_current_y, cake_current_width, cake_height, "#c97b52")
   
    cake_current_x += 25
    cake_current_y += 85
    cake_current_width -= 50

for i in range(3):
    draw_rect(ici_current_x, ici_current_y, ici_current_width, ici_height, "#ffffff")
    
    ici_current_x += 25
    ici_current_y += 85
    ici_current_width -= 50

for i in range(6):
    draw_rect(can_current_x, can_y, can_width_bottom, can_height, "#ff0000")
    draw_rect(tip_current_x, tip_y, tip_width_bottom, tip_height, "#000000")

    flame_t = turtle.Turtle()
    flame_t.hideturtle()
    flame_t.penup()
    
    candles.append({
        "flame_t": flame_t,
        "x": tip_current_x, 
        "y": tip_y + tip_height,
        "lit": False})

    can_current_x += 30    
    tip_current_x += 30


screen.update()
screen.onclick(try_light_candle)
screen.mainloop()
