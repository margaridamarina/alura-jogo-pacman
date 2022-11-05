import pygame

pygame.init()

screen = pygame.display.set_mode((800,600), 0)
points = 10

text = f"Score: {points}"

font = pygame.font.SysFont("arial", 48, True, False) #font, size, bold, italic
img_text = font.render(text, True, (255, 255, 0)) #texto, suavizado, color

while True:
    screen.blit(img_text, (100, 100))
    pygame.display.update()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()