import pygame

# initialize all pygame modules
pygame.init()

# set clock and fps so game runs at intended speed
clock = pygame.time.Clock()
FPS = 60

# Set display size and name it, so it adjusts based off user's resolution, and makes a windowed screen)
resolution_info = pygame.display.Info()
screen = pygame.display.set_mode((int(resolution_info.current_w * 0.93), 
                                  int(resolution_info.current_h * 0.93)))
pygame.display.set_caption("Parallax")

# define game variables(scrolling)
scroll = 0

# load in background images, create list, loop, load image layers
# blank list
backgrounds = []

# loop, make range 1-9 since I have 8 images that need to be loaded, 
# f-string to make it so {i} replaced with the value of i in each iteration of loop, note the subdirectories
# convert_alpha to convert image and maintain transparency
for i in range(1, 9):
    background = pygame.image.load(f"The_Dawn(parallax_scrolling_background)/Layers/{i}.png").convert_alpha()
    
    # make it so backgrounds fit to screen size
    background = pygame.transform.scale(background, (resolution_info.current_w, resolution_info.current_h))
    
    # append to add the loaded images into my list (backgrounds)
    backgrounds.append(background)
    
# determine background image width (will allow for srolling later)
background_width = backgrounds[0].get_width()
    
# draw images onto screen, iterate through list
def draw_background():
    # x variable loop so images draw next to eachother
    for x in range(5):
        # set different speeds of background layers to create parallax effect,
        # scroll * speed so scroll variable will be adjusted based on speed that each image is set to
        speed = 1
        # note that here the furthest image is being drawn first, closest image drawn last
        for i in backgrounds:
            screen.blit(i, ((x * background_width) - scroll * speed, 0))
            # increase speed at each iteration
            speed += 0.2

# game loop, with forever repeating while loop (when run = true)
run = True
while run:
    # cap frame rate
    clock.tick(FPS)
    
    # draw background in game loop
    draw_background()
    
    # keybinds, make a limit so you can only go left a certain amount (since images only properly scroll right)
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and scroll > 0:
        scroll -= 5
    if key[pygame.K_RIGHT] and scroll < 5000: 
        scroll += 5
    
    # event handler for ending loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    # update display
    pygame.display.update()
    
# if loop ends, game quits    
pygame.quit()
    
