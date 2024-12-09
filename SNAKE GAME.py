import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 800, 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
brown = (139, 69, 19)  # Brown color for background while the snake is running
dark_green = (0, 100, 0)
light_green = (34, 139, 34)
red = (213, 50, 80)
rock_color = (0, 0, 0)  # Dark black rock boundaries

# Rainbow colors for food
rainbow_colors = [
    (255, 0, 0),  # Red
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (75, 0, 130),  # Indigo
    (238, 130, 238)  # Violet
]

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Realistic Snake Game with Changing Food Size")

# Clock and font
clock = pygame.time.Clock()
snake_block = 40  # Size of snake block
snake_speed = 5   # Slower snake for realism

# Fonts
font_style = pygame.font.SysFont("ravie", 30)  # Changed font to Ravie for messages
score_font = pygame.font.SysFont("chiller", 40)  # Chiller font for score

# Score function
def display_score(score):
    value = score_font.render(f"YOUR SCORE: {score}", True, red)  # Uppercase "YOUR SCORE"
    screen.blit(value, [0, 0])

# Draw a more realistic snake
def draw_snake(snake_block, snake_list):
    for i, segment in enumerate(snake_list):
        # Alternate colors for a scaled effect
        color = light_green if i % 2 == 0 else dark_green
        pygame.draw.ellipse(screen, color, [segment[0], segment[1], snake_block, snake_block])

        # Draw eyes on the head
        if i == len(snake_list) - 1:  # Head
            # White sclera
            pygame.draw.circle(screen, white, (segment[0] + 10, segment[1] + 10), 8)
            pygame.draw.circle(screen, white, (segment[0] + 30, segment[1] + 10), 8)
            # Black pupils
            pygame.draw.circle(screen, black, (segment[0] + 10, segment[1] + 10), 4)
            pygame.draw.circle(screen, black, (segment[0] + 30, segment[1] + 10), 4)
            # Tongue
            tongue_length = 20
            tongue_width = 3
            pygame.draw.line(screen, red,
                             (segment[0] + 20, segment[1] + snake_block // 2),
                             (segment[0] + 20, segment[1] + snake_block // 2 + tongue_length),
                             tongue_width)

# Message display with moving text
def display_message(msg, color, x_pos):
    message = font_style.render(msg, True, color)
    text_rect = message.get_rect(center=(x_pos, height / 2))  # Moving text horizontally
    screen.blit(message, text_rect)

# Draw rock boundaries
def draw_boundaries():
    pygame.draw.rect(screen, rock_color, [0, 0, width, snake_block])  # Top boundary
    pygame.draw.rect(screen, rock_color, [0, 0, snake_block, height])  # Left boundary
    pygame.draw.rect(screen, rock_color, [width - snake_block, 0, snake_block, height])  # Right boundary
    pygame.draw.rect(screen, rock_color, [0, height - snake_block, width, snake_block])  # Bottom boundary

# Main game loop
def gameLoop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(snake_block, width - snake_block * 2) / snake_block) * snake_block + snake_block // 2
    foody = round(random.randrange(snake_block, height - snake_block * 2) / snake_block) * snake_block + snake_block // 2
    food_color = random.choice(rainbow_colors)

    food_size_small = snake_block // 2  # Small food size
    food_size_large = snake_block      # Large food size
    food_size = food_size_large  # Start with large size food

    last_time = pygame.time.get_ticks()  # To track time and change size

    while not game_over:

        while game_close:
            screen.fill((211, 211, 211))  # Changed background color to light gray on game over
            # Move the message text horizontally
            for i in range(0, width, 5):  # Adjust the step size for speed of text movement
                screen.fill((211, 211, 211))  # Refill background
                display_message("You lost! Press Q-Quit or C-Play Again", black, i)  # Moving message
                display_score(length_of_snake - 1)
                pygame.display.update()
                pygame.time.delay(30)  # Delay for smooth movement
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width - snake_block or x1 < snake_block or y1 >= height - snake_block or y1 < snake_block:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(brown)  # Set background to brown while the snake is running
        draw_boundaries()  # Draw boundaries

        # Check if it's time to change the food size
        current_time = pygame.time.get_ticks()
        if current_time - last_time >= 1000:  # 1000 ms = 1 second
            last_time = current_time
            # Toggle food size between small and large
            food_size = food_size_large if food_size == food_size_small else food_size_small

        pygame.draw.circle(screen, food_color, (foodx, foody), food_size // 4)  # Food size changes here
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(snake_block, snake_list)
        display_score(length_of_snake - 1)

        # Collision logic: Check if snake eats the food
        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            foodx = round(random.randrange(snake_block, width - snake_block * 2) / snake_block) * snake_block + snake_block // 2
            foody = round(random.randrange(snake_block, height - snake_block * 2) / snake_block) * snake_block + snake_block // 2
            food_color = random.choice(rainbow_colors)  # Randomize food color on each consumption
            length_of_snake += 1

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop() 