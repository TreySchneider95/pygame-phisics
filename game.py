import pygame
import button
from circle import Circle

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
start = False
distance_from_outside = 50
border_width = 5

start_img = pygame.image.load('imgs/start_btn.png').convert_alpha()
exit_img = pygame.image.load('imgs/exit_btn.png').convert_alpha()

# Define the play area boundaries
left_boundary = distance_from_outside + border_width
top_boundary = distance_from_outside + border_width
right_boundary = screen.get_width() - distance_from_outside - border_width
bottom_boundary = screen.get_height() - distance_from_outside - border_width
play_area = (left_boundary, top_boundary, right_boundary, bottom_boundary)

# List to store circles
circles = []

# Gravity value
gravity = 600  # Adjust this value to control the intensity of gravity

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Spawn a new circle at the click position with random direction
            mouse_position = pygame.mouse.get_pos()
            new_circle = Circle(200, mouse_position, play_area, gravity)
            circles.append(new_circle)

    screen.fill("black")

    if not start:
        start_btn = button.Button(350, 200, start_img, .8)
        exit_btn = button.Button(700, 200, exit_img, .8)
        start_btn.draw(screen)
        exit_btn.draw(screen)
        if start_btn.clicked:
            start = True
        if exit_btn.clicked:
            running = False
    
    else:
        # Render border
        pygame.draw.rect(
            screen,
            "red",
            pygame.Rect(
                distance_from_outside, 
                distance_from_outside,
                screen.get_width()-(distance_from_outside*2),
                screen.get_height()-(distance_from_outside*2)
            )
        )
        # Render play area
        pygame.draw.rect(
            screen,
            "black",
            pygame.Rect(
                distance_from_outside+border_width, 
                distance_from_outside+border_width,
                (screen.get_width()-(distance_from_outside*2))-(border_width*2),
                (screen.get_height()-(distance_from_outside*2))-(border_width*2)
            )
        )

        for circle in circles:
            circle.move(clock.get_time() / 1000.0)

        # Check for collisions between circles
        for i in range(len(circles)):
            for j in range(i + 1, len(circles)):
                circles[i].handle_collision(circles[j])

        for circle in circles:
            circle.render(screen, "red", 10)

    pygame.display.flip()

    # Limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
