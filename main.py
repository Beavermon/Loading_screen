# requires the latest version of Python and PIP installed. 

import pygame
import sys
from button import Button
from pygame import mixer

# list of things imported ^^

mixer.init()
pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Jazzy-Hands")
BG = pygame.image.load("image/Background.png")


# window configuration ^^

def get_font(size):
    return pygame.font.Font("font/font.ttf", size)


# game \/
def play():
    font = pygame.font.Font(pygame.font.get_default_font(), 100)
    combo = 0
    while True:
        pygame.mouse.get_pos()
        clock = pygame.time.Clock()

        screen = pygame.display.set_mode((800, 600))

        # first we will create the size of locked keys

        class Key:
            def __init__(self, x, y, color1, color2, key):
                self.x = x
                self.y = y
                self.color1 = color1
                self.color2 = color2
                self.key = key
                self.rect = pygame.Rect(self.x, self.y, 40, 40)
                self.handled = False

        # list of keys (a,s,d,f) & location of the 4 locked squares

        keys = [
            Key(100, 500, (255, 0, 0), (220, 0, 0), pygame.K_a),
            Key(200, 500, (0, 255, 0), (0, 220, 0), pygame.K_s),
            Key(300, 500, (0, 0, 255), (0, 0, 220), pygame.K_d),
            Key(400, 500, (255, 255, 0), (220, 220, 0), pygame.K_f),
        ]

        # let's load the map into the game
        def load(map):
            rects = []
            mixer.music.load(map + ".mp3")
            mixer.music.play()
            f = open(map + ".txt", 'r')
            data = f.readlines()

            for y in range(len(data)):
                for x in range(len(data[y])):
                    if data[y][x] == '0':
                        rects.append(pygame.Rect(keys[x].rect.centerx - 25, y * -100, 50, 25))
            return rects

        map_rect = load("freedom dive")

        while True:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # now we will loop through the keys and handle the events
            k = pygame.key.get_pressed()
            for key in keys:
                if k[key.key]:
                    pygame.draw.rect(screen, key.color1, key.rect)
                    key.handled = False
                if not k[key.key]:
                    pygame.draw.rect(screen, key.color2, key.rect)
                    key.handled = True
                # now when we press our keys they will change color
            for rect in map_rect:
                pygame.draw.rect(screen, (200, 0, 0), rect)
                rect.y += 4

                # speed ^^

                for key in keys:
                    if key.rect.colliderect(rect) and not key.handled:
                        map_rect.remove(rect)
                        combo += 1
                        key.handled = True
                        break
                if keys[0].rect.bottom < rect.y:
                    map_rect.remove(rect)
                    combo = 0
                # basically, if the rectangle's bottom thingy y coordinate is smaller (<) than the other rectangles y, \
                # then it will set combo counter to 0
                text = font.render(str(combo), True, "blue")
                screen.blit(text, (10, 10))

            pygame.display.update()
            clock.tick(60)
        screen.fill("black")

        pygame.display.update()


# options \/
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(45).render("Your goal is to reach 20 on the combo counter!", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="GO BACK!", font=get_font(75), base_color="Black", hovering_color="Red")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("jazzy-hands", True, "#FFD700")
        MENU_RECT = MENU_TEXT.get_rect(center=(940, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("image/Play Rect.png"), pos=(940, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("image/Options Rect.png"), pos=(940, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("image/Quit Rect.png"), pos=(940, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
