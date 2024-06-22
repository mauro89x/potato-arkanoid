import pygame
import pygame_menu as pgmenu
import os
from random import randint

size = width, height  = 800, 600
brick_width = 80
brick_height = 20
brick_offset = brick_width / 2
BLACK = (0,0,0)
WHITE = (255,255,255)
DARKBLUE = (36,90,190)
GREEN = (0,255,0)
LIGHTBLUE = (0,176,240)
PLATINUM = (229, 228, 226)
RED = (255,0,0)

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "../assets/sounds")
global_score = 0

class GameData():
    def __init__(self, level):
        self.level = level
        self.score = 0
        self.lives = 3
    
    def inc_score(self, score):
        self.score += score

    def inc_level(self):
        self.level += 1

    def dec_live(self):
        self.lives -= 1

    def reset_data(self):
        self.level = 1
        self.score = 0
        self.lives = 3

class Brick(pygame.sprite.Sprite):
    def __init__(self, posx, health, color, height):
        super().__init__()
        self.image = pygame.Surface([brick_width, brick_height])
        self.image.fill(BLACK)
        pygame.draw.rect(self.image, color, [0,0, brick_width, brick_height])
        self.rect = self.image.get_rect()
        self.rect.x = posx + brick_offset
        self.rect.y = height
        self.health = health
        self.score = 1

    def setColor(self, aColor):
        self.image.fill(aColor)

    def incrementScore(self):
        self.score += 1
        
class Pad(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, width, height], border_radius=10)
        self.rect = self.image.get_rect()
        self.rect.x = screen.get_width() / 2
        self.rect.y = screen.get_height() - 30

    def set_color(self, color):
        self.image.fill(color)

    def handle_control(self, ball):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-10, 0)
        if key[pygame.K_RIGHT] and self.rect.left < (width - self.rect.width):
            self.rect.move_ip(10, 0)
        if key[pygame.K_SPACE] and not ball.alive:
            ball.toggleAlive()
        if not ball.alive:
            ball.rect.x = self.rect.centerx

class Ball(pygame.sprite.Sprite):
    
    def __init__(self, color, width, height, gameData, padRect):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.alive = False
        pygame.draw.rect(self.image, color, [0, 0, width, height], border_radius=10)
        self.rect = self.image.get_rect()
        self.rect.x = screen.get_width() / 2
        self.rect.y = screen.get_height() / 2
        self.padRect = padRect
        speedx = randint(1,9)
        speedy = -9
        self.velocity = [speedx, speedy]
        self.gameData = gameData

    def update(self):
        if self.alive:
            if self.rect.top < 50:
                self.velocity[1] = -self.velocity[1]
            if self.rect.left < 0 or self.rect.right > screen.get_width(): 
                self.velocity[0] = -self.velocity[0]
            if self.rect.bottom > screen.get_height():
                self.gameData.dec_live()
                self.velocity = [5, -5]
                if self.gameData.lives == 0:
                    gameOverScreen(self.gameData)
                self.toggleAlive()
                self.resetBall()
            self.rect.move_ip((self.velocity))
    
    def resetBall(self):
        self.rect.x = self.padRect.centerx        
        self.rect.y = self.padRect.top - 15
        
    def set_velocity(self, xspeed, yspeed):
        self.velocity[0] = xspeed
        self.velocity[1] = yspeed

    def bounce(self):
        self.velocity[1] = -self.velocity[1]
    
    def toggleAlive(self):
        self.alive = not self.alive
     
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

def gameOverScreen(gameData):
    """Game over screen to restart"""
    pygame.mixer.music.load("./assets/music/game_over_music.mp3")
    pygame.mixer.music.play()
    menu = pgmenu.Menu(f"Game over, You've failed level {gameData.level}", screen.get_width(), screen.get_height(), theme=pgmenu.themes.THEME_GREEN)
    menu.add.button("Try again?", mainLoop, gameData)
    menu.add.button("Exit", pgmenu.events.EXIT)
    menu.mainloop(screen)

def levelCompletedScreen(gameData):
    """Level completed screen"""
    pygame.mixer.music.load("./assets/music/level_completed_music.mp3")
    pygame.mixer.music.play()
    menu = pgmenu.Menu(f"You've beaten level {gameData.level}!", screen.get_width(), screen.get_height(), theme=pgmenu.themes.THEME_GREEN)
    gameData.inc_level()
    menu.add.button("Next level!", mainLoop, gameData)
    menu.add.button("Exit", pgmenu.events.EXIT)
    menu.mainloop(screen)

