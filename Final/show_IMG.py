import pygame
import os

#Set up pygame and the display

MAP_PIXEL_SIZE=500

pygame.init()
lcd = pygame.display.set_mode((MAP_PIXEL_SIZE, MAP_PIXEL_SIZE))
pygame.mouse.set_visible(False)
lcd.fill((0, 0, 0))
pygame.display.update()

