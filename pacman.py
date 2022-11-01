from struct import pack
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600), 0)

vermelho = (255, 0, 0)
preto = (0,0,0)
velocidade = 1

class Pacman:
    def __init__(self):
        self.coluna = 1
        self.linha = 1
        self.centro_x = 400
        self.centro_y = 300
        self.tamanho = 800 // 30
        self.vel_x = 0
        self.vel_y = 0
        self.raio = self.tamanho // 2

    def calcular_regras(self):
        self.coluna = self.coluna + self.vel_x
        self.linha = self.linha + self.vel_y
        self.centro_x = int(self.coluna * (self.tamanho + self.raio))
        self.centro_y = int(self.linha * (self.tamanho + self.raio))

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

    def process_events(self, events):
        #Capture events
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = velocidade
                elif e.key == pygame.K_LEFT:
                    self.vel_x = -velocidade
                elif e.key == pygame.K_UP:
                    self.vel_y = -velocidade
                elif e.key == pygame.K_DOWN:
                    self.vel_y = velocidade
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = 0
                elif e.key == pygame.K_LEFT:
                    self.vel_x = 0
                elif e.key == pygame.K_UP:
                    self.vel_y = 0
                elif e.key == pygame.K_DOWN:
                    self.vel_y = 0


if __name__ == "__main__":
    pacman = Pacman()

    while True:
        #Calculate rules
        pacman.calcular_regras()

        #Draw screen
        screen.fill(preto)
        pacman.pintar(screen)
        pygame.display.update()
        pygame.time.delay(100)

        #Capture events
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                exit()
        pacman.process_events(events)