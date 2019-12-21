# -*- coding: cp1252 -*-
from __future__ import division
import pygame as g
import pygame
import math
import Features
import sys
import os
import multiprocessing

g.init()
g.display.init()
g.font.init()
g.key.set_repeat(500,50)
x=g.display.Info().current_w
y=g.display.Info().current_h
screenx=x
screeny=y

def RotatePoint(x,y,centerx,centery,degrees):
    sin=math.sin(math.radians(degrees))
    cos=math.cos(math.radians(degrees))
    x=x-centerx
    y=y-centery
    newx=x*cos-y*sin
    newy=x*sin+y*cos
    newx=newx+centerx
    newy=newy+centery
    return (newx,newy)

class Fractal():
    def __init__(self,screen,imaginary,real,quality,zoom,xoffset,yoffset,x,y,color,colorscheme,power=2,rotation=0):
        self.screen=screen
        self.imaginary=imaginary
        self.real=real
        self.quality=quality
        self.zoom=zoom
        self.xoffset=xoffset
        self.yoffset=yoffset
        self.x=x
        self.y=y
        self.bounded=0
        self.color=color
        self.colorscheme=colorscheme
        self.power=power
        self.rotation=rotation
        

    def Mandelbrot(self):
        b=""
        for x in range(0,self.x):
            for y in range(0,self.y):
                imaginary=(-(y-300)/150/self.zoom)+self.yoffset
                real=((x-300)/150/self.zoom)+self.xoffset
                if self.rotation != 0:
                    real,imaginary = RotatePoint(real,imaginary,self.xoffset,self.yoffset,self.rotation)
                z=complex(self.real,self.imaginary)
                c=complex(real,imaginary)
                for iteration in range(0,self.quality):
                    z=z**self.power+c
                    lastdis=math.sqrt((z.real*z.real)+(z.imag*z.imag))
                    if lastdis>2*self.quality:
                        b="break"
                        self.Color(x,y,iteration,self.quality,lastdis)
                        break
                if b!="break":
                    self.Color(x,y,self.quality,self.quality,0)
                else:
                    b=""
                    
    def Julia(self):
        b=""
        for x in range(0,self.x):
            for y in range(0,self.y):
                imaginary=(-(y-300)/150/self.zoom)+self.yoffset
                real=((x-300)/150/self.zoom)+self.xoffset
                if self.rotation != 0:
                    real,imaginary = RotatePoint(real,imaginary,self.xoffset,self.yoffset,self.rotation)
                z=complex(real,imaginary)
                c=complex(self.real,self.imaginary)
                for iteration in range(0,self.quality):
                    z=z**self.power+c
                    lastdis=math.sqrt((z.real*z.real)+(z.imag*z.imag))
                    if lastdis>2*self.quality:
                        b="break"
                        self.Color(x,y,iteration,self.quality,lastdis)
                        break
                    if iteration == self.quality:
                        self.Color(x,y,iteration,iteration,lastdis)
                if b!="break":
                    self.Color(x,y,self.quality,self.quality,0)
                else:
                    b=""
                    
    def Color(self,x,y,iteration,quality,lastdis,flip=False):
        if lastdis!=0 and self.color==True:
            iteration=iteration+1-math.log(math.log(lastdis))/math.log(self.power)
        color=((quality-iteration)/quality)
        if color > 1:
            color = 1
        c=self.ColorScale(color,self.colorscheme)
        try:
            self.screen.set_at((x,y),c)
        except Exception as e:
            pygame.quit()
            sys.exit()
        if flip==True:
            g.display.flip()

    def ColorScale(self,color,scheme):
        if len(scheme)<2:
            scheme=[[0,0,0],[0,0,0]]
        if color==1:
            return scheme[len(scheme)-1]
        if color==0:
            return scheme[0]
        co=color*(len(scheme)-1)
        c=[0,0,0]
        cint=int(co)
        b=co-cint
        c[0]=(scheme[cint+1][0]-scheme[cint][0])*b+scheme[cint][0]
        c[1]=(scheme[cint+1][1]-scheme[cint][1])*b+scheme[cint][1]
        c[2]=(scheme[cint+1][2]-scheme[cint][2])*b+scheme[cint][2]
        return c