def creditsScreen(gameData):
    """Shown when game is completed"""
    pygame.mixer.music.load("./assets/music/credits_music.mp3")
    pygame.mixer.music.play()
    menu = pgmenu.Menu(f"You've beaten the game. Your score is {gameData.score}", screen.get_width(), screen.get_height(), theme=pgmenu.themes.THEME_GREEN)
    gameData.reset_data()
    menu.add.button("Start again?", mainLoop, gameData)
    menu.add.button("Exit", pgmenu.events.EXIT)
    menu.mainloop(screen)

def menu():
    """Main menu"""
    pygame.mixer.music.play()
    gameData = GameData(1)
    menu = pgmenu.Menu("Potato Arkanoid", screen.get_width(), screen.get_height(), theme=pgmenu.themes.THEME_GREEN)
    menu.add.button("Play", mainLoop, gameData)
    menu.add.button("Exit", pgmenu.events.EXIT)
    menu.mainloop(screen)

def mainLoop(gameData):
    """Main loop"""
    pygame.mixer.music.stop()
    sprites_list = pygame.sprite.Group()
    brick_list = pygame.sprite.Group()
    font = pygame.font.Font(None, 32)
    score_tracker = 0
    destroy_brick_sound = load_sound("brick_destroy.wav")
    hit_brick_sound = load_sound("brick_hit_not_destroy.wav")
    pad_bounce_ball_sound = load_sound("pad_bounce_ball.wav")    
    pad = Pad(WHITE, 150, 25)
    ball = Ball(WHITE, 10,10, gameData, pad.rect)

    destroy_sound_channel = pygame.mixer.Channel(1)
    hit_brick_channel = pygame.mixer.Channel(2)

    sprites_list.add(pad)
    sprites_list.add(ball)

    ball.rect.x = pad.rect.centerx
    ball.rect.y = pad.rect.top - 10
    offset = 10

    if gameData.level == 1:
        for i in range(8):
            brick_list.add(Brick((brick_width + offset) * i, 1, RED, 100))
            
    if gameData.level == 2:
        for i in range(8):
            brick_list.add(Brick((brick_width + offset) * i, 2, RED, 100))
            brick_list.add(Brick((brick_width + offset) * i, 1, BLACK, 130))

    if gameData.level == 3:
        for i in range(8):
            brick_list.add(Brick((brick_width + offset) * i, 2, RED, 100))
            brick_list.add(Brick((brick_width + offset) * i, 1, BLACK, 130))
            brick_list.add(Brick((brick_width + offset) * i, 3, PLATINUM, 160))            

    if gameData.level == 4:
        creditsScreen(gameData)
        
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
            pad_bounce_ball_sound.play()
            offset = ball.rect.centerx - pad.rect.centerx
            if offset > 0:
                    if offset > 50 and offset < 75:  
                        ball.velocity[0] = 9
                    elif offset > 25 and offset < 49:                 
                        ball.velocity[0] = 6
                    elif offset > 15 and offset < 24:
                        ball.velocity[0] = 4
            else:  
                    if offset < -50 and offset > -75:
                        ball.velocity[0] = -9
                    elif offset < -25 and offset > -49:
                        ball.velocity[0] = -6
                    elif offset < -15 and offset > -24:
                        ball.velocity[0] = -4

            ball.velocity[1] = -ball.velocity[1]

        brick_hit = pygame.sprite.spritecollideany(ball, brick_list)
        if brick_hit:
            brick_hit.health -= 1
            hit_brick_channel.play(hit_brick_sound)
            if brick_hit.health == 0:
                brick_list.remove(brick_hit)
                if destroy_sound_channel.get_busy():
                    destroy_sound_channel.play(destroy_brick_sound)
                score_tracker += brick_hit.score
                gameData.inc_score(brick_hit.score)
            else:
                brick_hit.setColor(BLACK)
            ball.bounce()

        if len(brick_list) == 0:
            levelCompletedScreen(gameData)

        pad.handle_control(ball)
        
        textScore = font.render(f"Score: {score_tracker}", True, (WHITE))
        textScorePos = textScore.get_rect(centerx=70, y = 10)
        textLevel = font.render(f"Current level: {gameData.level}", True, (WHITE))
        textLevelPos = textLevel.get_rect(centerx=screen.get_width() - 100, y = 10)
        textLives = font.render(f"Lives: {gameData.lives}", True, (WHITE))
        textLivesPos = textLives.get_rect(centerx=screen.get_width() / 2, y = 10)
        screen.blit(textScore, textScorePos)
        screen.blit(textLevel, textLevelPos)
        screen.blit(textLives, textLivesPos)
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
    menu()
