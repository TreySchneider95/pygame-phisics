import random
import pygame
import math

class Circle:
    def __init__(self, speed, position, play_area, gravity=0):
        self.speed = speed
        self.position = pygame.Vector2(position)
        self.play_area = play_area
        self.gravity = gravity
        self.radius = 10  # Assuming a fixed radius for the circle

        # Initialize velocities based on direction
        direction = random.randint(0, 360)
        radians = math.radians(direction)
        self.vx = self.speed * math.cos(radians)
        self.vy = self.speed * math.sin(radians)

    def at_boundary(self):
        left, top, right, bottom = self.play_area

        # Check for collision with the left or right walls
        if self.position.x - self.radius <= left or self.position.x + self.radius >= right:
            return True
        
        # Check for collision with the top or bottom walls
        if self.position.y - self.radius <= top or self.position.y + self.radius >= bottom:
            return True
        
        return False

    def bounce(self):
        left, top, right, bottom = self.play_area

        # Check for collision with the left or right walls
        if self.position.x - self.radius <= left or self.position.x + self.radius >= right:
            self.vx = -self.vx
            self.position.x = max(self.position.x, left + self.radius)
            self.position.x = min(self.position.x, right - self.radius)
        
        # Check for collision with the top or bottom walls
        if self.position.y - self.radius <= top or self.position.y + self.radius >= bottom:
            self.vy = -self.vy
            self.position.y = max(self.position.y, top + self.radius)
            self.position.y = min(self.position.y, bottom - self.radius)

    def move(self, dt):
        if self.at_boundary():
            self.bounce()
        
        # Apply gravity to the vertical velocity
        self.vy += self.gravity * dt

        # Update the position
        self.position.x += self.vx * dt
        self.position.y += self.vy * dt
    
    def render(self, screen, color, size):
        return pygame.draw.circle(screen, color, self.position, size)

    def check_collision(self, other):
        distance = self.position.distance_to(other.position)
        return distance < self.radius + other.radius

    def handle_collision(self, other):
        if self.check_collision(other):
            # Calculate the normal vector
            normal = self.position - other.position
            normal = normal.normalize()

            # Calculate relative velocity
            relative_velocity = pygame.Vector2(self.vx - other.vx, self.vy - other.vy)
            velocity_along_normal = relative_velocity.dot(normal)

            if velocity_along_normal > 0:
                return

            # Calculate the impulse scalar
            impulse_scalar = -(2 * velocity_along_normal) / 2  # Since masses are equal

            # Apply impulse to the balls
            impulse = normal * impulse_scalar
            self.vx -= impulse.x
            self.vy -= impulse.y
            other.vx += impulse.x
            other.vy += impulse.y

            # Preserve the speed by normalizing the velocities
            self.normalize_velocity()
            other.normalize_velocity()

    def normalize_velocity(self):
        velocity = pygame.Vector2(self.vx, self.vy)
        speed = velocity.length()
        if speed != 0:
            factor = self.speed / speed
            self.vx *= factor
            self.vy *= factor