def Text(screen,size,pos,color,text):
    font=g.font.SysFont("arial",size)
    label=font.render(text,1,color)
    screen.blit(label,pos)

def KeepActive(conn):
    import pygame as g
    while True:
        g.display.update()
        g.event.get()
        if conn.poll==True:
            if conn.recv()==False:
                break

def SingleEntry(screen,string,forceFloat=True):
    screen.fill((0,0,200))
    Text(screen,36,(x/2-100,50),(255,255,255),"MandaFractal")
    Text(screen,35,(5,200),(0,200,0),string)
    but=Features.Button("Next",150,50)
    inbox=Features.Input(300,30,25,True)
    but.draw(screen,450,550)
    inbox.draw(screen,150,500)
    g.display.flip()
    value=0
    while True:
        events=g.event.get()
        for event in events:
            if event.type == g.QUIT:
                g.quit()
                sys.exit()
        if but.update(events)==True:
            g.display.flip()
        if but.getClicked(events)==True or inbox.entered==True:
            screen.fill((0,0,200))
            if forceFloat==True:
                return value
            else:
                return str(value)
        if inbox.update(events)==True:
            try:
                if inbox.value!="-" and forceFloat==True:
                    float(inbox.value+"0")
                    value=float(inbox.value)
                elif forceFloat==False:
                    value=inbox.value
            except:
                if forceFloat==True:
                    inbox.changeValue("")
            g.display.flip()

def Entry(screen,string,downval,upval):
    screen.fill((0,0,200))
    Text(screen,36,(x/2-100,50),(255,255,255),"MandaFractal")
    Text(screen,35,(5,200),(0,200,0),string)
    slide=Features.Slider(downval,upval,300,20)
    but=Features.Button("Next",150,50)
    inbox=Features.Input(300,30,25,True)
    slide.draw(screen,150,400,4)
    but.draw(screen,450,550)
    inbox.draw(screen,150,500)
    g.display.flip()
    value=0
    while True:
        events=g.event.get()
        for event in events:
            if event.type == g.QUIT:
                g.quit()
                sys.exit()
        if slide.update(events)==True:
            g.display.flip()
            value=slide.getValue()
            inbox.changeValue(str(value))
        if but.update(events)==True:
            g.display.flip()
        if but.getClicked(events)==True or inbox.entered==True:
            screen.fill((0,0,200))
            return value
        if inbox.update(events)==True:
            try:
                if inbox.value!="-":
                    float(inbox.value)
                    value=float(inbox.value)
            except:
                inbox.changeValue("")
            g.display.flip()

def Display(screen,img,real,quality,zoom,xoffset,yoffset,coloring,mandelbrot,julia):
    Fractals=Fractal(screen,img,real,quality,zoom,xoffset,yoffset,600,600,coloring)
    rect=g.Rect((0,0),(600,600))
    g.draw.rect(screen,(0,0,0),rect)
    Text(screen,50,(0,30),(0,0,255),"Loading...")
    g.display.flip()
    if mandelbrot==True:
        Fractals.Mandelbrot()
    elif julia==True:
        Fractals.Julia()
    rect=g.Rect((0,0),(600,600))
    screenshot=g.Surface((600,600))
    screenshot.blit(screen,rect)
    g.display.flip()

def Gradient(scheme):
    surf=g.Surface((300,1))
    for x in range(0,300):
        color=x/300
        if len(scheme)<2:
            scheme=[[0,0,0],[0,0,0]]
        co=color*(len(scheme)-1)
        c=[0,0,0]
        cint=int(co)
        b=co-cint
        c[0]=(scheme[cint+1][0]-scheme[cint][0])*b+scheme[cint][0]
        c[1]=(scheme[cint+1][1]-scheme[cint][1])*b+scheme[cint][1]
        c[2]=(scheme[cint+1][2]-scheme[cint][2])*b+scheme[cint][2]
        surf.set_at((x,0),c)
    surf=g.transform.scale(surf,(300,20))
    g.draw.rect(surf,(255,255,255),(0,0,299,20),3)
    return surf
    
