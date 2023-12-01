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

# Boolean fullscreen check variable so I can toggle between fs and windowed in game loop
fullscreen_toggle = False

# define game variables(scrolling)
scroll = 0

# load sprite
sprite = pygame.image.load("Player/1.png").convert_alpha()
sprite_width = sprite.get_width()
sprite_height = sprite.get_height()

# draw sprite
def draw_sprite():
    screen.blit(sprite, (960, 865))

# load backgrounds starting with ground:
# note: loading all 1 by 1 instead of list so I have full control over individual .png scrolling speed
ground_image = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\Island\\Layers\\L5.png").convert_alpha()

# get ground background width and height(do this for others also)
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

# load water with mountains
water_mountains = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\Island\\Layers\\L3.png").convert_alpha()
water_mountains_width = water_mountains.get_width()
water_mountains_height = water_mountains.get_height()

# load water with trees
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
            
# draw images including resized versions of these to implement later for fullscreen toggle
# range of 101 is arbitrary, just making sure it's enough without being too much
def draw_far_mountains(images):
    for x in range(101):
        screen.blit(images[0], ((x * images[0].get_width()) - scroll * 0.4, 0))

def draw_ground(images):
    for x in range(101):
        screen.blit(images[4], ((x * images[4].get_width()) - scroll * 6, 0))

def draw_water_mountains(images):
    for x in range(101):
        screen.blit(images[2], ((x * images[2].get_width()) - scroll * 1.2, 0))

def draw_water_trees(images):
    for x in range(101):
        screen.blit(images[3], ((x * images[3].get_width()) - scroll * 1.2, 0))

def draw_clouds(images):
    for x in range(101):
        screen.blit(images[1], ((x * images[1].get_width()) - scroll * 0.2, 0))

def draw_sun(images):
    for x in range(101):
        screen.blit(images[5], ((x * images[5].get_width()) - scroll * 0.00001, 0))
        
# make list of loaded images to simplify transform.scale
images_list = [far_mountains, clouds, water_mountains, water_trees, ground_image, sun]

# resize images with screen toggle: blank list, the for loop for transform/scale/append
def resize_images(images, screen_width, screen_height):
    resized_images = []
    for image in images:
        resized_image = pygame.transform.scale(image, (screen_width, screen_height))
        resized_images.append(resized_image)
    return resized_images

resized_images = resize_images(images_list, screen_width, screen_height)

# GAME LOOP, with forever repeating while loop (when run = true)
run = True
while run:
    # cap frame rate
    clock.tick(FPS)
    
    # event handler for ending loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        # Keybinds: 
        # make a limit so you can only go left a certain amount (since images only properly scroll right)
        # 0 for left so can't go left unless already travelled to the right a given amount
        # 192,000 for right because this pixel count matches the set range for x of 100 (# of layers side-by-side)    
        # loop with pygame.keydown so keybind will only trigger once when key is pressed
        elif event.type == pygame.KEYDOWN:
            
            # system controls:
            # quit
            if event.key == pygame.K_ESCAPE:
                run = False
            
            # pygame.key.get_mods to check the state of modifier keys, i.e. the alt keys
            elif event.key in [pygame.K_F11] or (event.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_ALT):
                
                # toggle windowed/fullscreen
                if fullscreen_toggle:
                    screen_width = 1920 * 0.5
                    screen_height = 1080 * 0.5
                        
                elif resolution.current_w < 1920 and resolution.current_h < 1080:
                    screen_width = resolution.current_w
                    screen_height = resolution.current_h
                        
                else:
                    screen_width = 1920
                    screen_height = 1080

                # draw background layers for if fullscreen button toggled
                # resized images variable for including images list with screen height and width
                resized_images = resize_images(images_list, screen_width, screen_height)
                
                draw_far_mountains(resized_images)
                draw_sun(resized_images)
                draw_clouds(resized_images)
                draw_water_mountains(resized_images)
                draw_water_trees(resized_images)
                draw_ground(resized_images)
                # draw sprite
                draw_sprite()

                # set display mode 
                pygame.display.set_mode((screen_width, screen_height))
                
                # not makes this False boolean variable True
                fullscreen_toggle = not fullscreen_toggle 
            
    # enable double-buffering (for smoother rendering), start by clearing screen with white or black bg
    # note: double buffering didn't end up being the fix for earlier image blending issue but keeping it in anyway
    screen.fill((0, 0, 0))
    
    # draw background layers (these are the how they're drawn by default, before user toggles fullscreen)
    draw_far_mountains(resized_images)
    draw_sun(resized_images)
    draw_clouds(resized_images)
    draw_water_mountains(resized_images)
    draw_water_trees(resized_images)    
    draw_ground(resized_images)
    # draw sprite
    draw_sprite()
        
    
    # initialize 'key' to use for keybinding in game loop
    key = pygame.key.get_pressed()   
    
    # sprite movement controls:
    if (key[pygame.K_LEFT] and scroll > 0) or (key[pygame.K_a] and scroll > 0):
        scroll -= 1.5       
    if (key[pygame.K_RIGHT] and scroll < 5000) or (key[pygame.K_d] and scroll < 5000):
        scroll += 1.5

    # update display (.flip since implemented double buffering)
    pygame.display.flip()
    
# if loop ends, game quits, sys.exit for smooth program termination and cleanup operations   
pygame.quit()
sys.exit()

# IDEAS (notes for me): Maybe have a bed at the end, that you can sleep in, when you wake up it's night or day
        
# Credits: 
# Code: Anthony Davey
# Free assets (background layers, sprites): 
# https://saurabhkgp.itch.io/the-island-parallax-background-platformer-side-scroller
# https://opengameart.org/content/backgrounds-for-2d-platformers
# https://www.cleanpng.com/png-real-sun-png-42776/download-png.html