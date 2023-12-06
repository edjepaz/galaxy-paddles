import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display in full screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()

pygame.display.set_caption("Dad's Pong Game")

# Load background and ball images
background_image = pygame.image.load("background.png")
ball_image = pygame.image.load("ball.png")


# colors
left_paddle_color = (210, 168, 106)
right_paddle_color = (184, 104, 82)
lead_score_color = (118, 162, 103)

# Resize images to match screen dimensions
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
ball_image = pygame.transform.scale(ball_image, (80, 80))  # Adjust size as needed

# Create background Rect
background_rect = background_image.get_rect()

# Paddle dimensions and speed
paddle_width, paddle_height = 10, 100
paddle_speed = 5
paddle_radius = 10  # Adjust the radius for rounded corners

# Create paddles and ball
left_paddle = pygame.Rect(50, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)
right_paddle = pygame.Rect(screen_width - 50 - paddle_width, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)

ball = pygame.Rect(screen_width // 2 - 20, screen_height // 2 - 20, 80, 80)
ball_speed_x, ball_speed_y = 0, 0  # Initial ball speed

# Score variables
left_player_score = 0
right_player_score = 0

# Set up font
font = pygame.font.Font(None, 36)
winner_font = pygame.font.Font(None, 64)

# Set up clock
clock = pygame.time.Clock()

# Variable to track whether the game is in the initial state
game_start = False

# Variable to track the game state
game_state = "running"  # Possible values: "running", "paused", "game_over"

# Load sound

# background music
pygame.mixer.music.load("music.mp3")  # Adjust the file name and format as needed
pygame.mixer.music.set_volume(0.5)  # Adjust the volume as needed
pygame.mixer.music.play(-1)  # Play the music indefinitely

# wall bounce sound
wall_hit_sound = pygame.mixer.Sound("wall_bounce.mp3")
score_hit_sound = pygame.mixer.Sound("score_hit.mp3")

# Function to display instructions on the screen
def display_instructions():
    title_font = pygame.font.Font(None, 64)
    title_message = "Lucas & Maggie"
    title_text = title_font.render(title_message, True,(114, 182, 207))

    instructions_font = pygame.font.Font(None, 36)
    instructions_text = [
        "Welcome to Dad's Pong Game!",
        "",
        "Player 1 (Left): Use W and S to move up and down",
        "Player 2 (Right): Use the arrow keys to move up and down",
        "",
        "Press SPACEBAR to start the game",
        "Press ESC to quit at any time",
    ]
    
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() //2, 100 + 1 * 40))
    for i, line in enumerate(instructions_text):
        text = instructions_font.render(line, True, (211, 123, 134))
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, 100 + i * 40))


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    keys = pygame.key.get_pressed()


    # Check if the game is over and allow restart with the space bar
    if game_state == "game_over" and keys[pygame.K_SPACE]:
        # Reset game state and scores
        game_state = "running"
        left_player_score = 0
        right_player_score = 0
        ball.x = screen_width // 2 - 20
        ball.y = screen_height // 2 - 20
        ball_speed_x, ball_speed_y = 5, 5  # Reset ball speed
        game_start = False    

    if keys[pygame.K_w]:
        left_paddle.y = max(left_paddle.y - paddle_speed, 0)
    if keys[pygame.K_s]:
        left_paddle.y = min(left_paddle.y + paddle_speed, screen_height - paddle_height)

    # Right paddle controls
    if keys[pygame.K_UP]:
        right_paddle.y = max(right_paddle.y - paddle_speed, 0)
    if keys[pygame.K_DOWN]:
        right_paddle.y = min(right_paddle.y + paddle_speed, screen_height - paddle_height)

    # Check if the space bar is pressed to start the game
    if not game_start and keys[pygame.K_SPACE]:
        # Set initial ball speed
        ball_speed_x, ball_speed_y = 5, 5
        game_start = True




    # Update ball position if the game has started
    if game_start and game_state == "running":
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Check if the game is over and set the game state to "game_over"
        if left_player_score >= 10 or right_player_score >= 10:
            game_state = "game_over"

        # Bounce ball off walls
        if ball.top <= 0 or ball.bottom >= screen_height:
            ball_speed_y *= -1
            wall_hit_sound.play() 

        # Check if the ball hits the left wall
        if ball.left <= 0:
            right_player_score += 1
            ball.x = screen_width // 2 - 20
            ball_speed_x *= -1
            score_hit_sound.play()


        # Check if the ball hits the right wall
        if ball.right >= screen_width:
            left_player_score += 1
            ball.x = screen_width // 2 - 20
            ball_speed_x *= -1
            score_hit_sound.play()

        # Ensure the ball stays within horizontal boundaries
        if ball.left <= 0 or ball.right >= screen_width:
            ball_speed_x *= -1

        # Bounce ball off paddles
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed_x *= -1

    # Draw everything
    screen.blit(background_image, background_rect)
    # Display instructions if the game is in the initial state
    if not game_start:
        display_instructions()

    if game_state == "running":
        # Draw paddles and ball if the game is still ongoing
        pygame.draw.rect(screen, left_paddle_color, left_paddle, border_radius=paddle_radius)
        pygame.draw.rect(screen, right_paddle_color, right_paddle, border_radius=paddle_radius)
        screen.blit(ball_image, ball)

        # Draw scores and player labels
        left_score_color = lead_score_color if left_player_score >= 10 or left_player_score > right_player_score else (77, 96, 105)
        right_score_color = lead_score_color if right_player_score >= 10 or right_player_score > left_player_score else (77, 96, 105)

        left_score_text = font.render("Player 1: " + str(left_player_score), True, left_score_color)
        right_score_text = font.render("Player 2: " + str(right_player_score), True, right_score_color)

        screen.blit(left_score_text, (screen_width // 4, 20))
        screen.blit(right_score_text, (3 * screen_width // 4 - right_score_text.get_width(), 20))

    elif game_state == "game_over":
        # Draw winner message
        winner_text = winner_font.render("Player {} wins!".format(1 if left_player_score >= 10 else 2), True, (177, 212, 128))
        winner_position = ((screen_width - winner_text.get_width()) // 2, screen_height // 2 - winner_text.get_height())
        screen.blit(winner_text, winner_position)

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