if __name__=="__main__":
    parent,child = multiprocessing.Pipe()
    yoffset=0
    xoffset=0
    lastyoffset=0
    lastxoffset=-0.5
    screen=g.display.set_mode((x,y),g.FULLSCREEN)
    Text(screen,50,(0,30),(0,0,255),"Loading...")
    g.display.flip()
    Fractals=Fractal(screen,0,0,50,1,-0.5,0,600,600,True,[[0,0,0],[143,0,255],[75,0,130],[0,255,0],[255,255,0],[0,255,255]])
    Fractals.Mandelbrot()
    Quit = False
    exitbut=Features.Button("Exit",150,40)
    renderbut=Features.Button("Render",150,40)
    savebut=Features.Button("Save",150,40)
    saveinput=Features.Input(200,30)
    imaginaryslide=Features.Slider(-2,2,200,10)
    realslide=Features.Slider(-2,2,200,10)
    imaginaryinput=Features.Input(200,30,20,True)
    realinput=Features.Input(200,30,20)
    qualityinput=Features.Input(100,30)
    zoominput=Features.Input(200,30,20)
    xoffsetslider=Features.Slider(-2.5,2.5,200,10)
    yoffsetslider=Features.Slider(-2.5,2.5,200,10)
    xoffsetinput=Features.Input(200,30,20)
    yoffsetinput=Features.Input(200,30,20)
    powerinput=Features.Input(200,30,20)
    fractaltype=Features.RadioBoxes(20,20,["mandelbrot set","julia set"])
    coloring=Features.SelectBox(20,20,"smooth coloring",True)
    redslider=Features.Slider(0,255,255,20)
    greenslider=Features.Slider(0,255,255,20)
    blueslider=Features.Slider(0,255,255,20)
    addcolorbut=Features.Button("Add Color",150,40)
    resetcolorbut=Features.Button("Reset Colors",150,40)
    rotationinput=Features.Input(80,30,3)
    exitbut.draw(screen,5,y-45)
    renderbut.draw(screen,x-155,y-45)
    savebut.draw(screen,x-310,y-45)
    saveinput.draw(screen,x-520,y-35)
    imaginaryslide.draw(screen,660,5,5,(255,255,255))
    imaginaryinput.draw(screen,660,40);Text(screen,25,(865,40),(0,0,255),"Imaginary Value")
    realslide.draw(screen,660,100,5,(255,255,255))
    realinput.draw(screen,660,155);Text(screen,25,(865,155),(0,0,255),"Real Value")
    qualityinput.draw(screen,660,215);Text(screen,25,(765,215),(0,0,255),"Quality")
    zoominput.draw(screen,660,275);Text(screen,25,(865,275),(0,0,255),"Zoom")
    xoffsetslider.draw(screen,660,335,5)
    xoffsetinput.draw(screen,660,370);Text(screen,25,(865,370),(0,0,255),"X offset")
    yoffsetslider.draw(screen,660,425,5)
    yoffsetinput.draw(screen,660,460);Text(screen,25,(865,460),(0,0,255),"Y offset")
    powerinput.draw(screen,660,520);Text(screen,25,(865,520),(0,0,255),"Power")
    fractaltype.draw(screen,5,610)
    coloring.draw(screen,300,610)
    redslider.draw(screen,720,580,0,(255,0,0),(0,0,0))
    greenslider.draw(screen,720,630,0,(0,255,0),(0,0,0))
    blueslider.draw(screen,720,680,0,(0,0,255),(0,0,0))
    addcolorbut.draw(screen,160,y-45)
    resetcolorbut.draw(screen,315,y-45)
    Text(screen,25,(350,650),(0,255,0),"color:")
    rotationinput.draw(screen,5,680);Text(screen,25,(95,680),(0,0,255),"rotation °")
    img,real,quality,zoom,xoffset,yoffset,color,mandelbrot,julia = [0]*9
    mandelbrot=True
    julia=False
    color=True
    justrendered=True
    saveinput.changeValue("Fractal.png")
    realinput.changeValue("0.0")
    imaginaryinput.changeValue("0.0")
    xoffsetinput.changeValue("0.0")
    yoffsetinput.changeValue("0.0")
    qualityinput.changeValue("50")
    zoominput.changeValue("1.0")
    powerinput.changeValue("2")
    g.display.flip()
    real=0.0
    img=0.0
    xoffset=0
    yoffset=0
    quality=50
    zoom=1.0
    lastxoffset=-0.5
    lastyoffset=0
    lastzoom=1.0
    lastm=True
    lastj=False
    lastpower=2
    lastreal=0
    lastimg=0
    power=2
    paths=False
    savename="Fractal.png"
    red=128
    green=128
    blue=128
    currentcolor=(red,green,blue)
    colorscheme=[[0,0,0],[143,0,255],[75,0,130],[0,255,0],[255,255,0],[0,255,255]]
    lastrotation=0
    rotation=0
    rotationinput.changeValue("0")
    rect=g.Rect((0,0),(600,600))
    screenshot=g.Surface((600,600))
    screenshot.blit(screen,rect)
    pallet=g.image.load("Color Pallet.png")
    pallet=g.transform.scale(pallet,(200,100))
    screen.blit(pallet,(500,610))
    g.draw.rect(screen,currentcolor,(450,650,40,40))
    screen.blit(Gradient(colorscheme),(475,screeny-35))
    while True:
        events=g.event.get()
        pygame.event.pump()
        if exitbut.update(events)==True:
            g.display.flip()
            if exitbut.getClicked(events)==True:
                g.quit()
                sys.exit()
        if renderbut.update(events)==True:
            g.display.flip()
            if renderbut.getClicked(events)==True:
                render=True
        if saveinput.update(events)==True:
            g.display.flip()
            savename=saveinput.value
        if savebut.update(events)==True:
            g.display.flip()
            if savebut.getClicked(events)==True:
                if "." in savename:
                    pygame.image.save(screenshot,savename)
                else:
                    pygame.image.save(screenshot,savename+".png")
        if imaginaryslide.update(events)==True:
            g.display.flip()
            img=imaginaryslide.getValue()
            imaginaryinput.changeValue(str(img))
        if realslide.update(events)==True:
            g.display.flip()
            real=realslide.getValue()
            realinput.changeValue(str(real))
        if imaginaryinput.update(events)==True:
            try:
                img=float(imaginaryinput.value)
            except:
                img=imaginaryslide.getValue()
            g.display.flip()
        if realinput.update(events)==True:
            try:
                real=float(realinput.value)
            except:
                real=realslide.getValue()
            g.display.flip()
        if qualityinput.update(events)==True:
            try:
                int(qualityinput.value+"0")
                quality=int(qualityinput.value)
            except:
                pass
            g.display.flip()
        if zoominput.update(events)==True:
            try:
                zoom=float(zoominput.value)
            except:
                pass
            g.display.flip()
        if xoffsetslider.update(events)==True:
            g.display.flip()
            xoffset=xoffsetslider.getValue()
            xoffsetinput.changeValue(str(xoffset))
        if yoffsetslider.update(events)==True:
            g.display.flip()
            yoffset=yoffsetslider.getValue()
            yoffsetinput.changeValue(str(yoffset))
        if xoffsetinput.update(events)==True:
            try:
                xoffset=float(xoffsetinput.value)
            except:
                xoffset=xoffsetslider.getValue()
            g.display.flip()
        if yoffsetinput.update(events)==True:
            try:
                yoffset=float(yoffsetinput.value)
            except:
                yoffset=yoffsetslider.getValue()
            g.display.flip()
        if powerinput.update(events)==True:
            try:
                power=float(powerinput.value)
            except:
                pass
            g.display.flip()
        if True in fractaltype.update(events):
            mandelbrot=fractaltype.getValue(0)
            julia=fractaltype.getValue(1)
            g.display.flip()
        if coloring.update(events)==True:
            color=coloring.selected
            g.display.flip()
        if redslider.update(events)==True:
            red=redslider.getValue()
            currentcolor=(red,green,blue)
            g.draw.rect(screen,currentcolor,(450,650,40,40))
            screen.blit(Gradient(colorscheme),(475,screeny-35))
            g.display.flip()
        if greenslider.update(events)==True:
            green=greenslider.getValue()
            currentcolor=(red,green,blue)
            g.draw.rect(screen,currentcolor,(450,650,40,40))
            screen.blit(Gradient(colorscheme),(475,screeny-35))
            g.display.flip()
        if blueslider.update(events)==True:
            blue=blueslider.getValue()
            currentcolor=(red,green,blue)
            g.draw.rect(screen,currentcolor,(450,650,40,40))
            screen.blit(Gradient(colorscheme),(475,screeny-35))
            g.display.flip()
        if addcolorbut.update(events)==True:
            g.display.flip()
            if addcolorbut.getClicked(events)==True:
                colorscheme.append(currentcolor)
                screen.blit(Gradient(colorscheme),(475,screeny-35))
                g.display.flip()
        if resetcolorbut.update(events)==True:
            if resetcolorbut.getClicked(events)==True:
                colorscheme=[]
                screen.blit(Gradient(colorscheme),(475,screeny-35))
            g.display.flip()
            
        if rotationinput.update(events)==True:
            try:
                rotation=float(rotationinput.value)
            except:
                pass
            g.display.flip()
        if justrendered==True:
            render=False
            justrendered=False
        if render==True:
            Fractals=Fractal(screen,img,real,quality,zoom,xoffset,yoffset,600,600,color,colorscheme,power,rotation)
            rect=g.Rect((0,0),(600,600))
            g.draw.rect(screen,(0,0,0),rect)
            Text(screen,50,(0,30),(0,0,255),"Loading...")
            g.display.flip()
            if mandelbrot==True:
                Fractals.Mandelbrot()
            elif julia==True:
                Fractals.Julia()
            rect=g.Rect((0,0),(600,600))
            screenshot=g.Surface((600,600))
            screenshot.blit(screen,rect)
            g.display.flip()
            justrendered=True
            lastxoffset=xoffset
            lastyoffset=yoffset
            lastzoom=zoom
            lastreal=real
            lastimg=img
            lastm=mandelbrot
            lastj=julia
            lastpower=power
            lastrotation=rotation
        for event in events:
            if event.type==g.MOUSEBUTTONDOWN:
                if event.pos[0]>=0 and event.pos[0]<=600 and event.pos[1]>=0 and event.pos[1]<=600 and event.button==1:
                    yoffset=(-(event.pos[1]-300)/150/lastzoom)+lastyoffset
                    xoffset=((event.pos[0]-300)/150/lastzoom)+lastxoffset
                    xoffset,yoffset = RotatePoint(xoffset,yoffset,lastxoffset,lastyoffset,lastrotation)
                    xoffsetinput.changeValue(str(xoffset))
                    yoffsetinput.changeValue(str(yoffset))
                if event.pos[0]>=500 and event.pos[0]<=700 and event.pos[1]>=610 and event.pos[1]<=710 and event.button==1:
                    currentcolor=screen.get_at((event.pos[0],event.pos[1]))
                    g.draw.rect(screen,currentcolor,(450,650,40,40))
                if event.pos[0]>=450 and event.pos[0]<=750 and event.pos[1]>=730 and event.pos[1]<=750 and event.button==1:
                    currentcolor=screen.get_at((event.pos[0],event.pos[1]))
                    g.draw.rect(screen,currentcolor,(450,650,40,40))
                if event.button==2:
                    if paths==False:
                        paths=True
                    else:
                        paths=False
                    screen.blit(screenshot,rect)
                    pygame.display.flip()
                if event.pos[0]>=0 and event.pos[0]<=600 and event.pos[1]>=0 and event.pos[1]<=600 and event.button==3:
                    img=(-(event.pos[1]-300)/150/lastzoom)+lastyoffset
                    real=((event.pos[0]-300)/150/lastzoom)+lastxoffset
                    real,img = RotatePoint(real,img,lastxoffset,lastyoffset,lastrotation)
                    realinput.changeValue(str(real))
                    imaginaryinput.changeValue(str(img))
                if event.pos[0]>=0 and event.pos[0]<=600 and event.pos[1]>=0 and event.pos[1]<=600 and event.button==4:
                    screen.blit(screenshot,(0,0))
                    s=g.Surface((600,600))
                    new=g.Surface((600,600))
                    s.blit(screen,(0,0),(0,0,600,600))
                    s=g.transform.smoothscale(s,(1200,1200))
                    new.blit(s,(0,0),(event.pos[0]*2-300,event.pos[1]*2-300,event.pos[0]*2+300,event.pos[1]*2+300))
                    screen.blit(new,(0,0))
                    x=event.pos[0]
                    y=event.pos[1]
                    yoffset=(-(y-300)/150/lastzoom)+lastyoffset
                    xoffset=((x-300)/150/lastzoom)+lastxoffset
                    xoffset,yoffset = RotatePoint(xoffset,yoffset,lastxoffset,lastyoffset,lastrotation)
                    xoffsetinput.changeValue(str(xoffset))
                    yoffsetinput.changeValue(str(yoffset))
                    lastyoffset=yoffset
                    lastxoffset=xoffset
                    lastzoom=lastzoom*2
                    zoominput.changeValue(str(lastzoom))
                    zoom=lastzoom
                    rect=g.Rect((0,0),(600,600))
                    screenshot=g.Surface((600,600))
                    screenshot.blit(screen,rect)
                    g.display.flip()
                if event.pos[0]>=0 and event.pos[0]<=600 and event.pos[1]>=0 and event.pos[1]<=600 and event.button==5:
                    screen.blit(screenshot,(0,0))
                    s=g.Surface((600,600))
                    clear=g.Surface((600,600))
                    clear.fill((0,0,0))
                    s.blit(screen,(0,0),(0,0,600,600))
                    s=g.transform.smoothscale(s,(300,300))
                    screen.blit(clear,(0,0))
                    screen.blit(s,(150,150))
                    lastzoom=lastzoom/2
                    zoominput.changeValue(str(lastzoom))
                    zoom=lastzoom
                    rect=g.Rect((0,0),(600,600))
                    screenshot=g.Surface((600,600))
                    screenshot.blit(screen,rect)
                    g.display.flip()
            if event.type==g.MOUSEMOTION:
                if event.pos[0]>=0 and event.pos[0]<=600 and event.pos[1]>=0 and event.pos[1]<=600 and paths==True:
                    #screen.blit(screenshot,rect)
                    screencopy=screenshot.copy()
                    Imaginary=(-(event.pos[1]-300)/150/lastzoom)+lastyoffset
                    Real=((event.pos[0]-300)/150/lastzoom)+lastxoffset
                    Real,Imaginary = RotatePoint(Real,Imaginary,lastxoffset,lastyoffset,lastrotation)
                    
                    if lastm==True:
                        z=complex(lastreal,lastimg)
                        c=complex(Real,Imaginary)
                        xcoord=(Real-lastxoffset)*lastzoom*150+300
                        ycoord=(lastyoffset-Imaginary)*lastzoom*150+300
                        nxc,nyc = RotatePoint(xcoord,ycoord,300,300,lastrotation)
                        for i in range(0,50):
                            lastnxc=nxc
                            lastnyc=nyc
                            try:
                                z=z**lastpower+c
                            except OverflowError:
                                pass
                            x=z.real
                            y=z.imag
                            xcoord=(x-lastxoffset)*(lastzoom*150)+300
                            ycoord=(lastyoffset-y)*(lastzoom*150)+300
                            try:
                                nxc,nyc=RotatePoint(xcoord,ycoord,300,300,lastrotation)
                                
                                pygame.draw.line(screencopy,(255,255,255),(nxc,nyc),(lastnxc,lastnyc))
                            except:
                                pass
                        
                    if lastj==True:
                        z=complex(Real,Imaginary)
                        c=complex(lastreal,lastimg)
                        xcoord=(Real-lastxoffset)*lastzoom*150+300
                        ycoord=(lastyoffset-Imaginary)*lastzoom*150+300
                        nxc,nyc = RotatePoint(xcoord,ycoord,300,300,lastrotation)
                        for i in range(0,50):
                            lastnxc=nxc
                            lastnyc=nyc
                            try:
                                z=z**lastpower+c
                            except OverflowError:
                                pass
                            x=z.real
                            y=z.imag
                            xcoord=(x-lastxoffset)*(lastzoom*150)+300
                            ycoord=(lastyoffset-y)*(lastzoom*150)+300
                            try:
                                nxc,nyc=RotatePoint(xcoord,ycoord,300,300,lastrotation)
                                
                                pygame.draw.line(screencopy,(255,255,255),(nxc,nyc),(lastnxc,lastnyc))
                            except:
                                pass
                    screen.blit(screencopy,rect)
                    pygame.display.flip()
