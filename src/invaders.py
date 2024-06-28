import pygame
size = width, height = 800, 600

invader_width = 40
invader_height = 40

BLACK = (0,0,0)
RED = (255,0,0)

class Invader(pygame.sprite.Sprite):
    """It contains no sprite yet..."""
    def __init__(self, color, points):
        super().__init__()
        self.image = pygame.Surface([invader_width, invader_height])
        self.image.fill(BLACK)
        pygame.draw.rect(self.image, color, [0,0, invader_width, invader_height])
        self.rect = self.image.get_rect()
        self.score = points
        self.velocity = [2, 0]

    def update(self):
        if self.rect.x >= width - 40 or self.rect.x < 5:
            self.velocity[0] = -self.velocity[0]    
        self.rect.move_ip((self.velocity))

class PlayerStarship(pygame.sprite.Sprite):
    """No sprites either...:X"""
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface([30,30])
        self.image.fill(BLACK)
        pygame.draw.rect(self.image, color, [0, 0, 30, 30])
        self.rect = self.image.get_rect()
        self.rect.x = screen.get_width() / 2
        self.rect.y = screen.get_height() / 2

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((size))
    pygame.display.set_caption("Invaiders!")
    pygame.mouse.set_visible(False)
    
    clock = pygame.time.Clock()

    invaders_sprite_list = pygame.sprite.Group()
    invader = Invader(RED, 1)
    invaders_sprite_list.add(invader)
    invader.rect.x = 80
    invader.rect.y = 60

    player = PlayerStarship(RED)
    player.rect.x = screen.get_width() / 2
    player.rect.y = 500
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        invaders_sprite_list.update()
        player.update()

        screen.fill(BLACK)

        screen.blit(player.image, player.rect)
        invaders_sprite_list.draw(screen)
        pygame.display.flip()
        clock.tick(60)
        

    
