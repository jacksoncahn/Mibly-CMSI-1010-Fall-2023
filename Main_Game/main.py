# Welcome to Mibly!
import pygame, sys
from button import Button
import pygame.rect as rect
import pygame.display as Display
import pygame.draw as Draw
import pygame.font as font
import random
from random import choice

clock = pygame.time.Clock()
pygame.init()

CHANGE_DIRECTION = pygame.USEREVENT + 1
SCREEN = pygame.display.set_mode((1000,662))

# Sets window title and icon.
pygame.display.set_caption("Mibly")
pygame.display.set_icon(pygame.image.load("Mibly/assets/Pictures/ship.png"))

# Sets a timer that is used to change the direction of the ships.
pygame.time.set_timer(CHANGE_DIRECTION, 2500)

# Variable that will be used to help the enemy ships know when to fire.
ENEMY_FIRE = pygame.USEREVENT + 2

# Global variable that is defined as the interval for how often the enemies shoot.
global enemy_shoot_interval
enemy_shoot_interval = 1000
pygame.time.set_timer(ENEMY_FIRE, enemy_shoot_interval)

global playGame
playGame = True

screen_rect = SCREEN.get_rect()

scoreFont = pygame.font.Font("Mibly/assets/font.ttf", 28)
scoreText = scoreFont

def loadImg(imgname):
    return pygame.image.load(imgname).convert_alpha()

# Backgrounds of each menu and screen.
BG = loadImg("Mibly/assets/Pictures/Title screen.png")
PBG = loadImg("Mibly/assets/Pictures/PAUSE_GAME.png")
GOBG = loadImg("Mibly/assets/Pictures/GameoverBg.png")

# Gets the height and width of the screen used later for ships and boundaries.
HEIGHT = SCREEN.get_height()
WIDTH = SCREEN.get_width()
screen_width = 1500
screen_height = 662

Player_Ship_Size = 20

text_size = 50
text = font.Font(None, text_size)

# Audio variables for sound effects.
laserSound = pygame.mixer.Sound("Mibly/assets/Sounds/laser.wav")
enemyDeath = pygame.mixer.Sound("Mibly/assets/Sounds/enemyDeath.wav")

# Separates the background and music sound effects.
background_music_channel = pygame.mixer.Channel(0)
sound_effects_channel = pygame.mixer.Channel(1)


# Defines the enemy ship within an object.
class Enemy_Ship(pygame.sprite.Sprite):
    def __init__(self, ship_picture, x, y):
        super().__init__()
        self.image = loadImg(ship_picture)
        self.reset_speed = 1
        self.speed = 0.7
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.alive = True
        self.direction = random.randint(1, 4)
        self.score = 0

# Resets the speed of the ship and chooses a direction variable.
    def change_direction(self):
        self.speed == self.reset_speed
        self.direction = random.randint(1, 4)
        return self.direction

# Moves the enemy ships in a certain direction.
    def move_down(self):
        self.y += self.speed
        self.rect.center = (self.x, self.y)

    def move_up(self):
        self.y -= self.speed
        self.rect.center = (self.x, self.y)

    def move_right(self):
        self.x += self.speed
        self.rect.center = (self.x, self.y)

    def move_left(self):
        self.x -= self.speed
        self.rect.center = (self.x, self.y)

# Determines which way the enemy ship will go.
    def move(self, direction):
        if direction == 1:
            self.move_down()
        if direction == 2:
            self.move_up()
        if direction == 3:
            self.move_right()
        if direction == 4:
            self.move_left()

# Keeps the enemy ships within the game window.
    def border_check(self):
        if self.x > 1000 or self.x < 0 or self.y > 400 or self.y < 0:
            self.speed = -self.speed
        else:
            pass

    def is_hit(self, player_beam):
        if pygame.Rect.colliderect(self.rect, player_beam.rect):
            self.alive = False
            return True
        return False

