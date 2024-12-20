import sqlite3
import pygame
from random import randrange as rnd

# Настройки окна
WIDTH, HEIGHT = 1200, 800
fps = 60

# Настройки ракетки
paddle_w = 330
paddle_h = 35
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)

# Настройки мяча
ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)

# Логин пользователя (будет передаваться при старте игры)
user_login = ""

def create_db():
    """Создает базу данных и таблицу пользователей, если она не существует."""
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        high_score INTEGER
    )
    ''')
    connection.commit()
    connection.close()

def add_or_update_user_score(score):
    """Добавляет нового пользователя или обновляет его рекорд."""
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    # Проверяем существование пользователя
    cursor.execute('SELECT high_score FROM users WHERE login=?', (user_login,))
    result = cursor.fetchone()

    if result is None:
        # Пользователь не найден, добавляем нового с текущим рекордом
        cursor.execute('INSERT INTO users (login, password, high_score) VALUES (?, ?, ?)',
                       (user_login, "", score))
    else:
        current_high_score = result[0]
        # Обновляем рекорд только если новый счет выше или если рекорд не установлен (NULL)
        if current_high_score is None or score > current_high_score:
            cursor.execute('UPDATE users SET high_score=? WHERE login=?', (score, user_login))

    connection.commit()
    connection.close()

def get_leaderboard():
    """Получает таблицу лидеров из базы данных."""
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    # Исправленный SQL-запрос с пробелом перед числом в LIMIT
    cursor.execute('SELECT login , high_score FROM users ORDER BY high_score DESC LIMIT 5')

    leaderboard = cursor.fetchall()
    connection.close()
    return leaderboard

def start_game(login):
    global user_login, dx, dy, block_list, color_list
    user_login = login
    dx, dy = 1, -1

    pygame.init()
    sc = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    img = pygame.image.load('1.jpg').convert()

    score = 0
    high_score = 0
    font = pygame.font.Font(None, 36)

    block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
    color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

    def display_message(message):
        text_surface = font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        sc.blit(text_surface, text_rect)
        return text_rect

    def draw_buttons():
        restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 30, 200, 50)
        leaderboard_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)
        pygame.draw.rect(sc, (0, 255, 0), restart_button)
        pygame.draw.rect(sc, (0, 0, 255), leaderboard_button)
        restart_text = font.render("Restart", True, (0, 0, 0))
        leaderboard_text = font.render("Лидеры", True, (255, 255, 255))
        sc.blit(restart_text, restart_text.get_rect(center=restart_button.center))
        sc.blit(leaderboard_text, leaderboard_text.get_rect(center=leaderboard_button.center))
        return restart_button, leaderboard_button

    def detect_collision(dx, dy, ball, rect):
        if dx > 0:
            delta_x = ball.right - rect.left
        else:
            delta_x = rect.right - ball.left
        if dy > 0:
            delta_y = ball.bottom - rect.top
        else:
            delta_y = rect.bottom - ball.top
        if abs(delta_x - delta_y) < 10:
            dx, dy = -dx, -dy
        elif delta_x > delta_y:
            dy = -dy
        elif delta_y > delta_x:
            dx = -dx
        return dx, dy

    def reset_game():
        nonlocal score
        score = 0
        block_list.clear()
        color_list.clear()
        block_list.extend([pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)])
        color_list.extend([(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)])
        ball.x = rnd(ball_rect, WIDTH - ball_rect)
        ball.y = HEIGHT // 2

    def show_leaderboard():
        """Отображает таблицу лидеров."""
        leaderboard = get_leaderboard()
        leaderboard_window = pygame.Surface((400, 300))

        leaderboard_window.fill((255, 255, 255))

        title = font.render("Таблица лидеров", True, (0, 0, 0))

        leaderboard_window.blit(title, (100, 10))

        for i, (name, score) in enumerate(leaderboard):
            text = font.render(f"{i + 1}. {name}: {score}", True, (0, 0, 0))
            leaderboard_window.blit(text, (50, 50 + i * 30))

        return leaderboard_window

    game_over = False
    show_leaderboard_flag = False
    close_leaderboard_flag = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        sc.blit(img, (0, 0))

        # Рисуем блоки и ракетку и мяч
        [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
        pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)
        pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)

        if not game_over:
            ball.x += ball_speed * dx
            ball.y += ball_speed * dy

            if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
                dx = -dx
            if ball.centery < ball_radius:
                dy = -dy

            if ball.colliderect(paddle) and dy > 0:
                dx, dy = detect_collision(dx, dy, ball, paddle)

            hit_index = ball.collidelist(block_list)
            if hit_index != -1:
                hit_rect = block_list.pop(hit_index)
                hit_color = color_list.pop(hit_index)
                dx, dy = detect_collision(dx, dy, ball, hit_rect)
                score += 10
                hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
                pygame.draw.rect(sc, hit_color, hit_rect)

            if ball.bottom > HEIGHT:
                game_over_message = 'GAME OVER! Your score: ' + str(score)
                add_or_update_user_score(score)  # Обновляем рекорд при проигрыше или выигрыше
                game_over = True
            elif not len(block_list):
                game_over_message = 'WIN!!! Your score: ' + str(score)
                add_or_update_user_score(score)  # Обновляем рекорд при выигрыше или проигрыше
                game_over = True
        else:
            message_rect = display_message(game_over_message)
            restart_button, leaderboard_button = draw_buttons()
            mouse_pos = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()

            if mouse_buttons[0]:
                if restart_button.collidepoint(mouse_pos):
                    reset_game()
                    game_over = False
                elif leaderboard_button.collidepoint(mouse_pos):
                    show_leaderboard_flag = True

        if show_leaderboard_flag:
            leaderboard_surface = show_leaderboard()
            sc.blit(leaderboard_surface, (WIDTH // 2 - 200, HEIGHT // 2 - 150))

            # Рисуем крестик для закрытия окна
            close_button = pygame.Rect(WIDTH // 2 + 180, HEIGHT // 2 - 150, 20, 20)
            pygame.draw.rect(sc, (255, 0, 0), close_button)
            font_small = pygame.font.Font(None, 24)
            close_text = font_small.render("X", True, (255, 255, 255))
            sc.blit(close_text, (WIDTH // 2 + 185, HEIGHT // 2 - 150))

            # Если кликнули на крестик, закрыть окно с таблицей лидеров
            if mouse_buttons[0] and close_button.collidepoint(mouse_pos):
                show_leaderboard_flag = False

        key = pygame.key.get_pressed()
        if not game_over:
            if key[pygame.K_LEFT] and paddle.left > 0:
                paddle.left -= paddle_speed
            if key[pygame.K_RIGHT] and paddle.right < WIDTH:
                paddle.right += paddle_speed

        pygame.display.flip()
        high_score_text = font.render(f'High Score: {high_score}', True, (255, 255, 255))
        sc.blit(high_score_text, (10, 10))
        clock.tick(fps)

if __name__ == "__main__":
    create_db()  # Создаем базу данных и таблицу пользователей перед началом игры.
    start_game("Player1")  # Запуск игры с логином по умолчанию
