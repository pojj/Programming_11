import simplegui
import random
import math


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_v = 0
        self.y_v = 0
        self.hp = 40 - (10 * difficulty)  # 10 hard   20 med   30 easy
        self.acc = 1
        self.max_speed = 5
        self.jump = -10
        self.double_jump = False
        self.invincible = 0
        self.width = 20  # NOT width, half width VERY MISS LEADING
        self.height = 20  # NOT height, half height
        self.direction = "right"
        self.moving = False  # True do animation
        self.frame = 1  # used for animation
        self.image = player_image
        self.image_hurt = player_image_hurt
        self.img_width = player_image_width
        self.img_height = player_image_height

    def up(self):
        self.y_v = self.jump

    def left(self):
        self.direction = "left"
        self.moving = True
        if self.x_v > -self.max_speed:
            self.x_v -= self.acc
            if self.x_v < -self.max_speed:
                self.x_v = -self.max_speed

    def right(self):
        self.direction = "right"
        self.moving = True
        if self.x_v < self.max_speed:
            self.x_v += self.acc
            if self.x_v > self.max_speed:
                self.x_v = self.max_speed

    # update with collision check
    def update_x(self):
        # update x cord
        self.x += self.x_v

        # check collision and put player at correct location
        for shape in obstacles:
            if shape.on_screen():
                if self.collision(shape.x, shape.y, shape.width, shape.height):

                    # if on left of box
                    if self.x < shape.x:
                        self.x = shape.x - shape.width - self.width

                    # if on right of box
                    if self.x > shape.x:
                        self.x = shape.x + shape.width + self.width
                    self.x_v = 0
                    break

    # update with collision check
    def update_y(self):
        # update y cord
        self.y += self.y_v

        # check collision and put player at correct location
        for shape in obstacles:
            if shape.on_screen():
                if self.collision(shape.x, shape.y, shape.width, shape.height):

                    # if on top of box
                    if self.y < shape.y:
                        self.y = shape.y - shape.height - self.height

                    # if below box
                    if self.y > shape.y:
                        self.y = shape.y + shape.height + self.height
                    self.y_v = 0
                    break

    # return True if collision
    def collision(self, x, y, width, height):
        in_x = abs(self.x - x) < (self.width + width)
        in_y = abs(self.y - y) < (self.height + height)
        if in_x and in_y:
            return True
        return False

    # slow down if not pressing a or d
    def decelerate(self, on_floor):
        # slow faster if on floor
        if on_floor:
            slow = 0.5
        else:
            slow = 0.3

        if self.x_v >= slow:
            self.x_v -= slow
        elif self.x_v <= -slow:
            self.x_v += slow
        else:
            self.x_v = 0

    # take damage and knockback by unit
    def take_damage(self, unit):
        # return True if player got hit not invincible
        if not self.invincible:
            self.hp -= unit.dmg

            # knock back
            if self.x > unit.x:
                self.x_v = unit.kb + unit.x_v
            if self.x < unit.x:
                self.x_v = -unit.kb + unit.x_v
            self.y_v = -unit.kb / 2 + unit.y_v

            self.invincible = 50
            return True
        return False

    # if on floor reset double jump
    def floor(self):
        for shape in obstacles:
            in_x = abs(self.x - shape.x) < (self.width + shape.width)
            on_y = (shape.y - self.y) == (self.height + shape.height)
            if in_x and on_y:
                self.double_jump = True
                return True
        return False

    # draw/animate
    def draw(self, canvas):
        columns = 8
        rows = 3

        # tick clock for animation
        if self.frame >= 79:
            self.frame = 0
        self.frame += 1

        # find column based on frame
        column = self.frame // 10

        # find correct row for directions
        if self.direction == "left":
            # bottom row
            row = 2

        if self.direction == "right":
            # middle row
            row = 1

        # size of one sprite
        player_img_size = [self.img_width / columns, self.img_height / 3]

        # find center tile with column and row
        tile_center = [player_img_size[0] / 2 + column * player_img_size[0],
                       player_img_size[1] / 2 + row * player_img_size[1]]

        # if hurt/invincible
        if self.invincible:
            image = self.image_hurt  # red sprite

        else:
            image = self.image  # green sprite

        # if moving draw animation
        if self.moving:
            canvas.draw_image(image, tile_center, player_img_size, [self.x, self.y], (self.width * 3, self.height * 3))
            self.moving = False

        # if not moving draw not moving sprite
        else:
            if self.direction == "right":
                canvas.draw_image(image,
                                  # center of right facing square
                                  [self.img_width / columns / 2, self.img_height / rows / 2],
                                  player_img_size,
                                  [self.x, self.y],
                                  (self.width * 3, self.height * 3))

            if self.direction == "left":
                canvas.draw_image(image,
                                  # center of left facing square
                                  [self.img_width / columns + self.img_width / columns / 2, self.img_height / rows / 2],
                                  player_img_size,
                                  [self.x, self.y],
                                  (self.width * 3, self.height * 3))
        
        # draw arrow to show location if too high
        if play.y + play.height < 0:
            canvas.draw_polygon([(play.x, 20), (play.x + 20, 35), (play.x - 20, 35)], 1, "Green", "Green")
                                
        # draw hp
        canvas.draw_polygon([(10, 20), (10, 10), (10 + self.hp * 10, 10), (10 + self.hp * 10, 20)], 1, "Red", "Red")


