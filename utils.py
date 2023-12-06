import pygame
def make_background(surface):

    moon= pygame.image.load("assets\kenney_platformer-pack-industrial\PNG\Default size\Ground.png").convert()
    stars= pygame.image.load("assets\Animated\Strip And GIF\space1_4-frames.png").convert()


    #image_wid=64
    #image_hgt=64
    for x in range(0,surface.get_width(), stars.get_width()):
        for y in range (0, surface.get_height(), stars.get_height()):
            surface.blit(stars, (x,y))
    for x in range(0,surface.get_width(), moon.get_width()):
        surface.blit(moon, (x,surface.get_height() - 2*(moon.get_height())))
        surface.blit(moon, (x, surface.get_height() -  moon.get_height()))




class Player:
    def __init__(self, img_path, x, y):
        self.img = pygame.image.load(img_path)
        self.x = x
        self.y = y
        self.x_change = 0
        self.y_change = 0

    def move(self):
        self.x += self.x_change
        self.y += self.y_change

        if self.x <= 0:
            self.x = 0
        elif self.x >= 768:
            self.x = 768

        if self.y <= 0:
            self.y = 0
        elif self.y >= 568:
            self.y = 568

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))