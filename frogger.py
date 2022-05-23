#!/usr/bin/env python3

import time
import os
import random

from graphics import *
from screeninfo import get_monitors


settings = {
    "road_lanes": 6,
    "river_lanes": 4,
    "max_mobs_per_lane": 3,
    "dist_between_mobs": 450,
    "mob_length": 200,
    "mob_speed": 10,
    "log_speed_min": 2,
    "log_speed_max": 10,
    "car_speed_min": 6,
    "car_speed_max": 16,
    "spawn_rate": 10,
    "spawn_rate_lane": 100,
    "window_x": 800,
    "window_y": 600,
    "frame_rate": 30,
}

car_colors = ["black","green4","blue3","red","white","gray","yellow","orange"]


def init():
    clearscreen()
    print("Welcome!")
    time.sleep(0.25)
    clearscreen()
    collect_screen_info()
    
def collect_screen_info():
    print("Monitor info:")
    try:
        for m in get_monitors():
            print(m)
        settings["window_x"] = m.width
        settings["window_y"] = m.height - 100
    except:
        print("Could not gather screen info! Using default 800x600")
    
def clearscreen():
    os.system("clear")
    
def open_window():
    win = GraphWin("Frogger",settings["window_x"],settings["window_y"],autoflush=False)
    win.setBackground("black")
    return(win)

def close_window(win):
    win.close()
    
def main():
    win = open_window()
    
    draw_menu(win)
    
    close_window(win)
    
    
def calc_button_size():
    button_width = int(settings["window_x"]/3)
    button_height = 50
    return(button_width,button_height)
    
def draw_menu(win):
    to_draw = []
    buttons = []
    centerX = settings["window_x"]/2
    centerY = settings["window_y"]/2
    lines = [75,125]

    title = Text(Point(centerX,lines[0]),"Frogger")
    title.setTextColor("white")
    title.setSize(30)
    title.setStyle("bold")
    to_draw.append(title)
    
    subtitle = Text(Point(centerX,lines[1]),"Slam Jones 2022")
    subtitle.setTextColor("white")
    subtitle.setSize(16)
    to_draw.append(subtitle)
    
    button_width,button_height = calc_button_size()
    buttons_text = ["Start","Settings","Quit"]
    
    P1X = centerX - (button_width/2)
    P2X = P1X + button_width
    P1Y = centerY - (button_height*2)
    P2Y = P1Y + button_height
    
    for item in buttons_text:
        button = Rectangle(Point(P1X,P1Y),Point(P2X,P2Y))
        button.setOutline("white")
        button.setFill("green4")
        button.setWidth(3)
        
        button_text = Text(Point((P1X+P2X)/2,(P1Y+P2Y)/2),item)
        button_text.setTextColor("white")
        button_text.setStyle("bold")
        button_text.setSize(12)
        
        to_draw.append(button)
        to_draw.append(button_text)
        
        buttons.append({"rect": button, "text": button_text,})
        
        P1Y = P2Y + button_height
        P2Y = P1Y + button_height
    
    for item in to_draw:
        item.draw(win)
    win.update()
    
    choice = ""
    
    while choice != "Quit":
        choice = ""
        click = win.getMouse()
        clickX = click.getX()
        clickY = click.getY()
        for button in buttons:
            P1X = button["rect"].getP1().getX()
            P1Y = button["rect"].getP1().getY()
            P2X = button["rect"].getP2().getX()
            P2Y = button["rect"].getP2().getY()

            if clickX >= P1X and clickX <= P2X and clickY >= P1Y and clickY <= P2Y:
                flash_button(win,button)
                choice = button["text"].getText()
    
        if choice == "Start":
            for item in to_draw:
                item.undraw()
                
            draw_game(win)
            
            for item in to_draw:
                item.draw(win)
        elif choice == "Settings":
            pass
            #draw_info_box(win,"Coming soon!")
        elif choice == "Quit":
            break
            
            
def redraw(win,item):
    item.undraw()
    item.draw(win)
                
            
