from struct import pack
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600), 0)

vermelho = (255, 0, 0)
preto = (0,0,0)

class Pacman:
    def __init__(self):
        self.centro_x = 400
        self.centro_y = 300
        self.tamanho = 100
        self.vel_x = 1
        self.vel_y = 1
        self.raio = self.tamanho // 2

    def calcular_regras(self):
        self.centro_x = self.centro_x + self.vel_x
        self.centro_y = self.centro_y + self.vel_y

        if self.centro_x  + self.raio > 800:
            self.vel_x = -1
        if self.centro_x  - self.raio < 0:
            self.vel_x = 1
        if self.centro_y  + self.raio > 600:
            self.vel_y = -1
        if self.centro_y  - self.raio < 0:
            self.vel_y = 1


    def pintar(self, tela):
        #Draw pacman's body
        pygame.draw.circle(tela, vermelho, (self.centro_x, self.centro_y), self.raio)

        #Draw pacman's mouth
        canto_boca = (self.centro_x, self.centro_y)
        labio_superior = (self.centro_x + self.raio, self.centro_y - self.raio)
        labio_inferior = (self.centro_x + self.raio, self.centro_y)
        pontos = [canto_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, preto, pontos, 0)

        #Draw pacman's eye
        olho_x = int(self.centro_x + self.raio / 4)
        olho_y = int(self.centro_y - self.raio * 0.6)
        olho_raio = int(self.raio/10)
        pygame.draw.circle(tela, preto, (olho_x, olho_y), olho_raio, 0)

if __name__ == "__main__":
    pacman = Pacman()

    while True:
        #Calculate rules
        pacman.calcular_regras()

        #Draw screen
        screen.fill(preto)
        pacman.pintar(screen)
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()