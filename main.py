import random

import pygame
import sys

pygame.init()

CELL_SIZE = 20
COLS = 40
ROWS = 30

BACKGROUND_COLOR = (230, 230, 255)
SNAKE_COLOR = (39, 99, 31)
APPLE_COLOR = (200, 10, 10)

FPS_INIT = 10

screen = pygame.display.set_mode((COLS * CELL_SIZE, ROWS * CELL_SIZE))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
start_x = random.randint(3, COLS - 5)
start_y = random.randint(3, ROWS - 5)
direc_x = random.randint(-1, 1)
arr = [-1, 1]
apple = (COLS - 1, ROWS // 2 - 1)
score = 0
font = pygame.font.SysFont(None, 36)
state = "PLAY"

if direc_x != 0:
    direc_y = 0
else:
    direc_y = arr[random.randint(0, 1)]

snake = [(start_x, start_y), (start_x - direc_x, start_y - direc_y), (start_x - direc_x * 2, start_y - direc_y * 2), (start_x - direc_x * 3, start_y - direc_y * 3), (start_x - direc_x * 4, start_y - direc_y * 4)]
direction = (direc_x, direc_y)

# 로직 함수 구현
# 먹이 생성
def spawn_apple(snake : list):
    global apple
    while True:
        # 랜덤 좌표
        apple = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if apple not in snake:
            break

# 리셋 함수 구현
def reset():
    global snake
    global direction
    global apple
    global state
    snake = [(start_x, start_y), (start_x - direc_x, start_y - direc_y), (start_x - direc_x * 2, start_y - direc_y * 2), (start_x - direc_x * 3, start_y - direc_y * 3), (start_x - direc_x * 4, start_y - direc_y * 4)]
    direction = (direc_x, direc_y)
    apple = (COLS - 1, ROWS // 2 - 1)
    state = "PLAY"

while True:
    print("state : ", state)
    # 1. 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)
            if event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            if event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
        if state == "DEAD":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state == "PLAY"
                    reset()

    # 2. 게임 로직 업뎃
    if state == "PLAY":
        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])
        
        if new_head in snake:
            state = "DEAD"
            
        snake.insert(0, new_head)
        if new_head == apple:
            spawn_apple(snake)
            score += 1
        else:
            snake.pop()
        
        if new_head[0] == -1 or new_head[0] == COLS or new_head[1] == -1 or new_head[1] == ROWS:
            state = "DEAD"

        # if new_head[0] == -1:
        #     new_head[0] = (COLS - 1, )


    # 3. 화면 그리기
    screen.fill(BACKGROUND_COLOR)
    for x, y in snake:
        pygame.draw.rect(screen, SNAKE_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, APPLE_COLOR, (apple[0] * CELL_SIZE, apple[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    score_text = font.render(f"Score: {score}", True, (255, 255, 255), (0, 0, 0)) #font.render(str, 글씨 가장 자리 부드럽게?, color, background_color)
    screen.blit(score_text, (5, 5))

    if state == "DEAD":
        over_text = font.render("Game Over! SPACE to restart", False, (255, 255, 255), (0, 0, 0))
        screen.blit(over_text, ((ROWS * CELL_SIZE) // 2 - 60, (COLS * CELL_SIZE) // 2 - 150))

    pygame.display.flip()
    clock.tick(FPS_INIT + score // 5)