class Enemy:
    def __init__(self, x, y, enemy_type):
        self.x = x
        self.y = y
        self.x_v = 0
        self.y_v = 0
        self.type = enemy_type
        self.direction = "left"

        # type specific attributes
        if self.type == 1:
            self.dmg = 1
            self.kb = 7  # knock back
            self.acc = 0.2
            self.max_speed = 2
            self.width = 30
            self.height = 30
            self.image = enemy1_image
            self.img_width = 89
            self.img_height = 130

        if self.type == 2:
            self.dmg = 1
            self.kb = 7
            self.acc = 0.1
            self.max_speed = 1
            self.bullet_speed = 5
            self.width = 15
            self.height = 20
            self.image = enemy2_image
            self.img_width = 46
            self.img_height = 130

        if self.type == 3:
            self.dmg = 2
            self.kb = 10
            self.acc = 0.4
            self.max_speed = 4
            self.jump = -10
            self.width = 30
            self.height = 30
            self.image = enemy3_image
            self.img_width = 87
            self.img_height = 150

        if self.type == 4:
            self.dmg = 2
            self.kb = 10
            self.acc = 0.3
            self.max_speed = 3
            self.bullet_speed = 7
            self.width = 15
            self.height = 20
            self.image = enemy4_image
            self.img_width = 50
            self.img_height = 121

        if self.type == 5:
            self.dmg = 2
            self.kb = 10
            self.acc = 0.2
            self.max_speed = 6
            self.width = 20
            self.height = 20
            self.image = enemy5_image
            self.img_width = 85
            self.img_height = 51

        if self.type == 6:
            self.dmg = 2
            self.kb = 10
            self.acc = 0.2
            self.max_speed = 4
            self.bullet_speed = 7
            self.width = 20
            self.height = 20
            self.image = enemy6_image
            self.img_width = 84
            self.img_height = 53

        if self.type == 7:
            self.dmg = 3
            self.kb = 10
            self.direction = 0  # radians for direction
            self.max_speed = 7
            self.width = 20
            self.height = 20
            self.image = enemy7_image
            self.img_width = 85
            self.img_height = 56

    def up(self):
        self.y_v = self.jump

    def left(self):
        self.direction = "left"
        if self.x_v > -self.max_speed:
            self.x_v -= self.acc

    def right(self):
        self.direction = "right"
        if self.x_v < self.max_speed:
            self.x_v += self.acc

    def float_up(self):
        if self.y_v > -self.max_speed:
            self.y_v -= self.acc

    def float_down(self):
        if self.y_v < self.max_speed:
            self.y_v += self.acc

    # update/collision
    def update_x(self):
        # update x cord
        self.x += self.x_v

        # check if collision put enemy on correct location
        for shape in obstacles:
            if shape.on_screen():
                if self.collision(shape.x, shape.y, shape.width, shape.height):

                    # if on left of box
                    if self.x < shape.x:
                        self.x = shape.x - shape.width - self.width

                    # if on right of box
                    if self.x > shape.x:
                        self.x = shape.x + shape.width + self.width
                    self.x_v = 0
                    break

    # update/collision
    def update_y(self):
        # update y cord
        self.y += self.y_v

        # check if collision put enemy on correct location
        for shape in obstacles:
            if shape.on_screen():
                if self.collision(shape.x, shape.y, shape.width, shape.height):

                    # if on top of box
                    if self.y < shape.y:
                        self.y = shape.y - shape.height - self.height

                    # if below box
                    if self.y > shape.y:
                        self.y = shape.y + shape.height + self.height
                    self.y_v = 0
                    break

    # if enemy is on screen return True
    def on_screen(self):
        if self.x - self.width <= WIDTH and self.x + self.width >= 0:
            return True
        return False

    # if collision return True
    def collision(self, x, y, width, height):
        in_x = abs(self.x - x) < (self.width + width)
        in_y = abs(self.y - y) < (self.height + height)
        if in_x and in_y:
            return True
        return False

    # if enemy is on floor return True
    def floor(self):
        for shape in obstacles:
            in_x = abs(self.x - shape.x) < (self.width + shape.width)
            on_y = (shape.y - self.y) == (self.height + shape.height)
            if in_x and on_y:
                return True
        return False

    # shoot at x, y cords
    def shoot(self, x, y):
        x_dif = x - self.x
        y_dif = y - self.y
        angle = math.atan2(y_dif, x_dif)
        bullet_x_v = self.bullet_speed * math.cos(angle)
        bullet_y_v = self.bullet_speed * math.sin(angle)
        bullets.append(Bullet(self.x, self.y, bullet_x_v, bullet_y_v, self.kb, self.dmg))

    # shoot self at player enemy.type == 7
    def shoot_fly(self):
        x_dif = play.x - self.x
        y_dif = play.y - self.y
        angle = math.atan2(y_dif, x_dif)
        x_v = self.max_speed * math.cos(angle)
        y_v = self.max_speed * math.sin(angle)
        self.x_v = x_v
        self.y_v = y_v
        self.direction = angle - math.pi

    # enemy specific ais

    # walk toward player
    def ai_1(self):
        self.y_v += GRAVITY
        if play.x > self.x:
            self.right()
        if play.x < self.x:
            self.left()

    # walk slow and shoot at player
    def ai_2(self):
        self.y_v += GRAVITY
        if play.x > self.x:
            self.right()
        if play.x < self.x:
            self.left()
        if random.randint(1, 100) == 1:
            self.shoot(play.x, play.y)

    # walk fast and jump
    def ai_3(self):
        self.y_v += GRAVITY
        if play.x > self.x:
            self.right()
        if play.x < self.x:
            self.left()
        if random.randint(1, 100) == 1 and play.y < self.y:
            if self.floor():
                self.up()

    # walk and shoot fast
    def ai_4(self):
        self.y_v += GRAVITY
        if play.x > self.x:
            self.right()
        if play.x < self.x:
            self.left()
        if random.randint(1, 50) == 1:
            self.shoot(play.x, play.y)

    # fly
    def ai_5(self):
        if play.x > self.x:
            self.right()
        if play.x < self.x:
            self.left()
        if play.y < self.y:
            self.float_up()
        if play.y > self.y:
            self.float_down()

    # fly and shoot
    def ai_6(self):
        if play.x > self.x:
            self.right()
        if play.x < self.x:
            self.left()
        if play.y < self.y:
            self.float_up()
        if play.y > self.y:
            self.float_down()
        if random.randint(1, 50) == 1:
            self.shoot(play.x, play.y)

    # rapidly change direction toward player
    def ai_7(self):
        if random.randint(1, 20) == 1:
            self.shoot_fly()

    def draw(self, canvas):
        # draw enemies that don't have rotation
        if self.type not in (5, 6, 7):
            if self.direction == "left":
                canvas.draw_image(self.image, [self.img_width / 2, self.img_height / 4],
                                  [self.img_width, self.img_height / 2], [self.x, self.y],
                                  (self.img_width, self.img_height / 2))

            if self.direction == "right":
                canvas.draw_image(self.image, [self.img_width / 2, self.img_height / 2 + self.img_height / 4],
                                  [self.img_width, self.img_height / 2], [self.x, self.y],
                                  (self.img_width, self.img_height / 2))

        # draw player facing enemies
        if self.type == 5 or self.type == 6:
            x_dif = self.x - play.x
            y_dif = self.y - play.y
            angle = math.atan2(y_dif, x_dif)
            canvas.draw_image(self.image, [self.img_width / 2, self.img_height / 2], [self.img_width, self.img_height],
                              [self.x, self.y], (self.img_width, self.img_height), angle)

        # draw enemies with radian direction value
        if self.type == 7:
            canvas.draw_image(self.image, [self.img_width / 2, self.img_height / 2], [self.img_width, self.img_height],
                              [self.x, self.y], (self.img_width, self.img_height), self.direction)


