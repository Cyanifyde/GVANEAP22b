
import random
import os
import psutil
import shutil
import threading
import math
import sys
#import matplotlib.pyplot as plt

def quit():
    pygame.quit()
    sys.exit()


def change_to_scene_1():
    global switch
    switch=1
    object_list.remove_set(["runmain","exit"])
    object_list.add_set([summonhouse,summonperson,startsim,simsettings])
    object_list.add([tellformenu,tellformenu2])

def change_to_scene_2():
    global switch
    switch=2
    object_list.remove_all_set()
    place_house()

def change_to_scene_3():
    check_file()
    change_to_scene_1()

def create_paths():
    global path_store
    path_store=path_store_set()
    g=house_list.dict.keys()
    g=list(g)
    for i, x in enumerate(g):
        x1=house_list.dict[x]
        for y in g[i+1:]:
            y2=house_list.dict[y]
            path=get_path(x1.loc2,y2.loc2)
            path_store.add([x1,y2],path)
            
def change_to_scene_5():
    global switch
    global group_people
    group_people=pygame.sprite.Group()
    global infectedlist
    infectedlist=pygame.sprite.Group()
    global noninfectedlist
    noninfectedlist=pygame.sprite.Group()
    switch=3
    object_list.remove_all_set()
    numcounter=button_summon()
    numcounter.no_box("numcounter","0",[10,10])
    object_list.add(numcounter)
    infectcounter=button_summon()
    infectcounter.no_box("infectcounter","0",[10,30])
    object_list.add(infectcounter)
    place_house()
    global people_group
    people_group=person_set(house_list)
    create_paths()
    for x in range(int(people_group.dict["initial_summon"])):
        people_group.make()
    people_group.infected=0
    for x in people_group.people:
        if x.dict["infected"]:
            people_group.infected+=1
            x.colour="red"
            infectedlist.add(x)
        else:
            noninfectedlist.add(x)

    

def check_file():
    # check if file is open
    os.startfile("person.txt")
    running=True
    while running==True:
        # check if file is open and if it is then wait
        running="notepad.exe" in (i.name() for i in psutil.process_iter())

def back_to_menu():
    global switch
    switch=0
    object_list.remove_set("menu")
    object_list.add_set([runmain,exit])

def create_place_house():
    # create houses and place them on the screen
    rect=house_list.make()
    object_list.add(rect)

def place_house():
    # place houses on the screen
    for x in house_list.dict:
        object_list.add(house_list.dict[x].obj)

def get_random_bool(chance):
    # get a random bool with a chance of chance
    if random.random()<chance:
        return True
    else:
        return False

def check_collision():
    # check if people collide with each other
    for x in infectedlist.sprites():
        # uses sprite collision
        blocks_hit_list = pygame.sprite.spritecollide(x, group_people, False, pygame.sprite.collide_circle)
        for y in blocks_hit_list:
            # if they collide then check if the other person is infected
            if y.dict["infected"]:
                pass
            else:
                try:
                    #draw line between them
                    pygame.draw.line(screen,"black",x.path[0],y.path[0])
                except:
                    pass
                # if they are not infected then check if they get infected
                chance=float(people_group.dict["infection_chance_spread"])
                if get_random_bool(chance):
                    if y.dict["infected"]==False:
                        y.dict["infected"]=True
                        y.change_colour("red")
                        people_group.infected+=1
                # if they are infected then check if they die
                if get_random_bool(float(people_group.dict["die_chance"])):
                    people_group.infected-=1
                    try:
                        people_group.people.remove(x)
                    except:
                        pass
                # if they are infected then check if they get better
                elif get_random_bool(float(people_group.dict["get_better_chance"])):
                    people_group.infected-=1
                    x.dict["infected"]=False
                    x.change_colour("blue")

def move_check_new():
    # check if people move
    for x in (people_group.people):
        # if they are not in a house then check if they move
        if get_random_bool(float(people_group.dict["move_chance"])):
            if x not in group_people.sprites():
                # if they move then get a random house and move to it
                y=house_list.dict[random.randint(1,len(house_list.dict))]
                g=y.loc
                if x.house.loc!=y.loc:
                    # if they are not in the house then move to the house
                    x.dict["goto"]=[g[0]+5,g[1]+5]
                    x.dict["inHouse"]=False
                    x.dict["gotoHouse"]=y
                    x.path=path_store.get_dir(x.house,y)
                    x.house=y
                    if x.dict["infected"]:
                        infectedlist.add(x)
                    else:
                        noninfectedlist.add(x)
                    group_people.add(x)

def scene_main_menu(running,num,select_run):
    num+=1
    screen.fill("black")
    if num>=len(image_of_house_run):
        num=0

    # check for events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            num=0

        # check if mouse is lifted after clicked
        if event.type == pygame.MOUSEBUTTONUP:
            select_run=False

        # check if mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            select_run=True
            select.make()
            buttons.check(buttons)

    # draw the background
    screen.blit(image_of_house_run[num], (0, 0))
    for x in object_list.dict:
        object_list.dict[x].draw(screen)
    if select_run==True:
        select.draw(screen)
    
    buttons.check_hover(buttons)

    return [running,num,select_run]

def scene_initialise(running,num,select_run):
    
    screen.fill("black")

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            quit()
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            select_run=False

        if event.type == pygame.MOUSEBUTTONDOWN:
            select_run=True
            select.make()
            buttons.check(buttons)

        # check if key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                object_list.remove_all_set()
                object_list.add_set(menu)

        # check if key is lifted
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                object_list.remove_all_set()
                object_list.add_set([summonhouse,summonperson,simsettings,startsim])
                object_list.add([tellformenu,tellformenu2])
   
    for x in object_list.dict:
        object_list.dict[x].draw(screen)
    if select_run==True:
        select.draw(screen)

    buttons.check_hover(buttons)

    return [running,num,select_run]

