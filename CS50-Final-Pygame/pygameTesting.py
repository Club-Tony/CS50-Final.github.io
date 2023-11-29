import pygame

# initialize all pygame modules
pygame.init()

# set clock and fps so game runs at intended speed
clock = pygame.time.Clock()
FPS = 60

# Set display size and name it (chose a default industry standard display size)
screen_width = 1440
screen_height = 810

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Parallax")

# define game variables(scrolling)
scroll = 0

# load ground background layers so they can be set manually at different speeds (7.png, 8.png)
ground_image_1 = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\The_Dawn(parallax_scrolling_background)\\Layers\\L5.png").convert_alpha()

# make it so ground fits to screen size
ground_image_1 = pygame.transform.scale(ground_image_1, (screen_width, screen_height))

# get ground background width and height, just getting for ground_image_1 cause 1 and 2 should be the same 
ground_width = ground_image_1.get_width()
ground_height = ground_image_1.get_width()

# load in background images, create list, loop, load image layers
# blank list
backgrounds = []

# loop, make range 1-5 since I have 4 bg image layers that need to be loaded, 1 ground image for later (L5) 
# f-string to make it so {i} replaced with the value of i in each iteration of loop, note the subdirectories
# convert_alpha to convert image and maintain transparency
for i in range(1, 5):
    background = pygame.image.load(f"Island/Layers/{i}.png").convert_alpha()
    
    # make it so backgrounds fit to screen size
    background = pygame.transform.scale(background, (screen_width, screen_height))
    
    # append to add the loaded images into my list (backgrounds)
    backgrounds.append(background)
    
# determine background image width (will allow for srolling later)
background_width = backgrounds[0].get_width()
    
# draw images onto screen, iterate through list
def draw_background():
    # x variable loop so images draw next to eachother
    # note: range is number of each layer being loaded, so in this case getting to 25 can be the end of game
    for x in range(26):
        # set different speeds of background layers to create parallax effect,
        # scroll * speed so scroll variable will be adjusted based on speed that each image is set to
        speed = 1
        # note that here the furthest image is being drawn first, closest image drawn last
        for i in backgrounds:
            screen.blit(i, ((x * background_width) - scroll * speed, 0))
            # increase speed at each iteration
            speed += 0.3
            
# draw ground images onto screen, they will be moving at a different speed so doing separately
def draw_ground():
    for x in range(26):
        screen.blit(ground_image_1, ((x * ground_width) - scroll * 3.8, 0))

# game loop, with forever repeating while loop (when run = true)
run = True
while run:
    # cap frame rate
    clock.tick(FPS)
    
    # draw background and ground in game loop
    draw_background()
    draw_ground()
    
    # keybinds, make a limit so you can only go left a certain amount (since images only properly scroll right)
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and scroll > 0:
        scroll -= 1.5
    if key[pygame.K_RIGHT] and scroll < 5000: 
        scroll += 1.5
    
    # event handler for ending loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    # update display
    pygame.display.update()
    
# if loop ends, game quits    
pygame.quit()
    
