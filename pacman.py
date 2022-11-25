import pygame, random
from abc import ABCMeta, abstractmethod



pygame.init()

screen = pygame.display.set_mode((800, 600), 0)
font = pygame.font.SysFont("arial", 24, True, False)

yellow = (255,255,0)
red = (255,0,0)
black = (0,0,0)
blue = (0,0,255)
white = (255,255,255)
cyan = (0,255,255)
orange = (255,140,0)
pink = (255,15,192)
speed = 1
up = 1
down = 2
right = 3
left = 4

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
    def refuse_move(self, directions):
        pass

    @abstractmethod
    def corner(self, directions):
        pass


class Cenario(ElementoJogo):
    def __init__(self, tamanho, pac):
        self.pacman = pac
        self.movables = []
        self.tamanho = tamanho
        self.points = 0
        self.state = 'playing'
        #0-Playing 1-Paused 2-GameOver 3-Win
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

    def add_movable(self, obj):
        self.movables.append(obj)

    def paint_points(self, tela):
        points_x = 30 * self.tamanho
        img_points = font.render(f"Score: {self.points}", True, red)
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
        if self.state == 'playing':
            self.paint_playing(tela)
        elif self.state == 'paused':
            self.paint_playing(tela)
            self.paint_paused(tela)
        elif self.state == 'game_over':
            self.paint_playing(tela)
            self.paint_game_over(tela)
        elif self.state == 'win':
            self.paint_playing(tela)
            self.paint_win(tela)

    def paint_text_center(self, tela, text):
        img_text = font.render(text, True, yellow)
        text_x = (tela.get_width() - img_text.get_width()) // 2
        text_y = (tela.get_height() - img_text.get_height()) // 2
        tela.blit(img_text, (text_x, text_y))

    def paint_game_over(self, tela):
        self.paint_text_center(tela, 'G A M E  O V E R')

    def paint_paused(self, tela):
        self.paint_text_center(tela, 'P A U S E D')

    def paint_win(self, tela):
        self.paint_text_center(tela, 'C O N G R A T U L A T I O N S , Y O U  W O N ! ! !')

    def paint_playing(self, tela):
        for line_number, line in enumerate(self.matriz):
            self.paint_line(tela, line_number, line)
        self.paint_points(tela)

    def get_directions(self, line, column):
        directions = []
        if self.matriz[int(line - 1)][int(column)] != 2:
            directions.append(up)
        if self.matriz[int(line + 1)][int(column)] != 2:
            directions.append(down)
        if self.matriz[int(line)][int(column - 1)] != 2:
            directions.append(left)
        if self.matriz[int(line)][int(column + 1)] != 2:
            directions.append(right)
        return directions

    def calculate_rules(self):
        if self.state == 'playing':
            self.calculate_rules_playing()
        elif self.state == 'paused':
            self.calculate_rules_paused()
        elif self.state == 'game_over':
            self.calculate_rules_game_over()

    def calculate_rules_paused(self):
        pass

    def calculate_rules_game_over(self):
        pass

    def calculate_rules_playing(self):
        for movable in self.movables:
            lin = int(movable.line)
            col = int(movable.column)
            lin_intention = int(movable.line_intention)
            col_intention = int(movable.column_intention)
            directions = self.get_directions(lin, col)
            if len(directions) >= 3:
                movable.corner(directions)
            if isinstance(movable, Ghost) and movable.line == self.pacman.line and movable.column == self.pacman.column:
                self.state = 'game_over'
            else:
                if 0 <= col_intention < 28 and 0 <= lin_intention < 29 and self.matriz[lin_intention][col_intention] != 2:
                    movable.accept_move()
                    if isinstance(movable, Pacman) and self.matriz[lin][col] == 1:
                        self.points += 1
                        self.matriz[lin][col] = 0
                        if self.points >= 306:
                            self.state = 'win'
                else: 
                    movable.refuse_move(directions)

    def process_events(self, evts):
        for e in evts:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if self.state == 'playing':
                        self.state = 'paused'
                    else:
                        self.state = 'playing'