class Bullet:
    def __init__(self, x, y, x_v, y_v, knock_back, damage):
        self.x = x
        self.y = y
        self.x_v = x_v
        self.y_v = y_v
        self.dmg = damage
        self.kb = knock_back

    # update
    def update(self):
        self.x += self.x_v
        self.y += self.y_v

    # if bullet go off screen
    def out_of_bounds(self):
        if self.x < 0:
            return True
        if self.x > WIDTH:
            return True
        if self.y < 0:
            return True
        if self.y > HEIGHT:
            return True
        return False

    # if bullet hit wall
    def collision(self, x, y, width, height):
        in_x = abs(x - self.x) < width
        in_y = abs(y - self.y) < height
        if in_x and in_y:
            return True
        return False

    def draw(self, canvas):
        canvas.draw_circle((self.x, self.y), 5, 1, "Red", "Red")


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width  # NOT width is width / 2
        self.height = height  # NOT height is height / 2

    # if on screen
    def on_screen(self):
        if self.x - self.width <= WIDTH and self.x + self.width >= 0:
            return True
        return False

    def draw(self, canvas):
        canvas.draw_polygon([[self.x + self.width, self.y - self.height],
                             [self.x + self.width, self.y + self.height],
                             [self.x - self.width, self.y + self.height],
                             [self.x - self.width, self.y - self.height]], 1, "Black", "Black")


