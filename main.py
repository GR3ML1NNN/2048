import pygame as pg
import random
import sys

pg.init()
pg.font.init()
screen = pg.display.set_mode((600, 600))
clock = pg.time.Clock()
screenWidth, screenHeight = pg.display.get_surface().get_size()
font = pg.font.SysFont('Arial', 60)

grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]

colors = {
    0: (144, 140, 170),
    2: (156, 207, 216),
    4: (62, 143, 176),
    8: (86, 148, 159),
    16: (40, 105, 131),
    32: (196, 167, 231),
    64: (144, 122, 169),
    128: (246, 193, 119),
    256: (234, 154, 151),
    512: (235, 111, 146),
    1024: (235, 111, 146),
    2048: (180, 99, 122)
}


def drawGrid(grid):
    global screenWidth, screenHeight
    global colors
    global font

    rowCount = 0
    x, y = 0, 0
    recWidth, recLength = screenWidth // 4, screenHeight // 4

    for i in grid:
        for j in i:
            if rowCount == screenWidth // recWidth:
                y += recLength
                x = 0
                rowCount = 0

            color = colors.get(j)
            pg.draw.rect(screen, color,
                         (x + 5, y + 5, recWidth - 10, recLength - 10), border_radius=8)

            screen.blit(font.render(str(j), True, (224, 222, 244)),
                        (x + (recWidth // 2 - 20),
                         y + (recLength // 2 - 30)))

            x += recWidth
            rowCount += 1


def left(grid):

    shiftLeft(grid)

    for i in range(4):
        for j in range(3):
            if grid[i][j] == grid[i][j + 1] and grid[i][j] != 0:
                grid[i][j] *= 2
                grid[i][j + 1] = 0
                j = 0

    shiftLeft(grid)
    return grid


def right(grid):
    shiftRight(grid)

    for i in range(4):
        for j in range(3, 0, -1):
            if grid[i][j] == grid[i][j - 1] and grid[i][j] != 0:
                grid[i][j] *= 2
                grid[i][j - 1] = 0
                j = 0

    shiftRight(grid)
    return grid


def up(grid):
    grid = rotate(grid)
    grid = left(grid)
    grid = rotate(grid)
    grid = rotate(grid)
    grid = rotate(grid)
    return grid


def down(grid):
    g = rotate(grid)
    g = left(g)
    shiftRight(g)
    g = rotate(g)
    g = rotate(g)
    g = rotate(g)
    return g


def shiftLeft(grid):
    for i in range(4):
        nums = []
        count = 0
        for j in range(4):
            if grid[i][j] != 0:
                nums.append(grid[i][j])
                count += 1
        grid[i] = nums
        grid[i].extend([0] * (4 - count))


def shiftRight(grid):
    for i in range(4):
        nums = []
        count = 0
        for j in range(4):
            if grid[i][j] != 0:
                nums.append(grid[i][j])
                count += 1
        grid[i] = [0] * (4 - count)
        grid[i].extend(nums)


def rotate(grid):
    grid = [[grid[j][i] for j in range(4)] for i in range(3, -1, -1)]
    return grid


def randomSquare(grid):
    i = random.randint(0, 3)
    j = random.randint(0, 3)
    flatGrid = [cell for row in grid for cell in row]
    while grid[i][j] != 0 and 0 in flatGrid:
        i = random.randint(0, 3)
        j = random.randint(0, 3)
        if 0 not in flatGrid:
            break
    if 0 in flatGrid:
        grid[i][j] = 2


def checkState(grid):
    for i in range(4):
        for j in range(4):
            if j != 3 and grid[i][j] == grid[i][j + 1] or \
                    i != 3 and grid[i][j] == grid[i + 1][j]:
                return False

    flatGrid = [cell for row in grid for cell in row]
    if 0 not in flatGrid:
        return True
    else:
        return False


def endScreen(win, lose):
    global screenWidth, screenHeight
    global font
    s = pg.Surface((screenWidth, screenHeight), pg.SRCALPHA)
    s.set_alpha(128)
    s.fill((0, 0, 0))
    screen.blit(s, (0, 0))

    if win:
        msg = "You Win"
    if lose:
        msg = "Maybe Next time..."

    screen.blit(font.render(msg, True, (224, 222, 244)),
                (screenWidth // 3, screenHeight // 3))


def main():
    global grid
    running = True
    win = False
    lose = False
    # initial sudo random start square
    randomSquare(grid)
    randomSquare(grid)
    while running:
        for event in pg.event.get():
            key = pg.key.get_pressed()
            if event.type == pg.QUIT:
                running = False
            if key[pg.K_ESCAPE]:
                running = False
            if key[pg.K_LEFT]:
                grid = left(grid)
                randomSquare(grid)
            if key[pg.K_RIGHT]:
                grid = right(grid)
                randomSquare(grid)
            if key[pg.K_UP]:
                grid = up(grid)
                randomSquare(grid)
            if key[pg.K_DOWN]:
                grid = down(grid)
                randomSquare(grid)

        if any(2048 in list for list in grid):
            win = True

        screen.fill("#f2e9e1")
        drawGrid(grid)

        if win and not lose:
            endScreen(win, lose)
        if lose and not win:
            endScreen(win, lose)

        lose = checkState(grid)
        pg.display.flip()
        clock.tick(8)

    pg.display.quit()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
