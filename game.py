from random import randint


class GameOverError(Exception):
    pass


class Board:

    def __init__(self):
        self._fields = [
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'x'],
            ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
        ]

    def draw(self, graphic_buffer):
        for index_y in range(len(self._fields)):
            for index_x in range(len(self._fields[index_y])):
                if self._fields[index_y][index_x] == 'o':
                    graphic_buffer[index_y][index_x] = ' '
                else:
                    graphic_buffer[index_y][index_x] = 'x'

    def is_field_occupied(self, index_y, index_x):
        if self._fields[index_y][index_x] == 'x':
            return True


class User:

    def __init__(self, y, x, step):
        self.x = x
        self.y = y
        self.step = step
        self.shoot_step = 1
        self.points = 0

    def draw(self, graphic_buffer):
        graphic_buffer[self.y][self.x] = 'U'

    def make_step(self, context):
        chosen_direction = input('a/d/')
        if chosen_direction == 'a':
            if not board.is_field_occupied(self.y, self.x - self.step):
                self.x -= self.step
        elif chosen_direction == 'd':
            if not board.is_field_occupied(self.y, self.x + self.step):
                self.x += self.step
        context.shoots.append(Shoot(self.y - 1, self.x, self.shoot_step))


class Monster:

    POINTS_FOR_DEAD = 2

    def __init__(self, board, step):
        self.set_up_monster(board)
        self.step = step

    def draw(self, graphic_buffer):
        graphic_buffer[self.y][self.x] = 'M'

    def set_up_monster(self, board):
        while True:
            y = randint(0, 0)
            x = randint(0,11)
            if board.is_field_occupied(y, x):
                continue
            else:
                self.x = x
                self.y = y
                break

    def make_step(self, context):
        if board.is_field_occupied(self.y + self.step, self.x):
            raise GameOverError('GAME OVER')
        elif (self.y, self.x) == (context.user.y, context.user.x):
            raise GameOverError('GAME OVER')
        else:
            self.y += self.step
        for shoot in context.shoots:
            if (self.y, self.x) == (shoot.y, shoot.x):
                if self not in context.dead_list:
                    context.dead_list.append(self)
                if shoot not in context.dead_list:
                    context.dead_list.append(shoot)
                    shoot.add_score(context.user, self.POINTS_FOR_DEAD)
                break


class Boss:
    POINTS_FOR_DEAD = 3

    def __init__(self, board, step, life):
        self.set_up_boss(board)
        self.step = step
        self.life = life

    def draw(self, graphic_buffer):
        graphic_buffer[self.y][self.x] = 'B'

    def set_up_boss(self, board):
        while True:
            y = 0
            x = randint(0, 11)
            if board.is_field_occupied(y, x):
                continue
            else:
                self.x = x
                self.y = y
                break

    def make_step(self, context):
        if board.is_field_occupied(self.y + self.step, self.x):
            raise GameOverError('GAME OVER')
        elif (self.y, self.x) == (context.user.y, context.user.x):
            raise GameOverError('GAME OVER')
        else:
            self.y += self.step
        for shoot in context.shoots:
            if (shoot.y, self.x) == (shoot.y, shoot.x):
                self.life -= 1
                if shoot not in context.dead_list:
                    context.dead_list.append(shoot)
                if self.life == 0 and self not in context.dead_list:
                    context.dead_list.append(self)
                    shoot.add_score(context.user, self.POINTS_FOR_DEAD)


class Shoot:

    def __init__(self, y, x, step):
        self.y = y
        self.x = x
        self.step = step

    def draw(self, graphic_buffer):
        graphic_buffer[self.y][self.x] = '|'

    def make_step(self, context):
        if self.y == 0:
            context.shoots.remove(self)
        self.y -= self.step
        for monster in context.monsters:
            if (self.y, self.x) == (monster.y, monster.x):
                if self not in context.dead_list:
                    context.dead_list.append(self)
                if monster not in context.dead_list:
                    context.dead_list.append(monster)
                    shoot.add_score(context.user, monster.POINTS_FOR_DEAD)
                break
        for boss in context.bosses:
            if (self.y, self.x) == (boss.y, boss.x):
                boss.life -= 1
                if self not in context.dead_list:
                    context.dead_list.append(self)
                if boss.life == 0 and boss not in context.dead_list:
                    context.dead_list.append(boss)
                    shoot.add_score(context.user, boss.POINTS_FOR_DEAD)
                break

    def add_score(self, user, points):
        user.points += points


class Context:

    def __init__(self, board, user, monsters, bosses, shoots, game_level, dead_list):
        self.board = board
        self.user = user
        self.monsters = monsters
        self.bosses = bosses
        self.shoots = shoots
        self.game_level = game_level
        self.dead_list = dead_list


def draw_scene(context, graphic_buffer):
    context.board.draw(graphic_buffer)
    context.user.draw(graphic_buffer)
    for shoot in context.shoots:
        shoot.draw(graphic_buffer)
    for monster in context.monsters:
        monster.draw(graphic_buffer)
    for boss in context.bosses:
        boss.draw(graphic_buffer)
    if game_over:
        letters = list('GAME OVER')
        offset = int((len(graphic_buffer[0]) - len(letters)) / 2)
        for x in range(0, len(letters)):
            graphic_buffer[int(len(graphic_buffer) / 2)][x + offset] = letters[x]
    for row in graphic_buffer:
        print(' '.join(row))
    print('level: {}, points: {}'.format(context.game_level, context.user.points))


graphic_buffer = [['' for _ in range(0, 13)] for _ in range(0, 17)]
board = Board()
context = Context(
    board=board,
    user=User(15, 6, 1),
    monsters=[Monster(board, 1)],
    bosses=[],
    shoots=[],
    game_level=1,
    dead_list=[]
)
while True:
    game_over = False
    draw_scene(context, graphic_buffer)
    old_game_level = context.game_level
    context.game_level = int(context.user.points / 20)
    context.game_level += 1
    if context.game_level != old_game_level:
        context.bosses.append(Boss(context.board, 1, 4))
    context.user.make_step(context)
    try:
        for monster in context.monsters:
            monster.make_step(context)
        if not context.bosses:
            if randint(0, 5) == 1:
                for index in range(context.game_level):
                    context.monsters.append(Monster(board, 1))
        for boss in context.bosses:
            boss.make_step(context)
        for shoot in context.shoots:
            shoot.make_step(context)
        for element in context.dead_list:
            if isinstance(element, Monster):
                context.monsters.remove(element)
            if isinstance(element, Shoot):
                context.shoots.remove(element)
            if isinstance(element, Boss):
                context.bosses.remove(element)
        context.dead_list = []
    except GameOverError as error:
        game_over = True
        draw_scene(context, graphic_buffer)
        break
