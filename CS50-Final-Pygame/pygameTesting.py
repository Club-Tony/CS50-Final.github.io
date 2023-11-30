import pygame

# initialize all pygame modules
pygame.init()

# set clock and fps so game runs at intended speed
clock = pygame.time.Clock()
FPS = 60

# Set display size and name it (setting )
screen_width = 1920
screen_height = 1080

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sunset Run")

# define game variables(scrolling)
scroll = 0

# load ground background layers so they can be set manually at different speeds (7.png, 8.png)
ground_image_1 = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\Island\\Layers\\L5.png").convert_alpha()

# get ground background width and height, just getting for ground_image_1 cause 1 and 2 should be the same 
ground_width = ground_image_1.get_width()
ground_height = ground_image_1.get_height()

# load water layers
water_mountains = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\Island\\Layers\\L3.png").convert_alpha()
water_mountains_width = water_mountains.get_width()
water_mountains_height = water_mountains.get_height()

water_trees = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\Island\\Layers\\L4.png").convert_alpha()
water_trees_width = water_trees.get_width()
water_trees_height = water_trees.get_height()

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
    for x in range(26):
        # set different speeds of background layers to create parallax effect,
        # scroll * speed so scroll variable will be adjusted based on speed that each image is set to
        speed = 0.5
        # note: the furthest image (far mountains) is being drawn first, closest image (clouds) drawn last
        for i in backgrounds:
            screen.blit(i, ((x * background_width) - scroll * speed, 0))
            # increase speed at each iteration, this will make clouds move 0.3 faster than far mountains
            speed += 0.3
            
# draw ground images onto screen, they will be moving at a different speed so doing separately
# range of 26 since game stops scrolling further right at 25 range (36,000 pixels)
def draw_ground():
    for x in range(26):
        screen.blit(ground_image_1, ((x * ground_width) - scroll * 6, 0))
        
# draw the 2 different water images onto screen
def draw_water_mountains():
    for x in range (26):
        screen.blit(water_mountains, ((x * water_mountains_width) - scroll * 1.2, 0))
        
def draw_water_trees():
    for x in range (26):
        screen.blit(water_trees, ((x * water_trees_width) - scroll * 1.2, 0))

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
    # note: double buffering didn't end up fixing my issue with L2.png, but keeping it in anyway
    screen.fill((0, 0, 0))
    
    # draw background, water/tree/close mountains layers, and ground in game loop
    draw_background()
    draw_water_mountains()
    draw_water_trees()
    draw_ground()
    
    # keybinds, make a limit so you can only go left a certain amount (since images only properly scroll right)
    # 0 for left so can't go left unless already travelled to the right a given amount
    # 36,000 for right because this pixel count matches the set range for x of 25 (25 img layers side by side)
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and scroll > 0:
        scroll -= 1.5
    if key[pygame.K_RIGHT] and scroll < 36000: 
        scroll += 1.5
    
    # update display
    pygame.display.flip()
    
# if loop ends, game quits    
pygame.quit()

    
# IDEAS (notes for me): Maybe have a bed at the end, that you can sleep in, when you wake up it's night or day
        
# Credits: 
# Code: Anthony Davey
# Free background layers: https://saurabhkgp.itch.io/the-island-parallax-background-platformer-side-scroller