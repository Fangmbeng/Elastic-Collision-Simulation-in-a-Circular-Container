
import pygame
import random
import math

# Window size
WIDTH, HEIGHT = 800, 800

# Circle container properties
CONTAINER_RADIUS = 200

# Circle properties
CIRCLE_RADIUS = 15  # Diameter is 30 pixels
CIRCLE_MASS = 1

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

class Circle:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        # Set horizontal velocity between 10 and 20 as specified
        magnitude = random.uniform(10, 20)
        angle = random.uniform(0, 2 * math.pi)
        self.vx = magnitude * math.cos(angle)
        self.vy = magnitude * math.sin(angle)
        self.trail = []
        self.mass = CIRCLE_MASS

    def update(self, dt=1.0):
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Apply gravity
        self.vy += 0.1 * dt
        
        # Handle collision with container
        self.check_container_collision()
        
        # Update trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 120:
            self.trail.pop(0)
    
    def check_container_collision(self):
        # Vector from center of container to circle
        dx = self.x - WIDTH // 2
        dy = self.y - HEIGHT // 2
        dist = math.sqrt(dx**2 + dy**2)
        
        # Check if circle is touching or outside container
        if dist >= CONTAINER_RADIUS - CIRCLE_RADIUS:
            # Calculate normal and tangent vectors for collision
            normal_x = dx / dist
            normal_y = dy / dist
            tangent_x = -normal_y
            tangent_y = normal_x
            
            # Calculate normal and tangent velocities
            v_normal = self.vx * normal_x + self.vy * normal_y
            v_tangent = self.vx * tangent_x + self.vy * tangent_y
            
            # Reverse normal velocity (elastic bounce)
            v_normal = -v_normal * 0.98  # Small energy loss for stability
            
            # Recalculate velocities
            self.vx = v_normal * normal_x + v_tangent * tangent_x
            self.vy = v_normal * normal_y + v_tangent * tangent_y
            
            # Adjust position to prevent sticking
            overlap = dist - (CONTAINER_RADIUS - CIRCLE_RADIUS)
            self.x -= overlap * normal_x
            self.y -= overlap * normal_y

    def draw(self, screen):
        # Draw trail with gradient opacity
        for i, (x, y) in enumerate(self.trail):
            alpha = int(255 * i / len(self.trail)) if self.trail else 0
            trail_color = (self.color[0], self.color[1], self.color[2], alpha)
            trail_surface = pygame.Surface((3, 3), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, trail_color, (1, 1), 1)
            screen.blit(trail_surface, (int(x) - 1, int(y) - 1))
        
        # Draw circle
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), CIRCLE_RADIUS)

def check_circle_collision(c1, c2):
    # Calculate distance between circles
    dx = c1.x - c2.x
    dy = c1.y - c2.y
    dist = math.sqrt(dx**2 + dy**2)
    
    # Check if circles are colliding
    if dist < 2 * CIRCLE_RADIUS:
        # Calculate normal and tangent vectors
        normal_x = dx / dist if dist > 0 else 0
        normal_y = dy / dist if dist > 0 else 1
        tangent_x = -normal_y
        tangent_y = normal_x
        
        # Calculate normal and tangent velocities before collision
        v1_normal = c1.vx * normal_x + c1.vy * normal_y
        v1_tangent = c1.vx * tangent_x + c1.vy * tangent_y
        v2_normal = c2.vx * normal_x + c2.vy * normal_y
        v2_tangent = c2.vx * tangent_x + c2.vy * tangent_y
        
        # Calculate velocities after elastic collision
        m1, m2 = c1.mass, c2.mass
        v1_normal_after = (v1_normal * (m1 - m2) + 2 * m2 * v2_normal) / (m1 + m2)
        v2_normal_after = (v2_normal * (m2 - m1) + 2 * m1 * v1_normal) / (m1 + m2)
        
        # Calculate final velocities
        c1.vx = v1_normal_after * normal_x + v1_tangent * tangent_x
        c1.vy = v1_normal_after * normal_y + v1_tangent * tangent_y
        c2.vx = v2_normal_after * normal_x + v2_tangent * tangent_x
        c2.vy = v2_normal_after * normal_y + v2_tangent * tangent_y
        
        # Prevent sticking by moving circles apart
        overlap = 2 * CIRCLE_RADIUS - dist
        c1.x += overlap * normal_x * 0.5
        c1.y += overlap * normal_y * 0.5
        c2.x -= overlap * normal_x * 0.5
        c2.y -= overlap * normal_y * 0.5
        
        return True
    return False

def create_random_circle(color):
    # Create a circle at a random position within the container
    # with some safety margin to avoid starting too close to edges
    margin = CIRCLE_RADIUS * 2
    max_radius = CONTAINER_RADIUS - margin
    
    # Use polar coordinates for better distribution
    r = random.uniform(0, max_radius)
    theta = random.uniform(0, 2 * math.pi)
    
    x = WIDTH // 2 + r * math.cos(theta)
    y = HEIGHT // 2 + r * math.sin(theta)
    
    return Circle(color, x, y)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Circle Collision Simulation")
    clock = pygame.time.Clock()
    
    # Create font for displaying collision count
    font = pygame.font.SysFont(None, 36)
    
    # Create circles ensuring they don't overlap
    circle1 = create_random_circle(RED)
    circle2 = create_random_circle(BLUE)
    
    # Make sure circles don't start overlapping
    dx = circle1.x - circle2.x
    dy = circle1.y - circle2.y
    dist = math.sqrt(dx**2 + dy**2)
    while dist < 2 * CIRCLE_RADIUS:
        circle2 = create_random_circle(BLUE)
        dx = circle1.x - circle2.x
        dy = circle1.y - circle2.y
        dist = math.sqrt(dx**2 + dy**2)
    
    collision_count = 0
    running = True
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Clear screen
        screen.fill(WHITE)
        
        # Draw container
        pygame.draw.circle(screen, BLACK, (WIDTH // 2, HEIGHT // 2), CONTAINER_RADIUS, 2)
        
        # Update circles
        circle1.update()
        circle2.update()
        
        # Check for collision between circles
        if check_circle_collision(circle1, circle2):
            collision_count += 1
        
        # Draw circles and trails
        circle1.draw(screen)
        circle2.draw(screen)
        
        # Display collision count
        collision_text = font.render(f"Collisions: {collision_count}/10", True, BLACK)
        screen.blit(collision_text, (20, 20))
        
        # Update display
        pygame.display.flip()
        
        # Cap frame rate
        clock.tick(60)
        
        # Stop after 10 collisions
        if collision_count >= 10:
            # Display final message
            final_text = font.render("Simulation complete! Click to close.", True, BLACK)
            screen.blit(final_text, (WIDTH//2 - final_text.get_width()//2, HEIGHT//2))
            pygame.display.flip()
            
            # Wait for user to close the window
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                        waiting = False
                        running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()
