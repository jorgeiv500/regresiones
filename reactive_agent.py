import pygame
import random
import sys

# Parámetros del entorno
WIDTH, HEIGHT = 600, 400
ROWS, COLS = 10, 15
CELL_SIZE = WIDTH // COLS

# Colores
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
RED = (255, 50, 50)

# Inicializa Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Agente Reactivo - Sin memoria ni planificación")
clock = pygame.time.Clock()

# Crea el entorno
grid = [[' ' for _ in range(COLS)] for _ in range(ROWS)]

def place_obstacles(count):
    placed = 0
    while placed < count:
        i = random.randint(0, ROWS - 1)
        j = random.randint(0, COLS - 1)
        if grid[i][j] == ' ' and [i, j] != [0, 0]:
            grid[i][j] = 'X'
            placed += 1

place_obstacles(30)

# Posición inicial del agente
agent_pos = [0, 0]

def draw_grid():
    screen.fill(WHITE)
    for i in range(ROWS):
        for j in range(COLS):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = GRAY
            if grid[i][j] == 'X':
                color = BLACK
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, WHITE, rect, 1)

    # Dibuja el agente
    i, j = agent_pos
    agent_rect = pygame.Rect(j * CELL_SIZE + 5, i * CELL_SIZE + 5, CELL_SIZE - 10, CELL_SIZE - 10)
    pygame.draw.rect(screen, RED, agent_rect)

    pygame.display.flip()

def get_percepts(pos):
    i, j = pos
    directions = {
        'up': (i-1, j),
        'down': (i+1, j),
        'left': (i, j-1),
        'right': (i, j+1)
    }
    percepts = {}
    for dir, (x, y) in directions.items():
        if 0 <= x < ROWS and 0 <= y < COLS:
            percepts[dir] = grid[x][y]
        else:
            percepts[dir] = 'wall'
    return percepts

def decide(percepts):
    options = [d for d, v in percepts.items() if v == ' ']
    return random.choice(options) if options else None

# Bucle principal
running = True
steps = 0
while running and steps < 200:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_grid()
    percepts = get_percepts(agent_pos)
    action = decide(percepts)

    if action:
        delta = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }[action]
        new_pos = [agent_pos[0] + delta[0], agent_pos[1] + delta[1]]
        agent_pos = new_pos

    else:
        print("🤖 El agente está atrapado.")
        running = False

    steps += 1
    clock.tick(5)

pygame.quit()
sys.exit()
