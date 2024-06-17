import pygame
import pygame_menu as pgmenu
import os 
size = width, height  = 800, 600
brick_width = 80
brick_height = 20

BLACK = (0,0,0)
WHITE = (255,255,255)
DARKBLUE = (36,90,190)
LIGHTBLUE = (0,176,240)
RED = (255,0,0)

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "assets/sounds")

class Brick(pygame.sprite.Sprite):
    def __init__(self, posx):
        super().__init__()
        self.image = pygame.Surface([brick_width, brick_height])
        self.image.fill(BLACK)
        pygame.draw.rect(self.image, RED, [0,0, brick_width, brick_height])
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = 50

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
        if self.rect.bottom > screen.get_height():
            gameOverScreen()
        self.rect.move_ip((self.velocity))
      
    def bounce(self):
        self.velocity[1] = -self.velocity[1]

def load_sound(name):
    """Utility to start pygame mixer and load a sound"""
    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    
    fullname = os.path.join(data_dir, name)
    sound = pygame.mixer.Sound(fullname)
    return sound

def gameOverScreen():
    """Game over screen to restart"""
    pygame.mixer.music.load("./assets/music/game_over_music.mp3")
    pygame.mixer.music.play()
    menu = pgmenu.Menu("Game over", screen.get_width(), screen.get_height(), theme=pgmenu.themes.THEME_GREEN)
    menu.add.button("Play again!", mainLoop)
    menu.add.button("Exit", pgmenu.events.EXIT)
    menu.mainloop(screen)

def menu():
    """Main menu"""
    pygame.mixer.music.play()
    menu = pgmenu.Menu("Potato Arkanoid", screen.get_width(), screen.get_height(), theme=pgmenu.themes.THEME_GREEN)
    menu.add.button("Jugar", mainLoop)
    menu.add.button("Salir", pgmenu.events.EXIT)
    menu.mainloop(screen)

def mainLoop():
    """Main loop"""
    pygame.mixer.music.stop()

    sprites_list = pygame.sprite.Group()

    brick_list = pygame.sprite.Group()

    destroy_brick_sound = load_sound("brick_destroy.wav")

    pad = Pad(WHITE, 150, 25)
    ball = Ball(WHITE, 10,10)
    sprites_list.add(pad)
    sprites_list.add(ball)
    offset = 10
    for i in range(8):
        brick_list.add(Brick((brick_width + offset) * i))

    clock = pygame.time.Clock()
    running = True
    
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        sprites_list.update()
        brick_list.update()

        screen.fill(DARKBLUE)

        pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2)

        sprites_list.draw(screen)
        brick_list.draw(screen)

        if(pygame.sprite.collide_mask(ball, pad)):            
            if ball.rect.x < pad.rect.centerx:
                if ball.velocity[0] > 0:
                    ball.velocity[0] = -ball.velocity[0]

            if ball.rect.x > pad.rect.centerx:
                if ball.velocity[0] < 0:
                    ball.velocity[0] = -ball.velocity[0]

            ball.bounce()
        
        brick_hit = pygame.sprite.spritecollideany(ball, brick_list)
        if brick_hit:
            brick_list.remove(brick_hit)
            destroy_brick_sound.play()
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