def draw_game(win):
    to_draw = []
    lanes = []
    draw_mobs = []
    undraw_mobs = []
    fell = False
    
    road_lanes = settings["road_lanes"]
    river_lanes = settings["river_lanes"]
    
    total_lanes = road_lanes + river_lanes + 2
    
    lane_height = settings["window_y"] / total_lanes
    
    P1X = 0
    P2X = settings["window_x"]
    P1Y = 0
    P2Y = lane_height
    
    
    ##### Create lanes and assign values
    for i in range(total_lanes):
        lane = Rectangle(Point(P1X,P1Y),Point(P2X,P2Y))
        if i > 0 and i <= river_lanes:
            lane.setFill("blue")
            l_type = "river"
            lane_speed = random.randrange(settings["log_speed_min"],settings["log_speed_max"])
        elif i > river_lanes and i <= road_lanes+river_lanes:
            lane.setFill("gray")
            l_type = "road"
            lane_speed = random.randrange(settings["car_speed_min"],settings["car_speed_max"])
        else:
            lane.setFill("green")
            l_type = "grass"
            lane_speed = 0
        to_draw.append(lane)
        
        #### lane_full object should contain all data needed to interact with it
        lane_full = {"lane": lane, "type": l_type, "mobs": [], "direction": "right", "last_spawn": 1000, "speed": lane_speed}
        if random.choice([True,False]):
            lane_full["direction"] = "left"
        
        lanes.append(lane_full)

        ##### Set positions for next lane
        P1Y = P2Y
        P2Y += lane_height
        
    frog = Circle(
        Point(settings["window_x"]/2, settings["window_y"] - lane_height/2),lane_height/4)
    frog.setFill("white")
    frog.setOutline("black")
    frog.setWidth(3)
    to_draw.append(frog)
        
    for item in to_draw:
        item.draw(win)
    win.update()
        
    key = ""
    last_spawn = 1000
    timer = 1
    lowest_fps = 1000
    avg_fps = 0
    frames = 0
    ticks = 0
    efps = 0
    start_time = time.time()
    
    ##### MAIN PLAY LOOP #####
    while key != "Escape":
        ##### Timer fucntions for calculating effective frame rate
        ##### Probably slows the whole thing down
        ##### But it can help identify issues
        
        clearscreen()
        timer = time.time() - start_time
        print("Last tick: "+str(round(timer,3)/1000)+"ms")
        frames += efps
        ticks += 1
        avg_fps = frames/ticks
        efps = int(1/timer)
        print("TARGET FPS: "+str(settings["frame_rate"]))
        print("Average fps: "+str(round(avg_fps)))
        print("Effective fps: "+str(efps))
        if efps < lowest_fps:
            lowest_fps = efps
        print("Lowest fps: "+str(lowest_fps))
        start_time = time.time()
        
        last_spawn += 1
        for lane in lanes:
            lane["last_spawn"] += 1
        key = win.checkKey()
        
        if key == "Up":
            if check_bounds(win,frog,key,lane_height):
                frog.move(0,-lane_height)
        elif key == "Down":
            if check_bounds(win,frog,key,lane_height):
                frog.move(0,lane_height)
        elif key == "Left":
            if check_bounds(win,frog,key,lane_height):
                frog.move(-lane_height/2,0)
        elif key == "Right":
            if check_bounds(win,frog,key,lane_height):
                frog.move(lane_height/2,0)
        
        #### Check for victory/fail conditions
        if frog.getCenter().getY() < lane_height:
            draw_info_box(win,"You win!")
            break
            
        #print(str(time.time() - start_time)+" time taken to process user input")

        #### Pick a random lane
        #### Spawn mobs if needed
        lane = random.choice(lanes)
        if last_spawn >= settings["spawn_rate"]:
            #### Check if less than max is on the lane ####
            #### Make sure it is not a grass lane ####
            #### Make sure enough time has passed since last spawn on this lane
            #### And make sure enough time has passed total
            if len(lane["mobs"]) < settings["max_mobs_per_lane"] and lane["type"] != "grass" and lane["last_spawn"] >= settings["spawn_rate_lane"]:
                print("Last spawn: "+str(lane["last_spawn"]/1000)+"ms")
                mob = spawn_mob(win,lane,lane_height,lane["direction"])
                redraw(win,frog)
                lane["mobs"].append(mob)
                draw_mobs.append(mob)
                last_spawn = 0
                lane["last_spawn"] = 0
                #print("Spawned mob")
                
        #print(str(time.time() - start_time)+" time taken to spawn mobs")
        
        #### Move all mobs in all lanes
        moved = 0
        for lane in lanes:
            for mob in lane["mobs"]:
                moved += 1
                if lane["direction"] == "right":
                    mob.move(lane["speed"],0)
                    #mob.move(settings["mob_speed"],0)
                    
                    if mob.getP1().getX() > settings["window_x"]:
                        lane["mobs"].remove(mob)
                        undraw_mobs.append(mob)

                if lane["direction"] == "left":
                    mob.move(-lane["speed"],0)
                    if mob.getP2().getX() < 0:
                        lane["mobs"].remove(mob)
                        undraw_mobs.append(mob)
        print("Moved {} mobs".format(str(moved)))
                        
        #print(str(time.time() - start_time)+" time taken to move mobs")
                
        #### If any need to be drawn or undrawn, do so now                
        for mob in draw_mobs:
            mob.draw(win)
            print(str(len(draw_mobs))+" mobs drawn")
        draw_mobs.clear()
        for mob in undraw_mobs:
            mob.undraw()
            print(str(len(undraw_mobs))+" mobs undrawn")
        undraw_mobs.clear()
        
        #print(str(time.time() - start_time)+" time taken to draw/undraw mobs")
        
        #### Check for collision
        #### Perhaps instead of checking each lane, assign a value to frog...
        #### ...which represents the lane that the frog is in
        frogY = frog.getCenter().getY()
        frogX = frog.getCenter().getX()
        for lane in lanes:
            if frogY > lane["lane"].getP1().getY() and frogY < lane["lane"].getP2().getY():
                #### Fell state indicates the frog died
                #### For road/grass lanes, default state is NOT fell
                #### For river lanes, default state is fell
                #### This state is reversed if frog is within bounds of a log
                if lane["type"] == "river":
                    fell = True
                for mob in lane["mobs"]:
                    P1X = mob.getP1().getX()
                    P1Y = mob.getP1().getY()
                    P2X = mob.getP2().getX()
                    P2Y = mob.getP2().getY()

                    if lane["type"] == "road":
                        if frogX > P1X and frogX < P2X and frogY > P1Y and frogY < P2Y:
                            fell = True
                    elif lane["type"] == "river":
                        if frogX > P1X and frogX < P2X and frogY > P1Y and frogY < P2Y:
                            fell = False
                            if lane["direction"] == "right":
                                frog.move(lane["speed"],0)
                            else:
                                frog.move(-lane["speed"],0)
        if fell or (frogX < 0 or frogX > settings["window_x"]):
            draw_info_box(win,"Oops!  You lose!")
            key = "Escape"
            break
            
        print(str((time.time() - start_time)/1000)+"ms taken to check collision")
        print(str((time.time() - start_time)/1000)+"ms taken total per tick")
                    
        #### Attempted frame rate is defined in settings
        update(settings["frame_rate"])
        
    #### When player has hit "Escape" key, proceed to erase playfield
    for item in to_draw:
        item.undraw()
    for lane in lanes:
        for mob in lane["mobs"]:
            mob.undraw()
        
        
