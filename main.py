# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
running = True

def prepare_image(file_name, scale, angle):
    img = pygame.image.load(file_name)
    img.convert()
    img = pygame.transform.rotozoom(img, angle, scale)

    img.set_colorkey("black")

    return img

class Console:
    def __init__(self, screen):
        self.x = 0
        self.y = 0
        self.width = screen.get_width()
        self.height = 100
        self.color = "white"
        self.text = ""
        self.font = pygame.font.SysFont(None, 22)
        self.screen = screen
        self.visible = True

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def draw(self):
        if not self.visible:
            return

        # draw transparent background with alpha 128
        # pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0, pygame.BLEND_RGBA_MULT)

        s = pygame.Surface((self.width, self.height))  # the size of your rect
        s.set_alpha(80)  # alpha level
        s.fill(self.color)  # this fills the entire surface
        screen.blit(s, (self.x, self.y))

        # pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        text = self.font.render(self.text, True, "white")

        # draw transparent text
        text.set_alpha(190)
        screen.blit(text, (self.x + 10, self.y + 10))

    def log(self, text):
        self.text = text

    def update(self):
        pass

class Player1:
    def __init__(self, screen, image_files, scale, angle):
        self.x = 0
        self.y = 0

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.screen = screen

        self.width = 50
        self.height = 50
        self.color = "green"
        self.speed_x = 0
        self.speed_y = 0
        self.acceleration = 0.1

        self.lifepoint = 10

        self.image_index = 0

        self.images = []
        for file_name in image_files:
            self.images.append(prepare_image(file_name, scale, angle))

        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()

    def draw(self):
        self.screen.blit(self.image, self.rect)

        # pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # prevent player from going off screen
        if self.x < 0:
            self.x = 0
        elif self.x > screen.get_width() - self.width:
            self.x = screen.get_width() - self.width
        if self.y < 0:
            self.y = 0
        elif self.y > screen.get_height() - self.height:
            self.y = screen.get_height() - self.height

        # add friction
        if self.speed_x > 0:
            self.speed_x -= self.acceleration * 0.5
        elif self.speed_x < 0:
            self.speed_x += self.acceleration * 0.5
        if self.speed_y > 0:
            self.speed_y -= self.acceleration * 0.5
        elif self.speed_y < 0:
            self.speed_y += self.acceleration * 0.5

        self.image_index += 1
        self.image_index %= len(self.images)

        self.image = self.images[self.image_index]

        self.rect.x = self.x
        self.rect.y = self.y


    def move(self, direction):
        if direction == "up":
            self.speed_y += -self.acceleration
        elif direction == "down":
            self.speed_y += self.acceleration
        elif direction == "left":
            self.speed_x += -self.acceleration
        elif direction == "right":
            self.speed_x += self.acceleration

class Player2:
    def __init__(self, screen, image_files, scale, angle):
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.screen = screen

        self.width = 50
        self.height = 50

        self.x = self.screen_width - (self.width)
        self.y = self.screen_height - (self.height)

        self.color = "green"
        self.speed_x = 0
        self.speed_y = 0
        self.acceleration = 0.1

        self.lifepoint = 10

        self.image_index = 0

        self.images = []
        for file_name in image_files:
            self.images.append(prepare_image(file_name, scale, angle))

        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()

    def draw(self):
        self.screen.blit(self.image, self.rect)

        # pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # prevent player from going off screen
        if self.x < 0:
            self.x = 0
        elif self.x > screen.get_width() - self.width:
            self.x = screen.get_width() - self.width
        if self.y < 0:
            self.y = 0
        elif self.y > screen.get_height() - self.height:
            self.y = screen.get_height() - self.height

        # add friction
        if self.speed_x > 0:
            self.speed_x -= self.acceleration * 0.5
        elif self.speed_x < 0:
            self.speed_x += self.acceleration * 0.5
        if self.speed_y > 0:
            self.speed_y -= self.acceleration * 0.5
        elif self.speed_y < 0:
            self.speed_y += self.acceleration * 0.5

        self.image_index += 1
        self.image_index %= len(self.images)

        self.image = self.images[self.image_index]

        self.rect.x = self.x
        self.rect.y = self.y


    def move(self, direction):
        if direction == "up":
            self.speed_y += -self.acceleration
        elif direction == "down":
            self.speed_y += self.acceleration
        elif direction == "left":
            self.speed_x += -self.acceleration
        elif direction == "right":
            self.speed_x += self.acceleration