def draw_handler(canvas):
    global goal, game_state, timer

    # if menu open
    if game_state == "menu":
        menu(canvas)
        return
    
    # close death/win screen after timer
    if game_state in ("dead", "alive"):
        timer += 1
        if timer > 200:
            game_state = "menu"
            return
    else:
        timer = 0
            
    # if dead
    if game_state == "dead":
        menu_dead(canvas)
        return

    # if won level
    if game_state == "alive":
        menu_alive(canvas)
        return
        
    # if image fails to load then this will show
    canvas.draw_text("If you are seeing this the background image did not load", (230, 230), 20, "White")
    canvas.draw_text("Refresh the page until this message is gone when you open a level", (200, 260), 20, "White")

    # draw scrolling background
    draw_background(canvas)

    # add GRAVITY to player velocity
    play.y_v += GRAVITY

    # tick down invincibility
    if play.invincible:
        play.invincible -= 1

    # check if on floor
    if play.floor():
        # if on surface and not moving left or right slow down:
        if (simplegui.KEY_MAP['a'] not in current_keys) and (simplegui.KEY_MAP['d'] not in current_keys):
            play.decelerate(True)  # true on floor

        # if on surface and pressing "w" jump
        if simplegui.KEY_MAP['w'] in current_keys:
            play.up()
            current_keys.remove(simplegui.KEY_MAP['w'])

    # if in air
    else:
        # slow down; slower
        if (simplegui.KEY_MAP['a'] not in current_keys) and (simplegui.KEY_MAP['d'] not in current_keys):
            play.decelerate(False)  # false in air

        # if have double jump
        if simplegui.KEY_MAP['w'] in current_keys and play.double_jump:
            play.up()
            play.double_jump = False
            current_keys.remove(simplegui.KEY_MAP['w'])

    # if pressing "a" and not moving too fast move left
    if simplegui.KEY_MAP['a'] in current_keys:
        play.left()

    # if pressing "d" and not moving too fast move right
    if simplegui.KEY_MAP['d'] in current_keys:
        play.right()

    # if too fast slow down
    if play.x_v > 5 or play.x_v < -5:
        play.decelerate(False)

    # update x cord check if collision
    play.update_x()

    # update y cord check if collision
    play.update_y()

    # access each bullet
    for bullet in bullets:
        # update bullet location
        bullet.update()

        # if bullet out of bound remove it
        if bullet.out_of_bounds():
            bullets.remove(bullet)
            continue

        # if bullet hits an obstacle on screen remove it
        for shape in obstacles:
            if shape.on_screen():
                if bullet.collision(shape.x, shape.y, shape.width, shape.height):
                    bullets.remove(bullet)
                    break

        # draw bullet
        bullet.draw(canvas)

        # if bullet hit player do thing and remove bullet
        if bullet.collision(play.x, play.y, play.width, play.height):
            if play.take_damage(bullet):
                bullets.remove(bullet)

    # access each enemy
    for enemy in enemies:
        # if on screen
        if enemy.on_screen():
            # player enemy collision,
            if play.collision(enemy.x, enemy.y, enemy.width, enemy.height):
                play.take_damage(enemy)

            # enemy type specific
            if enemy.type == 1:
                enemy.ai_1()

            if enemy.type == 2:
                enemy.ai_2()

            if enemy.type == 3:
                enemy.ai_3()

            if enemy.type == 4:
                enemy.ai_4()

            if enemy.type == 5:
                enemy.ai_5()

            if enemy.type == 6:
                enemy.ai_6()

            if enemy.type == 7:
                enemy.ai_7()

            # update enemy x cord check if collision
            enemy.update_x()

            # update enemy y cord check if collision
            enemy.update_y()

            # draw enemy
            enemy.draw(canvas)

    # draw all shapes in obstacles only on screen shapes
    for shape in obstacles:
        if shape.on_screen():
            shape.draw(canvas)

    # draw char
    play.draw(canvas)

    # if no hp
    if play.hp <= 0:
        game_state = "dead"

    # if fall off 
    if play.y >= HEIGHT + 200:
        game_state = "dead"

    # screen scroll between wall die
    if play.x + play.width < 0:
        game_state = "dead"

    # if reach goal win level
    if play.x + play.width >= goal:
        game_state = "alive"

    # scroll everything including goal
    if goal > WIDTH:
        play.x -= SCROLL_SPEED

        for shape in obstacles:
            shape.x -= SCROLL_SPEED

        for enemy in enemies:
            enemy.x -= SCROLL_SPEED

        for bullet in bullets:
            bullet.x -= SCROLL_SPEED

        goal -= SCROLL_SPEED

    # if on left of screen
    if play.x < play.width:
        play.x = play.width
        play.x_v = SCROLL_SPEED

    # if on right of screen
    if play.x > WIDTH - play.width:
        play.x = WIDTH - play.width
        play.x_v = SCROLL_SPEED


