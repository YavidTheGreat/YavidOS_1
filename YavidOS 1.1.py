import time
import sys, subprocess
import keyboard # pip install this in CMD
import copy
import math as m
import os
import threading
import ctypes
std_out_handle = ctypes.windll.kernel32.GetStdHandle(-11)
from playsound import playsound #pip install playsound THEN do: pip install playsound==1.2.2
global screen_clearer
screen_clearer = 0

class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

#Initial universal subprograms

def write_rewrite():
    ctypes.windll.kernel32.SetConsoleCursorPosition(std_out_handle, COORD(0, 0))

def play_sound():
    #playsound(r'C:\Users\david\Desktop\YavidOS_jingle1.mp3')    # Replace C:\Users\david\Desktop\YavidOS_jingle.mp3 with the path to your audio file
    ()


def clear_screen():
    operating_system = sys.platform

    if operating_system == 'win32':
        subprocess.run('cls', shell=True)
clear_screen()

class PixelDisplay:
    def __init__(self, width, height):
        global canvas_external
        self.width = width
        self.height = height
        self.canvas = [[" "] * width for i in range(height)] # initilise the canvas with spaces and resolution as 2d list
        canvas_external = self.canvas

    def set_pixel(self, x_across, y_vertical, character):
        if 0 <= x_across < self.width and 0 <= y_vertical < self.height:
            self.canvas[y_vertical][x_across] = str(character)
        else:
            print(f"Tried to set the pixel ({x_across}, {y_vertical}) and it is out of bounds")

    def clear(self):
        self.canvas = [[" "] * self.width for i in range(self.height)] # clears it back to spaces

    def render(self):
        for row in self.canvas:
            print("".join(row))

def line_joiner(x1, y1, x2, y2):
    
    line_points = []
    dx = abs(x2 - x1)   #gradients
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1  # Step direction for x
    sy = 1 if y1 < y2 else -1  # Step direction for y
    err = dx - dy

    while True:
        line_points.append([x1, y1])    # add current point to list
        if x1 == x2 and y1 == y2:       # stop if the endpoint is reached
            break
        e2 = 2 * err
        if e2 > -dy:        # the actual hokery pokery of the maths
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

    return line_points


def drawBoundingBox():    # Draw the bounding box
    global terminalEdges

        # return coordinates for the bounding box for the terminal window
    topLine = line_joiner(0, 0, width_res - 1, 0)  # Top border
    bottomLine = line_joiner(0, height_res - 1, width_res - 1, height_res - 1)  # Bottom border
    leftLine = line_joiner(0, 0, 0, height_res - 1)  # Left border
    rightLine = line_joiner(width_res - 1, 0, width_res - 1, height_res - 1)  # Right border
    boundingBox = topLine + bottomLine + leftLine + rightLine

    if terminalEdges == "Y":
        for x, y in boundingBox:
            terminal.set_pixel(x, y, "█")


def get_coordinates_in_range(start_row, start_col, rows, cols): #return all of the coordinates within an specified area for use with app icons
    coordinates = []
    for row in range(start_row, start_row + rows):
        for column in range(start_col, start_col + cols):
            coordinates.append([column, row])
    return coordinates


#Initial Variable for technicalities within 

mode = str(input("Enter mode (1 = custom, 2 = preset (recommended)): "))

if mode == "1":
    height_res = int(input("Enter the vertical resolution of desired console window (rec 50): "))     # terminal display resolution setting
    width_res = int(input("Enter the horizontal resolution of desired console window (rec 200): ")) 
    terminal = PixelDisplay(width_res, height_res)  # make the pixel display initilise the resolution

    terminalEdges = str(input("Do you want the terminal to have a bounding box? (Y or N): "))        # do you want edges
    while terminalEdges != "Y" and terminalEdges != "N":
        terminalEdges = str(input(f"Type a Y for yes or N for no (your answer was: {terminalEdges}): "))

    frameSpeed = str(input("Enter the framerate (recommended 20): "))                        # what framerate
    for decimal in frameSpeed:
        integerisedFrameSpeed = decimal.replace(".", "", 1)
    while integerisedFrameSpeed.isnumeric() != True:
        frameSpeed = input(f"Enter the framerate as a number or decimal (you entered {frameSpeed}) (recommended 20): ")
    frameSpeed = abs(float(frameSpeed))

elif mode == "2":
    height_res = 50
    width_res = 200
    terminal = PixelDisplay(width_res, height_res)
    frameSpeed = 20
    terminalEdges = "Y"

else:
    print("wrong input i hate you")


sound_thread = threading.Thread(target=play_sound)
sound_thread.start()


# contained cursor implementation

