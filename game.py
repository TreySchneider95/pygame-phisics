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

# Initial gravity value
gravity = 300  # Adjust this value to control the intensity of gravity

# Slider variables
slider_rect = pygame.Rect(50, 10, 200, 20)
slider_handle_rect = pygame.Rect(slider_rect.x, slider_rect.y, 10, slider_rect.height)
dragging = False

# Function to update gravity based on slider position
def update_gravity():
    global gravity
    slider_pos = (slider_handle_rect.x - slider_rect.x) / (slider_rect.width - slider_handle_rect.width)
    gravity = slider_pos * 1000  # Scale the gravity value

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if slider_handle_rect.collidepoint(event.pos):
                dragging = True
            else:
                # Spawn a new circle at the click position with random direction
                mouse_position = pygame.mouse.get_pos()
                if mouse_position[1] > slider_rect.bottom:  # Avoid clicking the slider
                    new_circle = Circle(200, mouse_position, play_area, gravity)
                    circles.append(new_circle)
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                slider_handle_rect.x = max(slider_rect.x, min(event.pos[0], slider_rect.right - slider_handle_rect.width))
                update_gravity()

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
        # Render slider
        pygame.draw.rect(screen, "white", slider_rect)
        pygame.draw.rect(screen, "red", slider_handle_rect)
        
        # Display gravity value
        font = pygame.font.SysFont(None, 24)
        gravity_text = font.render(f'Gravity: {gravity:.2f}', True, "white")
        screen.blit(gravity_text, (slider_rect.right + 20, slider_rect.y))

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
            circle.gravity = gravity  # Update gravity for each circle
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