# add pressed key to list
def keydown(key):
    current_keys.append(key)


# remove pressed key
def keyup(key):
    try:
        current_keys.remove(key)
    except ValueError:
        pass


# updates last clicked location
def mouse_handler(pos):
    global clicked
    clicked = pos


# draw background and scrolls it each time its run
def draw_background(canvas):
    canvas.draw_image(bkg_image, (bkg_width / 2, bkg_height / 2), (bkg_width, bkg_height), background_pos,
                      (WIDTH * 2, HEIGHT))
    if goal > WIDTH:
        background_pos[0] -= SCROLL_SPEED / 2
        background_pos[0] %= WIDTH


# menu when open game set difficulty
def menu(canvas):
    global difficulty, tick
    # draw text
    canvas.draw_text("Vydwo Gaims", (200, 100), 100, "Blue")
    canvas.draw_text("Instructions:", (50, 170), 50, "White")
    canvas.draw_text("-Pick difficulty", (100, 220), 30, "White")
    canvas.draw_text("-Pick level", (100, 260), 30, "White")
    canvas.draw_text("-Reach end", (100, 300), 30, "White")
    canvas.draw_text("-Don't die", (100, 340), 30, "White")
    canvas.draw_text("A/D - left/right", (50, 400), 30, "Orange")
    canvas.draw_text("W - jump/double jump", (50, 450), 30, "Orange")

    # this is me messing around with title screen
    if "tick" not in globals():
        tick = 0
    tick += 15
    tick %= 5000
    canvas.draw_image(fall_boi, (100 / 2, 130 / 2), (100, 130), (800, tick - 300), (300, 300), tick / 100)

    # difficulty buttons
    for i in range(3):
        canvas.draw_polygon([(350 + i * 100, 400), (420 + i * 100, 400), (420 + i * 100, 470), (350 + i * 100, 470)], 1,
                            "Green", "Green")

    # clicked location
    if 400 < clicked[1] < 470:
        if 350 < clicked[0] < 420:
            difficulty = 1
        if 450 < clicked[0] < 520:
            difficulty = 2
        if 550 < clicked[0] < 620:
            difficulty = 3

    # selected difficulty red square
    canvas.draw_polygon([(250 + difficulty * 100, 400),
                         (320 + difficulty * 100, 400),
                         (320 + difficulty * 100, 470),
                         (250 + difficulty * 100, 470)], 1, "Red", "Red")

    canvas.draw_text("Easy", (365, 440), 20, "White")
    canvas.draw_text("Medium", (451, 440), 20, "White")
    canvas.draw_text("Hard", (565, 440), 20, "White")


