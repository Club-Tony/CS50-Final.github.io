import sys, pygame
import random

pygame.init()

# Set display size so it adjusts based off user's resolution, and makes a windowed screen)
resolution_info = pygame.display.Info()
screen = pygame.display.set_mode((int(resolution_info.current_w * 0.93), 
                                  int(resolution_info.current_h * 0.93)))

# Set sprite (player) speed and clock (for controlling framerate)
speed = 5
clock = pygame.time.Clock()

# Set up scrolling parallax background img, 2 of each of the 8 layers, place each side by side
background_1 = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\The_Dawn(parallax_scrolling_background)\\Layers\\1.png")
background_1 = pygame.transform.scale(background_1, (resolution_info.current_w * 0.93, resolution_info.current_h * 0.93))
background_1_copy = background_1

background_2 = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\The_Dawn(parallax_scrolling_background)\\Layers\\2.png")
background_2 = pygame.transform.scale(background_2, (resolution_info.current_w * 0.93, resolution_info.current_h * 0.93))
background_2_copy = background_2

background_3 = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\The_Dawn(parallax_scrolling_background)\\Layers\\3.png")
background_3 = pygame.transform.scale(background_3, (resolution_info.current_w * 0.93, resolution_info.current_h * 0.93))
background_3_copy = background_3

background_4 = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\The_Dawn(parallax_scrolling_background)\\Layers\\4.png")
background_4 = pygame.transform.scale(background_4, (resolution_info.current_w * 0.93, resolution_info.current_h * 0.93))
background_4_copy = background_4

background_5 = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\The_Dawn(parallax_scrolling_background)\\Layers\\5.png")
background_5 = pygame.transform.scale(background_5, (resolution_info.current_w * 0.93, resolution_info.current_h * 0.93))
background_5_copy = background_5

background_6 = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\The_Dawn(parallax_scrolling_background)\\Layers\\6.png")
background_6 = pygame.transform.scale(background_6, (resolution_info.current_w * 0.93, resolution_info.current_h * 0.93))
background_6_copy = background_6

background_7 = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\The_Dawn(parallax_scrolling_background)\\Layers\\7.png")
background_7 = pygame.transform.scale(background_7, (resolution_info.current_w * 0.93, resolution_info.current_h * 0.93))
background_7_copy = background_7

background_8 = pygame.image.load("C:\\Users\\Davey\\Documents\\GitHub\\CS50-Final.github.io\\CS50-Final-Pygame\\The_Dawn(parallax_scrolling_background)\\Layers\\8.png")
background_8 = pygame.transform.scale(background_8, (resolution_info.current_w * 0.93, resolution_info.current_h * 0.93))
background_8_copy = background_8

# Create sprite (player) and shrink size
player = pygame.image.load("blackhole.gif")
player = pygame.transform.scale(player, (50, 50))

# Set screen_width and height to allow for random sprite starting point, and get rect for player
screen_width = int(resolution_info.current_w * 0.93)
screen_height = int(resolution_info.current_h * 0.93)

random_x = random.uniform(350, screen_width)
random_y = random.uniform(350, screen_height)

player_rect = player.get_rect()
player_rect.centerx = random_x
player_rect.centery = random_y

# Setup double buffering:
buffer = pygame.Surface((resolution_info.current_w, resolution_info.current_h))

# Game Loop (handling events). First, if quit, end loop:
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False
                
    # Keybinds:
    keys = pygame.key.get_pressed()   
           
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_rect.x -= speed
        
    pygame.display.update()
    
    # Clear buffer before drawing
    buffer.fill((0, 0, 0))
    
    # blit backgrounds (=should be drawn first, before the sprite or anything else) setup for parallax scroll
    buffer.blit(background_1, (0, 0))
    buffer.blit(background_1_copy, (screen_width, 0))
    
    buffer.blit(background_2, (0, 0))
    buffer.blit(background_2_copy, (screen_width, 0))
    
    buffer.blit(background_3, (0, 0))
    buffer.blit(background_3_copy, (screen_width, 0))
    
    buffer.blit(background_4, (0, 0))
    buffer.blit(background_4_copy, (screen_width, 0))
    
    buffer.blit(background_5, (0, 0))
    buffer.blit(background_5_copy, (screen_width, 0))
    
    buffer.blit(background_6, (0, 0))
    buffer.blit(background_6_copy, (screen_width, 0))
    
    buffer.blit(background_7, (0, 0))
    buffer.blit(background_7_copy, (screen_width, 0))
    
    buffer.blit(background_8, (0, 0))
    buffer.blit(background_8_copy, (screen_width, 0))
    
    # blit 'player' (draws img onto screen)
    buffer.blit(player, player_rect)
    
    # Swap buffer with screen
    screen.blit(buffer, (0, 0))
    pygame.display.flip()
    
    # Set FPS
    clock.tick(60)
    
pygame.quit()   
sys.exit()