def spawn_mob(win,lane,lane_height,lane_direction):
    #lane_centerX = (lane["lane"].getP1().getX() + lane["lane"].getP2().getX()) / 2
    lane_centerX = (lane["lane"].getP1().getY() + lane["lane"].getP2().getY()) / 2
    #print("Lane: "+str(lane))
    #print("Lane_centerX = "+str(lane_centerX))
    mob_height = lane_height * 0.9
    
    #### All mobs are spawning in the same lane!!!  WTF!!!
    
    P1Y = lane_centerX - (mob_height/4)
    #P1Y = lane_centerX + (mob_height/4)
    if lane_direction == "right":
        P1X = 0 - settings["mob_length"]
    elif lane_direction == "left":
        P1X = settings["window_x"] + settings["mob_length"]
    P2Y = P1Y + (mob_height/2)
    P2X = P1X + settings["mob_length"]
    
    mob = Rectangle(Point(P1X,P1Y),Point(P2X,P2Y))
    if lane["type"] == "road":
        color = random.choice(car_colors)
        mob.setFill(color)
    elif lane["type"] == "river":
        mob.setFill("brown")
    mob.setOutline("white")
    mob.setWidth(3)
    return(mob)
        
        
def check_bounds(win,frog,direction,move_dist):
    frogX = frog.getCenter().getX()
    frogY = frog.getCenter().getY()
    
    if direction == "Up":
        if frogY - move_dist < 0:
            return(False)
        return(True)
    elif direction == "Down":
        if frogY + move_dist > settings["window_y"]:
            return(False)
        return(True)
    elif direction == "Left":
        if frogX - move_dist < 0:
            return(False)
        return(True)
    elif direction == "Right":
        if frogX + move_dist > settings["window_x"]:
            return(False)
        return(True)
    
    
def draw_info_box(win,message):
    centerX = settings["window_x"]/2
    centerY = settings["window_y"]/2
    
    button_width,button_height = calc_button_size()
    
    P1X = centerX - button_width/2
    P2X = P1X + button_width
    P1Y = centerY - button_height/2
    P2Y = P1Y + button_height
    
    box = Rectangle(Point(P1X,P1Y),Point(P2X,P2Y))
    box.setFill("black")
    box.setOutline("white")
    box.setWidth(5)
    
    b_text = Text(Point(centerX, centerY), message)
    b_text.setSize(16)
    b_text.setStyle("bold")
    b_text.setTextColor("white")
    
    box.draw(win)
    b_text.draw(win)
    
    win.getKey()
    
    box.undraw()
    b_text.undraw()
    
    
def flash_button(win,button):
    button["rect"].setFill("white")
    button["rect"].setOutline("green4")
    button["text"].setTextColor("green4")
    
    win.update()
    time.sleep(0.05)
    
    button["rect"].setFill("green4")
    button["rect"].setOutline("white")
    button["text"].setTextColor("white")
    
    win.update()

    

def farewell():
    clearscreen()
    print("Farewell!")
    time.sleep(0.05)
    clearscreen()




init()
main()
farewell()
