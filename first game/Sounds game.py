# Original Code by: Isaiah Runkles
# Changes made by Shane M.D.
# February 2nd, 2022
# Game7 - sound and damage
# sounds now amit from a bomb exploding, collecting a power up, gaining a life and losing a life!
# SIDE NOTES - None! still working on some new updates as of right now!

# Import the pygame module
import pygame, time, sys

# Imports used to code the game
from pygame.locals import *
import random as rd
from pygameSupport import import_folder
import GameLogon as Gl
import sqlite3
from sqlite3 import Error

################################################################
#
# All The classes
#
################################################################

class Player(pygame.sprite.Sprite):
    moveCount = 0
    isMoving = False
    speed = 14
    Level = 1

    def setMoving(self, value):
        self.isMoving = value

    def increaseSpeed(self, increase):
        self.speed += increase

    def __init__(self):
        super(Player, self).__init__()
        self.animation = import_folder('./imgs/heart_idol')
        self.image = pygame.image.load("./imgs/heart.png").convert_alpha()
        self.surf = pygame.transform.scale(self.image,(51,45)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(center=((SCREEN_WIDTH / 2),(SCREEN_HEIGHT - 25)))
# Move the sprite based on speed
    def update(self, pressed_keys):
        playerIdol = ["./imgs/heart.png"]
        if self.moveCount > len(playerIdol) - 1:
            self.moveCount = 0
        self.surf = pygame.transform.scale(self.image,(51,45)).convert_alpha()
        self.moveCount += 1

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

    # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Arrows(pygame.sprite.Sprite):
    isDying = False
    def __init__(self):
        super(Arrows,self).__init__()
        self.dieCount = 2
        self.explode_frame = 0
        self.neg = False
        self.explode = import_folder('./imgs/arrow')
        self.image = pygame.image.load('./imgs/Arrow.png').convert_alpha()
        self.surf = pygame.transform.scale(self.image,(70,100)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(center=(rd.randint(5,SCREEN_WIDTH -10),rd.randint(1,10)))
        self.speed = rd.randint(4,10)
        self.etype = "Cupid"

    def update(self):
        if not self.isDying:
            self.rect.move_ip(0,5)
            if self.rect.top >=SCREEN_HEIGHT:
                self.kill()

            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
        else:
            if self.dieCount == 0:
                if self.explode_frame > len(self.explode) - 1:
                    # explosion sound
                    self.kill()
                else:
                    self.surf = pygame.transform.scale(self.explode[self.explode_frame],(70,100)).convert_alpha()
                    self.explode_frame += 1
            else:
                self.rect.move_ip(0,0)
                self.dieCount -= 1

class Power(pygame.sprite.Sprite):
    Rotating = True
    def __init__(self):
        super(Power,self).__init__()
        self.power = 2
        self.rotate_frame = 0
        self.surf = pygame.image.load('./imgs/powerup.png')
        self.Rotate = import_folder("./imgs/power up")
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(center=(rd.randint(5,SCREEN_WIDTH -10),rd.randint(1,10)))
        self.speed = rd.randint(4,10)
        self.etype = "power-up"

    def update(self):
        if self.Rotating:
            self.rect.move_ip(0,5)
            if self.rect.top >=SCREEN_HEIGHT:
                self.kill()

            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.power == 0:
                if self.rotate_frame > len(self.Rotate) - 1:
                    self.rotate_frame = 0
                else:
                    self.surf = self.Rotate[self.rotate_frame]
                    self.rotate_frame += 2
            else:
                self.rect.move_ip(0,0)
                self.power -= 1

class Bomb(pygame.sprite.Sprite):
    def __init__(self):
        super(Bomb,self).__init__()
        self.item = rd.choice(['Bomb'])
        self.molAngle = 10
        self.angle = 45
        self.angle = 0
        self.etype = ''
        if self.item == 'Bomb':
            self.etype = 'Bomb'

        if self.etype == 'Bomb':
            self.surf = pygame.image.load('./imgs/bomb.png').convert_alpha()
        self.rect = self.surf.get_rect(
            center=(player.rect.left + 20, player.rect.bottom - 80),
        )
        if self.etype == 'Bomb':
            self.speed = 5

    def update(self):
        Bomb_image = './imgs/bomb.png'
        self.angle += 0
        self.molAngle += 10
        self.angle %= 360
        if self.etype == 'Bomb':
            self.surf = pygame.transform.rotate(pygame.image.load(Bomb_image).convert_alpha(),self.molAngle)
        if self.rect.bottom <= 0:
            self.kill()
        else:
            self.rect.move_ip(0,-self.speed)

################################################################
#
# Functions, and all the Database stuff
#
################################################################

# Functions used to help assist adding to the DB
def getDbConnection():
    conn = None
    try:
        conn = sqlite3.connect("./GameStats.db")
    except Error as e:
        print(e)
    return conn

def saveGameStats(Player,highScore,Stage,Kills):
    conn = getDbConnection()
    curr = conn.cursor()
    updateSql = "UPDATE Stats set High_Score = ?, Level = ?, Enemies_Killed = ? WHERE Player_ID = ?"
    record = (highScore, Stage, Kills, Player)
    curr.execute(updateSql,record)
    conn.commit()
    conn.close()


################################################################
#
# The Game Loop
#
################################################################

def Game():
    global Score,highScore,lifeback,Kills,explosions,Stage,Ammo,Lives,D_Health,\
        ScoreLabel,ScoreValue,HighScoreValue,HighScoreValue,LivesLabel,LivesValue,\
        AmmoLabel,AmmoValue,LifeUP

    Player_ID = Gl.GameLogon()

    con = getDbConnection()
    curr = con.cursor()

    # Adds updated information into the DB
    rows = curr.execute("SELECT * FROM Stats WHERE Player_ID = ?",(Player_ID,)).fetchall()
    if len(rows) == 0:
        record = (Player_ID,0,0,0)
        sql = "INSERT INTO Stats (PLayer_ID,High_Score,Level,Enemies_Killed) values(?,?,?,?)"
        curr.execute(sql,record)
        con.commit()
    else:
        for row in rows:
            highScore = row[1]

    running = True
    Background.play()
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_LEFT or event.key == K_RIGHT:
                    player.setMoving(True)
                if event.key == K_UP:
                    if Ammo >= 1:
                        weapon = Bomb()
                        bomb_sprites.add(weapon)
                        all_sprites.add(weapon)
                        Ammo -= 1
                    elif Ammo < 0:
                        Ammo = 0
                        if event.key == K_UP:
                            pass
                if event.type == KEYUP:
                    if event.key == K_LEFT or event.key == K_RIGHT:
                        player.setMoving(False)

        # Arrows fall
            if event.type == ADDARROW:
                newArrow = Arrows()
                arrow_sprites.add(newArrow)
                all_sprites.add(newArrow)

        # Power up fall
            if event.type == ADDPOWER:
                powerup = Power()
                power_sprites.add(powerup)
                all_sprites.add(powerup)

            elif event.type == QUIT:
                saveGameStats(Player_ID, highScore, Stage, Kills)
                running = False

    # Makes Sure the score and highscore are the same
        if Score > highScore:
            highScore = Score
            HighScoreValue = myFont.render(str(highScore),1,BLACK)

        if lifeback >= 500:
            Lives += 1
            Life.play()
            lifeback = 0
            screen.blit(LifeUP,(100, 250))

    # These are the collisions
        for entity in bomb_sprites:
            cupid = pygame.sprite.spritecollideany(entity,arrow_sprites)
            if cupid != None:
                cupid.isDying = True
                entity.kill()
                Explosion.play()
                Score += 15
                lifeback += 15
                Kills += 1
                explosions += 1
                if explosions > 10:
                    Stage += 1
                    explosions = 0

        # Finds the Rect collision between Player and Arrow
        if pygame.sprite.spritecollide(PlayerVar.sprite,arrow_sprites,False):
            # Finds the Mask Collision(Pixel Perfect) between Player and Arrow
            if pygame.sprite.spritecollide(PlayerVar.sprite,arrow_sprites,True, pygame.sprite.collide_mask):
                Damage.play()
                Lives -= 1
                if Lives == 0:
                    time.sleep(0.2)
                    saveGameStats(Player_ID, highScore, Stage, Kills)
                    running = False
            else:
                pass

        if pygame.sprite.spritecollide(PlayerVar.sprite,power_sprites,False):
            if pygame.sprite.spritecollide(PlayerVar.sprite,power_sprites,True,pygame.sprite.collide_mask):
                Upgrade.play()
                Ammo += 10
                Score += 20
                lifeback += 20
            else:
                pass

        # Updating Sprites
        screen.fill((150, 150, 150))

        pressed_keys = pygame.key.get_pressed()
        PlayerVar.update(pressed_keys)
        arrow_sprites.update()
        bomb_sprites.update()
        power_sprites.update()

        if Score > highScore:
            highScore = Score
            HighScoreValue = myFont.render(str(highScore),1,BLACK)
        AmmoValue = myFont.render(str(Ammo), 1, BLACK)
        ScoreValue = myFont.render(str(Score), 1, BLACK)
        LivesValue = myFont.render(str(Lives), 1, BLACK)
        HighScoreValue = myFont.render(str(highScore),1,BLACK)
        screen.blit(ScoreLabel, (SCREEN_WIDTH - 130, 2))
        screen.blit(ScoreValue, (SCREEN_WIDTH - 45, 2))
        screen.blit(HighScoreLabel, (SCREEN_WIDTH - 690, 2))
        screen.blit(HighScoreValue, (SCREEN_WIDTH - 555, 2))
        screen.blit(AmmoLabel, (SCREEN_WIDTH - 690, 25))
        screen.blit(AmmoValue, (SCREEN_WIDTH - 600, 25))
        screen.blit(LivesLabel, (SCREEN_WIDTH - 690, 48))
        screen.blit(LivesValue, (SCREEN_WIDTH - 615, 48))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        pygame.display.flip()
        clock.tick(60)

################################################################
#
# These are all Set up variables to be used later
#
################################################################

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Setup variables
clock = pygame.time.Clock()
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
BLACK = (0,0,0)
Score = 0
highScore = 0
lifeback = 0
Kills = 0
explosions = 0
Stage = 1
Ammo = 15
Lives = 3
D_Health = 1000

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pew pew")

# Sets up the text, however does not import them into game
myFont = pygame.font.SysFont("Comicsans", 25)
sFont = pygame.font.SysFont('ComicSans',120)
ScoreLabel = myFont.render('Score:',1,BLACK)
ScoreValue = myFont.render(str(Score),1,BLACK)
HighScoreLabel = myFont.render('HighScore:',1,BLACK)
HighScoreValue = myFont.render(str(highScore),1,BLACK)
AmmoLabel = myFont.render("Bombs:",1,BLACK)
AmmoValue = myFont.render(str(Ammo),1,BLACK)
LivesLabel = myFont.render("Lives:",1,BLACK)
LivesValue = myFont.render(str(Lives),1,BLACK)
LifeUP = sFont.render('Life UP!!!',1,BLACK)

# Sets up time for when objects appear & fall
ADDARROW = pygame.USEREVENT + 1
pygame.time.set_timer(ADDARROW,1000)
ADDPOWER = pygame.USEREVENT + 2
pygame.time.set_timer(ADDPOWER,int(rd.uniform(7000,10000)))

# Instantiate player
player = Player()

# Create groups to hold enemy sprites and all sprites
all_sprites = pygame.sprite.Group()
arrow_sprites = pygame.sprite.Group()
bomb_sprites = pygame.sprite.Group()
power_sprites = pygame.sprite.Group()
PlayerVar = pygame.sprite.GroupSingle()
# Add sprites to those groups
all_sprites.add(player)
PlayerVar.add(player)

# These are the sounds
Background = pygame.mixer.Sound('./sounds/Background.wav')
Explosion = pygame.mixer.Sound("./sounds/Explosion.wav")
Upgrade = pygame.mixer.Sound("./sounds/Upgrade.wav")
Damage = pygame.mixer.Sound("./sounds/Damage.wav")
Life = pygame.mixer.Sound("./sounds/newlife.wav")

# Sets the volume of the sounds
Explosion.set_volume(0.5)
Upgrade.set_volume(0.5)
Damage.set_volume(0.5)
Life.set_volume(1.0)
Background.set_volume(0.2)

# Runs the game loop
Game()
