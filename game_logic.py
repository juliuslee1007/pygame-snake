import random

from settings import COLS, ROWS


# 먹이 생성
def spawn_apple(snake : list):
    while True:
        # 랜덤 좌표
        apple = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if apple not in snake:
            return apple

# 리셋 함수 구현
def reset():
    start_x = random.randint(3, COLS - 5)
    start_y = random.randint(3, ROWS - 5)
    direc_x = random.randint(-1, 1)
    if direc_x != 0:
        direc_y = 0
    else:
        direc_y = [-1, 1][random.randint(0, 1)]
    snake = [(start_x, start_y), (start_x - direc_x, start_y - direc_y), (start_x - direc_x * 2, start_y - direc_y * 2), (start_x - direc_x * 3, start_y - direc_y * 3), (start_x - direc_x * 4, start_y - direc_y * 4)]
    direction = (direc_x, direc_y)
    apple = (COLS - 1, ROWS // 2 - 1)
    score = 0
    return snake, direction, apple, score 

def update(snake, direction, apple, score):
    """
    한 프레임의 게임 상태를 업데이트한다.
    반환값:(snake, food, score, alive)
        allive = False 이면 게임 오버
    """
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])
    
    if new_head in snake:
        return snake, apple, score, False
    if new_head[0] == -1 or new_head[0] == COLS or new_head[1] == -1 or new_head[1] == ROWS:
        return snake, apple, score, False 
       
    snake.insert(0, new_head)

    if new_head == apple:
        apple = spawn_apple(snake)
        score += 1
    else:
        snake.pop()
    
    return snake, apple, score, True