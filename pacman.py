import pygame, random
from abc import ABCMeta, abstractmethod



pygame.init()

screen = pygame.display.set_mode((800, 600), 0)
fonte = pygame.font.SysFont("arial", 24, True, False)

yellow = (255,255,0)
red = (255,0,0)
black = (0,0,0)
blue = (0,0,255)
white = (255,255,255)
velocidade = 1
acima = 1
abaixo = 2
direita = 3
esquerda = 4

class ElementoJogo(metaclass=ABCMeta):
    @abstractmethod
    def paint(self, tela):
        pass

    @abstractmethod
    def calculate_rules(self):
        pass

    @abstractmethod
    def process_events(self, events):
        pass


class Movivel(metaclass=ABCMeta):
    @abstractmethod
    def accept_move(self):
        pass

    @abstractmethod
    def refuse_move(self, direcoes):
        pass

    @abstractmethod
    def esquina(self, direcoes):
        pass


class Cenario(ElementoJogo):
    def __init__(self, tamanho, pac, fan):
        self.pacman = pac
        self.fantasma = fan
        self.moviveis = [pac, fan]
        self.tamanho = tamanho
        self.points = 0
        self.matriz = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    def paint_points(self, tela):
        points_x = 30 * self.tamanho
        img_points = fonte.render(f"Score: {self.points}", True, red)
        tela.blit(img_points, (points_x, 50))

    def paint_line(self, tela, line_number, line):
        for column_number, column in enumerate(line):
            x = column_number * self.tamanho
            y = line_number * self.tamanho
            half = self.tamanho // 2
            color = black
            if column == 2:
                color = blue
            pygame.draw.rect(tela, color, (x, y, self.tamanho, self.tamanho), 0)
            if column == 1:
                pygame.draw.circle(tela, red, (x + half, y + half), self.tamanho // 10, 0)
    
    def paint(self, tela):
        for line_number, line in enumerate(self.matriz):
            self.paint_line(tela, line_number, line)
        self.paint_points(tela)

    def get_directions(self, linha, coluna):
        direcoes = []
        if self.matriz[int(linha - 1)][int(coluna)] != 2:
            direcoes.append(acima)
        if self.matriz[int(linha + 1)][int(coluna)] != 2:
            direcoes.append(abaixo)
        if self.matriz[int(linha)][int(coluna - 1)] != 2:
            direcoes.append(esquerda)
        if self.matriz[int(linha)][int(coluna + 1)] != 2:
            direcoes.append(direita)
        return direcoes

    def calculate_rules(self):
        for movivel in self.moviveis:
            lin = int(movivel.linha)
            col = int(movivel.coluna)
            lin_intencao = int(movivel.linha_intencao)
            col_intencao = int(movivel.coluna_intencao)
            direcoes = self.get_directions(lin, col)
            if len(direcoes) >= 3:
                movivel.esquina(direcoes)
            if 0 <= col_intencao < 28 and 0 <= lin_intencao < 29 and self.matriz[lin_intencao][col_intencao] != 2:
                movivel.accept_move()
            else: 
                movivel.refuse_move()

    def process_events(self, evts):
        for e in evts:
            if e.type == pygame.QUIT:
                exit()


class Pacman(ElementoJogo, Movivel):
    def __init__(self, tamanho):
        self.column = 1
        self.line = 1
        self.centro_x = 400
        self.centro_y = 300
        self.tamanho = tamanho
        self.vel_x = 0
        self.vel_y = 0
        self.raio = self.tamanho // 2
        self.column_intention = self.column
        self.line_intention = self.line

    def calculate_rules(self):
        self.column_intention = self.column + self.vel_x
        self.line_intention = self.line + self.vel_y
        self.centro_x = int(self.column * self.tamanho + self.raio)
        self.centro_y = int(self.line * self.tamanho + self.raio)

    def paint(self, tela):
        #Draw pacman's body
        pygame.draw.circle(tela, red, (self.centro_x, self.centro_y), self.raio)

        #Draw pacman's mouth
        canto_boca = (self.centro_x, self.centro_y)
        labio_superior = (self.centro_x + self.raio, self.centro_y - self.raio)
        labio_inferior = (self.centro_x + self.raio, self.centro_y)
        pontos = [canto_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, black, pontos, 0)

        #Draw pacman's eye
        olho_x = int(self.centro_x + self.raio / 4)
        olho_y = int(self.centro_y - self.raio * 0.6)
        olho_raio = int(self.raio/10)
        pygame.draw.circle(tela, black, (olho_x, olho_y), olho_raio, 0)

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

    def process_mouse_events(self, events):
        delay = 100
        for e in events:
            if e.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = e.pos
                self.column = (mouse_x - self.centro_x) / delay
                self.line = (mouse_y - self.centro_y) / delay

    def accept_move(self):
        self.line = self.line_intention
        self.column = self.column_intention

    def refuse_move(self, direcoes):
        self.line_intention = self.line
        self.column_intention = self.column   

    def esquina(self, direcoes):
        pass


class Fantasma(ElementoJogo):
    def __init__(self, cor, tamanho):
        self.coluna = 6.0
        self.linha = 2.0
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.velocidade = 1
        self.direcao = abaixo
        self.tamanho = tamanho
        self.cor = cor

    def paint(self, tela):
        fatia = self.tamanho // 8
        px = int(self.coluna * self.tamanho)
        py = int(self.linha * self.tamanho)
        contorno = [(px, py + self.tamanho), 
                    (px + fatia, py + fatia * 2),
                    (px + fatia * 2, py + fatia // 2),
                    (px + fatia * 3, py),
                    (px + fatia * 5, py),
                    (px + fatia * 6, py + fatia // 2),
                    (px + fatia * 7, py + fatia * 2),
                    (px + self.tamanho, py + self.tamanho)]
        pygame.draw.polygon(tela, self.cor, contorno, 0)

        olho_raio_ext = fatia
        olho_raio_int = fatia // 2

        olho_esq_x = int(px + fatia * 2.5)
        olho_esq_y = int(py + fatia * 2.5)

        olho_dir_x = int(px + fatia * 5.5)
        olho_dir_y = int(py + fatia * 2.5)

        pygame.draw.circle(tela, white, (olho_esq_x, olho_esq_y), olho_raio_ext, 0)
        pygame.draw.circle(tela, black, (olho_esq_x, olho_esq_y), olho_raio_int, 0)
        pygame.draw.circle(tela, white, (olho_dir_x, olho_dir_y), olho_raio_ext, 0)
        pygame.draw.circle(tela, black, (olho_dir_x, olho_dir_y), olho_raio_int, 0)


    def calculate_rules(self):
        if self.direcao == acima:
            self.linha_intencao -= self.velocidade
        if self.direcao == abaixo:
            self.linha_intencao += self.velocidade
        if self.direcao == esquerda:
            self.coluna_intencao -= self.velocidade
        if self.direcao == direita:
            self.coluna_intencao += self.velocidade

    def mudar_direcao(self, direcoes):
        self.direcao = random.choice(direcoes)

    def esquina(self, direcoes):
        self.mudar_direcao(direcoes)

    def accept_move(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def refuse_move(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.mudar_direcao(direcoes)

    def process_events(self, events):
        pass

if __name__ == "__main__":
    size = 600 // 30
    pacman = Pacman(size)
    blinky = Fantasma(red, size)
    cenario = Cenario(size, pacman, blinky)

    while True:
        #Calculate rules
        pacman.calculate_rules()
        cenario.calculate_rules()
        blinky.calculate_rules()

        #Draw screen
        screen.fill(black)
        cenario.paint(screen)
        pacman.paint(screen)
        blinky.paint(screen)
        pygame.display.update()
        pygame.time.delay(100)

        #Capture events
        events = pygame.event.get()
        pacman.process_events(events)
        cenario.process_events(events)