# Defines the enemy beam within an object.
class Enemy_Beam(pygame.sprite.Sprite):
    def __init__(self, beam_image, x, y, ship_x, ship_y):
        super().__init__()
        self.image = loadImg(beam_image)
        self.image = pygame.transform.scale(self.image, (15, 40))
        self.rect = self.image.get_rect()
        self.rect.x = ship_x + 30
        self.rect.y = ship_y
        self.speed = 1.5
        self.fired = False

    def move_down(self):
        self.rect.y += self.speed

# Updates the beam and checks for movement and if it touches the player. 
    def update(self):
        if self.fired:
            self.move_down()
            if player_ship.alive and player_ship.is_hit(self):
                player_ship.alive = False
                self.kill()
            if self.rect.y >= (HEIGHT+200):
                self.kill()

# Defines the explosion animation, plays when player beam touches an enemy.
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.explosion = []
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame1.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame1.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame2.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame2.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame3.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame3.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame4.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame4.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame5.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame5.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame6.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame6.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame7.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame7.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame8.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame8.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame9.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame9.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame10.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame10.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame11.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame11.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame12.png"))
        self.explosion.append(pygame.image.load("Mibly/assets/Explosion/explosion_frame12.png"))

        self.frame = 0
        self.image = self.explosion[self.frame]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = [self.x, self.y]

    def animate(self, sprite_group):
        self.frame += 1
        if self.frame >= len(self.explosion):
            sprite_group.remove(self)
            self.frame = 0
        self.image = self.explosion[self.frame]


# Defines the player ship that the player will control.
class Player_Ship(pygame.sprite.Sprite):
    def __init__(self, ship_picture, x, y):
        super().__init__()
        self.image = loadImg(ship_picture)
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.radius = Player_Ship_Size
        self.speed = 0
        self.alive = True
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move_right(self):
        if self.rect.x < 1000:
            self.rect.x += 8

    def move_left(self):
        if self.rect.x > 0:
            self.rect.x -= 8

# Keeps the player within the bounds of the screen.
    def out_of_bounds(self, surface_rect):
        self.rect.clamp_ip(surface_rect)

    def is_hit(self, Enemy_Beam):
        if pygame.Rect.colliderect(self.rect, Enemy_Beam.rect) == True:
            self.alive = False