class Pacman(ElementoJogo, Movivel):
    def __init__(self, tamanho):
        self.column = 1
        self.line = 1
        self.center_x = 400
        self.center_y = 300
        self.tamanho = tamanho
        self.vel_x = 0
        self.vel_y = 0
        self.radius = self.tamanho // 2
        self.column_intention = self.column
        self.line_intention = self.line
        self.opening = 0
        self.speed_opening = 1

    def calculate_rules(self):
        self.column_intention = self.column + self.vel_x
        self.line_intention = self.line + self.vel_y
        self.center_x = int(self.column * self.tamanho + self.radius)
        self.center_y = int(self.line * self.tamanho + self.radius)

    def paint(self, tela):
        #Draw pacman's body
        pygame.draw.circle(tela, yellow, (self.center_x, self.center_y), self.radius)

        #Draw pacman's mouth
        self.opening += self.speed_opening
        if self.opening > self.radius:
            self.speed_opening = -1
        if self.opening <= 0:
            self.speed_opening = 1
        canto_boca = (self.center_x, self.center_y)
        labio_superior = (self.center_x + self.radius, self.center_y - self.opening)
        labio_inferior = (self.center_x + self.radius, self.center_y + self.opening)
        pontos = [canto_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, black, pontos, 0)

        #Draw pacman's eye
        eye_x = int(self.center_x + self.radius / 4)
        eye_y = int(self.center_y - self.radius * 0.6)
        eye_radius = int(self.radius/10)
        pygame.draw.circle(tela, black, (eye_x, eye_y), eye_radius, 0)

    def process_events(self, events):
        #Capture events
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = speed
                elif e.key == pygame.K_LEFT:
                    self.vel_x = -speed
                elif e.key == pygame.K_UP:
                    self.vel_y = -speed
                elif e.key == pygame.K_DOWN:
                    self.vel_y = speed
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
                self.column = (mouse_x - self.center_x) / delay
                self.line = (mouse_y - self.center_y) / delay

    def accept_move(self):
        self.line = self.line_intention
        self.column = self.column_intention

    def refuse_move(self, directions):
        self.line_intention = self.line
        self.column_intention = self.column   

    def corner(self, directions):
        pass


class Ghost(ElementoJogo):
    def __init__(self, color, tamanho):
        self.column = 13.0
        self.line = 15.0
        self.line_intention = self.line
        self.column_intention = self.column
        self.speed = 1
        self.direction = down
        self.tamanho = tamanho
        self.color = color

    def paint(self, tela):
        slice = self.tamanho // 8
        px = int(self.column * self.tamanho)
        py = int(self.line * self.tamanho)
        contorno = [(px, py + self.tamanho), 
                    (px + slice, py + slice * 2),
                    (px + slice * 2, py + slice // 2),
                    (px + slice * 3, py),
                    (px + slice * 5, py),
                    (px + slice * 6, py + slice // 2),
                    (px + slice * 7, py + slice * 2),
                    (px + self.tamanho, py + self.tamanho)]
        pygame.draw.polygon(tela, self.color, contorno, 0)

        eye_radius_ext = slice
        eye_radius_int = slice // 2

        eye_esq_x = int(px + slice * 2.5)
        eye_esq_y = int(py + slice * 2.5)

        eye_dir_x = int(px + slice * 5.5)
        eye_dir_y = int(py + slice * 2.5)

        pygame.draw.circle(tela, white, (eye_esq_x, eye_esq_y), eye_radius_ext, 0)
        pygame.draw.circle(tela, black, (eye_esq_x, eye_esq_y), eye_radius_int, 0)
        pygame.draw.circle(tela, white, (eye_dir_x, eye_dir_y), eye_radius_ext, 0)
        pygame.draw.circle(tela, black, (eye_dir_x, eye_dir_y), eye_radius_int, 0)


    def calculate_rules(self):
        if self.direction == up:
            self.line_intention -= self.speed
        if self.direction == down:
            self.line_intention += self.speed
        if self.direction == left:
            self.column_intention -= self.speed
        if self.direction == right:
            self.column_intention += self.speed

    def mudar_direction(self, directions):
        self.direction = random.choice(directions)

    def corner(self, directions):
        self.mudar_direction(directions)

    def accept_move(self):
        self.line = self.line_intention
        self.column = self.column_intention

    def refuse_move(self, directions):
        self.line_intention = self.line
        self.column_intention = self.column
        self.mudar_direction(directions)

    def process_events(self, events):
        pass

if __name__ == "__main__":
    size = 600 // 30
    pacman = Pacman(size)
    blinky = Ghost(red, size)
    inky = Ghost(cyan, size)
    clyde = Ghost(orange, size)
    pinky = Ghost(pink, size)
    cenario = Cenario(size, pacman)
    cenario.add_movable(pacman)
    cenario.add_movable(blinky)
    cenario.add_movable(inky)
    cenario.add_movable(clyde)
    cenario.add_movable(pinky)


    while True:
        #Calculate rules
        pacman.calculate_rules()
        cenario.calculate_rules()
        blinky.calculate_rules()
        inky.calculate_rules()
        clyde.calculate_rules()
        pinky.calculate_rules()


        #Draw screen
        screen.fill(black)
        cenario.paint(screen)
        pacman.paint(screen)
        blinky.paint(screen)
        inky.paint(screen)
        clyde.paint(screen)
        pinky.paint(screen)
        pygame.display.update()
        pygame.time.delay(100)

        #Capture events
        events = pygame.event.get()
        pacman.process_events(events)
        cenario.process_events(events)