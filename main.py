import pygame
import random

pygame.init()

# Screen settings
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ghost Castle by Cyberchain")

# Fps
fps = 60
clock = pygame.time.Clock()

# Default basic settings
player_start_lives = 3
ghost_start_speed = 3
ghost_start_acceleration = 0.3
score = 0

# Change basic settings Lives/Speed
player_lives = player_start_lives
ghost_currently_speed = ghost_start_speed

# Random position axis
ghost_x = random.choice([-1, 1])
ghost_y = random.choice([-1, 1])

# Background Picture
bg_castle = pygame.image.load("img/background.jpg")
bg_castle_rect = bg_castle.get_rect()
bg_castle_rect.topleft = (0, 0)

# Ghost Picture
image_ghost = pygame.image.load("img/ghost.png")
image_ghost = pygame.transform.scale(image_ghost, (100, 100))
image_ghost_rect = image_ghost.get_rect()
image_ghost_rect.center = (width//2, height//2)

# Color
dark_yellow = pygame.Color("#bfb517")

# Fonts
title_font = pygame.font.Font("fonts/cartoon.ttf", 64)
other_font = pygame.font.Font("fonts/cartoon.ttf", 32)

# Text Score
score_text = other_font.render(f"Score: {score}", True, dark_yellow)
score_text_rect = score_text.get_rect()
score_text_rect.topleft = (width - 150, 20)

# Text Lives
lives_text = other_font.render(f"Lives: {player_lives}", True, dark_yellow)
lives_text_rect = score_text.get_rect()
lives_text_rect.topleft = (width - 140, 60)

# Text GameOver
gameover_text = title_font.render("Game Over!", True, dark_yellow)
gameover_text_rect = gameover_text.get_rect()
gameover_text_rect.center = (width//2, height//2)

# Text Continue
continue_text = other_font.render("Play again? Press any mouse button...", True, dark_yellow)
continue_text_rect = continue_text.get_rect()
continue_text_rect.center = (width//2, height//2 + 60)

# Title Music
pygame.mixer.music.load("media/music.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0)

# Success Sound
success_click = pygame.mixer.Sound("media/success.wav")
success_click.set_volume(0.03)

# Miss Sound
miss_click = pygame.mixer.Sound("media/wrong.wav")
miss_click.set_volume(0.03)

# Bounce Sound
bounce_sound = pygame.mixer.Sound("media/bounce.wav")
bounce_sound.set_volume(0.1)

# Main Cycle
lets_continue = True
while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False

        # Position mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_x = event.pos[0]
            click_y = event.pos[1]
            # Random direction
            previous_x = ghost_x
            previous_y = ghost_y

            while previous_x == ghost_x and previous_y == ghost_y:
                ghost_x = random.choice([-1, 1])
                ghost_y = random.choice([-1, 1])

            # Colidation Ghost/Mouse
            if image_ghost_rect.collidepoint(click_x, click_y):
                # print("mys+hgost")
                success_click.play()
                score += 1
                ghost_start_speed += ghost_start_acceleration
            else:
                miss_click.play()
                player_lives -= 1

    # Ghost Move/Speed
    image_ghost_rect.x += ghost_x * ghost_start_speed
    image_ghost_rect.y += ghost_y * ghost_start_speed

    # Ghost Bounce
    if image_ghost_rect.left < 0 or image_ghost_rect.right >= width:
        bounce_sound.play()
        ghost_x = -1 * ghost_x
    elif image_ghost_rect.top < 0 or image_ghost_rect.bottom >= height:
        bounce_sound.play()
        ghost_y = -1 * ghost_y

    # Update text
    score_text = other_font.render(f"Score: {score}", True, dark_yellow)
    lives_text = other_font.render(f"Lives: {player_lives}", True, dark_yellow)

    # Blit
    screen.blit(bg_castle, bg_castle_rect)
    screen.blit(image_ghost, image_ghost_rect)
    screen.blit(score_text, score_text_rect)
    screen.blit(lives_text, lives_text_rect)

    pygame.display.update()

    # Cycle Slowdown
    clock.tick(fps)

    # GameOver
    if player_lives == 0:
        screen.blit(gameover_text, gameover_text_rect)
        screen.blit(continue_text, continue_text_rect)
        pygame.display.update()
        pygame.mixer.music.stop()

        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    player_lives = player_start_lives
                    ghost_start_speed = ghost_currently_speed
                    image_ghost_rect.center = (width//2, height//2)
                    ghost_x = random.choice([-1, 1])
                    ghost_y = random.choice([-1, 1])
                    pygame.mixer.music.play(-1, 0)
                    pause = False
                elif event.type == pygame.QUIT:
                    pause = False
                    lets_continue = False

pygame.quit()
