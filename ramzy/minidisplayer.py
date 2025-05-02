import pygame as pg
import multiprocessing
from screeninfo import get_monitors


# Initialize Pygame
pg.init()
clock = pg.time.Clock()

# Get HDMI (second) monitor resolution
monitors = get_monitors()
if len(monitors) < 2:
    disp = monitors[0]
    width,height = 680,480
    x,y = disp.x,disp.y
    window = pg.display.set_mode((width,height),pg.NOFRAME,display = 0)
    pg.display.set_caption('main')

else:
    disp = monitors[1]  # Assuming HDMI is second
    width, height = disp.width, disp.height
    x, y = disp.x, disp.y
    window = pg.display.set_mode((width, height), pg.FULLSCREEN, display = 1)
    pg.display.set_caption('minidisplay')

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
        screen.fill((255,255,255))

    pg.display.flip()
    clock.tick(pg.display.get_current_refresh_rate())
    
pg.quit()

