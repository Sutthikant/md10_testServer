# Example file showing a basic pygame "game loop"
import asyncio
import threading
import logging
from dataclasses import dataclass

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

class Player:
    def __init__(self, screen, image_files, scale, angle):
        self.x = 0
        self.y = 0
        self.id = None
        self.height = 50
        self.width = 50

        self.screen = screen

        self.image_index = 0

        self.images = []
        for file_name in image_files:
            self.images.append(prepare_image(file_name, scale, angle))

        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()

        self.numBullet = 0

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.image_index += 1
        self.image_index %= len(self.images)

        self.image = self.images[self.image_index]

        self.rect.x = self.x
        self.rect.y = self.y

class Bullet:
    def __init__(self, screen, image_files, scale, angle, id):
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

        self.id = id

    def draw(self):
        if not self.is_active:
            return

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def update(self):
        self.image_index += 1
        self.image_index %= len(self.images)

        self.image = self.images[self.image_index]

        self.rect.x = self.x
        self.rect.y = self.y

@dataclass
class EventsData:
    down_key: bool
    up_key: bool
    left_key: bool
    right_key: bool
    fire_key: bool

async def send_events(eventsData, writer):
    while running:
        move_x = -1 if eventsData.left_key else 1 if eventsData.right_key else 0
        move_y = -1 if eventsData.up_key else 1 if eventsData.down_key else 0
        fire = 1 if eventsData.fire_key else 0

        message = f"{move_x},{move_y},{fire}\n"
        # fake send data
        # await asyncio.sleep(1)

        writer.write(message.encode())
        await writer.drain()
        await asyncio.sleep(0.2)

        logging.info(f"send_events coroutine: sent {message}")

async def receive_events(player, other_players, bullets, reader):
    while running:
        # fake_data = "0,50,200,1,400,600,2,25,550".encode()
        message = await reader.readline()

        # fake receive data
        # await asyncio.sleep(1)
        # message = fake_data

        logging.info(f"message received: {message.decode()}")
        pre_data_parts = message.decode().split(":")
        data_parts= pre_data_parts[0].split(",")
        data_parts = data_parts[:-1]
        bullet_parts = pre_data_parts[1].split(",")
        bullet_parts[-1] = bullet_parts[-1][:-1]
        print(data_parts, bullet_parts)

        for i in range(0, len(data_parts), 3):
            player_id = int(data_parts[i])
            if player_id == player.id:
                player.x = float(data_parts[i+1])
                player.y = float(data_parts[i+2])

            else:
                check = False
                for other_player in other_players:
                    if player_id == other_player.id:
                        other_player.x = float(data_parts[i+1])
                        other_player.y = float(data_parts[i+2])
                        check = True
                        break
                if not check:
                    other_player = Player(screen, ["images/e-ship1.png", "images/e-ship2.png", "images/e-ship3.png"], 0.25, 0)
                    other_player.id = player_id
                    other_players.append(other_player)
                    other_players[-1].x = float(data_parts[i+1])
                    other_players[-1].y = float(data_parts[i+2])

        if len(bullet_parts) != 1:
            for i in range(0, len(bullet_parts), 4):
                bullet_id = int(bullet_parts[i])
                bullet_status = int(bullet_parts[i + 1])
                print(bullet_status)
                if bullet_status == 0:
                    print("Yes")
                    for bullet in bullets:
                        if bullet.id == bullet_id:
                            bullets.remove(bullet)
                else:
                    have_bullet = False
                    for bullet in bullets:
                        if bullet.id == bullet_id:
                            bullet.x = float(bullet_parts[i + 2])
                            bullet.y = float(bullet_parts[i + 3])
                            have_bullet = True
                            break
                    if not have_bullet:
                        bullet = Bullet(screen, ['images/bullet.png'], 0.25, 0, bullet_id)
                        bullet.x = float(bullet_parts[i + 2])
                        bullet.y = float(bullet_parts[i + 3])
                        bullet.speed_y = -1
                        bullets.append(bullet)
                # if player_id == player.id:
                #     print(1)
                #     if player.numBullet < 3:
                #         print(2)
                #         bullet = Bullet(screen, ['images/bullet.png'], 0.25, 0, player_id)
                #         bullet.x = float(bullet_parts[i + 1])
                #         bullet.y = float(bullet_parts[i + 2])
                #         bullet.speed_y = -1
                #         bullets.append(bullet)
                #         player.numBullet += 1
                # else:
                #     for other_player in other_players:
                #         if player_id == other_player.id:
                #             print(3)
                #             if other_player.numBullet < 3:
                #                 print(4)
                #                 bullet = Bullet(screen, ['images/bullet.png'], 0.25, 0, player_id)
                #                 bullet.x = float(bullet_parts[i + 1])
                #                 bullet.y = float(bullet_parts[i + 2])
                #                 bullet.speed_y = -1
                #                 bullets.append(bullet)
                #                 other_player.numBullet += 1

        # await asyncio.sleep(0.05)

async def data_exchange(player, eventsData, other_players, bullets):
    reader, writer = await asyncio.open_connection("localhost", 8888)

    initial_data = await reader.readline()
    logging.info(f"initial data received: {initial_data.decode()}")
    data_parts=initial_data.decode().split(":")
    player.id = int(data_parts[1])

    send_events_task = asyncio.create_task(send_events(eventsData, writer))
    receive_events_task = asyncio.create_task(receive_events(player, other_players, bullets, reader))

    await asyncio.gather(send_events_task, receive_events_task)

    print("data_exchange coroutine finished")

def data_exchange_thread_func(player, eventsData, other_players, bullets):
    global running

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(data_exchange(player, eventsData, other_players, bullets))

    loop.close()

    print("data_exchange thread finished")

def main():
    global running

    other_players = []

    player = Player(screen, ["images/ship1.png", "images/ship2.png", "images/ship3.png"], 0.25, 0)
    console = Console(screen)
    bullets = []

    eventsData = EventsData(False, False, False, False, False)

    # create data exchange thread
    data_exchange_thread = threading.Thread(target=data_exchange_thread_func, args=(player, eventsData, other_players, bullets))
    data_exchange_thread.start()

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    eventsData.up_key = True
                elif event.key == pygame.K_DOWN:
                    eventsData.down_key = True
                elif event.key == pygame.K_LEFT:
                    eventsData.left_key = True
                elif event.key == pygame.K_RIGHT:
                    eventsData.right_key = True
                elif event.key == pygame.K_SPACE:
                    eventsData.fire_key = True
                    pass
                elif event.key == pygame.K_c:
                    if console.visible:
                        console.hide()
                    else:
                        console.show()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    eventsData.up_key = False
                elif event.key == pygame.K_DOWN:
                    eventsData.down_key = False
                elif event.key == pygame.K_LEFT:
                    eventsData.left_key = False
                elif event.key == pygame.K_RIGHT:
                    eventsData.right_key = False
                elif event.key == pygame.K_SPACE:
                    eventsData.fire_key = False


        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # draw other players
        
        bullet_del = False

        for bullet in bullets:
            bullet.update()
            bullet.draw()

        # bullets = [bullet for bullet in bullets if bullet.is_active]

        for other_player in other_players:
            other_player.update()
            other_player.draw()

        if player.id is not None:
            player.update()
            player.draw()

        bullet_status = [bullet.id for bullet in bullets]

        console.log(f"Player x: {int(player.x)}, y: {int(player.y)}, bullets: {bullet_status}")
        console.draw()

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    data_exchange_thread.join()
    pygame.quit()

if __name__ == "__main__":
    format = "SRV: %(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.ERROR,
                        datefmt="%F-%H-%M-%S")

    main()