class Bullet:
    def __init__(self, screen, image_files, scale, angle):
        self.x = 0
        self.y = 0

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.screen = screen

        self.width = 10
        self.height = 10
        self.color = "red"
        self.speed_x = 0
        self.speed_y = 0

        self.is_active = True

        self.image_index = 0

        self.images = []
        for file_name in image_files:
            self.images.append(prepare_image(file_name, scale, angle))

        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()

    def draw(self):
        if not self.is_active:
            return

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def update(self):

        self.x += self.speed_x
        self.y += self.speed_y

        if self.x < 0 or self.x > self.screen_width or self.y < 0 or self.y > self.screen_height:
            self.is_active = False
            return

        self.image_index += 1
        self.image_index %= len(self.images)

        self.image = self.images[self.image_index]

        self.rect.x = self.x
        self.rect.y = self.y


player1 = Player1(screen, ["images/ship1.png", "images/ship2.png", "images/ship3.png"], 0.25, 180)
player2 = Player2(screen, ["images/e-ship1.png", "images/e-ship2.png", "images/e-ship3.png"], 0.25, 0)
console = Console(screen)

down_key = False
up_key = False
left_key = False
right_key = False

down_key2 = False
up_key2 = False
left_key2 = False
right_key2 = False

bullets = []
bullets2 = []

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                up_key = True
            elif event.key == pygame.K_DOWN:
                down_key = True
            elif event.key == pygame.K_LEFT:
                left_key = True
            elif event.key == pygame.K_RIGHT:
                right_key = True
            elif event.key == pygame.K_w:
                up_key2 = True
            elif event.key == pygame.K_s:
                down_key2 = True
            elif event.key == pygame.K_a:
                left_key2 = True
            elif event.key == pygame.K_d:
                right_key2 = True
            elif event.key == pygame.K_SPACE:
                bullet = Bullet(screen, ['images/bullet.png'], 0.25, 0)
                bullet.x = player1.x + player1.width / 2 - bullet.width / 2
                bullet.y = player1.y + player1.height / 2 - bullet.height / 2
                bullet.speed_y = +1
                bullets.append(bullet)
            elif event.key == pygame.K_q:
                bullet = Bullet(screen, ['images/bullet.png'], 0.25, 0)
                bullet.x = player2.x + player2.width / 2 - bullet.width / 2
                bullet.y = player2.y + player2.height / 2 - bullet.height / 2
                bullet.speed_y = -1
                bullets2.append(bullet)

            elif event.key == pygame.K_c:
                if console.visible:
                    console.hide()
                else:
                    console.show()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                up_key = False
            elif event.key == pygame.K_DOWN:
                down_key = False
            elif event.key == pygame.K_LEFT:
                left_key = False
            elif event.key == pygame.K_RIGHT:
                right_key = False
            elif event.key == pygame.K_w:
                up_key2 = False
            elif event.key == pygame.K_s:
                down_key2 = False
            elif event.key == pygame.K_a:
                left_key2 = False
            elif event.key == pygame.K_d:
                right_key2 = False


    if up_key:
        player1.move("up")
    if down_key:
        player1.move("down")
    if left_key:
        player1.move("left")
    if right_key:
        player1.move("right")
    if up_key2:
        player2.move("up")
    if down_key2:
        player2.move("down")
    if left_key2:
        player2.move("left")
    if right_key2:
        player2.move("right")

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    player1.update()
    player1.draw()

    player2.update()
    player2.draw()

    # remove inactive bullets
    for bullet in bullets:
        # when the ship got hit
        if (bullet.x >= (player2.x) and bullet.x <= (player2.x + (player2.width))) and (bullet.y >= (player2.y) and bullet.y <= (player2.y + (player2.height))):
            player2.lifepoint -= 1
            bullets.remove(bullet)
        
        bullet.update()
        bullet.draw()

    for bullet in bullets2:
        # when the ship got hit
        if (bullet.x >= (player1.x) and bullet.x <= (player1.x + (player1.width))) and (bullet.y >= (player1.y) and bullet.y <= (player1.y + (player1.height))):
            player1.lifepoint -= 1
            bullets2.remove(bullet)
        
        bullet.update()
        bullet.draw()

    bullets = [bullet for bullet in bullets if bullet.is_active]
    bullets2 = [bullet for bullet in bullets2 if bullet.is_active]


    # when the ship got hit

    console.log(f"Player 1: {int(player1.x)}, y: {int(player1.y)}; Speed x: {int(player1.speed_x)}, Speed y: {int(player1.speed_y)}")
    console.log(f"Player 2: {int(player2.x)}, y: {int(player2.y)}; Speed x: {int(player2.speed_x)}, Speed y: {int(player2.speed_y)}")
    console.log(f"Player 1: {int(player1.lifepoint)}      Player 2: {int(player2.lifepoint)}")
    console.draw()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()