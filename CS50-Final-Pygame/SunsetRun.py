# import pygame library, also sys to allow for smooth program termination and cleanup operations
import pygame
import sys

# initialize all pygame modules, and the .mixer module specifically, for better audio control
pygame.init()

# incase device can't do audio (which cs50 codespace can't), implement a try except block
try:
    pygame.mixer.init()
except pygame.error:
    print("No audio device found, running without audio")

# set clock and fps so game runs at intended speed, set night cycle clock
clock = pygame.time.Clock()
FPS = 60

nighttime = 0
fade_black = 0

# get display info/set default width/height of game screen
resolution = pygame.display.Info()

# set default screen resolution variables
screen_width = 1920
screen_height = 1080

# create copies of the screen dimensions for later to use for rescaling when changing window size
og_screen_width = 1920
og_screen_height = 1080

# set display, name display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sunset Run")

# Boolean fullscreen check variable so I can toggle between fs and windowed in game loop
fullscreen_toggle = False

# define game variables(scrolling) Note: scroll speed based on fps, so 60 fps is scroll = 1 means scrolling 60 pixels per second
scroll = 0

# stamina bar, create variable to keep track starting at 100%, have it decrease certain amount each frame-
# when space bar is being used
stamina = 1500

# initializing cooldown and boost now so it can be used in game loop later, have boost initially as true to allow player to boost initially
cooldown = 0
boost = True

# set adjust percentage for height of sprite adjustment
y_adjust_percentage = 0.09
y_adjust = int(screen_height * y_adjust_percentage)

# keep track of current frame for animating sprite, initialize a counter frame to slow down animation later
current_frame = 0
counter_frame = 0

# sprite direction faced variable
sprite_facing = "right"

# SPRITE ANIMATION: Load one for idle frame, create list for frames 2-7
sprite_idle = pygame.image.load("Player/1.png").convert_alpha()

sprite_run = []
for i in range(2, 8):
    run_load = pygame.image.load(f"Player/{i}.png").convert_alpha()
    sprite_run.append(run_load)

# set sprite position on screen
sprite_width = sprite_run[0].get_width()
sprite_height = sprite_run[0].get_height()

idle_sprite_width = sprite_idle.get_width()
idle_sprite_height = sprite_idle.get_height()

# include another copy of sprite width and height for use later in game loop when adjusting - 
# window size since sprite_width and sprite_height values get changed
initial_sprite_width = sprite_run[0].get_width()
initial_sprite_height = sprite_run[0].get_height()

initial_idle_sprite_width = sprite_idle.get_width()
initial_idle_sprite_height = sprite_idle.get_height()

# define last_key so it can update later in game loop, default right so sprite loads properly at game start
last_key = "right"

# define bool for sprite running
sprite_running = False
   
