import pygame
from pygame import *
import random

pygame.init()

width_screen = 800
height = 800
screen = pygame.display.set_mode((width_screen, height))
pygame.display.set_caption("It's your Car game.")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
light_green = (148, 238, 144)
gray = (100, 100, 100)

road_size = 600
border_width = 10
border_height = 50

# Lane positions
lane_width = road_size / 3
left = 100
center = left + lane_width
right = left + 2 * lane_width

lanes = [left, center, right]

gameover = False
speed = 2
score = 0

# Road and border
road = (100, 0, road_size, height)
left_edge = (100, 0, border_width, height)
right_edge = (700, 0, border_width, height)

# Movement
lane_move_in_y_axis = 0

# Initial coordinates of the car
player_x_coordinate = 400
player_y_coordinate = 600

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        size_of_car = 75 / image.get_rect().width
        new_width = int(image.get_rect().width * size_of_car)
        new_height = int(image.get_rect().height * size_of_car)
        self.image = pygame.transform.scale(image, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class Player(Vehicle):
    def __init__(self, image, x, y):
        image = pygame.image.load("all_images/car.png")
        super().__init__(image, x, y)

player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

player_ = Player(None,player_x_coordinate, player_y_coordinate)
player_group.add(player_)

# Obstacles as vehicle images
image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('all_images/' + image_filename)
    vehicle_images.append(image)

# When car collided
crash = pygame.image.load('all_images/crash.png')
crash_rect = crash.get_rect()

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(120)  # FPS set

    # Keyboard movements
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player_.rect.left > left+100:
                player_.rect.x -= 200
            elif event.key == K_RIGHT and player_.rect.right < right + border_width:
                player_.rect.x += 200
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player_, vehicle):
                    
                    gameover = True
                    
                    #determine where to position the crash image
                    if event.key == K_LEFT:
                        player_.rect.left = vehicle.rect.right
                        crash_rect.center = [player_.rect.left, (player_.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        player_.rect.right = vehicle.rect.left
                        crash_rect.center = [player_.rect.right, (player_.rect.center[1] + vehicle.rect.center[1]) / 2]
    # Background of the screen set
    screen.fill(light_green)

    # Road
    pygame.draw.rect(screen, gray, road)

    # Borders
    pygame.draw.rect(screen, red, left_edge)
    pygame.draw.rect(screen, red, right_edge)

    # Draw the zebra crossing kind of line to distinguish lanes
    lane_move_in_y_axis += speed * 2
    if lane_move_in_y_axis >= border_height * 2:
        lane_move_in_y_axis = 0
    for y in range(border_height * -2, height, border_height * 2):
        pygame.draw.rect(screen, white, (center, y + lane_move_in_y_axis, border_width, border_height))
        pygame.draw.rect(screen, white, (right, y + lane_move_in_y_axis, border_width, border_height))

    # Vehicle of player
    player_group.draw(screen)

    # Random vehicle generation
    if len(vehicle_group) < 2:
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 2:
                add_vehicle = False
                break

        if add_vehicle:
            lane = random.choice(lanes)
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane+100, height / -2)
            vehicle_group.add(vehicle)

    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        # Remove vehicle once it goes off screen
        if vehicle.rect.top >= height:
            vehicle.kill()
            # Add to score
            score += 1
            # Speed up the game after passing 5 vehicles
            if score > 0 and score % 5 == 0:
                speed += 1

    vehicle_group.draw(screen)

    # Display the score
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score: ' + str(score), True, white)
    text_rect = text.get_rect()
    text_rect.center = (100, 600)
    screen.blit(text, text_rect)


    #collision checked
    if pygame.sprite.spritecollide(player_, vehicle_group, True):
        gameover = True
        crash_rect.center = [player_.rect.center[0], player_.rect.top]
    #Game over
    if gameover:
        screen.blit(crash, crash_rect)
        pygame.draw.rect(screen, red, (0, 50, width_screen, 100))

        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Game over. Play again? (Enter Y or N)', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width_screen / 2, 100)
        screen.blit(text, text_rect)

        pygame.display.update()
        while gameover:
            clock.tick(120)
            for event in pygame.event.get():
                if event.type == QUIT:
                    gameover = False
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        #Reset
                        gameover = False
                        speed = 2
                        score = 0
                        vehicle_group.empty()
                        player_.rect.center = [player_x_coordinate, player_y_coordinate]
                    elif event.key == K_n:
                        #Exit
                        gameover = False
                        running = False

    pygame.display.update()

pygame.quit()
