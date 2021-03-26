import pygame

class Vector2():
    @classmethod
    def Right(cls):
        return pygame.Vector2(1, 0)

    @classmethod
    def Up(cls):
        return pygame.Vector2(0, -1)

    @classmethod
    def Standard(cls):
        return pygame.Vector2(1, 1)

    @classmethod
    def Zero(cls):
        return pygame.Vector2(0, 0)