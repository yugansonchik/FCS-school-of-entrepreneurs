import pygame
import random
import os
import time

# Определение размеров экрана
SCREEN_WIDTH = 375
SCREEN_HEIGHT = 667

# Определение размеров контейнера
CONTAINER_WIDTH = 150
CONTAINER_HEIGHT = 150

# Определение скорости падения мусора
FALLING_SPEED = 0.5

# Определение размеров мусора
TRASH_WIDTH = 70
TRASH_HEIGHT = 70

# Загрузка изображений мусора
BOTTLE_IMAGE_PATH = os.path.join("images", "bottle.png")
PACKAGE_IMAGE_PATH = os.path.join("images", "package.png")
FOOD_IMAGE_PATH = os.path.join("images", "food.png")
CONT_PAPER_IMAGE_PATH = os.path.join("images", "cont.png")
PACK_IMAGE_PATH = os.path.join("images", "pack.png")
PAPER_IMAGE_PATH = os.path.join("images", "paper.png")

# Определение списка возможных типов мусора
TRASH_TYPES = [
    {"path": BOTTLE_IMAGE_PATH, "container": "glass"},
    {"path": PACKAGE_IMAGE_PATH, "container": "plastic"},
    {"path": FOOD_IMAGE_PATH, "container": "organic"},
    {"path": PAPER_IMAGE_PATH, "container": "paper"},
    {"path": CONT_PAPER_IMAGE_PATH, "container": "cont"},
    {"path": PACK_IMAGE_PATH, "container": "pack"}
]

# Определение позиции контейнера
CONTAINER_POSITION = (SCREEN_WIDTH // 2 - CONTAINER_WIDTH // 2, SCREEN_HEIGHT - CONTAINER_HEIGHT - 10)

# Инициализация Pygame
pygame.init()

# Создание окна игры
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Garbage Sorting Game")

# Загрузка изображения фона
BACKGROUND_IMAGE_PATH = os.path.join("images", "background.jpg")
background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Загрузка звуковых эффектов
CORRECT_SOUND_PATH = os.path.join("sounds", "correct.wav")
WRONG_SOUND_PATH = os.path.join("sounds", "wrong.wav")
correct_sound = pygame.mixer.Sound(CORRECT_SOUND_PATH)
wrong_sound = pygame.mixer.Sound(WRONG_SOUND_PATH)

# Загрузка изображений мусора
def load_trash_image(path):
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, (TRASH_WIDTH, TRASH_HEIGHT))
    return image

bottle_image = load_trash_image(BOTTLE_IMAGE_PATH)
package_image = load_trash_image(PACKAGE_IMAGE_PATH)
food_image = load_trash_image(FOOD_IMAGE_PATH)
paper_image = load_trash_image(PAPER_IMAGE_PATH)
cont_image = load_trash_image(CONT_PAPER_IMAGE_PATH)
pack_image = load_trash_image(PACK_IMAGE_PATH)

# Создание объекта мусора
def create_trash():
    x = random.randint(0, SCREEN_WIDTH - TRASH_WIDTH)
    y = 0
    trash_type = random.choice(TRASH_TYPES)
    trash = {
        "x": x,
        "y": y,
        "image": load_trash_image(trash_type["path"]),
        "container": trash_type["container"]
    }
    trashes.append(trash)

# Создание нескольких объектов мусора в начале игры
trashes = []
for _ in range(1):
    create_trash()

# Отслеживание времени создания мусора
last_spawn_time = time.time()
SPAWN_DELAY = 5.0  # Задержка между созданиями мусора (в секундах)

# Инициализация счетчика
score = 0

# Отображение окна приветствия
welcome_screen = True
while welcome_screen:
    screen.fill((255, 255, 255))

    # Отображение текста приветствия
    font = pygame.font.Font(None, 14)
    text1 = font.render("Дорогой друг!", True, (0, 0, 0))
    text2 = font.render("Эта игра поможет тебе научиться сортировать мусор!", True, (0, 0, 0))
    text3 = font.render("Ты встретишь отходы, принадлежащие разным фракциям", True, (0, 0, 0))
    text4 = font.render("Передвигая мусорный контейнер, поймай отходы определенной фракции", True, (0, 0, 0))

    text1_rect = text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
    text2_rect = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
    text3_rect = text3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    text4_rect = text4.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))

    screen.blit(text1, text1_rect)
    screen.blit(text2, text2_rect)
    screen.blit(text3, text3_rect)
    screen.blit(text4, text4_rect)

    # Обновление экрана
    pygame.display.flip()

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            welcome_screen = False
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            welcome_screen = False

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            # Обработка движения мыши для перемещения контейнера
            container_x, _ = event.pos
            container_x -= CONTAINER_WIDTH // 2
            if container_x < 0:
                container_x = 0
            elif container_x > SCREEN_WIDTH - CONTAINER_WIDTH:
                container_x = SCREEN_WIDTH - CONTAINER_WIDTH
            CONTAINER_POSITION = (container_x, CONTAINER_POSITION[1])

    # Очистка экрана
    screen.fill((255, 255, 255))

    # Отображение фона
    screen.blit(background_image, (0, 0))

    # Отображение контейнера
    container_image = pygame.image.load(os.path.join("images", "container.png"))
    container_image = pygame.transform.scale(container_image,(CONTAINER_WIDTH, CONTAINER_HEIGHT))
    screen.blit(container_image, CONTAINER_POSITION)

    # Обработка движения и отображение мусора
    for trash in trashes:
        x = trash["x"]
        y = trash["y"]
        image = trash["image"]
        container = trash["container"]
        screen.blit(image, (x, y))

        # Перемещение мусора вниз по экрану
        trash["y"] += FALLING_SPEED

        # Обработка попадания мусора в контейнер
        if (
            x > CONTAINER_POSITION[0]
            and x < CONTAINER_POSITION[0] + CONTAINER_WIDTH
            and y + TRASH_HEIGHT > CONTAINER_POSITION[1]
        ):
            if container == "paper":
                correct_sound.play()
                score += 1
            elif container in ["glass", "cont", "pack", "plastic"]:
                correct_sound.play()
                score += 1
            else:
                wrong_sound.play()
                score -= 1

            trashes.remove(trash)
            create_trash()

    # Создание нового мусора с определенным интервалом времени
    current_time = time.time()
    if current_time - last_spawn_time >= SPAWN_DELAY:
        create_trash()
        last_spawn_time = current_time

    # Отображение счетчика
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    score_text_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    screen.blit(score_text, score_text_rect)

    # Обновление экрана
    pygame.display.flip()

# Завершение игры
pygame.quit()