# Sunset Run
### Video Demo:  https://www.youtube.com/watch?v=haHnsTj2VpM
### Description:
### Sidescroller game named Sunset Run, made with Python and Pygame, a library for writing video games. This was made through my local vscode on my pc, then translated to cs50's codespace to be able to turn it in with submit50.
---
### Note for CS50 staff:
#### IMPORTANT: Pygame window does not open in cs50's codespace environment (at least for me). The game works fine if opened as an executable or if ran on a local codespace.
#### Github link to SunsetRun.py and SunsetRun.exe: https://github.com/Club-Tony/CS50-Final.github.io/tree/main/CS50-Final-Pygame
---
# Installation:
### https://drive.google.com/drive/u/0/folders/14eEOFYOJt43Cw41fB7fDK-_90E1IsdFD

### To play in local IDE: <br> Download "Sunset_Run" folder above, and all of its contents (except the .exe). Unzip, and make sure pygame is installed in your IDE by typing into your terminal: pip install pygame

### To play with the .exe: <br> Download the "Sunset_Run" folder, then the .exe separately from this github folder by downloading the raw. Ignore the suspicious file flag (I'm an unrecognized publisher so it automatically flags as suspicious). Move SunsetRun.exe into your extracted Sunset_Run folder.
---
### Note: Cloud codespaces may not work to open the pygame window properly, so use your IDE locally if possible.

### Also, make sure your computer's scale and layout settings are at 100% or lower. If higher, game window may be oversized for users with 1920 x 1080 resolution monitors. On windows: Settings - Display - Scale and layout: 100%
---
### Changes I had to make when importing this project into cs50's codespace:
#### Music: Made the option so game can run without music if necessary, because cs50 doesn't support audio, at least not pygame's audio device.
---
# Files:

### Music:

#### "Moon boots i want your attention loop.mp3" <br> an mp3 of the song: Moon Boots - I Want Your Attention, edited by me in FL Studio DAW for conciseness and so it loops smoothly.
---
### Fonts:

#### "Default pygame font" <br> for exit button text, controls, and stamina bar

#### "Branda-yolq.ttf" <br> for game over screen

#### "ChrustyRock-ORLA.ttf" <br> for welcome screen and congratulations screen
---
### Images (.png):

#### L1.png, L2, L3, L4, L5, and L6.png <br> background layers for parallax scrolling background

#### 1.png, 2, 3, 4, 5, 6, and 7.png <br> sprite frames, for idle still and running animation

