


import pygame

from settings import *


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)
        self.small = pygame.font.SysFont(None, 12)
        self.middlesmall = pygame.font.SysFont(None, 24)
        try:
            self.apple = pygame.image.load("assets/sprites/apple.png")
            self.apple = pygame.transform.scale(self.apple, (32, 32))
        except FileNotFoundError as e:
            print("apple", e)
            self.apple = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            self.apple.fill(APPLE_COLOR)
        self.snake_body = pygame.image.load("assets/sprites/snake_body.png")
        self.snake_body = pygame.transform.scale(self.snake_body, (20, 20))
        self.snake_head = pygame.image.load("assets/sprites/snake_head.png")
        self.snake_head = pygame.transform.scale(self.snake_head, (20, 20))
        self.snake_tail = pygame.image.load("assets/sprites/snake_tail.png")
        self.snake_tail = pygame.transform.scale(self.snake_tail, (20, 20))
        self.snake_corner = pygame.image.load("assets/sprites/snake_corner.png")
        self.snake_corner = pygame.transform.scale(self.snake_corner, (20, 20))

    def draw(self, snake, food, score):
        # 매 프레임 전체를 검은색으로 지우고 다시 그림 (플리커 방지)
        self.screen.fill(BACKGROUND_COLOR)

        snake_head = self.snake_head.get_rect(topleft=(snake[0][0] * CELL_SIZE, snake[0][1] * CELL_SIZE))
        rotated_h = pygame.transform.rotate(self.snake_head, snake[0][2] * 90)
        self.screen.blit(rotated_h, snake_head)
        snake_tail = self.snake_tail.get_rect(topleft=(snake[-1][0] * CELL_SIZE, snake[-1][1] * CELL_SIZE))
        rotated_t = pygame.transform.rotate(self.snake_tail, snake[-2][2] * 90)
        self.screen.blit(rotated_t, snake_tail)

        # 뱀의 각 칸을 셀 좌표 → 픽셀 좌표로 변환해서 그림
        # 예: (3, 5) → 픽셀 (3*20, 5*20) = (60, 100)
        f_dir = snake[0][2]
        for x, y, dir in snake[1:-1:]:
            if f_dir == dir:
                snake_body = self.snake_body.get_rect(topleft=(x * CELL_SIZE, y * CELL_SIZE))
                rotated_b = pygame.transform.rotate(self.snake_body, dir * 90)
                self.screen.blit(rotated_b, snake_body)
            else:
                snake_corner = self.snake_corner.get_rect(topleft=(x * CELL_SIZE, y * CELL_SIZE))
                if f_dir > dir:
                    rotated_c = pygame.transform.rotate(self.snake_corner, (dir - (abs(dir - f_dir) % 3)) * 90)
                else:
                    rotated_c = pygame.transform.rotate(self.snake_corner, ((f_dir + dir) / 2 + 0.5) * 90)
                self.screen.blit(rotated_c, snake_corner)
            f_dir = dir
            # self.mouth_open(food, snake)

        # 음식 그리기
        apple = self.apple.get_rect(center=(food[0] * CELL_SIZE + (CELL_SIZE) // 2, food[1] * CELL_SIZE + (CELL_SIZE) // 3))
        self.screen.blit(self.apple, apple)

        # 점수를 좌측 상단에 표시
        score_text = self.font.render(f"Score: {score}", True, (0,0,0))
        self.screen.blit(score_text, (5, 5))

    # def draw_game_over(self, score):
    #     # Game Over 메시지를 화면 정중앙에 표시
    #     # get_rect(center=...)로 텍스트 크기에 상관없이 자동 중앙 정렬
    #     msg = self.font.render("Game Over!  SPACE to restart", True, (0,0,0))
    #     self.screen.blit(msg, msg.get_rect(center=(ROWS * CELL_SIZE // 2 + 5 * CELL_SIZE, COLS * CELL_SIZE // 2 - 3 * CELL_SIZE)))

    def mouth_open(self, apple, snake):
        if snake[0] in [(apple[0] - 1, apple[1]), (apple[0] + 1, apple[1]), (apple[0], apple[1] - 1), (apple[0], apple[1] + 1), (apple[0] - 2, apple[1]), (apple[0] + 2, apple[1]), (apple[0], apple[1] - 2), (apple[0], apple[1] + 2)]:
            pygame.draw.rect(self.screen, MOUTH_COLOR,
                         (snake[0][0] * CELL_SIZE, snake[0][1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))


    def _center_text(self, text, y, font = None, color = WHITE):
        font = font or self.font
        surface = font.render(text, True, color)
        self.screen.blit(surface, surface.get_rect(center=(WIDTH // 2, y)))

    def draw_name_input(self, score, nickname):
        self.screen.fill(BLACK)
        self._center_text("Game Over", HEIGHT * (12/38), None, RED)
        self._center_text(f"Score : {score}", HEIGHT * (15/38))
        self._center_text("Enter your nickname:", HEIGHT * (18/38))
        self._center_text(f"{nickname}", HEIGHT * (20/38))
        self._center_text("ENTER ↲ = save   ESC = skip", HEIGHT * (25/38))

    def draw_ranking(self, rows, score, r):
        # DB에서 받아온 상위 10명을 표로 표시
        # rows 예시: [{"nickname": "abc", "score": 12}, ...]
        self.screen.fill(BLACK)
        self._center_text("TOP 10", HEIGHT * (1/25))
        self._center_text(f"Your score : {score}", HEIGHT * (3/25), None, GREEN)
        if not rows:
            # DB 설정이 안 됐거나 네트워크 오류일 때
            self._center_text("(no data)", HEIGHT // 2, self.small)
        else:
            for i, v in enumerate(rows, 1):
                if i == 1 or i == 2 or i == 3:
                    text = self.middlesmall.render(f"{i}. {v['nickname']} :    {v['score']}", True, RAINBOW[r % 7])
                    self.screen.blit(text, text.get_rect(center=(WIDTH * (1/40) * CELL_SIZE, (3.5 + 2.2 * i) * CELL_SIZE)))
                elif i == 10:
                    text = self.middlesmall.render(f"{i}. {v['nickname']} :    {v['score']}", True, RED)
                    self.screen.blit(text, text.get_rect(center=(WIDTH * (1/40) * CELL_SIZE, (3.5 + 2.2 * i) * CELL_SIZE)))
                else:
                    text = self.middlesmall.render(f"{i}. {v['nickname']} :    {v['score']}", True, WHITE)
                    self.screen.blit(text, text.get_rect(center=(WIDTH * (1/40) * CELL_SIZE, (3.5 + 2.2 * i) * CELL_SIZE)))
        self._center_text("SPACE to restart", HEIGHT * (24/25))