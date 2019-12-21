from __future__ import division
import pygame,sys

pygame.init()
pygame.display.init()
pygame.font.init()

def Text(screen,size,pos,color,text):
    font=pygame.font.SysFont("arial",size)
    label=font.render(text,1,color)
    screen.blit(label,pos)

class Button():
    def __init__(self,text,xsize,ysize,colorup=(200,200,200),colordown=(150,150,150)):
        self.text=text
        self.xsize=xsize
        self.ysize=ysize
        self.colorup=colorup
        self.colordown=colordown
        self.clicked=False

    def draw(self,screen,x,y,color=None):
        if color==None:
            color=self.colorup
        self.x=x
        self.y=y
        self.screen=screen
        rect=pygame.Rect((x,y),(self.xsize,self.ysize))
        pygame.draw.rect(screen,color,rect)
        pygame.draw.rect(screen,(75,75,75),rect,5)
        Text(screen,15,(x+self.xsize/2-4*len(self.text),y+self.ysize/2-10),(0,0,0),self.text)

    def getClicked(self,events,eventtype=pygame.MOUSEBUTTONUP,update=False):
        for event in events:
            if event.type==eventtype:
                if event.button==1 and event.pos[0]>=self.x and event.pos[1]>=self.y and event.pos[0]<=self.x+self.xsize and event.pos[1]<=self.y+self.ysize:
                    return True
        return False

    def update(self,events):
        if self.getClicked(events,pygame.MOUSEBUTTONDOWN,True)==True:
            self.draw(self.screen,self.x,self.y,self.colordown)
            return True
        for event in events:
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONUP:
                if event.button==1:
                    self.draw(self.screen,self.x,self.y,self.colorup)
                    return True

class Slider():
    def __init__(self,botvalue,topvalue,xsize,ysize):
        self.botvalue=botvalue
        self.topvalue=topvalue
        self.xsize=xsize
        self.ysize=ysize
        self.spos=0.5*xsize
        self.pressing=False

    def draw(self,screen,x,y,roundvalue=0,color=(255,255,255),invertcolor=True,text=True):
        if invertcolor==True:
            invertcolor=(255-color[0],255-color[1],255-color[2])
        self.x=x
        self.y=y
        self.screen=screen
        self.color=color
        self.roundvalue=roundvalue
        self.invertcolor=invertcolor
        rect=pygame.Rect((x,y),(self.xsize+5,self.ysize))
        pygame.draw.rect(screen,invertcolor,rect)
        pygame.draw.rect(screen,color,rect,3)
        rect=pygame.Rect((x+self.spos,y),(5,self.ysize))
        pygame.draw.rect(screen,color,rect)
        rect=pygame.Rect((x,y+self.ysize+3),(self.xsize,15))
        pygame.draw.rect(screen,invertcolor,rect)
        Text(screen,17,(x+(self.xsize/2)-len(str(round(self.getValue())))/2*9,y+self.ysize+2),color,str(self.getValue()))
        if text==True:
            Text(screen,20,(x-len(str(self.botvalue))*11-2,y),color,str(self.botvalue))
            Text(screen,20,(x+self.xsize+7,y),color,str(self.topvalue))

    def update(self,events):
        for event in events:
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN and self.pressing==False:
                if event.button==1 and event.pos[0]>=self.x and event.pos[1]>=self.y and event.pos[0]<=self.x+self.xsize and event.pos[1]<=self.y+self.ysize:
                    self.pressing=True
                    self.spos=event.pos[0]-self.x
                    pygame.mouse.get_rel()
            if event.type==pygame.MOUSEBUTTONUP:
                if event.button==1:
                    self.pressing=False
        if self.pressing==True:
            mov=pygame.mouse.get_rel()[0]
            if self.spos+mov>=0 and self.spos+mov<=self.xsize:
                self.spos=self.spos+mov
        self.draw(self.screen,self.x,self.y,self.roundvalue,self.color,self.invertcolor,False)
        return self.pressing

    def getValue(self):
        return round(self.spos/self.xsize*(self.topvalue-self.botvalue)+self.botvalue,self.roundvalue)

class Input():
    def __init__(self,xsize,ysize,maxchars=10,focused=False):
        self.xsize=xsize
        self.ysize=ysize
        self.value=""
        self.focused=focused
        self.entered=False
        self.lasttick=pygame.time.get_ticks()
        self.cursor=""
        self.maxchars=maxchars
        self.prevvalue=""

    def draw(self,screen,x,y,color=(255,255,255)):
        self.screen=screen
        self.x=x
        self.y=y
        self.color=color
        invertcolor=(255-color[0],255-color[1],255-color[2])
        self.invertcolor=invertcolor
        rect=pygame.Rect((x,y),(self.xsize,self.ysize))
        pygame.draw.rect(screen,invertcolor,rect)
        pygame.draw.rect(screen,color,rect,3)
        Text(screen,20,(x+2,y+2),color,self.value+self.cursor)

    def update(self,events):
        CursorUpdate=False
        if self.prevvalue!=self.value:
            self.prevvalue=self.value
            return True
        
        if self.focused==True and self.cursorUpdate()==True:
            return True
        elif self.focused==False:
            if self.cursor!=" ":
                self.cursor=" "
                self.draw(self.screen,self.x,self.y,self.color)
                return True
        for event in events:
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONUP:
                if event.button==1 and event.pos[0]>=self.x and event.pos[1]>=self.y and event.pos[0]<=self.x+self.xsize and event.pos[1]<=self.y+self.ysize:
                    self.focused=True
                elif event.button==1:
                    self.focused=False
            if event.type==pygame.KEYDOWN and self.focused==True:
                if event.key==pygame.K_BACKSPACE:
                    try:
                        self.value=self.value[:-1]
                    except:
                        pass
                elif event.key==pygame.K_RETURN:
                    self.entered=True
                elif event.key <=127 and len(self.value)<=self.maxchars-1:
                    self.value=self.value+chr(event.key)
                self.draw(self.screen,self.x,self.y,self.color)
                return True
            else:
                return False

    def changeValue(self,value):
        self.value=value
        self.draw(self.screen,self.x,self.y,self.color)

    def cursorUpdate(self):
        if pygame.time.get_ticks()-self.lasttick>=1000 and self.cursor=="|":
            self.cursor=""
            rect=pygame.Rect((self.x,self.y),(self.xsize,self.ysize))
            pygame.draw.rect(self.screen,self.invertcolor,rect)
            pygame.draw.rect(self.screen,self.color,rect,3)
            Text(self.screen,20,(self.x+2,self.y+2),self.color,self.value+self.cursor)
            self.lasttick=pygame.time.get_ticks()
            return True
        elif pygame.time.get_ticks()-self.lasttick>=1000:
            self.cursor="|"
            rect=pygame.Rect((self.x,self.y),(self.xsize,self.ysize))
            pygame.draw.rect(self.screen,self.invertcolor,rect)
            pygame.draw.rect(self.screen,self.color,rect,3)
            Text(self.screen,20,(self.x+2,self.y+2),self.color,self.value+self.cursor)
            self.lasttick=pygame.time.get_ticks()
            return True
        return False

