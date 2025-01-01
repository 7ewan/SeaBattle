import pygame
import sys
import os
import random
import sqlite3

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('white')
    pygame.display.flip()
    clock.tick(30)
pygame.quit()