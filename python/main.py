import pygame
from pygame.locals import *
import sys

class KyoroboTimer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
