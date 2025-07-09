import json
import random as r
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up screen
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dice Roller")

# Load fonts
font = pygame.font.SysFont(None, 48)

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)
    low = config['bounds']['low']
    high = config['bounds']['high'] # Can only currently be upto 6
    is_rigged = config['rigged']['status']
    rigged_number = config['rigged']['rigged_number']

def roll_dice():
    return rigged_number if is_rigged else r.randint(low, high)

# Define dot positions (relative to center of die face)
def get_dice_dots(value, center, size):
    cx, cy = center
    offset = size // 4
    positions = {
        1: [(cx, cy)],
        2: [(cx - offset, cy - offset), (cx + offset, cy + offset)],
        3: [(cx, cy), (cx - offset, cy - offset), (cx + offset, cy + offset)],
        4: [(cx - offset, cy - offset), (cx + offset, cy - offset),
            (cx - offset, cy + offset), (cx + offset, cy + offset)],
        5: [(cx, cy), (cx - offset, cy - offset), (cx + offset, cy - offset),
            (cx - offset, cy + offset), (cx + offset, cy + offset)],
        6: [(cx - offset, cy - offset), (cx + offset, cy - offset),
            (cx - offset, cy), (cx + offset, cy),
            (cx - offset, cy + offset), (cx + offset, cy + offset)]
    }
    return positions.get(value, [])

def draw_dice(value, center, size):
    pygame.draw.rect(screen, (0, 0, 0), (*[c - size//2 for c in center], size, size), border_radius=12)
    pygame.draw.rect(screen, (255, 255, 255), (*[c - size//2 + 4 for c in center], size - 8, size - 8), border_radius=10)
    for dot_pos in get_dice_dots(value, center, size):
        pygame.draw.circle(screen, (0, 0, 0), dot_pos, 6)

def main():
    rolled_number = None
    running = True

    while running:
        screen.fill((255, 255, 255))  # Clear screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                rolled_number = roll_dice()

        # Draw dice and message
        if rolled_number:
            draw_dice(rolled_number, center=(WIDTH // 2, HEIGHT // 2 - 40), size=100)

            # Draw text at bottom
            text = font.render(f"You rolled: {rolled_number}", True, (0, 0, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))
        else:
            prompt = font.render("Click to roll the dice!", True, (0, 0, 0))
            screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 - 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