# define sprite_position for this initial draw (pre using fullscreen toggle)
sprite_position = ((screen_width // 2) - (sprite_width // 2), screen_height - sprite_height - y_adjust)
    
# draw sprite (animation and idle)
def draw_sprite(screen_width, screen_height, sprite_position): 
    current_sprite = sprite_run[current_frame] 
    current_idle_sprite = sprite_idle
    
    # initiate resize sprite variables to account for toggle fullscreen
    sprite_width_adjust = int(sprite_width * (screen_width / 1920))
    sprite_height_adjust = int(sprite_height * (screen_height / 1080))
    
    # fix specific scaling issue with the idle sprite size when resizing to smaller screen
    if screen_width == 1920 and screen_height == 1080:
        sprite_position = ((screen_width // 2) - (sprite_width // 2), screen_height - sprite_height - y_adjust)
        
        idle_rescaler = 1
    else:
        idle_rescaler = 0.75
        
        # fix specific scaling issue with the idle sprite position when resizing to smaller screen 
        sprite_position = screen_width // 2 - 25, screen_height - sprite_height + 10

    idle_sprite_width_adjust = int(initial_idle_sprite_width * (screen_width / 1920) * idle_rescaler)
    idle_sprite_height_adjust = int(initial_idle_sprite_height * (screen_height / 1080) * idle_rescaler)
     
    resized_sprite = pygame.transform.scale(current_sprite, (sprite_width_adjust, sprite_height_adjust))
    resized_idle_sprite = pygame.transform.scale(current_idle_sprite, (idle_sprite_width_adjust, idle_sprite_height_adjust))
    
    # make flipped version of sprite for facing left. true and false are x and y arguments. True = flip
    flipped_sprite = pygame.transform.flip(resized_sprite, True, False)
    flipped_idle_sprite = pygame.transform.flip(resized_idle_sprite, True, False)
    
    # use sprite_facing variable to ensure sprite idle is facing correct way when stopped
    if sprite_facing == "left":
        if sprite_running:
            # draw running sprites
            screen.blit(flipped_sprite, sprite_position)
        else:
            # draw idle sprite
            screen.blit(flipped_idle_sprite, sprite_position)
        
    elif sprite_facing == "right":
        
        if sprite_running:              
            # use sprite_position to draw running sprite
            screen.blit(resized_sprite, sprite_position)
        else:
            # draw idle sprite        
            screen.blit(resized_idle_sprite, sprite_position)

# load backgrounds starting with ground:
# note: loading all 1 by 1 instead of list so I have full control over individual .png scrolling speed
ground_image = pygame.image.load("Island\Layers\L5.png").convert_alpha()

# get ground background width and height(do this for others also)
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

# load water with mountains
water_mountains = pygame.image.load("Island\Layers\L3.png").convert_alpha()
water_mountains_width = water_mountains.get_width()
water_mountains_height = water_mountains.get_height()

# load water with trees
water_trees = pygame.image.load("Island\Layers\L4.png").convert_alpha()
water_trees_width = water_trees.get_width()
water_trees_height = water_trees.get_height()

# load custom L2 (clouds)
clouds = pygame.image.load("Island\Layers\L2.png").convert_alpha()
clouds_width = clouds.get_width()
clouds_height = clouds.get_height()

# load mountains background (L1.png)
far_mountains = pygame.image.load("Island\Layers\L1.png").convert_alpha()
far_mountains_width = far_mountains.get_width()
far_mountains_height = far_mountains.get_height()

# load sun 
sun = pygame.image.load("Island\Layers\L6.png").convert_alpha()
sun_width = sun.get_width()
sun_height = sun.get_height()

# load shelter (fire and tent), adjust the width and height here before game loop to avoid drawing/scrolling issues
shelter = pygame.image.load("fire.png").convert_alpha()
shelter_width = shelter.get_width() * 1.2
shelter_height = shelter.get_height() * 1.8

tent = pygame.image.load("tent.png").convert_alpha()
tent_width = tent.get_width() * 0.3
tent_height = tent.get_height() * 1.3

# load and (later) play music, -1 arg for indefinite loop, make it muted/off by default
# also create a boolean variable for volume muting and for first toggle to make it so music not playing at first
# another try except block incase audio device not found
try:
    music = pygame.mixer.music.load("Music\Moon boots i want your attention loop.mp3")
    pygame.mixer.music.set_volume(0.75)
except pygame.error:
    pass
                                          
volume_toggle = False
first_volume_toggle = False
 
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
        screen.blit(images[5], ((x * images[5].get_width()) - scroll * 0.0001, 0))
        
# make list of loaded images to simplify transform.scale
images_list = [far_mountains, clouds, water_mountains, water_trees, ground_image, sun]

# resize images with screen toggle: blank list, the for loop for transform/scale/append
def resize_images(images, screen_width, screen_height):
    resized_images = []
    for image in images:
        resized_image = pygame.transform.scale(image, (screen_width, screen_height))
        resized_images.append(resized_image)
    return resized_images

# define resized images so it works later in game loop
resized_images = resize_images(images_list, screen_width, screen_height)

# NIGHTTIME
# transparent tint with same size as screen (double parentheses for representing rgb values)
night_tint = pygame.Surface((screen_width, screen_height))

# dark blue color for tint 
night_tint.fill((0, 0, 128))

# alpha value of tint to set transparency, create variable to use in if statement in game loop
# max_opacity = 185 so so it matches max alpha_value
max_opacity = 185

# fade to black
black_tint = pygame.Surface((screen_width, screen_height))

# TEXT
# game over text
# create font object None makes it pygame default font, otherwise need to use loaded font, 2nd arg = size
game_over = pygame.font.Font("Branda-yolq.ttf", 100)

# you win text
congrats = pygame.font.Font("ChrustyRock-ORLA.ttf", 93)

# buttons, define button dimensions and position, create Rect (rectangle), then draw in game loop
button_width = 130
button_height = 55
button_x = (screen_width - button_width) // 2
button_y = (screen_height - button_height) * 0.7

button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

# button text font and size
exit_button = pygame.font.Font(None, 85)

# game start text
controls = pygame.font.Font(None, 75)
controls_2 = pygame.font.Font(None, 75)
controls_3 = pygame.font.Font(None, 75)
start_text = pygame.font.Font("ChrustyRock-ORLA.ttf", 115)
start_text_2 = pygame.font.Font("ChrustyRock-ORLA.ttf", 115)
stamina_instruction = pygame.font.Font(None, 55)

# GAME LOOP, with forever repeating while loop (while run = true)
# note: basically anything not depending on an event can be placed in main game loop not in event handler loop
run = True
while run:
            
    # cap frame rate
    clock.tick(FPS)

    # increment night cycle
    nighttime += 0.03 

    # min function takes any # of arguments, returns the smallest of arguments provided
    color_value = min(nighttime, 128)
    alpha_value = min(nighttime, 185)

    # update night tint with color and alpha value on each iteration
    night_tint.fill((0, 0, color_value))
    night_tint.set_alpha(alpha_value)
    
    # initialize 'key' variable to use for keybinding in game loop, allows for holding down keys
    # initialize in the main game loop, outside any event handling loops
    key = pygame.key.get_pressed()
    
    black_alpha_value = min(fade_black, 255) # 255 for full opacity
        
    # update black tint
    black_tint.fill((0, 0, 0))
    black_tint.set_alpha(black_alpha_value)
    
    # event handler loop (have all events during game under this for loop) i.e. if statements, other loops
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        # handle mouse click for highlighting exit button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                run = False  
                   
        # Keybinds:
        # volume toggle and escape keybinds (consolodating the pygame.keygame calls together to prevent conflicts)
        # loop with pygame.keydown so keybind will only trigger once when key is pressed
        # this starts song infinite loop on first m keypress, then from that point m will only toggle mute/unmute    
        if event.type == pygame.KEYDOWN:
            
            # pygame.key.get_mods to check the state of modifier keys, i.e. the alt keys 
            if event.key in [pygame.K_F11] or (event.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_ALT):
                
                # not makes this False boolean variable True
                fullscreen_toggle = not fullscreen_toggle 
                
                # toggle windowed/fullscreen, start by checking if user has < 1920 x 1080 resolution
                if fullscreen_toggle or (resolution.current_w < 1920 and resolution.current_h < 1080):
                    screen_width = 1920 * 0.5
                    screen_height = 1080 * 0.5                        
                else:
                    screen_width = 1920
                    screen_height = 1080

                # draw background layers for if fullscreen button toggled
                # resized images variable for including images list with screen height and width
                resized_images = resize_images(images_list, screen_width, screen_height)
                
                # Adjust sprite position if screen size is reduced
                # start by specifically adjusting its height since it's scuffed
                if screen_width < 1920:
                    sprite_height = 130
                    # calculate what the corresponding new width would be to avoid distoring the image
                    initial_sprite_aspect_ratio = initial_sprite_width / initial_sprite_height
                    sprite_width = sprite_height * initial_sprite_aspect_ratio
                else:
                    sprite_width = initial_sprite_width
                    sprite_height = initial_sprite_height
                    
                if screen_width == 1920 * 0.5 and screen_height == 1080 * 0.5:
                    sprite_position = ((screen_width // 2) - (sprite_width // 2), screen_height * 0.78)  
                else: 
                    sprite_position = ((screen_width // 2) - (sprite_width // 2), screen_height - sprite_height - y_adjust)
                    
                # set display mode after determining screen width/height changes, but before drawing
                pygame.display.set_mode((screen_width, screen_height))          
                
            # volume button        
            if event.key == pygame.K_m:
                if first_volume_toggle == False:
                    # start music after first volume toggle
                    pygame.mixer.music.play(-1)
                    
                    # 'not' makes these False boolean variables True
                    first_volume_toggle = not first_volume_toggle
                
                volume_toggle = not volume_toggle
                
                # volume control
                if volume_toggle and first_volume_toggle == True:
                    pygame.mixer.music.set_volume(0.75)
                else: 
                    pygame.mixer.music.set_volume(0)
                    
            # system controls: quit
            elif event.key == pygame.K_ESCAPE:
                run = False
               
    # increment fade to black when night is at its darkest
    if alpha_value >= max_opacity:
        # if statement so fade_black doesn't exceed 255
        if fade_black < 255:
            fade_black += 1  
            
    # enable double-buffering (for smoother rendering), start by clearing screen with white or black bg
    screen.fill((0, 0, 0))
    
    # draw background layers (these are the how they're drawn by default, before user toggles fullscreen)
    draw_far_mountains(resized_images)
    draw_sun(resized_images)
    draw_clouds(resized_images)
    draw_water_mountains(resized_images)
    draw_water_trees(resized_images)    
    draw_ground(resized_images)
           
    # sprite movement controls:
    # make a limit so you can only go left a certain amount (since images only properly scroll right)
    # for right, choose pixel count suitable for how long I want sprite to be able to run right 
    # make variable here to keep track of last key pressed between left/right to flip sprite accordingly  
    if (key[pygame.K_LEFT] and scroll > 0) or (key[pygame.K_a] and scroll > 0):
        scroll -= 1.5
        last_key = "left"
        sprite_facing = "left"
        sprite_running = True  
             
    elif (key[pygame.K_RIGHT] and scroll < 15000) or (key[pygame.K_d] and scroll < 15000):
        scroll += 1.5
        last_key = "right"
        sprite_facing = "right"
        sprite_running = True    
        
    elif not (key[pygame.K_LEFT] or key[pygame.K_RIGHT] or key[pygame.K_a] or key[pygame.K_d]):
        sprite_running = False
        
    speed_boost_left = ((key[pygame.K_SPACE] and key[pygame.K_LEFT]) and scroll > 0) or (key[pygame.K_SPACE] and key[pygame.K_a]) and scroll > 0
    if speed_boost_left and boost:
        scroll -= 3
        
    speed_boost_right = ((key[pygame.K_SPACE] and key[pygame.K_RIGHT]) and scroll < 15000) or (key[pygame.K_SPACE] and key[pygame.K_d]) and scroll < 15000    
    if speed_boost_right and boost:
        scroll += 3    
    
    # sprite animation implementation
    # if idle (left or right keys not being pressed):
    if not (key[pygame.K_LEFT] or key[pygame.K_a]) and not (key[pygame.K_RIGHT] or key[pygame.K_d]):
        draw_sprite(screen_width, screen_height, sprite_position)
    else:
        # used counter_frame to slow down animation, set counter_frame faster when boosting
        counter_frame += 1
        if (speed_boost_left or speed_boost_right) and counter_frame >= 2.2:
            current_frame += 1
            counter_frame = 0
        elif (not speed_boost_left or not speed_boost_right) and counter_frame >= 4:
            current_frame += 1
            counter_frame = 0
        if current_frame >= len(sprite_run):
            current_frame = 0
        
        draw_sprite(screen_width, screen_height, sprite_position)           
        
    # implement stamina bar
    # set stamina bar width, then set its current width divided by value of stamina
    stamina_bar = 250
    stamina_bar_current = (stamina / 1500) * stamina_bar
    
    stamina_bar_border = 3
    
    # draw stamina bar and border, border first since it needs to be drawn before since it's opaque
    draw_stamina_bar_border = pygame.draw.rect(screen, (255, 100, 255), (150 - stamina_bar_border, 1000 - stamina_bar_border, stamina_bar + 2 * stamina_bar_border, 10 + 2 * stamina_bar_border))
    draw_stamina = pygame.draw.rect(screen, (0, 255, 0), (150, 1000, stamina_bar_current, 10))
    
    if screen_width < 1920 and screen_height < 1080:
            
            # rescale variable for original and current screen size to use for rescaling
            rescaler = screen_width / og_screen_width
            
            rescaled_stamina_bar_x = int(150 * rescaler)
            rescaled_stamina_bar_y = int(1000 * rescaler)
            rescaled_stamina_bar_width = int(stamina_bar_current * rescaler)
            rescaled_stamina_bar_height = int(10 * rescaler)
            
            rescaled_stamina_bar_border = int(3 * rescaler)
            
            rescaled_stamina_bar_border_x = int((150 - stamina_bar_border) * rescaler)
            rescaled_stamina_bar_border_y = int((1001 - stamina_bar_border) * rescaler)
            rescaled_stamina_bar_border_width = int((stamina_bar + 2 * stamina_bar_border) * rescaler)
            rescaled_stamina_bar_border_height = int((10 + 2 * stamina_bar_border) * rescaler)
            
            pygame.draw.rect(screen, (255, 0, 255), (rescaled_stamina_bar_border_x + 1, rescaled_stamina_bar_border_y, rescaled_stamina_bar_border_width, rescaled_stamina_bar_border_height))
            pygame.draw.rect(screen, (0, 255, 0), (rescaled_stamina_bar_x, rescaled_stamina_bar_y, rescaled_stamina_bar_width, rescaled_stamina_bar_height))  
                    
    else:
        draw_stamina_bar_border = pygame.draw.rect(screen, (255, 0, 255), (150 - stamina_bar_border, 1000 - stamina_bar_border, stamina_bar + 2 * stamina_bar_border, 10 + 2 * stamina_bar_border))
        draw_stamina = pygame.draw.rect(screen, (0, 255, 0), (150, 1000, stamina_bar_current, 10))
    
    # keep track of time (for seconds instead of ms divide by 1000)
    time = pygame.time.get_ticks() // 1000
    
    # cooldown for set amount of time can't boost (use spacebar), set max for stamina so it can't be < 0   
    if (speed_boost_left or speed_boost_right) and stamina > 4:
        stamina -= 4
        stamina = max(0, stamina)
        if stamina <= 4 and boost: 
            cooldown = time
            boost = False
        elif stamina <= 4 and boost and time > cooldown + 10:
            cooldown = time
            boost = False
    
    # "and not boost and time >= 1" below to prevent countdown happening on game launch
    if time <= cooldown + 10 and not boost and time >= 1:
        # display countdown time, and set boost to False in order to activate cooldown
        countdown_timer = int(10 - (time - cooldown))
        countdown_overlay_font = pygame.font.Font(None, 35)
        countdown_overlay = countdown_overlay_font.render(str(countdown_timer), True, (255, 255, 255))
        
        boost = False
        
        # draw countdown overlay/rescale if window size changes
        if screen_width < 1920 and screen_height < 1080:
            
            # rescale variable for original and current screen size to use for rescaling
            rescaler = screen_width / og_screen_width
            
            rescaled_countdown_overlay_font = pygame.font.Font(None, int(35 * rescaler))
            rescaled_countdown_overlay = rescaled_countdown_overlay_font.render(str(countdown_timer), True, (255, 255, 255))
            screen.blit(rescaled_countdown_overlay, (420 * rescaler, 993 * rescaler + 1))
            
        else:
            screen.blit(countdown_overlay, (420, 993))
            
    if (time > cooldown + 10) and stamina > 4:
        boost = True
                     
    if not (speed_boost_left or speed_boost_right) and stamina < 1500:
        stamina += 2                   
    
    # if scroll reached endgame scroll distance, create a message
    # first draw end game items a little before reaching final distance (125 pixels apart is good)
    if 14875 <= scroll <= 15875:
        # draw camp objects, - scroll * 6 for the width so it appears static, matching ground scroll speed
        # make adjustment variables to set x and y locations for images
        # add the above number after the if statement multiplied by 6 to get the correct x/y always for shelter images
        shelter_x = screen_width - shelter_width - scroll * 6 + 89200
        shelter_y = screen_height - shelter_height
        tent_x = screen_width - tent_width - scroll * 6 + 89200
        tent_y = screen_height - tent_height
        
        if screen_width < 1920 and screen_height < 1080:
            
            # rescale variable for original and current screen size to use for rescaling
            rescaler = screen_width / og_screen_width
            
            # make rescaled variables, use round to make sure it returns an int
            rescaled_shelter_width = shelter.get_width() * 0.5
            rescaled_shelter_height = shelter.get_height() * 0.5
            rescaled_shelter = pygame.transform.scale(shelter, (rescaled_shelter_width, rescaled_shelter_height))
            shelter_x = ((screen_width) - (rescaled_shelter_width) - (scroll * 6 + 89200) + 179260) * rescaler
            shelter_y = (screen_height - rescaled_shelter_height) * 0.885
            
            rescaled_tent_width = tent.get_width() * 0.5
            rescaled_tent_height = tent.get_height() * 0.5
            rescaled_tent = pygame.transform.scale(tent, (rescaled_tent_width, rescaled_tent_height))
            tent_x = ((screen_width) - (rescaled_tent_width) - (scroll * 6 + 89200) + 179375) * rescaler
            tent_y = (screen_height - rescaled_tent_height) * 0.885
            
            if 0 <= shelter_x <= screen_width:
                screen.blit(rescaled_shelter, (shelter_x, shelter_y))
            if 0 <= tent_x <= screen_width:
                screen.blit(rescaled_tent, (tent_x, tent_y))           
                
        else:
            shelter_x = screen_width - shelter_width - scroll * 6 + 89200
            shelter_y = screen_height - shelter_height
            tent_x = screen_width - tent_width - scroll * 6 + 89200
            tent_y = screen_height - tent_height
            
            if 0 <= shelter_x <= screen_width:
                screen.blit(shelter, (shelter_x, shelter_y))
            if 0 <= tent_x <= screen_width:
                screen.blit(tent, (tent_x, tent_y))
    
    # if statement for congrats screen, have this number 125 pixels higher than shelter/tent draw location for match        
    if scroll >= 15000:
        # make fade black increment 0 so no fade to black occurs, also make nighttime stop increment for good measure
        fade_black = 0
        nighttime = 0
        
        congrats_render = congrats.render("You made it to shelter safely before dark!", True, (0, 255, 0))
        congrats_text_width = congrats_render.get_width()
        congrats_text_height = congrats_render.get_height()
        congrats_text_center_x = screen_width / 2 - congrats_text_width / 2
        congrats_text_center_y = screen_height / 2 - congrats_text_height / 2
        
        # button scale with fullscreen toggle, get original button/text size, multiple by rescale variable
        if screen_width < 1920 and screen_height < 1080:
            
            # rescale variable for original and current screen size to use for rescaling
            rescaler = screen_width / og_screen_width
            
            # rescale button dimensions and position and button_rect
            button_width = 130 * rescaler
            button_height = 55 * rescaler
            button_x = (screen_width - button_width) // 2 
            button_y = (screen_height - button_height) * 0.7
            button_rect = pygame.Rect(button_x, button_y, int(button_width), int(button_height))
            
            # rescale button and text, use int to prevent type error since it's expecting int not float
            exit_button = pygame.font.Font(None, int(85 * rescaler))
            congrats = pygame.font.Font("ChrustyRock-ORLA.ttf", int(93 * rescaler))  
            
        # revert button and text scaling to default when screen is 1920 x 1080 (the default)
        # do this by setting above variable to their default values
        else:
            button_width = 130
            button_height = 55
            button_x = (screen_width - button_width) // 2
            button_y = (screen_height - button_height) * 0.7
            button_rect = pygame.Rect(button_x, button_y, int(button_width), int(button_height))
            exit_button = pygame.font.Font(None, 85)
            congrats = pygame.font.Font("ChrustyRock-ORLA.ttf", 93)
        
        # draw you win text and exit button/text
        screen.blit(congrats_render, (congrats_text_center_x, congrats_text_center_y))
        exit_button_render = exit_button.render("Quit", True, (0, 0, 0))
        
        # change button appearance when mouse hovers over
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (255, 255, 255), button_rect)
        else:
            pygame.draw.rect(screen, (255, 0, 0), button_rect)
            
        # draw exit button render
        screen.blit(exit_button_render, (button_x, button_y))
        
    # draw night tint and fade to black: 0, 0 makes it draw from top left of screen
    screen.blit(night_tint, (0, 0))
    screen.blit(black_tint, (0, 0))
    
    # if black, have text up that says you're lost, and can't find your way back
    if fade_black > 0: 
      
        # create render arguments: text, boolean for whether or not to antialias, then rgb for color
        game_over_render = game_over.render("You're lost, and can't find your way back", True, (255, 0, 0))
        game_over_text_width = game_over_render.get_width()
        game_over_text_height = game_over_render.get_height()
        text_center_x = screen_width / 2 - game_over_text_width / 2
        text_center_y = screen_height / 2 - game_over_text_height / 2
        
        # button scale with fullscreen toggle, get original button/text size, multiple by rescale variable
        if screen_width < 1920 and screen_height < 1080:
            
            # rescale variable for original and current screen size to use for rescaling
            rescaler = screen_width / og_screen_width
            
            # rescale button dimensions and position and button_rect
            button_width = 130 * rescaler
            button_height = 55 * rescaler
            button_x = (screen_width - button_width) // 2
            button_y = (screen_height - button_height) * 0.7
            button_rect = pygame.Rect(button_x, button_y, int(button_width), int(button_height))
            
            # rescale button and text, use int to prevent type error since it's expecting int not float
            exit_button = pygame.font.Font(None, int(85 * rescaler))
            game_over = pygame.font.Font("Branda-yolq.ttf", int(100 * rescaler)) 
            
        # revert button and text scaling to default when screen is 1920 x 1080 (the default)
        # do this by setting above variable to their default values
        else:
            button_width = 130
            button_height = 55
            button_x = (screen_width - button_width) // 2
            button_y = (screen_height - button_height) * 0.7
            button_rect = pygame.Rect(button_x, button_y, int(button_width), int(button_height))
            exit_button = pygame.font.Font(None, 85)
            game_over = pygame.font.Font("Branda-yolq.ttf", 100)
            
        # create render arguments for button text
        exit_button_render = exit_button.render("Quit", True, (0, 0, 0))
        
        # draw game over text
        screen.blit(game_over_render, (text_center_x, text_center_y))
        
        # draw button rectangle
        pygame.draw.rect(screen, (255, 0, 0), button_rect)
        
        # change button appearance when mouse hovers over            
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (255, 255, 255), button_rect)
        else:
            pygame.draw.rect(screen, (255, 0, 0), button_rect) 
            
        # draw exit button text
        screen.blit(exit_button_render, (button_x, button_y))
        
    # render/draw start text, do this last so it's drawn after everything else
    # keep track of time (for seconds instead of ms divide by 1000)
    time = pygame.time.get_ticks() // 1000
    if time < 60:
        controls_render = controls.render(" Controls:          WASD - L/R movement             SPACE - Boost", True, (0, 0, 205))
        controls_render_2 = controls_2.render("                             M - Music on/off                         ESC - Exit", True, (0, 0, 205))
        controls_render_3 = controls_3.render("      F11 - Window size/scroll speed (only visually, equal total distance)", True, (0, 0, 205))
        start_text_render = start_text.render("Night is approaching", True, (255, 245, 0))
        start_text_render_2 = start_text_2.render("Find shelter soon", True, (255, 245, 0))
        stamina_instruction_render = stamina_instruction.render("<- Stamina", True, (255, 255, 255))
        
        # remove instructions if scrolling, and/or if game starts fading to black
        if scroll != 0:
            pass
        elif alpha_value >= max_opacity:
            black_alpha_value = min(fade_black, 255)
            black_tint.fill((0, 0, 0))
            black_tint.set_alpha(black_alpha_value)
            if fade_black < 255:
                
                if black_alpha_value != 0:
                    fade_black += 1
                    screen.blit(black_tint, (0, 0))
                    
        # include rescaling if toggled     
        elif screen_width < 1920 and screen_height < 1080:
    
            # rescale variable for original and current screen size to use for rescaling
            rescaler = screen_width / og_screen_width
            
            rescaled_controls = pygame.font.Font(None, int(75 * rescaler))
            rescaled_controls_2 = pygame.font.Font(None, int(75 * rescaler))
            rescaled_controls_3 = pygame.font.Font(None, int(75 * rescaler))
            rescaled_start_text = pygame.font.Font(("ChrustyRock-ORLA.ttf"), int(115 * rescaler))
            rescaled_start_text_2 = pygame.font.Font(("ChrustyRock-ORLA.ttf"), int(115 * rescaler))
            rescaled_stamina_instruction = pygame.font.Font(None, int(55 * rescaler))
            
            controls_render = rescaled_controls.render(" Controls:          WASD - L/R movement             SPACE - Boost", True, (0, 0, 205))
            controls_render_2 = rescaled_controls_2.render("                             M - Music on/off                         ESC - Exit", True, (0, 0, 205))
            controls_render_3 = rescaled_controls_3.render("      F11 - Window size/scroll speed (only visually, equal total distance)", True, (0, 0, 205))
            start_text_render = rescaled_start_text.render("Night is approaching", True, (255, 245, 0))
            start_text_render_2 = rescaled_start_text_2.render("Find shelter soon", True, (255, 245, 0))
            stamina_instruction_render = rescaled_stamina_instruction.render("<- Stamina", True, (255, 255, 255))
            
            screen.blit(controls_render, (0 * rescaler, 10 * rescaler))
            screen.blit(controls_render_2, (0 * rescaler, 85 * rescaler))
            screen.blit(controls_render_3, (55 * rescaler, 155 * rescaler))
            screen.blit(start_text_render, (370 * rescaler, 525 * rescaler)) 
            screen.blit(start_text_render_2, (470 * rescaler, 400 * rescaler))    
            screen.blit(stamina_instruction_render, (412 * rescaler, 984 * rescaler))
                
        else:        
            screen.blit(controls_render, (0, 10))
            screen.blit(controls_render_2, (0, 85))
            screen.blit(controls_render_3, (55, 155))
            screen.blit(start_text_render, (370, 525)) 
            screen.blit(start_text_render_2, (470, 400))    
            screen.blit(stamina_instruction_render, (412, 984))

    # update display (.flip since implemented double buffering)
    pygame.display.flip()
    
# if loop ends, game quits, sys.exit for smooth program termination and cleanup operations   
pygame.quit()
sys.exit()


# Credits: 
# Code: Anthony Davey
# Free assets: 
# background layers - https://saurabhkgp.itch.io/the-island-parallax-background-platformer-side-scroller
# bg layer: clouds (edited for bg transparency) - ?
# bg layer: sun (edited for bg transparency) - https://www.cleanpng.com/png-real-sun-png-42776/download-png.html
# player sprite - https://www.spriters-resource.com/mobile/senransamuraikingdom/sheet/117279/
# tent - https://www.spriters-resource.com/pc_computer/heroes3/sheet/45028/
# bonfire - https://www.spriters-resource.com/pc_computer/strangetelephone/sheet/151419/
# music (edited for conciseness/looping) - https://anjunadeep.com/us/products/87179-i-want-your-attention
# fonts - branda-font-f30036, chrusty-rock-font-f35152