# if player dead
def menu_dead(canvas):
    canvas.draw_image(MENU_DEAD, (MENU_WIDTH / 2, MENU_HEIGHT / 2), (MENU_WIDTH, MENU_HEIGHT), (WIDTH / 2, HEIGHT / 2),
                      (WIDTH, HEIGHT))


# if player win level
def menu_alive(canvas):
    canvas.draw_image(MENU_ALIVE, (MENU_WIDTH / 2, MENU_HEIGHT / 2), (MENU_WIDTH, MENU_HEIGHT), (WIDTH / 2, HEIGHT / 2),
                      (WIDTH, HEIGHT))


# helper functions to start levels, by setting correct variables
def level1():
    global play, obstacles, enemies, bullets, goal, bkg_image, bkg_width, bkg_height, game_state
    play = Player(300, 380)
    obstacles = [Rectangle(x[0], x[1], x[2], x[3]) for x in map1]
    enemies = [Enemy(x[0], x[1], x[2]) for x in map1_enemies]
    bullets = []
    goal = 9900

    bkg_image = BKG1
    bkg_width = BKG1_WIDTH
    bkg_height = BKG1_HEIGHT
    game_state = "game"


def level2():
    global play, obstacles, enemies, bullets, goal, bkg_image, bkg_width, bkg_height, game_state
    play = Player(300, 380)
    obstacles = [Rectangle(x[0], x[1], x[2], x[3]) for x in map2]
    enemies = [Enemy(x[0], x[1], x[2]) for x in map2_enemies]
    bullets = []
    goal = 10500

    bkg_image = BKG2
    bkg_width = BKG2_WIDTH
    bkg_height = BKG2_HEIGHT
    game_state = "game"


def level3():
    global play, obstacles, enemies, bullets, goal, bkg_image, bkg_width, bkg_height, game_state
    play = Player(300, 380)
    obstacles = [Rectangle(x[0], x[1], x[2], x[3]) for x in map3]
    enemies = [Enemy(x[0], x[1], x[2]) for x in map3_enemies]
    bullets = []
    goal = 10000

    bkg_image = BKG3
    bkg_width = BKG3_WIDTH
    bkg_height = BKG3_HEIGHT
    game_state = "game"


def level4():
    global play, obstacles, enemies, bullets, goal, bkg_image, bkg_width, bkg_height, game_state
    play = Player(300, 380)
    obstacles = [Rectangle(x[0], x[1], x[2], x[3]) for x in map4]
    enemies = [Enemy(x[0], x[1], x[2]) for x in map4_enemies]
    bullets = []
    goal = 9000

    bkg_image = BKG4
    bkg_width = BKG4_WIDTH
    bkg_height = BKG4_HEIGHT
    game_state = "game"


def level5():
    global play, obstacles, enemies, bullets, goal, bkg_image, bkg_width, bkg_height, game_state
    play = Player(300, 380)
    obstacles = [Rectangle(x[0], x[1], x[2], x[3]) for x in map5]
    enemies = [Enemy(x[0], x[1], x[2]) for x in map5_enemies]
    bullets = []
    goal = 11000

    bkg_image = BKG5
    bkg_width = BKG5_WIDTH
    bkg_height = BKG5_HEIGHT
    game_state = "game"


# high def player for menu screen
fall_boi = simplegui.load_image("https://media.discordapp.net/attachments/728842796156452964/854936814497300485/thing.png")

# player sprites
player_image = simplegui.load_image("https://media.discordapp.net/attachments/728842796156452964/852414890189783100/player_sprite.png")
player_image_hurt = simplegui.load_image("https://media.discordapp.net/attachments/728842796156452964/852583348949483520/player_sprite_hurt.png")
player_image_width = 222
player_image_height = 84

# dead body/alive
MENU_DEAD = simplegui.load_image("https://media.discordapp.net/attachments/728842796156452964/854398211090939945/dead.png")
MENU_ALIVE = simplegui.load_image("https://media.discordapp.net/attachments/728842796156452964/854398651421294622/alive.png")
MENU_WIDTH = 1000
MENU_HEIGHT = 500

