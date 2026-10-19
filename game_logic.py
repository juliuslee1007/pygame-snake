import random

from settings import COLS, ROWS


# 먹이 생성
def spawn_apple(snake : list):
    while True:
        # 랜덤 좌표
        apple = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
        if apple not in tuple(snake[:2]):
            return apple

def convert_dir(dir_x, dir_y):
    if dir_x == 1 and dir_y == 0:
        return 0
    elif dir_x == 0 and dir_y == -1:
        return 1
    elif dir_x == -1 and dir_y == 0:
        return 2
    else:
        return 3
# 리셋 함수 구현
def reset():
    start_x = random.randint(3, COLS - 5)
    start_y = random.randint(3, ROWS - 5)
    direc_x = random.randint(-1, 1)
    if direc_x != 0:
        direc_y = 0
    else:
        direc_y = [-1, 1][random.randint(0, 1)]
    snake = [(start_x, start_y, convert_dir(direc_x, direc_y)), (start_x - direc_x, start_y - direc_y, convert_dir(direc_x, direc_y)), (start_x - direc_x * 2, start_y - direc_y * 2, convert_dir(direc_x, direc_y)), (start_x - direc_x * 3, start_y - direc_y * 3, convert_dir(direc_x, direc_y)), (start_x - direc_x * 4, start_y - direc_y * 4, convert_dir(direc_x, direc_y))]
    direction = (direc_x, direc_y)
    apple = (COLS - 1, ROWS // 2 - 1)
    score = 0
    return snake, direction, apple, score 

def update(snake, direction, apple, score):
    eat_apple = False
    """
    한  프레임의 게임 상태를 업데이트한다.
    반환값:(snake, food, score, alive)
        allive = False 이면 게임 오버
    """
    head_x, head_y, direc = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1], convert_dir(direction[0], direction[1]))
    
    if new_head in snake:
        return snake, apple, score, False, False
    if new_head[0] == -1 or new_head[0] == COLS or new_head[1] == -1 or new_head[1] == ROWS:
        return snake, apple, score, False, False
       
    snake.insert(0, new_head)

    if (new_head[0], new_head[1]) == apple:
        apple = spawn_apple(snake)
        score += 1
        eat_apple = True
    else:
        snake.pop()
    
    return snake, apple, score, True, eat_apple