import pygame
import sys
import os
import random
import sqlite3

pygame.init()


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, 'white', (
                    (self.left + self.cell_size * x), (self.top + self.cell_size * y), self.cell_size, self.cell_size),
                                 1)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if (x < self.left or x > self.left + self.width * self.cell_size or
                y < self.top or y > self.top + self.height * self.cell_size):
            return None
        return (x - self.left) // self.cell_size, (y - self.top) // self.cell_size

    def on_click(self, cell_pos):
        print(cell_pos)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


size = width, height = 1200, 800
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

board1 = Board(10, 10)
board1.set_view(20, 20, 70)

board2 = Board(10, 10)
board2.set_view(160 + 10 * 70 + 20, 20, 70)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board1.get_click(event.pos)
            board2.get_click(event.pos)

    screen.fill('black')
    board1.render(screen)
    board2.render(screen)
    pygame.display.flip()

pygame.quit()
