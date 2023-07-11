import pygame
import random

from utils.settings import *
from utils.support import import_folder

class Camera(pygame.sprite.Sprite):

    def __init__(self, position, groups):
        super().__init__(groups)
        
        self.sprite_type = 'camera'
        
        self.image = pygame.image.load('../Graphics/graphics/camera.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(HITBOX_OFFSET[self.sprite_type])

        # Stats
        self.exp = -1 # This prints OBSERVER in the UI
        self.speed = 10 # Speed for moving around
        
        #Movement
        self.direction = pygame.math.Vector2()

    def input(self):
        keys = pygame.key.get_pressed()

        # Movement Input
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
            self.can_move = False
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
            self.can_move = False
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
            self.can_move = False
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
            self.can_move = False
        else:
            self.direction.x = 0
    
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.hitbox.y += self.direction.y * speed
        self.rect.center = self.hitbox.center
        

    def update(self):
        self.input()
        self.move(self.speed)
