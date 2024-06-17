import pygame
import pygame_menu as pgmenu

size = width, height  = 800, 600

BLACK = (0,0,0)
WHITE = (255,255,255)
DARKBLUE = (36,90,190)
LIGHTBLUE = (0,176,240)

class Pad(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.rect.x = screen.get_width() / 2
        self.rect.y = screen.get_height() - 30

    def handle_control(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-10, 0)
        if key[pygame.K_RIGHT] and self.rect.left < (width - self.rect.width):
            self.rect.move_ip(10, 0)    

class Ball(pygame.sprite.Sprite):
    
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width, height], border_radius=10)
        self.rect = self.image.get_rect()
        self.rect.x = screen.get_width() / 2
        self.rect.y = screen.get_height() / 2
        self.velocity = [-5,5]

    def update(self):
        if self.rect.top < 0:
            self.velocity[1] = -self.velocity[1]
        if self.rect.left < 0 or self.rect.right > screen.get_width(): 
            self.velocity[0] = -self.velocity[0]
        self.rect.move_ip((self.velocity))
      
    def bounce(self):
        self.velocity[1] = -self.velocity[1]
        
def menu():
    """Menu principal del juego"""
    pygame.mixer.music.play()

    menu = pgmenu.Menu("Potato Arkanoid", screen.get_width(), screen.get_height(), theme=pgmenu.themes.THEME_GREEN)
    menu.add.button("Jugar", mainLoop)
    menu.add.button("Salir", pgmenu.events.EXIT)
    menu.mainloop(screen)


def mainLoop():
    """Main loop del juego """
    pygame.mixer.music.stop()

    sprites_list = pygame.sprite.Group()
    pad = Pad(WHITE, 150, 25)
    ball = Ball(WHITE, 10,10)
    sprites_list.add(pad)
    sprites_list.add(ball)
    clock = pygame.time.Clock()
    running = True
    
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        sprites_list.update()

        screen.fill(DARKBLUE)

        pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2)

        sprites_list.draw(screen)

        if(pygame.sprite.collide_mask(ball, pad)):            
            if ball.rect.x < pad.rect.centerx:
                if ball.velocity[0] > 0:
                    ball.velocity[0] = -ball.velocity[0]

            if ball.rect.x > pad.rect.centerx:
                if ball.velocity[0] < 0:
                    ball.velocity[0] = -ball.velocity[0]

            ball.bounce()
        pad.handle_control()
        pygame.display.flip()
        clock.tick(60)
    menu()

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("./assets/music/main_menu_music.mp3")
    screen = pygame.display.set_mode((size))
    pygame.display.set_caption("Potato Arkanoid")
    pygame.mouse.set_visible(False)
    print(f'Screen initialized... {screen.get_width()} x {screen.get_height()}')
    menu()