# Defines the player beam as an object that will be shot by the player.
class Player_Beam(pygame.sprite.Sprite):
    def __init__(self, player_ship, x, y):
        super().__init__()
        self.image = loadImg("Mibly/assets/Pictures/laser.png")
        self.image = pygame.transform.scale(self.image, (15, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.fired = False
        self.score = 0
        self.touchingBound = False
        self.speed = 5

    def reset_position(self, player_ship):
        self.rect.x = player_ship.rect.x + 22.5

    def move_up(self):
        self.rect.y -= self.speed

# Updates the beam and checks for movement and if it touches an enemy. 
    def update(self):
        if self.fired:
            self.move_up()
            enemy_hit = False
            for enemy in enemy_sprite_group:
                if enemy.is_hit(self):
                    enemy_hit = True
                    pygame.mixer.Sound.play(enemyDeath)
                    self.score += 1
                    break

            if enemy_hit:
                self.reset_position(player_ship)
                enemy.alive = False
                self.rect.y = 660
                self.fired = False

            if self.rect.y < -200:
                self.reset_position(player_ship)
                self.rect.y = 660
                self.fired = False
   
            
def group_count(enemy_sprite_group):
    return len(enemy_sprite_group)

# Puts the sprites in a group so they can be removed.
enemy_sprite_group = pygame.sprite.Group()
explosion_sprite_group = pygame.sprite.Group()

# Defines the function startup that gives each variable a global variable that will add every sprite onto the screen.
def startup():
    global player_ship
    player_ship = Player_Ship("Mibly/assets/Pictures/ship.png", 470, 640)
    global playerBeam
    playerBeam = Player_Beam(player_ship, 570, 660)
    global player_beam_group
    player_beam_group = pygame.sprite.Group(playerBeam)
    global enemy_beam_group
    enemy_beam_group = pygame.sprite.Group()
    global player_ship_group
    player_ship_group = pygame.sprite.Group()
    player_ship_group.add(player_ship)
    player_beam_group.add(playerBeam)

    if group_count(enemy_sprite_group) <= 20:
        for _ in range(20):
            enemy_sprite_group.add(Enemy_Ship("Mibly/assets/Pictures/EnemyShip.png", random.randrange(1000), random.randrange(400)))

    global last_enemy_shot_time
    last_enemy_shot_time = pygame.time.get_ticks()

def get_font(size):
    return pygame.font.Font("Mibly/assets/font.ttf", size)

# Loads background music.
pygame.mixer.music.load('Mibly/assets/Sounds/bgMusic.wav')

# Function that plays the background music when called as true, paused while false.
def backgroundMusicPlay(play=False):
    if play:
        pygame.mixer.music.unpause()
        pygame.mixer.music.load('Mibly/assets/Sounds/bgMusic.wav')
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.pause()

# Function that plays the menu music when called as true, paused while false.
def menuMusicPlay(play=False):
    if play:
        pygame.mixer.music.load('Mibly/assets/Sounds/menuMusic.wav')
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.pause()

# Function that plays the game over music when called.
def gameOverMusicPlay(play=False):
    if play:
        pygame.mixer.music.load('Mibly/assets/Sounds/gameOver.wav')
        pygame.mixer.music.set_volume(3)
        pygame.mixer.music.play()

global gameState
gameState = 0

global paused
paused = False
event = None

# Main function that plays the game.
def play():
    startup()
    
    global gameState
    global paused

    menuMusicPlay(False)
    backgroundMusicPlay(True)

    while gameState == 1:    
        enemy_shoot_interval = 1000
        maxScore = 10

        while gameState == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == CHANGE_DIRECTION:
                    for enemy in enemy_sprite_group:
                        enemy.change_direction()
# If pause button is clicked, everything freezes
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if MENU_BUTTON.checkForInput(GAME_MENU_MOUSE_POS):
                        paused = not paused

                if event.type == ENEMY_FIRE:
                    if group_count(enemy_sprite_group) <= 20:
                        enemy_sprite_group.add(
                            Enemy_Ship("Mibly/assets/Pictures/EnemyShip.png", random.randrange(1000),
                                       random.randrange(200)))
                    random_enemy = choice(list(enemy_sprite_group))
                    new_enemy_beam = Enemy_Beam("Mibly/assets/Pictures/enemyLaser.png", random_enemy.x, random_enemy.y,
                                                random_enemy.rect.x, random_enemy.rect.y)
                    new_enemy_beam.speed += 0.6 * (playerBeam.score // 10)
                    new_enemy_beam.fired = True
                    enemy_beam_group.add(new_enemy_beam)

# As the score increases, the speed and frequency of the enemy beams increases.
                if playerBeam.score >= maxScore:
                    maxScore += 10
                    if enemy_shoot_interval > 1:
                        enemy_shoot_interval = int(enemy_shoot_interval//1.25)
                    playerBeam.speed += 0.22
                    for beam in enemy_beam_group:
                        beam.speed += 0.6
                    pygame.time.set_timer(ENEMY_FIRE, enemy_shoot_interval)
                    
# Allows game objects to be drawn and move/function while game is not paused.
            if not paused:
                enemy_sprite_group.draw(SCREEN)
                player_ship_group.draw(SCREEN)
                explosion_sprite_group.draw(SCREEN)

                playerBeam.update()

                for enemy in enemy_sprite_group:
                    enemy.move(enemy.direction)
                    enemy.border_check()
                    if not enemy.alive:
                        enemy_sprite_group.remove(enemy)
                        explosion_sprite_group.add(Explosion(enemy.x, enemy.y))

                for explosion in explosion_sprite_group:
                    explosion.animate(explosion_sprite_group)

                score_text = scoreText.render("Score:" + str(playerBeam.score), True, "white")
                textRect = score_text.get_rect()

                offset_x = 10 
                offset_y = 10

                textRect.topleft = (offset_x, offset_y)

                GAME_MENU_MOUSE_POS = pygame.mouse.get_pos()

                MENU_BUTTON = Button(image=pygame.image.load("Mibly/assets/Pictures/PauseMenu.png"), pos=(960, 45),
                                    text_input="", font=get_font(23),
                                    base_color="White", hovering_color="White")

                SCREEN.fill((0, 0, 0))
                SCREEN.blit(BG, (0, 0))

                enemy_sprite_group.draw(SCREEN)
                explosion_sprite_group.draw(SCREEN)

                for beam in enemy_beam_group:
                    beam.update()

                enemy_beam_group.draw(SCREEN) 

                keystrokes = pygame.key.get_pressed()

                player_beam_group.draw(SCREEN)
                player_ship_group.draw(SCREEN)

# When the player "dies", the game state is changed to the game over screen.
                if player_ship.alive == True:
                    player_beam_group.draw(SCREEN)
                else:
                    gameState = 3
                
                SCREEN.blit(score_text, textRect)

                if keystrokes[pygame.K_LEFT]:
                    player_ship.move_left()

                if playerBeam.fired == False:
                    playerBeam.reset_position(player_ship)

                if keystrokes[pygame.K_RIGHT]:
                    player_ship.move_right()

                if keystrokes[pygame.K_SPACE] and not playerBeam.fired:
                    playerBeam.fired = True
                    pygame.mixer.Sound.play(laserSound)
                    playerBeam.reset_position(player_ship)

                for button in [MENU_BUTTON]:
                    button.changeColor(GAME_MENU_MOUSE_POS)
                    button.update(SCREEN)

                player_ship.out_of_bounds(screen_rect)
                player_beam_group.update()

            clock.tick(60)

            pygame.display.flip()
            pygame.display.update()

    game_over_menu()



# Main menu function at the start of the program.
def main_menu():

    backgroundMusicPlay(False)
    menuMusicPlay(True)
    
    global gameState
    while gameState == 0:

        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("MIBLY!!!", True, "#33c3cc")
        MENU_RECT = MENU_TEXT.get_rect(center=(520, 100))
        
        MENU_SPLASH = pygame.image.load("Mibly/assets/Pictures/MainMenuSplash.png").convert_alpha()
        SPLASH_POS = (342, 135)
        SCREEN.blit(MENU_SPLASH, SPLASH_POS)
        
        PLAY_BUTTON = Button(image=None, pos=(500, 470),
                            text_input="PLAY", font=get_font(35), base_color="#33c3cc", hovering_color="White")
        
        
        QUIT_BUTTON = Button(image=None, pos=(500, 585),
                            text_input="QUIT", font=get_font(35), base_color="#33c3cc", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

# While the mouse hovers over the button, it changes to a different color.
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
# If the player clicks a button, then it will play that buttons' function.
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    gameState = 1
                    play()
                    
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Defines the pause menu.
def pause_menu():

    global gameState, paused
    backgroundMusicPlay(False)

# While the game state is in the pause state, everything is frozen.
    while gameState == 2:
        keystrokes = pygame.key.get_pressed()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# If the player either clicks the pause button or the rest of the screen, the game unpauses.
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                paused = not paused
                
# If the game is not paused, everything unfreezes and is drawn.
        if not paused:  
            enemy_sprite_group.draw(SCREEN)
            player_ship_group.draw(SCREEN)
            explosion_sprite_group.draw(SCREEN)

            playerBeam.update()

            playerBeam.update()

            for enemy in enemy_sprite_group:
                enemy.move(enemy.direction)
                enemy.border_check()
                if not enemy.alive:
                    enemy_sprite_group.remove(enemy)
                    explosion_sprite_group.add(Explosion(enemy.x, enemy.y))

            for explosion in explosion_sprite_group:
                explosion.animate(explosion_sprite_group)

            enemy_beam_group.draw(SCREEN)

            for beam in enemy_beam_group:
                beam.update()

            enemy_beam_group.draw(SCREEN)

            keystrokes = pygame.key.get_pressed()
            player_beam_group.draw(SCREEN)
            player_ship_group.draw(SCREEN)

            if player_ship.alive == True:
                player_beam_group.draw(SCREEN)
            else:
                gameState = 3
            score_text = scoreText.render("Score:" + str(playerBeam.score), True, "white")
            textRect = score_text.get_rect()
            SCREEN.blit(score_text, textRect)

            if keystrokes[pygame.K_LEFT]:
                player_ship.move_left()

            if playerBeam.fired == False:
                playerBeam.reset_position(player_ship)

            if keystrokes[pygame.K_RIGHT]:
                player_ship.move_right()

            if playerBeam.fired == False:
                playerBeam.reset_position(player_ship)

            if keystrokes[pygame.K_SPACE] and not playerBeam.fired:
                playerBeam.fired = True
                pygame.mixer.Sound.play(laserSound)
                playerBeam.reset_position(player_ship)

            player_ship.out_of_bounds(screen_rect)

            player_beam_group.update()

        pygame.display.update()

# Defines the game over screen.
def game_over_menu():

    backgroundMusicPlay(False)
    gameOverMusicPlay(True)

    global gameState
    while gameState == 3:

# If the player ship is not alive, the code will run.
        if player_ship.alive == False:
            
            GOVER_MOUSE_POS = pygame.mouse.get_pos()

            SCREEN.fill("white")

            

            GOVER_TEXT = get_font(45).render("Game Over", True, ('Red'))
            GOVER_RECT = GOVER_TEXT.get_rect(center=(500,150))

            SCREEN.blit(GOBG, (0,0))
            SCREEN.blit(GOVER_TEXT, GOVER_RECT)
            

            GOVER_BACK = Button(image=None, pos=(500,400), text_input = "BACK TO MAIN MENU", font=get_font(35), base_color=('Red'), hovering_color=(192,49,238))


            GOVER_BACK.changeColor(GOVER_MOUSE_POS)
            GOVER_BACK.update(SCREEN)
            
            GOVER_QUIT = Button(image =None, pos=(500, 300), text_input = "Quit the Game", font= get_font(35), base_color=('Red'), hovering_color =(192,49,238))
            GOVER_QUIT.changeColor(GOVER_MOUSE_POS)
            GOVER_QUIT.update(SCREEN)

            GOVER_TRAGAIN = Button(image=None, pos=(500,500), text_input = "TRY AGAIN?", font=get_font(35), base_color=('Red'), hovering_color=(192,49,238))
            GOVER_TRAGAIN.changeColor(GOVER_MOUSE_POS)
            GOVER_TRAGAIN.update(SCREEN)
            
            scoreFont = pygame.font.Font("Mibly/assets/font.ttf", 40)
            scoreText = scoreFont
            score_text = scoreText.render("Score:" + str(playerBeam.score), True, "white")
            textRect = score_text.get_rect()
            textRect.topleft = (375, 10)
            SCREEN.blit(score_text, textRect)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
# If the player clicks a button, then it will play that buttons' function.
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if GOVER_BACK.checkForInput(GOVER_MOUSE_POS):
                        gameState = 0
                        player_ship.alive = True
                        main_menu()

                    if GOVER_TRAGAIN.checkForInput(GOVER_MOUSE_POS):
                        gameState = 1
                        player_ship.alive = True
                        play()

                    if GOVER_QUIT.checkForInput(GOVER_MOUSE_POS):
                        pygame.quit()
                        sys.exit
            pygame.display.update()


    play()

main_menu()


