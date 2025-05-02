import pygame as pg
import multiprocessing
from screeninfo import get_monitors

MINIDISPLAY_DIMENSIONS = (640,480)

# Initialize Pygame
pg.init()
clock = pg.time.Clock()

# Get monitor resolution
monitors = get_monitors()

# find and use minidisplay
for i in range(len(monitors)):
    disp = monitors[i]  
    width, height = disp.width, disp.height
    if (width,height) == MINIDISPLAY_DIMENSIONS:
        x, y = disp.x, disp.y
        window = pg.display.set_mode((width, height), pg.FULLSCREEN, display = 1)
        pg.display.set_caption('minidisplay')
        break

# if minidisplay not present, show 640x480p rectangle on primary monitor
if (width,height) != MINIDISPLAY_DIMENSIONS:
    print("minidisplay not detected!")
    disp = monitors[0]
    width,height = MINIDISPLAY_DIMENSIONS
    x,y = disp.x,disp.y
    window = pg.display.set_mode((width,height),pg.NOFRAME,display = 0)
    pg.display.set_caption('main')

screen = pg.display.get_surface()


# Draw black and white content (simple checkerboard for demo)
# screen.fill((0, 0, 0))  # Black background
# for i in range(0, width, 100):
#   for j in range(0, height, 100):
#     if (i // 100 + j // 100) % 2 == 0:
#         pg.draw.rect(screen, (255, 255, 255), (i, j, 100, 100))


# pg.display.flip()



for i in range(1000):
    if i%2:
        screen.fill((0,0,0))
    else:
        # screen.fill((255,255,255))
        pg.draw.rect(screen, (255,255,255), (width//2 - 50, height//2 - 50, 100,100))

    pg.display.flip()
    clock.tick(pg.display.get_current_refresh_rate())
    
pg.quit()

