
import pygame
import random


class store:
   def __init__(self):
       self.dict = {}
   # add an object to the dictionary
   def add(self, obj):
       # if obj is a list, add each item in the list
       if type(obj) is list:
           for i in obj:
               self.dict[i.tag] = i
       else:
           self.dict[obj.tag] = obj
   # remove an object from the dictionary
   def remove(self, obj):
       # if obj is a list, remove each item in the list
       if type(obj) is list:
           for i in obj:
               del self.dict[i.tag]
       else:
           del self.dict[obj.tag]
   # remove all items in the dictionary
   def remove_all(self):
       # remove all items in the dictionary
       self.dict = {}


# child class of store
class objects(store):
    def __init__(self):
        super().__init__()
        
    def button_store(self,obj):
        self.button_obj=obj

    def remove_set(self,obj):
        
        if type(obj) is list:
            for i in obj:
                self.button_obj.remove(i)
                self.remove(i)
        else:
            self.button_obj.remove(obj)
            self.remove(obj)

    def add_set(self,obj):

        self.button_obj.add(obj)
        self.add(obj)

    def remove_all_set(self):
        self.button_obj.remove_all()
        return super().remove_all()

class buttons_set(store):
    def check(self,buttons):
        # check if button is pressed
        pos=pygame.mouse.get_pos()
        try:
            for i in self.dict:
                g=self.dict[i]
                if pos[0]>=(g.boxx-g.textwidth) and pos[1]>=(g.boxy-g.textheight) and pos[0]<=(g.boxxwidth+g.boxx-g.textwidth) and pos[1]<=(g.boxy+g.boxyheight-g.textheight):
                    buttons.dict[i].func()
                    return True
        except:pass
    
    def check_hover(self,buttons):
        pos=pygame.mouse.get_pos()
        for i in self.dict:
            g=self.dict[i]
            if pos[0]>=(g.boxx-g.textwidth) and pos[1]>=(g.boxy-g.textheight) and pos[0]<=(g.accwidth) and pos[1]<=(g.accheight):
                buttons.dict[i].create("red")
            else:
                buttons.dict[i].create("blue")

class circle_summon():
    def __init__(self):
        self.tag=None
        self.radius=None
        self.colour=None

    def make(self,name,colour,loc):
        self.tag=name
        self.colour=colour
        self.loc=loc
    def set(self,loc):
        self.loc=loc
    
    def draw_mouse(self,screen):
        pygame.draw.circle(screen, self.colour , pygame.mouse.get_pos(), self.radius)
    def draw(self,screen):
        pygame.draw.circle(screen,self.colour,self.loc,5)



class button_summon():
    def __init__(self):
        self.smallfont = pygame.font.SysFont('Corbel',20) 
        self.tag=None

    def make(self,name,buttoncolour,textcolour,textloc,text,func):
        self.tag=name
        self.buttoncolour=buttoncolour
        self.textcolour=textcolour
        self.textloc=textloc
        text = self.smallfont.render(text , True , self.textcolour)
        self.text=text
        self.boxxwidth=text.get_width()+10
        self.boxyheight=text.get_height()+5
        self.textwidth=text.get_width()/2
        self.textheight=text.get_height()/2
        self.boxx=self.textloc[0]-6
        self.boxy=self.textloc[1]-3
        self.func=func
        self.rectangle=rect_summon()
        self.accwidth=self.boxxwidth+self.boxx-self.textwidth
        self.accheight=self.boxy+self.boxyheight-self.textheight
        self.create(self.buttoncolour)
        self.nobox=False
    def create(self,colour):
        self.colour=colour
        self.rectangle.make(self.tag,colour,[self.boxx-self.textwidth,self.boxy-self.textheight],self.boxxwidth,self.boxyheight)
    def no_box(self,name,text,loc):
        self.tag=name
        self.nobox=True
        self.loc=loc
        self.textcolour="black"
        self.smallfont = pygame.font.SysFont('arial',15) 
        self.text = self.smallfont.render(text , True , self.textcolour)

    def change_text_nobox(self,text):
        self.text = self.smallfont.render(text , True , self.textcolour)
    def draw(self,screen):
        if self.nobox:
            screen.blit(self.text , self.loc)
        else:
            self.rectangle.draw(screen)
            screen.blit(self.text , [self.textloc[0]-self.textwidth,self.textloc[1]-self.textheight])