#### "fire.png" and "tent.png" <br> bonfire with a cooking pot on top, and a tent. Found at end of the game.
---
## "SunsetRun.py"
### This is the Python file with all the code that makes this game run. Below I will go over all the features and what they do.
---
### First, I think it's important to mention the goal of the game, and overall mechanics. Game starts, sprite is standing still. Sprite is centered in the middle of the screen throughout the game. There is a night cycle, so it will slowly start to get dark as time passes. Sprite can't move left at start, but can move right. The goal is to travel about 15000 (pixels) to the right to find shelter. If it gets too dark, game over. If you make it to shelter, congrats screen appears.
---
#### Welcome screen:
##### Appears at game launch, in the center is text with vague directions to find shelter soon, because night is approaching. At the top of the screen are the controls: WASD for left/right movement, SPACE for boost, ESC to exit, M to toggle music, and F11 to toggle window size. Welcome screen is visible for 60 seconds, or until sprite moves to the right and starts progressing. You can return to the left to view the controls again if needed.
---
#### Keybinds/Mouse input:
##### Related to what I wrote about the welcome screen, I implemented keybinds with pygames library functions so they work as intended for a sidescroller. I also implemented mouse input utility so the game recognizes if the user is trying to press a button.
---
#### Stamina bar:
##### This is an ingame mechanic that is necessary to complete the game without failing. Green bar in pink rectangle. Drains when boost is being used (spacebar). If it drains to 0, there is a 10 second cooldown period where you can't use boost. When not boosting, the bar recovers stamina at half the speed that it get used up when boosting.
---
#### A multilayered parallax scrolling background:
##### This was the first major hurdle of the project, as it involved adding a lot of logic to make sure it worked as intended. For one, the background layers had to be drawn in different orders, to add different things to the forefront, and to make sure nothing that was supposed to be appearing a certain way was drawn on top of another layer. Also each of these layers had to loop, so basically drawn side by side, and to make sure it was perfectly repeating otherwise there would be obvious visual flaws that take away from the background seeming infinite. On top of that, each of the layers had to each be set a different scrolling speed, to make it function as a parallax scrolling background. This had to be set up so the layers meant to appear distant, scrolled more slowly. Like the sun, clouds, and far mountains. The middle section like the water, island with trees and hills had to be a bit faster. And finally, the ground layer had to be scrolling the fastest to create the illusion of accurate movement of faraway objects. Also, had to make sure it couldn't scroll further left from starting point of the game.
---
#### A frame-animated character:
##### This was another big hurdle, as it involved working with GIMP (a photoshop type program which I was not at all familiar with), but more relevantly, involved using logic to create the illusion of an animated sprite. This involved making a list of each frame of the sprite's run movement, and having it iterate through the list so it changes which frame was drawn on the screen, and finally making a counter to adjust how fast the list would iterate to create the illusion of a running sprite when moving left or right, and to make sure it matched how fast the ground background layer was scrolling. There was also some image flipping I had to do for each frame depending on whether I was running left or right, or whether I stopped left or right. I wanted the idle and running frames to be drawn properly depending on the way I was facing. Also boosted the speed the list would iterate whenever boost was being used (spacebar) which increased the scrolling speed.
---
#### Left to right sidescrolling:
##### This involved setting keybinds (a, d, left arrow key, right arrow key) and creating a counter to adjust how fast the scroll speed going left or right was depending on what was being pressed. This also included the boost key (spacebar) and adjusting the speed based on whether that was being pressed. As mentioned before, it was important that the background layers were drawn side by side, in order to create the illusion of sidescrolling.
---
#### Buttons:
##### Implemented an exit button that appears on screen for either game over or congratulations screen. Added text inside the button, that highlighted whenever mouse hovered over it to make the button feel more interactive. Pygame.exit() is initiated when this button is pressed, and program exits.
---
#### Day and night cycle:
##### This was done by setting an increment counter that added a surface tint that grew a darker blue color as time passed ingame. When it reaches a given amount, I added another counter that makes the game fade to black, at which point game over screen appears.
---
#### Game over screen:
##### Appears when screen fully fades to black, includes red text with a new creepy looking font with a game over message, and an exit button.
---
#### Congrats screen:
##### Appears when the tent and fire sprites are touched, marking the end of the game. Green text in a new font appear with a congratulations message, as well as the exit button. Also turns off the fade to black and nighttime tint.
---
#### Fullscreen toggle (default 1920 x 1080, toggle between this and smaller screen size):
##### The biggest hurdle by far for this project. At game launch screen starts at 1920 x 1080, I set a keybind (F11 or alt + enter) to adjust screen size between the default, and a smaller screen size. This was implemented for convenience incase someone didn't want to play with fullscreen, or incase the user's monitor resolution was less than 1920 x 1080. What made this a hurdle was having to rescale everything that was drawn in when toggled (images, text, rectangles for buttons) and making sure it rescaled back properly when toggled again to default screen size. Rescaling properly means making sure that the screen doesn't just shrink while everything else stays the same size. The easiest part to rescale was the background layers, because these already took up the full width and height of the default screen so they could just be shortened by doing (draw function stuff here * 0.5) for example. Everything aside from this, the text, sprite, and rectangles were harder to scale because they don't draw exactly where you want them to be on the screen by default. You have to make an initial change so it displays the way you want. Then you have to make sure all these aspects shrink properly when the screen shrinks, and positions properly. Often times when rescaling you'll have to make some manual adjustments to make sure when rescaling, everything appears the same as it did by default, just obviously smaller. As a side note, the game can be completed in about 2 min and 10 sec with the default screen size, and about 30 seconds more quickly than that when using the smaller screen size. This is because when the screen is smaller, it adjusts the scroll speed, and the time it takes for it to tint dark and show the game over screen. But, it's important to note that it does not make the game easier/harder, it only visually scrolls faster and the endgame arrives more quickly.
---
#### Music:
##### Imported a .mp3 into the file, that was edited through fl studio so it looped nicely. Set a keybind M so the music starts if it's pressed, music is off by default. If m has been pressed at least once, the music stays on, and m key just functions as a mute/unmute button but music keeps looping in the background.
---
#### Two additional loaded images to simulate a shelter/campsite for reaching the end of the game:
##### Tent and fire appear at the endgame, at which point when reached you cannot scroll further (15000 pixels to the right), the logic to set this up as intended was harder than expected. I set it up so the images would draw all the way to the right of the screen when a certain distance just below 15000 pixels was reached (14875). When 15000 is reached, sprite appears to be standing next to these drawn images and congrats screen appears.
---
#### Drawing images/rectangles/text onto screen:
##### Just wanted to note that when drawing things onto the screen, the size of the objects being drawn in had to be specific, as well as the x, y locations to make them draw on screen in the intended spot. The width and height of each image could be adjusted as well, to be made either smaller or larger. This was really only a hurdle when working out how to rescale/resize when fullscreen toggle button was pressed, which as mentioned before resized the screen.
---
#### Brief explanation of pygame coding logistics:
##### As a general rule, you start by importing the libraries you need and activating all the pygame modules you'll need. I imported pygame and sys (sys is optional but helps with smooth program termination). Before the game loop starts you can declare any variables that don't need to be changed while in the game loop. Then, for a game to actually work you'll need a game loop, which is basically a forever repeating loop i.e. run = True ... While run: etc. Within the game loop, you can set the FPS, essentially how fast your game will run. You would have an event handler within this loop (pygame.event.get()), this is where you handle any ingame events, conditions, anything that needs to be changed in the game, while the game is running. This could be keybinds, determining when something is drawn, or under what condition, adjusting scroll speed, or implementing window resizing and changes. At the end of the game loop, you can update the display (pygame.display.flip(), pygame.display.get_surface). Finally, after the game loop you can end the program with pygame.quit() and optionally sys.exit() after this to ensure smooth program termination and cleanup operations.