class SelectBox():
    def __init__(self,xsize,ysize,text,selected=False):
        self.xsize=xsize
        self.ysize=ysize
        self.text=text
        self.selected=selected

    def draw(self,screen,x,y,color=(255,255,255)):
        self.screen=screen
        self.x=x
        self.y=y
        self.color=color
        invertcolor=(255-color[0],255-color[1],255-color[2])
        self.invertcolor=invertcolor
        rect=pygame.Rect((x,y),(self.xsize+5+11*len(self.text),self.ysize))
        pygame.draw.rect(screen,invertcolor,rect)
        rect=pygame.Rect((x,y),(self.xsize,self.ysize))
        pygame.draw.rect(screen,invertcolor,rect)
        pygame.draw.rect(screen,color,rect,3)
        if self.selected==True:
            rect=pygame.Rect((x+5,y+5),(self.xsize-10,self.ysize-10))
            pygame.draw.rect(screen,color,rect)
        Text(screen,20,(x+self.xsize+5,y),color,self.text)

    def update(self,events):
        for event in events:
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1 and event.pos[0]>=self.x and event.pos[1]>=self.y and event.pos[0]<=self.x+self.xsize and event.pos[1]<=self.y+self.ysize:
                    if self.selected==False:
                        self.selected=True
                    elif self.selected==True:
                        self.selected=False
                    self.draw(self.screen,self.x,self.y,self.color)
                    return True

    def changeValue(self,value):
        self.selected=value
        self.draw(self.screen,self.x,self.y,self.color)

class SelectBoxes():
    def __init__(self,xsize,ysize,texts):
        self.xsize=xsize
        self.ysize=ysize
        self.sboxes=[]
        for text in texts:
            self.sboxes.append(SelectBox(xsize,ysize,text))

    def draw(self,screen,x,y,color=(255,255,255)):
        self.screen=screen
        self.x=x
        self.y=y
        self.color=color
        ypos=y
        for sbox in self.sboxes:
            sbox.draw(screen,x,ypos,color)
            ypos=ypos+self.ysize+10

    def update(self,events):
        supdate=[False]*len(self.sboxes)
        spot=0
        for sbox in self.sboxes:
            if sbox.update(events)==True:
                supdate[spot]=True
            spot=spot+1
        return supdate

    def changeValue(self,index,value):
        self.sboxes[index].changeValue(value)

    def getValue(self,index):
        return self.sboxes[index].selected

class RadioBoxes():
    def __init__(self,xsize,ysize,texts):
        self.xsize=xsize
        self.ysize=ysize
        self.sboxes=[]
        for text in texts:
            self.sboxes.append(SelectBox(xsize,ysize,text))
        self.sboxes[0].selected=True

    def draw(self,screen,x,y,color=(255,255,255)):
        self.screen=screen
        self.x=x
        self.y=y
        self.color=color
        ypos=y
        for sbox in self.sboxes:
            sbox.draw(screen,x,ypos,color)
            ypos=ypos+self.ysize+10

    def update(self,events):
        supdate=[False]*len(self.sboxes)
        spot=0
        for sbox in self.sboxes:
            if sbox.update(events)==True:
                supdate[spot]=True
            spot=spot+1
        spot=0
        if True in supdate:
            for update in supdate:
                self.sboxes[spot].changeValue(update)
                spot=spot+1
        return supdate

    def changeValue(self,index,value):
        self.sboxes[index].changeValue(value)

    def getValue(self,index):
        return self.sboxes[index].selected
            

if __name__ == "__main__":
    pygame.key.set_repeat(500,50)
    but = Button("test",100,30)
    dis = pygame.display.set_mode((600,600))
    pygame.display.set_caption("test")
    but.draw(dis,50,50)
    while 1:
        events=pygame.event.get()
        if but.update(events)==True:
            pygame.display.flip()
        pygame.display.flip()
        if but.getClicked(events,pygame.MOUSEBUTTONUP) == True:
            dis.fill((0,0,0))
            break
    dis.fill((0,0,0))
    s=RadioBoxes(30,30,["mandelbrot set","julia set"])
    s.draw(dis,50,50,(255,255,255))
    pygame.display.flip()
    while 1:
        events=pygame.event.get()
        updates=s.update(events)
        if True in updates:
            pygame.display.flip()
            if updates[0]==True:
                print(s.getValue(0))
