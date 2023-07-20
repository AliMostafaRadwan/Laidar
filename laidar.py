import pygame
import math

# Initialize pygame
pygame.init()

# Set the screen dimensions
screen_width, screen_height = 800, 600

# Set the colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("LIDAR Simulation")

# Function to calculate the distance between two points
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Main game loop
def main():
    running = True
    lidar_circle_pos = [screen_width // 2, screen_height // 2]  # Start the circle at the center
    points = []
    structure_type = "bar"  # Change to "circle" to test with a circle structure

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get the state of arrow keys
        keys = pygame.key.get_pressed()
        speed = 1  # Adjust the speed of circle movement

        if keys[pygame.K_LEFT]:
            lidar_circle_pos[0] -= speed
        if keys[pygame.K_RIGHT]:
            lidar_circle_pos[0] += speed
        if keys[pygame.K_UP]:
            lidar_circle_pos[1] -= speed
        if keys[pygame.K_DOWN]:
            lidar_circle_pos[1] += speed

        # Clear the screen
        screen.fill(white)

        # Draw the structure
        if structure_type == "bar":
            pygame.draw.rect(screen, black, (screen_width // 2 - 50, screen_height // 2 - 200, 100, 400))
        elif structure_type == "circle":
            pygame.draw.circle(screen, black, (screen_width // 2, screen_height // 2), 150)

        # Draw the LIDAR points and lines
        for x, y in points:
            pygame.draw.circle(screen, red, (int(x), int(y)), 2)
            pygame.draw.line(screen, red, (lidar_circle_pos[0], lidar_circle_pos[1]), (int(x), int(y)), 1)

        # Calculate the distance from the LIDAR circle to the points on the structure
        points = []
        for angle in range(0, 360, 5):  # Simulate LIDAR points with 5-degree increments
            radian_angle = math.radians(angle)
            x = lidar_circle_pos[0] + 1000 * math.cos(radian_angle)
            y = lidar_circle_pos[1] + 1000 * math.sin(radian_angle)

            # Check if the LIDAR point intersects with the structure
            if structure_type == "bar":
                if screen_width // 2 - 50 <= x <= screen_width // 2 + 50 and screen_height // 2 - 200 <= y <= screen_height // 2 + 200:
                    points.append((x, y))
            elif structure_type == "circle":
                if distance(screen_width // 2, screen_height // 2, x, y) <= 150:
                    points.append((x, y))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
