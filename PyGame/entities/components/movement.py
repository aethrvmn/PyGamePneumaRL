import pygame


class MovementHandler:

    def __init__(self):
        self.direction = pygame.math.Vector2()

    def move(self, speed, hitbox, obstacle_sprites, rect):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        hitbox.x += self.direction.x * speed
        self.collision('horizontal', hitbox, obstacle_sprites)
        hitbox.y += self.direction.y * speed
        self.collision('vertical', hitbox, obstacle_sprites)
        rect.center = hitbox.center

    def collision(self, direction, hitbox, obstacle_sprites):
        if direction == 'horizontal':
            for sprite in obstacle_sprites:
                # The following works for static obstacles only
                if sprite.hitbox.colliderect(hitbox):
                    # Moving Right
                    if self.direction.x > 0:
                        hitbox.right = sprite.hitbox.left
                    # Moving Left
                    if self.direction.x < 0:
                        hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in obstacle_sprites:
                # The following works for static obstacles only
                if sprite.hitbox.colliderect(hitbox):
                    # Moving Down
                    if self.direction.y > 0:
                        hitbox.bottom = sprite.hitbox.top
                    # Moving Up
                    if self.direction.y < 0:
                        hitbox.top = sprite.hitbox.bottom