cursor_pos_1 = [(height_res//2), (width_res//2)]    #intially cursor at centre
def show_cursor():
    global height_res, width_res, cursor_pos_1
    cursor_font = "𝕏"   # to be changed in settings

    terminal.set_pixel(cursor_pos_1[1],cursor_pos_1[0], cursor_font)
    
    if keyboard.is_pressed("up") and not (keyboard.is_pressed("down") or keyboard.is_pressed("right") or keyboard.is_pressed("left")):
        cursor_pos_1[0] = cursor_pos_1[0] - 1

    elif keyboard.is_pressed("down") and not (keyboard.is_pressed("right") or keyboard.is_pressed("up") or keyboard.is_pressed("left")):
        cursor_pos_1[0] = cursor_pos_1[0] + 1

    elif keyboard.is_pressed("right") and not (keyboard.is_pressed("down") or keyboard.is_pressed("up") or keyboard.is_pressed("left")):
        cursor_pos_1[1] = cursor_pos_1[1] + 1

    elif keyboard.is_pressed("left") and not (keyboard.is_pressed("down") or keyboard.is_pressed("up") or keyboard.is_pressed("right")):
        cursor_pos_1[1] = cursor_pos_1[1] - 1

    elif keyboard.is_pressed("up") and keyboard.is_pressed("right"):
        cursor_pos_1[0] = cursor_pos_1[0] - 1
        cursor_pos_1[1] = cursor_pos_1[1] + 1

    elif keyboard.is_pressed("up") and keyboard.is_pressed("left"):
        cursor_pos_1[0] = cursor_pos_1[0] - 1
        cursor_pos_1[1] = cursor_pos_1[1] - 1

    elif keyboard.is_pressed("down") and keyboard.is_pressed("right"):
        cursor_pos_1[0] = cursor_pos_1[0] + 1
        cursor_pos_1[1] = cursor_pos_1[1] + 1

    elif keyboard.is_pressed("down") and keyboard.is_pressed("left"):
        cursor_pos_1[0] = cursor_pos_1[0] + 1
        cursor_pos_1[1] = cursor_pos_1[1] - 1



#Application functions -------------------------------------
#ideas - graphing calculator, paint program, hotbar application so you can remove it, file explorer, save variables from the actual screen, raycaster game

def taskBar():  #run in every program, can terminate it from the taskbar - HOME - OPTIONS - FILE - (game of choice) - (LIVE OS STATISTICS) - SHUT DOWN
    ()

# 2D Map (0 = empty space, 1 = wall)
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Player properties
player_x, player_y = 1.5, 1.5  # Starting position near a wall
player_angle = 0  # Looking straight to the right
FOV = m.pi / 3  # Field of view (60 degrees)
max_depth = 20  # Maximum ray distance
SCREEN_WIDTH = 200  # Reduced for simplicity in IDLE
SCREEN_HEIGHT = 50  # Reduced for simplicity in IDLE
an = 0.1
ad = 0.1
# ASCII characters for shading
SHADES = "█▓▒⣿░"

def walking_sim():
    def cast_rays():
        """Cast rays and calculate screen data."""
        screen = []
        for col in range(SCREEN_WIDTH):
            # Calculate the angle for this ray
            ray_angle = (player_angle - FOV / 2) + (col / SCREEN_WIDTH) * FOV
            ray_dir_x = m.cos(ray_angle)
            ray_dir_y = m.sin(ray_angle)

            distance = 0
            hit_wall = False

            while not hit_wall and distance < max_depth:
                distance += 0.1
                # Test where the ray hits in the grid
                test_x = int(player_x + ray_dir_x * distance)
                test_y = int(player_y + ray_dir_y * distance)

                # Check bounds
                if test_x < 0 or test_x >= len(MAP[0]) or test_y < 0 or test_y >= len(MAP):
                    hit_wall = True
                    distance = max_depth  # Pretend wall is at max distance
                elif MAP[test_y][test_x] == 1:  # Wall hit
                    hit_wall = True

            # Calculate wall height based on distance
            wall_height = int(SCREEN_HEIGHT / (distance if distance > 0 else 1))
            shade_index = min(len(SHADES) - 1, int(distance * (len(SHADES) / max_depth)))
            shade = SHADES[shade_index]

            # Create column
            column = [" "] * SCREEN_HEIGHT
            start = max(0, (SCREEN_HEIGHT - wall_height) // 2)
            end = min(SCREEN_HEIGHT, start + wall_height)
            for row in range(start, end):
                column[row] = shade
            screen.append(column)

        return screen

    def render_screen(screen):
        """Render the calculated screen to the terminal."""
        write_rewrite()
        rows = []
        for row in range(SCREEN_HEIGHT):
            row_str = "".join(screen[col][row] for col in range(SCREEN_WIDTH))
            rows.append(row_str)
        frame = "\n".join(rows)
        print(frame)

    def game_loop():
        """Main game loop for movement and rendering."""
        global player_x, player_y, player_angle, screen_clearer

        while True:
            # Render the screen
            screen = cast_rays()
            render_screen(screen)

            # Player controls
            print("Use WASD to move (W: forward, S: backward, A/D: rotate left/right), Q to quit.")

            if keyboard.is_pressed("q") or keyboard.is_pressed("esc"):
                screen_clearer = 0
                print("Exiting game...")
                break

            elif keyboard.is_pressed("w+a"):
                new_x = player_x + m.cos(player_angle) * ad
                new_y = player_y + m.sin(player_angle) * ad
                if MAP[int(new_y)][int(new_x)] == 0:
                    player_x, player_y = new_x, new_y
                player_angle -= an

            elif keyboard.is_pressed("w+d"):
                new_x = player_x + m.cos(player_angle) * ad
                new_y = player_y + m.sin(player_angle) * ad
                if MAP[int(new_y)][int(new_x)] == 0:
                    player_x, player_y = new_x, new_y
                player_angle += an

            elif keyboard.is_pressed("s+a"):
                new_x = player_x - m.cos(player_angle) * ad # 0.1
                new_y = player_y - m.sin(player_angle) * ad # 0.1
                if MAP[int(new_y)][int(new_x)] == 0:
                    player_x, player_y = new_x, new_y
                player_angle -= an

            elif keyboard.is_pressed("s+d"):
                new_x = player_x - m.cos(player_angle) * ad # 0.1
                new_y = player_y - m.sin(player_angle) * ad # 0.1
                # Check for wall collision
                if MAP[int(new_y)][int(new_x)] == 0:
                    player_x, player_y = new_x, new_y
                player_angle += an

            elif keyboard.is_pressed("w"):
                new_x = player_x + m.cos(player_angle) * ad
                new_y = player_y + m.sin(player_angle) * ad
                if MAP[int(new_y)][int(new_x)] == 0:
                    player_x, player_y = new_x, new_y

            elif keyboard.is_pressed("s"):  # Move backward
                new_x = player_x - m.cos(player_angle) * ad # 0.1
                new_y = player_y - m.sin(player_angle) * ad # 0.1
                # Check for wall collision
                if MAP[int(new_y)][int(new_x)] == 0:
                    player_x, player_y = new_x, new_y

            elif keyboard.is_pressed("a"):  # Rotate left
                player_angle -= an
            elif keyboard.is_pressed("d"):# Rotate right
                player_angle += an

    # Start the game loop
    game_loop()



def painter():
    global cursor_pos_1, frameSpeed, canvasDrawing, screen_clearer
    penColor1 = "█"
    penColor2 = "▓"
    penColor3 = "▒"
    penColor4 = "░"
    canvasDrawing = []


    def line_tool():
        #print("line")
        ()

    def eraser_tool():
        #print("eraser")
        ()

    def sideBar():
        global mode
        mode = "BRUSH"

    def clear_canvas():
        global canvasDrawing
        if keyboard.is_pressed("C"):
            clear_screen()
            canvasDrawing = []


    def brush_tool(penColor):
        global mode, canvasDrawing
        if mode == "BRUSH":
            pixelToDraw = copy.deepcopy(cursor_pos_1)
            if keyboard.is_pressed("space") and (pixelToDraw not in canvasDrawing):
                canvasDrawing.append(pixelToDraw)  # needs to let it go to the next frame first

            for x, y in (canvasDrawing):
                terminal.set_pixel(y, x, penColor)

    while True:
        time.sleep(1/frameSpeed)
  
        if keyboard.is_pressed("esc"):
            screen_clearer = 0
            break

        #clear_screen()
        write_rewrite()
        terminal.clear()
        show_cursor()

        sideBar()
        brush_tool(penColor1)
        line_tool()
        eraser_tool()
        clear_canvas()

        drawBoundingBox()
        terminal.render()
        print("C     - clear canvas")
        print("SPACE - draw")
        print("ESC   - exit")




def lineDrawer():
    global target_across, target_height, origin, height_res, width_res, frameSpeed, screen_clearer
    target_across = 10  # initilise target position
    target_height = 10
    origin = [(height_res//2), (width_res//2)] #centre point for line to start from


    #Movement functions
    def up():
        global target_height
        target_height -= 1


    def down():
        global target_height
        target_height += 1


    def left():
        global target_across
        target_across -= 1


    def right():
        global target_across
        target_across += 1

    #Check the target isnt out of bounds, if it is go back to other side
    def checkTarget():
        global target_height, target_across
        if target_height > (height_res - 2):
            target_height = 2
        elif target_height < 2:
            target_height = height_res - 2
        elif target_across > (width_res - 2):
            target_across = 2
        elif target_across < 2:
            target_across = width_res - 2


    def keyLogger():
        global target_height, target_across
        if keyboard.is_pressed("up"):
            up()
        elif keyboard.is_pressed("down"):
            down()
        elif keyboard.is_pressed("left"):
            left()
        elif keyboard.is_pressed("right"):
            right()




    while True: # display the stuff
        write_rewrite()
        checkTarget()
        keyLogger()
        #clear_screen()
        terminal.clear()
            
        pixelListRaw = line_joiner(origin[1], origin[0], target_across, target_height)

        # Draw the line from origin to target
        pixelListRaw = line_joiner(origin[1], origin[0], target_across, target_height)
        for x, y in pixelListRaw:
            terminal.set_pixel(x, y, "0")

            # Draw the bounding box
        drawBoundingBox()
        terminal.render()
        if keyboard.is_pressed("esc"):
            screen_clearer = 0
            break
        time.sleep(1/frameSpeed)

#Application functions to appear on desktop and be run


def applications():
    #first app
    global cursor_pos_1
    application_region_1 = get_coordinates_in_range(3, 2, 10, 4)
    application_visible_area = copy.deepcopy(application_region_1)    #making a custom icon for it and making it all still so you can hover over and detect it
    application_visible_area.remove([2, 11])    # makes a copy so that i can change the visible area but not the area used to detect the cursor as they are normally linked
    application_visible_area.remove([2, 10])
    application_visible_area.remove([3, 9])
    application_visible_area.remove([3, 8])
    application_visible_area.remove([4, 7])
    application_visible_area.remove([4, 6])
    application_visible_area.remove([5, 5])
    application_visible_area.remove([5, 4])

    application_highlighting_1 = "█"

     # give it a name and make it print it underneath the icon
    appname1 = ["L", "I", "N", "E", "_", "T", "E", "S", "T", "E", "R"]
    for across in range(len(appname1)):
        terminal.set_pixel(across + 2, 6, appname1[across])

    if cursor_pos_1 in application_region_1 and keyboard.is_pressed("enter"):
        lineDrawer()
    elif cursor_pos_1 in application_region_1:
        application_highlighting_1 = "▒"

    for x, y in application_visible_area:
        terminal.set_pixel(y, x, application_highlighting_1)


    #2nd app (paint)
    application_region_2 = get_coordinates_in_range(3, 8, 10, 4)
    application_visible_area_2 = copy.deepcopy(application_region_2)
    application_visible_area_2.remove([8, 9])
    application_visible_area_2.remove([8, 4])
    application_visible_area_2.remove([10, 4])
    application_visible_area_2.remove([11, 5])
    application_visible_area_2.remove([11, 6])
    application_visible_area_2.remove([11, 7])
    application_visible_area_2.remove([11, 8])
    application_visible_area_2.remove([10, 9])
    
    application_highlighting_2 = "█"

    appname2 = ["P", "A", "I", "N", "T"]
    for across2 in range(len(appname2)):
        terminal.set_pixel(across2 + 5, 12, appname2[across2])

    if cursor_pos_1 in application_region_2 and keyboard.is_pressed("enter"):
        painter()
    elif cursor_pos_1 in application_region_2:
        application_highlighting_2 = "▒"

    for x, y in application_visible_area_2:
        terminal.set_pixel(y, x, application_highlighting_2)


    #walking game
    application_highlighting_3 = "█"
    appname3 = ["W", "A", "L", "K", "I", "N", "G", "_", "S", "I", "M"]
    application_region_3 = get_coordinates_in_range(3, 14, 10, 4)
    application_visible_area_3 = copy.deepcopy(application_region_3)
    for x, y in line_joiner(8, 16, 11, 14):
        application_visible_area_3.remove([y, x])


    for across3 in range(len(appname3)):
        terminal.set_pixel(across3 + 3, 18, appname3[across3])

    if cursor_pos_1 in application_region_3 and keyboard.is_pressed("enter"):
        walking_sim()
    elif cursor_pos_1 in application_region_3:
        application_highlighting_3 = "▒"

    for x, y in application_visible_area_3:
        terminal.set_pixel(y, x, application_highlighting_3)


# initial desktop visualisation


while True:
    write_rewrite()
    terminal.clear()
    drawBoundingBox()
    
    applications()
    show_cursor()   # cursor implementation
    
    #clear_screen()  
    terminal.render()
    print("cursor position:", cursor_pos_1, "screen_clearer: ", screen_clearer)
    print("GENERAL CONTROLLS INCLUDE: ESC - exit program")
    print("                    ARROW KEYS - move cursor + diagonally")
    print("                         ENTER - select highlighted task")
    if screen_clearer < 2:
        clear_screen()
        screen_clearer = screen_clearer + 1
    time.sleep(1/frameSpeed)