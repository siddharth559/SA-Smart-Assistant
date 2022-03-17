#!/usr/bin/python3.8

import turtle
import random
import time
import math
import threading as th
image='plane.gif'
image1='invader.gif'
global a
a=turtle.Turtle()
a.penup()
screen = turtle.Screen()
screen.setup(700,590)
screen.addshape(image)
screen.addshape(image1)
screen.bgpic("background.gif")
a.shape(image)
apos=0
a.setposition(x=apos,y=-250)
##############################################
score=0
scoret = turtle.Turtle(visible=False)
scoret.penup()
scoret.setposition(x = 310, y = 250)
scoret.write(str(score),font=('Candara', 30))
##############################################
global bullet
bullet=turtle.Turtle()
bullet.penup()
bullet.hideturtle()
bullet.shape("triangle")
bullet.color("yellow")
bullet.left(90)

##############################################

def right():
    x=a.xcor()
    y=a.ycor()
    if x<350 and x>-350:
        x+=10
        a.setposition(x,y)
#th1=th.Thread(
#th1.setDaemon(True)
def left():
    x=a.xcor()
    y=a.ycor()
    if x<350 and x>-350:
        x-=10
        a.setposition(x,y)
#th2=th.Thread(target=left)
#th2.setDaemon(True)
def fire():
    global bst
    bst="time"
    print(bst)
    if bullet.isvisible()==True:
        bullet.hideturtle()
    if bst=="time":
        x=a.xcor()
        y=a.ycor()+10
        bullet.setposition(x,y)
        bullet.showturtle()  
screen.onkeypress(right , "Right")
screen.onkeypress(left, "Left")
screen.onkey(fire, "space")
screen.listen()
#######################################################################################
inv=turtle.Turtle(shape=image1)
inv.hideturtle()
inv.penup()

inv.speed(0)
posit = random.randint(-250, 250)
inv.showturtle()
inv.setx(posit)
inv.sety(250)
inv.right(90)
inv.speed(3)
ba=inv.pos()



def touch():
    global inv
    global score
    global scoret
    x=int(bullet.xcor())
    y=int(bullet.ycor())
    x_=int(inv.xcor())
    y_=int(inv.ycor())
    if y in range(y_-15, y_+16):
        if x!=0:
            if x in range(x_-30,x_+31):
                score+=10
                scoret.clear()
                scoret.write(str(score),font=('Candara', 30))
                return True
def touchwall():
    try:
        global inv
        x=int(bullet.xcor())
        y=int(bullet.ycor())
        x_=int(inv.xcor())
        y_=int(inv.ycor())
        if y==290:
            return 2
        if y_==-290:
            return 4
    except:
        print(Exception)
        if y_==-290:
            return 4

bst="ntime"
while True:
    if touch()==True:
        inv.hideturtle()
        x__ = random.randint(-250, 250)
        inv.setposition(x__,250)
        inv.showturtle()
    elif touchwall()==2:
        bullet.hideturtle()
        x=bullet.xcor() ## its random any other location could also have been assisgned
        y=bullet.ycor()
        bullet.setposition(x,y-10)
        bst="ntime"
    elif touchwall()==4:
        inv.hideturtle()
        x__ = random.randint(-250, 250)
        inv.setposition(x__,250)
        inv.showturtle()
        break
        
    else:
        ix=inv.xcor()
        iy=inv.ycor()
        inv.setposition(ix,iy-2)
        if bst=="time":
            bx=bullet.xcor()
            by=bullet.ycor()
            bullet.setposition(bx,by+2)

screen.mainloop()
