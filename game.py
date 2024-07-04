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

# Initial gravity value and ball speed
gravity = 300  # Adjust this value to control the intensity of gravity
ball_speed = 200  # Initial ball speed

# Slider variables
slider_rect_gravity = pygame.Rect(50, 10, 200, 20)
slider_handle_rect_gravity = pygame.Rect(slider_rect_gravity.x, slider_rect_gravity.y, 10, slider_rect_gravity.height)
slider_rect_play_area = pygame.Rect(425, 10, 200, 20)
slider_handle_rect_play_area = pygame.Rect(slider_rect_play_area.x, slider_rect_play_area.y, 10, slider_rect_play_area.height)
slider_rect_speed = pygame.Rect(850, 10, 200, 20)
slider_handle_rect_speed = pygame.Rect(slider_rect_speed.x, slider_rect_speed.y, 10, slider_rect_speed.height)
dragging_gravity = False
dragging_play_area = False
dragging_speed = False

# Function to update gravity based on slider position
def update_gravity():
    global gravity
    slider_pos = (slider_handle_rect_gravity.x - slider_rect_gravity.x) / (slider_rect_gravity.width - slider_handle_rect_gravity.width)
    gravity = slider_pos * 1000  # Scale the gravity value

# Function to update play area size based on slider position
def update_play_area():
    global play_area
    slider_pos = (slider_handle_rect_play_area.x - slider_rect_play_area.x) / (slider_rect_play_area.width - slider_handle_rect_play_area.width)
    distance_from_outside = 50 + (slider_pos * 200)  # Adjust this range as needed
    play_area = (
        distance_from_outside + border_width,
        distance_from_outside + border_width,
        screen.get_width() - distance_from_outside - border_width,
        screen.get_height() - distance_from_outside - border_width
    )

# Function to update ball speed based on slider position
def update_ball_speed():
    global ball_speed
    slider_pos = (slider_handle_rect_speed.x - slider_rect_speed.x) / (slider_rect_speed.width - slider_handle_rect_speed.width)
    ball_speed = 100 + (slider_pos * 500)  # Adjust the range as needed

# Initial play area boundaries
update_play_area()

# List to store circles
circles = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if slider_handle_rect_gravity.collidepoint(event.pos):
                dragging_gravity = True
            elif slider_handle_rect_play_area.collidepoint(event.pos):
                dragging_play_area = True
            elif slider_handle_rect_speed.collidepoint(event.pos):
                dragging_speed = True
            else:
                # Spawn a new circle at the click position with random direction
                mouse_position = pygame.mouse.get_pos()
                if mouse_position[1] > slider_rect_speed.bottom:  # Avoid clicking the sliders
                    new_circle = Circle(ball_speed, mouse_position, play_area, gravity)
                    circles.append(new_circle)
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_gravity = False
            dragging_play_area = False
            dragging_speed = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging_gravity:
                slider_handle_rect_gravity.x = max(slider_rect_gravity.x, min(event.pos[0], slider_rect_gravity.right - slider_handle_rect_gravity.width))
                update_gravity()
            elif dragging_play_area:
                slider_handle_rect_play_area.x = max(slider_rect_play_area.x, min(event.pos[0], slider_rect_play_area.right - slider_handle_rect_play_area.width))
                update_play_area()
            elif dragging_speed:
                slider_handle_rect_speed.x = max(slider_rect_speed.x, min(event.pos[0], slider_rect_speed.right - slider_handle_rect_speed.width))
                update_ball_speed()

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
        # Render gravity slider
        pygame.draw.rect(screen, "white", slider_rect_gravity)
        pygame.draw.rect(screen, "red", slider_handle_rect_gravity)
        
        # Display gravity value
        font = pygame.font.SysFont(None, 24)
        gravity_text = font.render(f'Gravity: {gravity:.2f}', True, "white")
        screen.blit(gravity_text, (slider_rect_gravity.right + 20, slider_rect_gravity.y))

        # Render play area size slider
        pygame.draw.rect(screen, "white", slider_rect_play_area)
        pygame.draw.rect(screen, "red", slider_handle_rect_play_area)
        
        # Display play area size value
        play_area_size_text = font.render(f'Play Area Size: {play_area[0]:.2f}', True, "white")
        screen.blit(play_area_size_text, (slider_rect_play_area.right + 20, slider_rect_play_area.y))

        # Render ball speed slider
        pygame.draw.rect(screen, "white", slider_rect_speed)
        pygame.draw.rect(screen, "red", slider_handle_rect_speed)
        
        # Display ball speed value
        ball_speed_text = font.render(f'Ball Speed: {ball_speed:.2f}', True, "white")
        screen.blit(ball_speed_text, (slider_rect_speed.right + 20, slider_rect_speed.y))

        # Render border
        pygame.draw.rect(
            screen,
            "red",
            pygame.Rect(
                play_area[0] - border_width, 
                play_area[1] - border_width,
                play_area[2] - play_area[0] + 2 * border_width,
                play_area[3] - play_area[1] + 2 * border_width
            )
        )
        # Render play area
        pygame.draw.rect(
            screen,
            "black",
            pygame.Rect(
                play_area[0], 
                play_area[1],
                play_area[2] - play_area[0],
                play_area[3] - play_area[1]
            )
        )

        for circle in circles:
            circle.gravity = gravity  # Update gravity for each circle
            circle.play_area = play_area  # Update play area for each circle
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