class rect_summon():
    def __init__(self):
        self.tag=None
        self.colour=None
    def make(self,name,colour,loc,height,width):
        self.tag=name
        self.colour=colour
        self.width=width
        self.height=height
        self.loc=loc
    def draw(self,screen):
        pygame.draw.rect(screen,self.colour,pygame.Rect(self.loc[0], self.loc[1], self.height, self.width))
        
class selection_summon():
    def __init__(self):
        self.tag=None
        self.colour=None
    def make(self,name,colour):
        self.tag=name
        self.colour=colour
    def draw(self,loc1,loc2,screen):
        loc1x=loc1[0]
        loc1y=loc1[1]
        loc2x=loc2[0]
        loc2y=loc2[1]
        if loc1x<loc2x:
            if loc1y<loc2y:
                s = pygame.Surface((loc2x-loc1x,loc2y-loc1y))
                s.set_alpha(128)
                s.fill((255,255,255))
                screen.blit(s, (loc1x,loc1y))
            else:
                s = pygame.Surface((loc2x-loc1x,loc1y-loc2y))
                s.set_alpha(128)
                s.fill((255,255,255))
                screen.blit(s, (loc1x,loc2y))
        else:
            if loc2y<loc1y:
                s = pygame.Surface((loc1x-loc2x,loc1y-loc2y))
                s.set_alpha(128)
                s.fill((255,255,255))
                screen.blit(s, (loc2x,loc2y))
            else:
                s = pygame.Surface((loc1x-loc2x,loc2y-loc1y))
                s.set_alpha(128)
                s.fill((255,255,255))
                screen.blit(s, (loc2x,loc1y))

class selection():
    def __init__(self):
        self.rect=selection_summon()
        self.rect.make("selectionbox",(0,255,0))
        self.current_pos=pygame.mouse.get_pos()
        self.end_pos=None
    def make(self):
        self.start_pos=pygame.mouse.get_pos()
    def draw(self,screen):
        self.current_pos=pygame.mouse.get_pos()
        self.rect.draw(self.start_pos,self.current_pos,screen)

class house_set(store):
    def make(self):
        loc=pygame.mouse.get_pos()
        loc=[loc[0]-5,loc[1]-5]
        rectangle=rect_summon()
        rectangle.make(len(self.dict)+1,"black",loc,10,10)
        house_created=house_summon(len(self.dict)+1,loc,rectangle)
        self.add(house_created)
        return rectangle

class house_summon(store):
    def __init__(self,tag,loc,obj):
        super().__init__()
        self.tag=tag
        self.loc=loc
        self.loc2=[loc[0]+5,loc[1]+5]
        self.obj=obj

class person_set(store):
    def __init__(self,housing):
        super().__init__()
        self.people=[]
        self.moveinglist=[]
        self.infected=0
        self.housing=housing
        f = open("person.txt", "r")
        l=f.read().splitlines()
        newlist=[]
        newlist2={}
        for x in l:
            newlist.append(x.split(" ")[0])
        for x in newlist:
            newlist2[x.split("=")[0]]=x.split("=")[1]
        self.dict=newlist2
    def make(self):
        if self.dict["spawn"]!="None":
            house=self.housing.dict[random.randint(1,len(self.housing.dict))]
        else:
            house=None
        vars=self.dict
        person=person_summon(house,vars)
        self.people.append(person)