# enemy images
enemy1_image = simplegui.load_image("https://media.discordapp.net/attachments/728842796156452964/852601522242977832/enemy1.png")
enemy2_image = simplegui.load_image("https://media.discordapp.net/attachments/728842796156452964/852604833503510538/enemy2.png")
enemy3_image = simplegui.load_image("https://media.discordapp.net/attachments/728842796156452964/852595823853830159/enemy3.png")
enemy4_image = simplegui.load_image("https://media.discordapp.net/attachments/728842796156452964/852950308481007626/enemy4.png")
enemy5_image = simplegui.load_image("https://media.discordapp.net/attachments/728842796156452964/852414883080175656/enemy5.png")
enemy6_image = simplegui.load_image("https://media.discordapp.net/attachments/728842796156452964/852414886344785940/enemy6.png")
enemy7_image = simplegui.load_image("https://media.discordapp.net/attachments/728842796156452964/852947409385685042/enemy7.png")

# city scrape
BKG1 = simplegui.load_image("https://media.discordapp.net/attachments/728842796156452964/852414878773674024/background1.png")
BKG1_WIDTH = 1777
BKG1_HEIGHT = 481

# factory
BKG2 = simplegui.load_image("https://media.discordapp.net/attachments/728842796156452964/854051619061891152/background2.png")
BKG2_WIDTH = 1326
BKG2_HEIGHT = 260

# grass, tree, mountains
BKG3 = simplegui.load_image("https://media.discordapp.net/attachments/728842796156452964/854048500017659934/background3.png")
BKG3_WIDTH = 1040
BKG3_HEIGHT = 260

# cave
BKG4 = simplegui.load_image("https://media.discordapp.net/attachments/728842796156452964/854049595382300723/background4.png")
BKG4_WIDTH = 1570
BKG4_HEIGHT = 436

# purple forest
BKG5 = simplegui.load_image("https://media.discordapp.net/attachments/728842796156452964/854043759875325952/background5.png")
BKG5_WIDTH = 1040
BKG5_HEIGHT = 260

# frame dimensions
WIDTH = 1000
HEIGHT = 500

# menu/alive/dead
game_state = "menu"

# last clicked location, for menu screen currently on easy difficulty
clicked = (385, 435)

# gravity
GRAVITY = 0.4

# speed screen and bkg scroll
SCROLL_SPEED = 2

# location of bkg center changes when scrolling
background_pos = [0, HEIGHT / 2]

# current pressed keys
current_keys = []

# level design and enemies
map1 = [(800, 450, 800, 50), (1800, 400, 20, 20), (2000, 400, 20, 20), (2200, 400, 20, 20), (2400, 400, 20, 20),
        (3000, 450, 400, 50), (3500, 300, 10, 10), (3800, 490, 10, 10), (4300, 450, 300, 50), (5800, 450, 1000, 50),
        (5100, 300, 20, 20), (5700, 200, 500, 10), (6300, 300, 20, 20), (7000, 450, 50, 50), (7100, 350, 50, 50),
        (7200, 250, 50, 50), (7300, 150, 50, 50), (8200, 450, 500, 50), (9400, 450, 500, 50)]
map1_enemies = [(6200, 160, 1), (6100, 160, 1), (6000, 160, 1), (6200, 370, 1), (7300, 70, 1), (6300, 260, 2),
                (8500, 370, 1), (8450, 370, 1), (7100, 270, 1), (8600, 380, 2), (8300, 370, 3)]

map3 = [(500, 450, 500, 50), (1200, 350, 20, 20), (1400, 300, 20, 20), (1600, 250, 20, 20), (1800, 200, 20, 20),
        (2000, 150, 20, 20), (2200, 100, 20, 20), (3000, 400, 500, 100), (3450, 100, 50, 100), (3700, 400, 50, 100),
        (4000, 450, 100, 50), (4300, 450, 20, 20), (4450, 400, 20, 20), (4600, 350, 20, 20), (4750, 300, 20, 20),
        (4900, 250, 20, 20), (5050, 200, 20, 20), (5200, 150, 20, 20), (5350, 100, 20, 20), (6500, 450, 1000, 50),
        (8200, 450, 500, 50), (9500, 450, 500, 50)]
