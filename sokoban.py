import sys
import pygame
import sqlite3
pygame.init()

# названия уровней
levels = ["level1.txt", "level2.txt", "level3.txt",
          "level4.txt", "level5.txt", "level6.txt",
          "level7.txt", "level8.txt", "level9.txt", "level10.txt"]


# класс для создания блоков и тд
class Blocks(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# класс для создания и передвижения героя
class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y


# запуск игры
def main():
    start_screen()


# выход из игры
def terminate():
    pygame.quit()
    sys.exit()


# функция для запуска стартового окна
def start_screen():
    screen = pygame.display.set_mode([550, 570])
    screen_saver = Blocks(0, 0, "screensaver.png")
    screen.fill((255, 255, 255))
    screen.blit(screen_saver.image, screen_saver.rect)
    while 1:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                terminate()

            if i.type == pygame.MOUSEBUTTONDOWN:
                # проверка "нажата" ли кнопка
                if 133 <= i.pos[0] <= 415 and 144 <= i.pos[1] <= 208:
                    f = open("level_end.txt", "r")
                    k = 0
                    for o in f:
                        k = int(o.lstrip())
                    if k != 0:
                        con = sqlite3.connect("Sokoban.db")
                        cur = con.cursor()

                        info = cur.execute("SELECT * from sokoban").fetchall()
                        if len(info) != 0:

                            info1 = cur.execute("SELECT Game from sokoban").fetchall()

                            cur.execute("""UPDATE sokoban SET Level=Level + 1
                                                             WHERE Game = ?""", (info1[-1][0],))
                            con.commit()

                            con = sqlite3.connect("Sokoban.db")
                            cur = con.cursor()

                            info = cur.execute("SELECT * from sokoban").fetchall()
                            if k + 1 > 10:
                                k = 9
                            new_data, new2 = [info[-1][0] + 1, k + 1], [info[-1][0] + 2, 0]
                            cur.execute("INSERT INTO sokoban VALUES(?, ?)", new_data)
                            cur.execute("INSERT INTO sokoban VALUES(?, ?)", new2)
                        else:
                            if k + 1 > 10:
                                k = 9
                            new_data = [1, k + 1]
                            cur.execute("INSERT INTO sokoban VALUES(?, ?)", new_data)

                        con.commit()

                    g = open("level_end.txt", "w")
                    g.write("0")
                    g.close()
                    f.close()
                    game_play()

                if 133 <= i.pos[0] <= 415 and 250 <= i.pos[1] <= 314:
                    game_play()

                if 133 <= i.pos[0] <= 415 and 464 <= i.pos[1] <= 536:
                    terminate()

                if 133 <= i.pos[0] <= 415 and 358 <= i.pos[1] <= 425:
                    best_result()

        pygame.display.update()


# функция для последнего игрового окна
def end_screen():
    # занесение результата в бд
    f = open("level_end.txt", "r")
    k = 0
    for o in f:
        k = int(o.lstrip())
    if k != 0:
        con = sqlite3.connect("Sokoban.db")
        cur = con.cursor()

        info = cur.execute("SELECT * from sokoban").fetchall()
        if len(info) != 0:
            new_data = [info[-1][0] + 1, 10]
            cur.execute("INSERT INTO sokoban VALUES(?, ?)", new_data)
        else:
            new_data = [1, k + 1]
            cur.execute("INSERT INTO sokoban VALUES(?, ?)", new_data)

        con.commit()

    f.close()

    # отрисовка и обработка событий конечного окна
    screen = pygame.display.set_mode([550, 570])
    screen_saver = Blocks(0, 0, "end_screen.png")
    screen.fill((255, 255, 255))
    screen.blit(screen_saver.image, screen_saver.rect)
    while 1:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                terminate()

            if i.type == pygame.MOUSEBUTTONDOWN:
                if 127 <= i.pos[0] <= 388 and 336 <= i.pos[1] <= 394:
                    start_screen()

                if 128 <= i.pos[0] <= 389 and 451 <= i.pos[1] <= 502:
                    terminate()

        pygame.display.update()


# функция для вывода лучшего результата за все время
def best_result():
    screen = pygame.display.set_mode([550, 570])
    screen_saver = Blocks(0, 0, "best_result.png")
    screen.fill((255, 255, 255))
    screen.blit(screen_saver.image, screen_saver.rect)

    con = sqlite3.connect("Sokoban.db")
    cur = con.cursor()

    info = cur.execute("SELECT Level from sokoban WHERE Level >= 0").fetchall()

    result = 0

    if len(info) != 0:
        int_results = [int(i[0]) for i in info]
        result = max(int_results)

    if result > 10:
        result = 10

    name = "r" + str(result) + ".png"
    best_results = Blocks(180, 240, name)
    screen.blit(best_results.image, best_results.rect)

    while 1:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                terminate()

            if i.type == pygame.MOUSEBUTTONDOWN:
                # проверка кнопок
                if 38 <= i.pos[0] <= 240 and 476 <= i.pos[1] <= 544:
                    start_screen()

                if 318 <= i.pos[0] <= 521 and 476 <= i.pos[1] <= 544:
                    terminate()

        pygame.display.update()


# функция для перехода на следующий уровень
def next_level():
    screen = pygame.display.set_mode([550, 570])
    screen_saver = Blocks(0, 0, "next_level.png")
    screen.fill((255, 255, 255))
    screen.blit(screen_saver.image, screen_saver.rect)
    while 1:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                terminate()

            if i.type == pygame.MOUSEBUTTONDOWN:
                # проверка кнопок
                if 133 <= i.pos[0] <= 415 and 144 <= i.pos[1] <= 208:

                    game_play()

                else:
                    # изменение номера уровня
                    # если не нажата кнопка перепройти уровень
                    f = open("level_end.txt", "r")
                    k = 0
                    for o in f:
                        k = int(o.lstrip())

                    con = sqlite3.connect("Sokoban.db")
                    cur = con.cursor()

                    info = cur.execute("SELECT Game from sokoban").fetchall()

                    if k < 10:
                        cur.execute("""UPDATE sokoban SET Level=Level + 1
                                     WHERE Game = ?""", (info[-1][0], ))

                    con.commit()

                    g = open("level_end.txt", "w")
                    if k + 1 <= 10:
                        g.write(str(k + 1))
                    else:
                        g.write("0")
                    g.close()
                    f.close()

                if 133 <= i.pos[0] <= 415 and 250 <= i.pos[1] <= 314:
                    game_play()

                if 133 <= i.pos[0] <= 415 and 358 <= i.pos[1] <= 425:

                    con = sqlite3.connect("Sokoban.db")
                    cur = con.cursor()

                    # занесение результатов в бд

                    f = open("level_end.txt", "r")
                    k = 0
                    for o in f:
                        k = int(o.lstrip())

                    info = cur.execute("SELECT * from sokoban").fetchall()
                    if len(info) != 0:
                        new_data = [info[-1][0] + 1, k + 1]
                        cur.execute("INSERT INTO sokoban VALUES(?, ?)", new_data)
                    else:
                        new_data = [1, k + 1]
                        cur.execute("INSERT INTO sokoban VALUES(?, ?)", new_data)

                    con.commit()

                    start_screen()

                if 133 <= i.pos[0] <= 415 and 464 <= i.pos[1] <= 536:

                    con = sqlite3.connect("Sokoban.db")
                    cur = con.cursor()

                    # занесение результатов в бд

                    f = open("level_end.txt", "r")
                    k = 0
                    for o in f:
                        k = int(o.lstrip())
                    info = cur.execute("SELECT * from sokoban").fetchall()
                    if len(info) != 0:
                        new_data = [info[-1][0] + 1, k + 1]
                        cur.execute("INSERT INTO sokoban VALUES(?, ?)", new_data)
                    else:
                        new_data = [1, k + 1]
                        cur.execute("INSERT INTO sokoban VALUES(?, ?)", new_data)

                    con.commit()

                    terminate()

        pygame.display.update()


# функция для получения уровня
def get_level():
    f = open("level_end.txt", "r")
    k = 0
    for i in f:
        k = int(i.lstrip())
    new_level = "level1.txt"
    if k + 1 <= 10:
        new_level = levels[k]

    f.close()
    return open(new_level, "r")


# функция, реализующая ход игры
def game_play():

    # создание групп спрайтов
    screen = pygame.display.set_mode([550, 580])
    blocks = pygame.sprite.Group()

    boxes = pygame.sprite.Group()
    place_blocks = pygame.sprite.Group()

    blocks.add(Blocks(400, 0, "again.jpg"))
    blocks.add(Blocks(480, 0, "menu.png"))
    blocks.add(Blocks(50, 0, "text.png"))
    boxes_num = Blocks(180, 0, "num0.png")

    # создание переменных и интерфейса
    new_level = False

    block_coords = []
    boxes_coords = []
    place_blocks_coords = []

    level = get_level()

    hero = None
    hero_right = True
    hero_x_coo = 0
    hero_y_coo = 0

    # прорисовка игрового поля
    y = 30
    for i in level:
        x = 0
        for k in i.lstrip():
            if k == ".":
                blocks.add(Blocks(x, y, '1.png'))
                block_coords.append([x, y])
            if k == "#":
                blocks.add(Blocks(x, y, '2.png'))
                block_coords.append([x, y])
            if k == "0":
                boxes.add(Blocks(x, y, 'box.jpg'))
                boxes_coords.append([x, y])
            if k == "@":
                hero = Hero(x, y, 'hero.jpg')
                hero_x_coo = x
                hero_y_coo = y
            if k == "+":
                place_blocks.add(Blocks(x, y, '3.png'))
                place_blocks_coords.append([x, y])

            x += 50

        y += 50

    # общий цикл игры
    while 1:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                terminate()

            # проверка нажатия на кнопки "меню" и "заново"
            if i.type == pygame.MOUSEBUTTONDOWN:
                if 400 <= i.pos[0] <= 430 and 0 <= i.pos[1] <= 30:
                    game_play()

                if 480 <= i.pos[0] <= 510 and 0 <= i.pos[1] <= 30:
                    start_screen()

            # проверка на событие передвижение героя
            if i.type == pygame.KEYDOWN:
                k = True
                p = True
                if i.key == pygame.K_LEFT:

                    # проверка на возможность передвижения
                    for w in block_coords:
                        if w[0] == hero_x_coo - 50 and w[1] == hero_y_coo:
                            k = False
                            break
                    if k:
                        # проверка на наличие блоков и ящиков рядом
                        for w in boxes_coords:
                            if w[0] == hero_x_coo - 50 and w[1] == hero_y_coo and \
                                    ([hero_x_coo - 100, hero_y_coo] in boxes_coords or
                                     [hero_x_coo - 100, hero_y_coo] in block_coords):
                                p = False
                            if w[0] == hero_x_coo - 50 and w[1] == hero_y_coo and \
                                    [hero_x_coo - 100, hero_y_coo] not in block_coords and \
                                    [hero_x_coo - 100, hero_y_coo] not in boxes_coords:
                                w[0] -= 50
                                break
                        if p:
                            hero_x_coo -= 50
                            if hero_right:
                                hero_right = False
                                hero.image = pygame.transform.flip(hero.image, 1, 0)

                if i.key == pygame.K_RIGHT:

                    # проверка на возможность передвижения
                    for w in block_coords:
                        if w[0] == hero_x_coo + 50 and w[1] == hero_y_coo:
                            k = False
                            break
                    if k:
                        # проверка на наличие блоков и ящиков рядом
                        for w in boxes_coords:
                            if w[0] == hero_x_coo + 50 and w[1] == hero_y_coo and \
                                    ([hero_x_coo + 100, hero_y_coo] in boxes_coords or
                                     [hero_x_coo + 100, hero_y_coo] in block_coords):
                                p = False
                                break

                            if w[0] == hero_x_coo + 50 and w[1] == hero_y_coo and \
                                    [hero_x_coo + 100, hero_y_coo] not in block_coords and \
                                    [hero_x_coo + 100, hero_y_coo] not in boxes_coords:
                                w[0] += 50
                                break
                        if p:
                            hero_x_coo += 50
                            if not hero_right:
                                hero_right = True
                                hero.image = pygame.transform.flip(hero.image, 1, 0)

                if i.key == pygame.K_UP:

                    # проверка на возможность передвижения
                    for w in block_coords:
                        if w[1] == hero_y_coo - 50 and w[0] == hero_x_coo:
                            k = False
                            break
                    if k:
                        # проверка на наличие блоков и ящиков рядом
                        for w in boxes_coords:
                            if w[0] == hero_x_coo and w[1] == hero_y_coo - 50 and \
                                    ([hero_x_coo, hero_y_coo - 100] in boxes_coords or
                                     [hero_x_coo, hero_y_coo - 100] in block_coords):
                                p = False
                                break

                            if w[0] == hero_x_coo and w[1] == hero_y_coo - 50 and \
                                    [hero_x_coo, hero_y_coo - 100] not in block_coords and \
                                    [hero_x_coo, hero_y_coo - 100] not in boxes_coords:
                                w[1] -= 50
                                break
                        if p:
                            hero_y_coo -= 50

                if i.key == pygame.K_DOWN:

                    # проверка на возможность передвижения
                    for w in block_coords:
                        if w[1] == hero_y_coo + 50 and w[0] == hero_x_coo:
                            k = False
                            break
                    if k:
                        # проверка на наличие блоков и ящиков рядом
                        for w in boxes_coords:
                            if w[0] == hero_x_coo and w[1] == hero_y_coo + 50 and \
                                    ([hero_x_coo, hero_y_coo + 100] in boxes_coords or
                                     [hero_x_coo, hero_y_coo + 100] in block_coords):
                                p = False
                                break

                            if w[0] == hero_x_coo and w[1] == hero_y_coo + 50 and \
                                    [hero_x_coo, hero_y_coo + 100] not in block_coords and \
                                    [hero_x_coo, hero_y_coo + 100] not in boxes_coords:
                                w[1] += 50
                                break
                        if p:
                            hero_y_coo += 50

                # перерисовка игрового поля
                boxes = pygame.sprite.Group()
                nums = 0
                for w in boxes_coords:
                    if w in place_blocks_coords:
                        nums += 1
                        boxes.add(Blocks(w[0], w[1], 'box_done.jpg'))
                    else:
                        boxes.add(Blocks(w[0], w[1], 'box.jpg'))

                # проверка на выполнение уровня
                if nums == 3:
                    new_level = True

                # изменения количества верно поставленых ящиков
                name = "num" + str(nums) + ".png"

                boxes_num = Blocks(180, 0, name)

        screen.fill((255, 255, 255))
        blocks.draw(screen)
        place_blocks.draw(screen)
        boxes.draw(screen)
        screen.blit(hero.image, hero.rect)
        screen.blit(boxes_num.image, boxes_num.rect)

        pygame.display.update()

        hero.update(hero_x_coo, hero_y_coo)
        blocks.update()
        boxes.update()
        place_blocks.update()

        # переход на новый уровень
        if new_level:
            f = open("level_end.txt", "r")
            k = 0
            for i in f:
                k = int(i.lstrip())
            if k + 1 == 10:
                end_screen()
            if k + 1 <= 9:
                next_level()

            f.close()


# функция запуска игры
if __name__ == '__main__':
    main()
