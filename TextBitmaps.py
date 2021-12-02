import pygame
from pygame.constants import (KEYDOWN, QUIT, K_ESCAPE)
import os


class Settings:
    window_width = 1000
    window_height = 650
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")

    @staticmethod
    def get_dim():
        return (Settings.window_width, Settings.window_height)

    @staticmethod
    def get_imagepath(filename):
        return os.path.join(Settings.path_image, filename)


class Spritelib(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(Settings.get_imagepath(filename)).convert()
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Letters(object):
    def __init__(self, spritelib) -> None:
        super().__init__()
        self.offset = (6, 6)
        self.dim = (18, 18)
        self.dist = (14, 14)
        self.nof = {'rows': 4, 'cols': 10}
        self.letters = {}
        self.lettername = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                           'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '-', ' ', 'copy', 'square')
        self.letterrect = {}
        self.spritelib = spritelib
        self.create_letterrect()
        self.convert()

    def create_letterrect(self):
        letterindex = 0
        for row in range(self.nof['rows']):
            for col in range(self.nof['cols']):
                left = self.offset[0]+col*(self.dim[0]+self.dist[0])
                top = self.offset[1]+row*(self.dim[1]+self.dist[1])
                width, height = self.dim
                r = pygame.Rect(left, top, width, height)
                self.letterrect[self.lettername[letterindex]] = r
                letterindex += 1

    def draw_rect(self, screen):
        for (key, value) in self.letterrect.items():
            pygame.draw.rect(screen, (255, 255, 255), value, 1)

    def draw_letter(self, screen):
        for (key, value) in self.letterrect.items():
            screen.blit(self.letters[key], value.move(600, 0))

    def draw_string(self, screen, pos, string):
        screen.blit(self.get_text(string), pos)

    def convert(self):
        for (key, value) in self.letterrect.items():
            self.letters[key] = self.spritelib.image.subsurface(value)

    def get_letter(self, letter):
        if letter in self.letters:
            return self.letters[letter]
        else:
            return self.letters['square']

    def get_text(self, text):
        l = len(text) * self.dim[0]
        h = 1 * self.dim[1]
        bitmap = pygame.Surface((l, h))
        for a in range(len(text)):
            bitmap.blit(self.get_letter(text[a]), (a*self.dim[0], 0))
        return bitmap


class TextBitmaps(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.get_dim())
        self.clock = pygame.time.Clock()
        self.filename = "chars.png"
        self.running = False
        self.input = ""

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_BACKSPACE:
                    self.input = self.input[:-1]
                else:
                    self.input += event.unicode

    def run(self):
        spritelib = Spritelib(self.filename)
        letters = Letters(spritelib)
        self.running = True
        while self.running:
            self.clock.tick(60)
            self.watch_for_events()

            self.screen.fill((0, 0, 0))
            spritelib.draw(self.screen)
            # letters.draw_rect(self.screen)
            # letters.draw_letter(self.screen)
            letters.draw_string(self.screen, (400, 200), self.input)

            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"

    demo = TextBitmaps()
    demo.run()