def scene_place_houses(running,num,select_run):
     
    screen.fill("white")

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            quit()
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            pass

        if event.type == pygame.MOUSEBUTTONDOWN:
            create_place_house()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                select_run=False
                change_to_scene_1()
   
    for x in object_list.dict:
        object_list.dict[x].draw(screen)

    buttons.check_hover(buttons)

    return [running,num,select_run]


from sys import getsizeof
def scene_simulation(running,num,select_run,speed=5,num2=0,time_elapsed_since_last_action=0,values={},values2={}):
    num+=1
    num2+=1
    
    if num%speed==0 or speed==1:
        screen.fill("white")
        check_collision()
        move_check_new()
        group_people.update(0,screen)
        num=0

    #group_people.update(1,screen)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                people_group.make()
            if event.key == pygame.K_UP:
                speed-=1
            if event.key == pygame.K_DOWN:
                speed+=1
            if event.key == pygame.K_LEFT:
                """plt.plot(values.keys(), values.values(),label = "line 1")
                plt.plot(values2.keys(), values2.values(), label = "line 2")
                plt.xlabel('x - axis')
                plt.ylabel('y - axis')
                plt.title('My first graph!')
    
                plt.show()"""

    if speed<1:
        speed=1
    
    # draw the scene
    for x in object_list.dict:
        object_list.dict[x].draw(screen)
    
    # gets the time since the last frame
    dt = clock.get_time() 
    num2+=time_elapsed_since_last_action
    time_elapsed_since_last_action += dt
    # checks if 200ms has passed since the last action
    if time_elapsed_since_last_action > 200:

        if people_group.infected<0:
            people_group.infected=0
        object_list.dict["numcounter"].change_text_nobox(str(len(people_group.people)))
        object_list.dict["infectcounter"].change_text_nobox(str(people_group.infected))
        
        time_elapsed_since_last_action = 0
        # saves the number of people and the number of infected people
        values[num2/10000]=len(people_group.people)
        values2[num2/10000]=people_group.infected
    return [running,num,select_run,speed,num2,time_elapsed_since_last_action,values,values2]

import pygame
from zurich import *

pygame.init()
pygame.display.set_caption('NEA')

# load the icon and images
Icon = pygame.image.load('images/a.png')
image = pygame.image.load('images/house1.png')
main_image1 = pygame.transform.scale(image, (500, 500))
image = pygame.image.load('images/house3.png')
main_image3 = pygame.transform.scale(image, (500, 500))
image = pygame.image.load('images/house5.png')
main_image5 = pygame.transform.scale(image, (500, 500))
image = pygame.image.load('images/house4.png')
main_image4 = pygame.transform.scale(image, (500, 500))
image = pygame.image.load('images/house2.png')
main_image2 = pygame.transform.scale(image, (500, 500))
image_of_house_run=[main_image1,main_image3,main_image5,main_image4,main_image2]
from pygame.locals import FULLSCREEN,DOUBLEBUF,RESIZABLE,OPENGL,HWSURFACE
pygame.display.set_icon(Icon)
args=DOUBLEBUF |HWSURFACE 
screen = pygame.display.set_mode([500,500],args,8)
clock = pygame.time.Clock()
time= pygame.time
num=0

select=selection()
select_run=False

object_list=objects()
buttons=buttons_set()

object_list.button_store(buttons)

runmain=button_summon()
runmain.make("runmain","blue","white",[250,130],"Run Simulation Startup",change_to_scene_1)

exit=button_summon()
exit.make("exit","blue","white",[250,160],"Quit",quit)

object_list.add_set([exit,runmain])

summonhouse=button_summon()
summonhouse.make("summonhouse","blue","white",[80,20],"Place houses",change_to_scene_2)

summonperson=button_summon()
summonperson.make("summonperson","blue","white",[80,50],"Summon Person",change_to_scene_3)

simsettings=button_summon()
simsettings.make("simsettings","blue","white",[80,80],"Simulation settings",None)

startsim=button_summon()
startsim.make("startsim","blue","white",[80,110],"Start Simulation",change_to_scene_5)

menu=button_summon()
menu.make("menu","blue","white",[80,20],"Menu Screen",back_to_menu)

goto_sim_menu=button_summon()
goto_sim_menu.make("simmenu","blue","white",[80,20],"Simulation menu",change_to_scene_1)

tellformenu=button_summon()
tellformenu.make("tellformenu","blue","white",[80,140],"press escape",None)

tellformenu2=button_summon()
tellformenu2.make("tellformenu2","blue","white",[80,160],"to get menu",None)

chnagefile=button_summon()
chnagefile.make("chnagefile","blue","white",[250,130],"Change the items in the file, and save when done",None)

house_list=house_set()

args=[True,num,select_run]
switch=0
num=0
running = True
while running:
    # main loop
    pygame.display.set_caption("Fps: " + str(int(clock.get_fps())))
    if switch==0:
        # runs the scene
        args=scene_main_menu(*args)
        #updates the screen
        pygame.display.flip()
        # sets the fps
        clock.tick(10)
    if switch==1:
        args=scene_initialise(*args)
        pygame.display.flip()
        clock.tick(50)
    if switch==2:
        args=scene_place_houses(*args)
        pygame.display.flip()
        clock.tick(50)

    if switch==3:
        args=scene_simulation(*args)
        pygame.display.flip()
        clock.tick()
    num+=1
    # updates the variables
    running= args[0]