class person_summon(pygame.sprite.Sprite):
    def __init__(self,house,vars,colour="blue") :
        self.dict={}
        self.tag=''.join(random.choice("aqwsderfgtyhjuiklopmnbvcxz") for i in range(20))
        self.house=house
        self.vars=vars
        self.dict["infected"]=(random.random()<float(self.vars["infection_chance"]))
        self.dict["inHouse"]=(self.vars["spawn"]!="None")
        self.dict["goto"]=None
        self.dict["gotoHouse"]=None
        self.dict["loc"]=self.house.loc2
        self.temppath=[]
        self.width=self.dict["loc"][0]
        self.height=self.dict["loc"][1]
        self.radius=23
        self.image = pygame.Surface([100, 100])
        self.colour = colour
        self.rect = self.image.get_rect()
        self.rect.center = (self.width, self.height)
        self.image.fill("red")
        
        super().__init__()

    def move(self,screen):
        try:
            self.draw_circ(screen)
            self.image.fill("red")
            self.rect.x=self.path[0][0]
            self.rect.y=self.path[0][1]
            del self.path[0]
        except:
            self.kill()

    def update(self,num,screen):
        if num==0:
            self.move(screen)
        else:
            self.draw_circ(screen)

    def draw_circ(self,screen):
        try:
            pygame.draw.circle(screen, self.colour, (self.path[0][0],self.path[0][1]), 5)
        except:
            self.kill()
    def change_colour(self,colour):
        self.colour=colour

class person_summon2(store):
    def __init__(self,house,vars,moveinglist):
        super().__init__()
        self.tag=''.join(random.choice("aqwsderfgtyhjuiklopmnbvcxz") for i in range(20))
        self.house=house
        self.vars=vars
        self.circ=None
        self.temppath=[]
        self.moveinglist=moveinglist
        self.setup()

    def setup(self):
        self.dict["infected"]=(random.random()<float(self.vars["infection_chance"]))
        self.dict["inHouse"]=(self.vars["spawn"]!="None")
        self.dict["goto"]=None
        self.dict["gotoHouse"]=None
        self.dict["loc"]=self.house.loc2
        

    def make(self):
        g=circle_summon()
        if self.dict["infected"]==True:
            g.make(self.tag,"red",self.dict["loc"])
        else:
            g.make(self.tag,"blue",self.dict["loc"])
        self.circ=g
        return g

    def draw(self,screen):
        self.circ.draw(screen)
    def change_colour(self,colour):
        self.circ.colour=colour

    def move(self):
        try:
            self.dict["loc"]=self.path[0]
            self.make()
            del self.path[0]
        except:
            self.moveinglist.remove(self)

    def in_house(self):
        return self.dict["inHouse"]




def distance(start,end):
    return ((start[0] - end[0]) ** 2) + ((start[1] - end[1]) ** 2)

def get_path(start,end):
    array=[]
    adj=[[0, -1], [0, 1], [-1, 0], [1, 0],[-1, -1], [-1, 1], [1, 1], [1, -1]]
    current=start
    shortest=current
    running=True
    while running== True:
        shortest_dist=distance(current,end)
        for x in adj:
            pos=[current[0]+x[0],current[1]+x[1]]
            dist=distance(pos,end)
            if shortest_dist>=dist:
                shortest=pos
                current=pos
                shortest_dist=dist
        if shortest==end:
            running=False
        array.append(shortest)
    return array


def switch_arr(arr):
    new_arr=[]
    for x in range(len(arr)):
        g=x+1
        new_arr.append(arr[-g])
    new_arr.pop(0)
    return new_arr

class path_store_set(store):
    def add(self,obj,obj1):
        self.dict[str([obj[0].tag,obj[1].tag])]=[obj1,switch_arr(obj1)]
    def get_dir(self,house1,house2):
        if house1!=None and house2!=None :
            for x in self.dict:
                list_one= eval(x)
                if house1.tag in list_one:
                    if house2.tag in list_one:
                        arr=self.dict[x]
                        if list_one.index(house1.tag)==0:
                            return arr[0].copy()
                        if list_one.index(house2.tag)==0:
                            return arr[1].copy()

