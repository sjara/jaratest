import pygame as pg
import numpy as np
import multiprocessing
from screeninfo import get_monitors

MINIDISPLAY_DIMENSIONS = (640,480)
ACTIVE_AREA = (480,480)

def pixels_from_img(surface: pg.Surface, img: np.ndarray):
    # get surface info
    width,height = surface.get_size()
    xOffset = (width - height)//2
    scaleFactor = height//img.shape[0]
    
    # map image to pixels
    scaledImg = np.kron(img,np.ones((scaleFactor,scaleFactor)))

    # allocate pixels array, 3d array for each RGB values
    pixels = np.zeros((width,height,3))

    # use np.stack to create white image
    pixels[xOffset:xOffset+height,:] = np.stack((scaledImg,scaledImg,scaledImg),axis=2)

    return pixels


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
        screen = pg.display.set_mode((width, height), pg.FULLSCREEN, display = 1)
        pg.display.set_caption('minidisplay')
        break

# if minidisplay not present, show 640x480p rectangle on primary monitor
if (width,height) != MINIDISPLAY_DIMENSIONS:
    print("minidisplay not detected!")
    disp = monitors[0]
    width,height = MINIDISPLAY_DIMENSIONS
    x,y = disp.x,disp.y
    screen = pg.display.set_mode((width,height),pg.NOFRAME,display = 0)
    pg.display.set_caption('main')

surface = pg.display.get_surface()

surface.fill((0,0,0))

for i in range(10):
    img = np.zeros((4,4),dtype=int)
    img[i%4,i%4] = 255

    pixels = pixels_from_img(surface,img)
    pg.surfarray.blit_array(surface,pixels)
    
    pg.display.flip()
    # clock.tick(pg.display.get_current_refresh_rate())
    pg.time.wait(150)
    surface.fill((0,0,0))
    pg.display.flip()
    pg.time.wait(850)
    
pg.quit()

