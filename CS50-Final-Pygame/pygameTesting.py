# import pygame library, also sys to allow for smooth program termination and cleanup operations
import pygame
import sys

# initialize all pygame modules
pygame.init()

# set clock and fps so game runs at intended speed
clock = pygame.time.Clock()
FPS = 60

# get display info/set default width/height of game screen
resolution = pygame.display.Info()

screen_width = 1920
screen_height = 1080

# if user resolution is lower than default, change it
if resolution.current_w < 1920 and resolution.current_h < 1080:
    screen_width = resolution.current_w
    screen_height = resolution.current_h

# set display, name display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sunset Run")

# fullscreen check variable so I can toggle between fs and windowed in game loop
not_fullscreen = False

# define game variables(scrolling)
scroll = 0

# load ground background layers so they can be set manually at different speeds (7.png, 8.png)
ground_image = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\Island\\Layers\\L5.png").convert_alpha()

# get ground background width and height
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

# load water layers
water_mountains = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\Island\\Layers\\L3.png").convert_alpha()
water_mountains_width = water_mountains.get_width()
water_mountains_height = water_mountains.get_height()

water_trees = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\Island\\Layers\\L4.png").convert_alpha()
water_trees_width = water_trees.get_width()
water_trees_height = water_trees.get_height()

# load custom L2 (clouds) note: made clouds with GIMP software to adjust transparency so it worked seamlessly
clouds = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\Island\\Layers\\L2.png").convert_alpha()
clouds_width = clouds.get_width()
clouds_height = clouds.get_height()

# load mountains background (L1.png)
far_mountains = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\Island\\Layers\\L1.png").convert_alpha()
far_mountains_width = far_mountains.get_width()
far_mountains_height = far_mountains.get_height()

# load sun 
sun = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\Island\\Layers\\L6.png").convert_alpha()
sun_width = sun.get_width()
sun_height = sun.get_height()

# load in background images, create list, loop, load image layers
# blank list
backgrounds = []

# loop, make range 1-3 since I have 2 bg image layers that need to be loaded, 1 ground image for later (L5)
# and 2 other layers that need to be at their own speed 
# f-string to make it so {i} replaced with the value of i in each iteration of loop, note the subdirectories
# and include L before {i} because each of my .png starts with an L before the number i.e. (L1.png)
# convert_alpha to convert image and maintain transparency
for i in range(1, 2):
    background = pygame.image.load(f"Island/Layers/L{i}.png").convert_alpha()
    
    # append to add the loaded images into my list (backgrounds)
    backgrounds.append(background)
    
# determine background image width (will allow for srolling later)
background_width = backgrounds[0].get_width()
    
# draw "background" images (far mountains, and clouds) onto screen, iterate through list
def draw_background():
    # x variable loop so images draw next to eachother
    # note: range is number of each layer being loaded, so in this case getting to 25 can be the end of game
    for x in range(101):
        # set different speeds of background layers to create parallax effect,
        # scroll * speed so scroll variable will be adjusted based on speed that each image is set to
        speed = 0.5
        # note: the furthest image (far mountains) is being drawn first, closest image (clouds) drawn last
        for i in backgrounds:
            screen.blit(i, ((x * background_width) - scroll * speed, 0))
            # increase speed at each iteration, this will make clouds move 0.3 faster than far mountains
            speed += 0.3
            
# draw ground images onto screen, they will be moving at a different speed so doing separately
# range of 101 since game stops scrolling further right at 100 range (192,000 pixels)
def draw_ground():
    for x in range(101):
        screen.blit(ground_image, ((x * ground_width) - scroll * 6, 0))
        
# draw the 2 different water images onto screen
def draw_water_mountains():
    for x in range (101):
        screen.blit(water_mountains, ((x * water_mountains_width) - scroll * 1.2, 0))
        
def draw_water_trees():
    for x in range (101):
        screen.blit(water_trees, ((x * water_trees_width) - scroll * 1.2, 0))
        
# draw clouds and sun (edited these to scale/make transparent through gimp)
def draw_clouds():
    for x in range (101):
        screen.blit(clouds, ((x * clouds_width) - scroll * 0.3, 0))

def draw_sun():
    for x in range (101):
        screen.blit(sun, ((x * sun_width) - scroll * 0.00001, 0))
        
# make list of loaded images to simplify transform.scale
images_list = [far_mountains, clouds, water_mountains, water_trees, ground_image, sun]

# game loop, with forever repeating while loop (when run = true)
run = True
while run:
    # cap frame rate
    clock.tick(FPS)
    
    # event handler for ending loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    # enable double-buffering (for smoother rendering), start by clearing screen with white or black bg
    # note: double buffering didn't end up fixing my image blending issue but keeping it in anyway
    screen.fill((0, 0, 0))
    
    # draw background(far mountains), clouds, water/tree/close mountains layers, and ground in game loop
    draw_background()
    draw_sun()
    draw_clouds()
    draw_water_mountains()
    draw_water_trees()
    draw_ground()
    
    # keybinds: 
    # make a limit so you can only go left a certain amount (since images only properly scroll right)
    # 0 for left so can't go left unless already travelled to the right a given amount
    # 192,000 for right because this pixel count matches the set range for x of 100 (# of layers side-by-side)
    key = pygame.key.get_pressed()
    
    # sprite movement controls:
    if key[pygame.K_LEFT] and scroll > 0:
        scroll -= 1.5
    if key[pygame.K_a] and scroll > 0:
        scroll -= 1.5       
    if key[pygame.K_RIGHT] and scroll < 192000: 
        scroll += 1.5
    if key[pygame.K_d] and scroll < 192000:
        scroll += 1.5
    
    # system controls:
    # quit
    if key[pygame.K_ESCAPE]:
        pygame.quit()
    
    # loop with pygame.keydown so keybind will only trigger once when key is pressed
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            
            # pygame.key.get_mods to check the state of modifier keys, i.e. the alt keys
            if event.key in [pygame.K_f, pygame.K_F11] or (event.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_ALT):
                
                # toggle windowed/fullscreen
                if not_fullscreen:
                    screen_width = 1920 * 0.5
                    screen_height = 1080 * 0.5
                        
                elif resolution.current_w < 1920 and resolution.current_h < 1080:
                    screen_width = resolution.current_w
                    screen_height = resolution.current_h
                        
                else:
                    screen_width = 1920
                    screen_height = 1080
                       
                # resize images with screen toggle: blank list, the for loop for load/transform/scale/append
                resized_images = []
                for image in images_list:
                    resized_image = pygame.transform.scale(image, (screen_width, screen_height))
                    resized_images.append(resized_image)
                
                # set display mode 
                pygame.display.set_mode((screen_width, screen_height))
                    
                not_fullscreen = not not_fullscreen
            
    # update display
    pygame.display.flip()
    
# if loop ends, game quits, sys.exit for smooth program termination and cleanup operations   
pygame.quit()
sys.exit()

    
# IDEAS (notes for me): Maybe have a bed at the end, that you can sleep in, when you wake up it's night or day
        
# Credits: 
# Code: Anthony Davey
# Free background layers: 
# https://saurabhkgp.itch.io/the-island-parallax-background-platformer-side-scroller
# https://opengameart.org/content/backgrounds-for-2d-platformers
# https://www.cleanpng.com/png-real-sun-png-42776/download-png.html