map3_enemies = [(2200, 60, 5), (3400, 270, 1), (3300, 270, 1), (3450, 270, 1), (3350, 100, 5), (4700, 20, 5),
                (4800, 20, 5), (7200, 370, 3), (7250, 380, 4), (7250, 20, 6), (7300, 370, 3), (7000, 380, 2),
                (6900, 370, 1), (8200, 0, 5), (8500, 0, 6), (8200, 370, 3)]

map2 = [(800, 450, 800, 50), (2200, 450, 400, 50), (2500, 350, 100, 50), (3100, 400, 350, 50), (3600, 150, 50, 150),
        (4000, 450, 450, 50), (4600, 350, 20, 20), (4750, 300, 20, 20), (4900, 250, 20, 20), (5050, 200, 20, 20),
        (5200, 150, 20, 20), (5350, 100, 20, 20), (6000, 450, 500, 50), (7200, 450, 500, 50), (8000, 500, 300, 200),
        (8200, 500, 100, 300), (9000, 450, 300, 50), (10000, 450, 500, 50)]
map2_enemies = [(2000, 370, 1), (2100, 370, 1), (2385, 380, 2), (3100, 270, 3), (3300, 270, 3), (4000, 380, 4),
                (4100, 380, 4), (5400, 80, 5), (5500, 0, 5), (6000, 370, 3), (6100, 380, 4), (6300, 380, 2),
                (6500, 380, 2), (8200, 170, 3), (8000, 270, 3), (8300, 180, 2), (8050, 280, 2), (9000, 380, 4)]

map4 = [(500, 450, 500, 50), (1200, 500, 50, 200), (1400, 500, 50, 300), (1600, 500, 50, 400), (2500, 0, 700, 250),
        (2500, 500, 700, 100), (3800, 450, 500, 50), (4500, 400, 20, 20), (4650, 400, 20, 20), (4800, 400, 20, 20),
        (4950, 400, 20, 20), (5100, 400, 20, 20), (5250, 400, 20, 20), (5400, 400, 20, 20), (5550, 400, 20, 20),
        (5700, 400, 20, 20), (5850, 400, 20, 20), (6000, 400, 20, 20), (7000, 450, 800, 50), (7000, 0, 800, 100),
        (8500, 450, 500, 50)]
map4_enemies = [(1600, 70, 3), (2200, 370, 1), (2400, 370, 1), (2600, 370, 1), (2800, 370, 1), (3000, 370, 1),
                (3185, 380, 2), (3700, 380, 4), (3800, 380, 4), (3900, 380, 4), (5700, 20, 6), (5500, 20, 7),
                (6400, 370, 1), (6700, 370, 1), (7000, 370, 1), (7300, 370, 1), (7600, 370, 1), (7000, 370, 3),
                (7500, 380, 4), (7800, 370, 3)]

map5 = [(2500, 450, 2500, 50), (5250, 450, 50, 50), (5500, 450, 50, 50), (5750, 450, 50, 50), (7000, 450, 1000, 50),
        (9000, 450, 500, 50), (1800, 100, 50, 150), (2800, 100, 50, 150), (10500, 450, 500, 50), (8250, 400, 50, 100),
        (10000, 0, 50, 200), (10000, 500, 50, 200), (6000, 0, 50, 200), (6000, 500, 50, 200)]
map5_enemies = [(1500, 0, 5), (2000, 0, 5), (2500, 0, 5), (3000, 0, 5), (3500, 0, 5), (4000, 0, 5), (1600, 370, 3),
                (2100, 370, 3), (2600, 370, 3), (3100, 370, 3), (3600, 370, 3), (4100, 370, 3), (5250, 0, 6),
                (5500, 0, 6), (5750, 0, 6), (6900, 100, 7), (7000, 100, 7), (7100, 100, 7), (6900, 380, 2),
                (7000, 380, 2), (7100, 380, 2), (9100, 370, 3), (9200, 370, 3), (9300, 370, 3), (9400, 370, 3),
                (9500, 370, 3), (9700, 100, 7)]

# Create a frame and start handlers
frame = simplegui.create_frame("Home", WIDTH, HEIGHT, 100)
frame.add_button("Level 1", level1)
frame.add_button("Level 2", level2)
frame.add_button("Level 3", level3)
frame.add_button("Level 4", level4)
frame.add_button("Level 5", level5)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(mouse_handler)
frame.set_draw_handler(draw_handler)
frame.start()
