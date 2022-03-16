# Isaiah Runkles
# February 14, 2022
# Game2
# This will be the second game I create. This is to help me better understand OOR and Pygame

import pygame, time
from pygame.locals import *
from pygameSupport import import_folder
import GameLogon as Gl
import sqlite3
from sqlite3 import Error
import random as rd

###################################
#
# All The Classes
#
###################################

class Ship(pygame.sprite.Sprite):
    frame = 0
    isMoving = False

    def setMoving(self, value):
        self.isMoving = value

    def __init__(self):
        super(Ship, self).__init__()
        self.Ship_choice = "./imgs/Ships/AX1.png", "./imgs/Ships/FX1.png", "./imgs/Ships/EX1.png"
        self.Ship = rd.choice(self.Ship_choice)
        self.surf = pygame.image.load(self.Ship).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(center=((SCREEN_WIDTH / 7),(SCREEN_HEIGHT - 200)))

    def update(self, pressed_keys):
        playerIdle = [self.Ship]
        if self.frame > len(playerIdle) - 1:
            self.frame = 0
        self.surf = pygame.image.load(playerIdle[self.frame]).convert_alpha()
        self.frame += 1
        global etype

        if self.Ship == "./imgs/Ships/AX1.png":
            self.speedLR = 7
            self.speedUD = 7
            etype = 'AX1'
        elif self.Ship == "./imgs/Ships/FX1.png":
            self.speedLR = 6
            self.speedUD = 6
            etype = 'FX1'
        elif self.Ship == "./imgs/Ships/EX1.png":
            self.speedLR = 5
            self.speedUD = 5
            etype = 'EX1'

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speedLR, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speedLR, 0)
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speedUD)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speedUD)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Asteroid(pygame.sprite.Sprite):
    Blowing_up = False
    def __init__(self):
        super(Asteroid,self).__init__()
        self.molAngle = 0
        self.boom = 2
        self.boom_frame = 0
        self.size = rd.uniform(40,80)
        self.animation = import_folder("./imgs/Asteroid_Boom")
        self.image = pygame.image.load('./imgs/Asteroid.png').convert_alpha()
        self.surf = pygame.transform.scale(self.image,(self.size,self.size)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(center=((SCREEN_WIDTH - 30),rd.randint(1,450)))
        self.speed = rd.randint(4,10)
        self.etype = "Asteroid"

    def update(self):
        if not self.Blowing_up:
            Asteroid_image = ('./imgs/Asteroid.png')
            self.rect.move_ip(-5,0)
            if self.rect.top >=SCREEN_HEIGHT:
                self.kill()
            self.molAngle += 5
            if self.etype == 'Asteroid':
                self.image = pygame.transform.rotate(pygame.image.load(Asteroid_image).convert_alpha(),self.molAngle)
                self.surf = pygame.transform.scale(self.image,(self.size,self.size)).convert_alpha()
        else:
            if self.boom == 0:
                if self.boom_frame > len(self.animation) - 1:
                    self.kill()
                else:
                    self.surf = pygame.transform.scale(self.animation[self.boom_frame],(self.size,self.size)).convert_alpha()
                    self.boom_frame += 1
            else:
                self.rect.move_ip(0,0)
                self.boom -= 1

class Gun(pygame.sprite.Sprite):
    def __init__(self):
        super(Gun,self).__init__()
        self.etype = etype
        if self.etype == 'FX1':
            self.surf = pygame.image.load('./imgs/Lasers/FX1_pew.png').convert_alpha()
            self.rect = self.surf.get_rect(
                 center=(player.rect.left + 50, player.rect.bottom - 34),)
            self.speed = 7
        elif self.etype == 'EX1':
            self.surf = pygame.image.load('./imgs/Lasers/EX1_pew.png').convert_alpha()
            self.rect = self.surf.get_rect(
                 center=(player.rect.left + 63, player.rect.bottom - 32),)
            self.speed = 9
        elif self.etype == 'AX1':
            self.surf = pygame.image.load('./imgs/Lasers/AX1_pew.png').convert_alpha()
            self.rect = self.surf.get_rect(
                 center=(player.rect.left + 44, player.rect.bottom - 30),)
            self.speed = 8

    def update(self):
         if self.rect.bottom <= 0:
            self.kill()
         else:
            self.rect.move_ip(self.speed,0)

class Debris(pygame.sprite.Sprite):
    no_proof = False
    def __init__(self):
        super(Debris,self).__init__()
        self.molAngle = 0
        self.exterminate = 0
        self.destroy_frame = 0
        self.size = rd.uniform(40,60)
        self.animation = import_folder('./imgs/Debris_Boom')
        self.image = pygame.image.load('./imgs/Debris.png').convert_alpha()
        self.surf = pygame.transform.scale(self.image,(self.size,self.size)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(center=((SCREEN_WIDTH - 30),rd.randint(1,450)))
        self.speed = rd.randint(4,10)
        self.etype = "Past_Ship"

    def update(self):
        if not self.no_proof:
            Ship_image = ('./imgs/Debris.png')
            self.rect.move_ip(-5,0)
            if self.rect.top >= SCREEN_HEIGHT:
                self.kill()
            self.molAngle += 1
            if self.etype == 'Past_Ship':
                self.image = pygame.transform.rotate(pygame.image.load(Ship_image).convert_alpha(),self.molAngle)
                self.surf = pygame.transform.scale(self.image,(self.size,self.size)).convert_alpha()
        else:
              if self.exterminate == 0:
                if self.destroy_frame > len(self.animation) - 1:
                    self.kill()
                else:
                    self.surf = pygame.transform.scale(self.animation[self.destroy_frame],(self.size,self.size)).convert_alpha()
                    self.destroy_frame += 1
              else:
                  self.rect.move_ip(0,0)
                  self.exterminate -= 1

class Alien(pygame.sprite.Sprite):
    boom = False
    def __init__(self):
        super(Alien,self).__init__()
        self.Alien = 1
        self.Alien_frame = 0
        self.rotate = 0
        self.animation = import_folder("./imgs/Alien_Boom")
        self.image = pygame.image.load('./imgs/Alien.png').convert_alpha()
        self.surf = pygame.transform.scale(self.image,(70,40)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(center=((SCREEN_WIDTH - 30),rd.randint(1,450)))
        self.speed = rd.randint(4,10)
        self.etype = "Alien"

    def update(self):
        if not self.boom:
            Asteroid_image = ('./imgs/Alien.png')
            self.rect.move_ip(-5,0)
            if self.rect.top >=SCREEN_HEIGHT:
                self.kill()
            if self.etype == 'Alien':
                self.image = pygame.image.load(Asteroid_image).convert_alpha()
                self.surf = pygame.transform.scale(self.image,(70,40)).convert_alpha()
        else:
            if self.Alien == 0:
                if self.Alien_frame > len(self.animation) - 11:
                    self.kill()
                else:
                    self.surf = pygame.transform.scale(self.animation[self.Alien_frame],(70,40)).convert_alpha()
                    self.Alien_frame += 1
            else:
                self.rect.move_ip(0,0)
                self.Alien -= 1

####################################
#
# Database Code
#
####################################

def getDbConnection():
    conn = None
    try:
        conn = sqlite3.connect("./database.db")
    except Error as e:
        print(e)
    return conn

def saveGameStats(Player,HighScore):
    conn = getDbConnection()
    curr = conn.cursor()
    updateSql = "UPDATE Asteroid_Stats set HighScore = ?, Enemies_Killed = ? WHERE name = ?"
    record = (HighScore,Kills,Player)
    curr.execute(updateSql,record)
    conn.commit()
    conn.close()


####################################
#
# main game loop
#
####################################


def Game():

    global Lives, ScoreValue, ScoreLabel, Score, LivesLabel, LivesValue,\
    HighScore, HighScoreLabel, HighScoreValue, Kills, Background, Health, Warning


    Player_ID = Gl.GameLogon()

    con = getDbConnection()
    curr = con.cursor()

    # Adds updated information into the DB
    rows = curr.execute("SELECT * FROM Asteroid_Stats WHERE name = ?",(Player_ID,)).fetchall()
    if len(rows) == 0:
        record = (Player_ID,0,0)
        sql = "INSERT INTO Asteroid_Stats (name,HighScore,Enemies_Killed) values(?,?,?)"
        curr.execute(sql,record)
        con.commit()
    else:
        for row in rows:
            HighScore = row[1]

    running = True
    background.play()
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                    player.setMoving(True)
                if event.key == K_SPACE:
                        weapon = Gun()
                        pew_sprites.add(weapon)
                        all_sprites.add(weapon)
                if event.type == KEYUP:
                    if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN:
                        player.setMoving(False)

            elif event.type == QUIT:
                saveGameStats(Player_ID, HighScore)
                running = False


            if Score >= 700:
                if event.type == ADDASTEROID:
                    newasteroid = Asteroid()
                    asteroid_sprites.add(newasteroid)
                    all_sprites.add(newasteroid)
                    pygame.time.set_timer(ASTEROID_FIELD,12000,1)
                if event.type == ASTEROID_FIELD:
                    screen.blit(Warning, (200,200))
            else:
                if event.type == ADDALIEN:
                    newalien = Alien()
                    alien_sprites.add(newalien)
                    all_sprites.add(newalien)

            if event.type == ADDOLD_SHIP:
                newcrash = Debris()
                debris_sprites.add(newcrash)
                all_sprites.add(newcrash)

        screen.blit(Background, (0,0))

        pressed_keys = pygame.key.get_pressed()
        PlayerVar.update(pressed_keys)
        asteroid_sprites.update()
        pew_sprites.update()
        debris_sprites.update()
        alien_sprites.update()


        for entity in pew_sprites:
            boom = pygame.sprite.spritecollideany(entity,asteroid_sprites)
            if boom != None:
                entity.kill()
                Score += 20
                Kills += 1
                explosion.play()
                boom.Blowing_up = True

        for entity in pew_sprites:
            erase = pygame.sprite.spritecollideany(entity,debris_sprites)
            if erase != None:
                entity.kill()
                Score += 20
                Kills += 1
                explosion.play()
                erase.no_proof = True

        for entity in pew_sprites:
            destroy = pygame.sprite.spritecollideany(entity,alien_sprites)
            if destroy != None:
                entity.kill()
                Score += 20
                explosion.play()
                destroy.boom = True

##############################################
# above - collision with weapon and enemies
####################
# below- collision with player and enemies
##############################################

        if pygame.sprite.spritecollide(PlayerVar.sprite,asteroid_sprites,False):
            if pygame.sprite.spritecollide(PlayerVar.sprite,asteroid_sprites,True, pygame.sprite.collide_mask):
                if etype == 'FX1':
                    Health -= 20
                elif etype == 'AX1':
                    Health -= 50
                elif etype == 'EX1':
                    Health -= 10
                hurt.play()
                if Health < 0:
                    Health = 0
                if Health == 0:
                    time.sleep(0.2)
                    saveGameStats(Player_ID, HighScore)
                    running = False
            else:
                pass

        if pygame.sprite.spritecollide(PlayerVar.sprite,alien_sprites,False):
            if pygame.sprite.spritecollide(PlayerVar.sprite,alien_sprites,True, pygame.sprite.collide_mask):
                if etype == 'FX1':
                    Health -= 20
                elif etype == 'AX1':
                    Health -= 50
                elif etype == 'EX1':
                    Health -= 10
                hurt.play()
                if Health < 0:
                    Health = 0
                if Health == 0:
                    time.sleep(0.2)
                    saveGameStats(Player_ID, HighScore)
                    running = False
            else:
                pass

        if pygame.sprite.spritecollide(PlayerVar.sprite,debris_sprites,False):
            if pygame.sprite.spritecollide(PlayerVar.sprite,debris_sprites,True, pygame.sprite.collide_mask):
                if etype == 'FX1':
                    Health -= 20
                elif etype == 'AX1':
                    Health -= 50
                elif etype == 'EX1':
                    Health -= 10
                hurt.play()
                if Health < 0:
                    Health = 0
                if Health == 0:
                    time.sleep(0.2)
                    saveGameStats(Player_ID, HighScore)
                    running = False
            else:
                pass


        if Score > HighScore:
            HighScore = Score
            HighScoreValue = myFont.render(str(HighScore),1,BLACK)
        ScoreValue = myFont.render(str(Score), 1, BLACK)
        LivesValue = myFont.render(str(Health),1,BLACK)
        HighScoreValue = myFont.render(str(HighScore),1,BLACK)
        screen.blit(ScoreLabel, (SCREEN_WIDTH - 880, 460))
        screen.blit(ScoreValue, (SCREEN_WIDTH - 810, 460))
        screen.blit(LivesLabel, (SCREEN_WIDTH - 720, 460))
        screen.blit(LivesValue, (SCREEN_WIDTH - 630, 460))
        screen.blit(HighScoreLabel, (SCREEN_WIDTH - 570, 460))
        screen.blit(HighScoreValue, (SCREEN_WIDTH - 460, 460))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        pygame.display.flip()
        clock.tick(60)


########################################
#
# All Variables Used
#
########################################

# Initialize pygame
pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
clock = pygame.time.Clock()
Score = 0
HighScore = 0
Kills = 0
Lives = 3
BLACK = (0,0,0)
RED = (255,0,0)
etype = ''
Health = 100

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroid Game")

myFont = pygame.font.SysFont("Comicsans", 20)
sFont = pygame.font.SysFont('Comicsans', 120)
ScoreLabel = myFont.render('Score:',1,BLACK)
ScoreValue = myFont.render(str(Score),1,BLACK)
LivesLabel = myFont.render("Health:",1,BLACK)
LivesValue = myFont.render(str(Health),1,BLACK)
HighScoreLabel = myFont.render("Highscore: ",1,BLACK)
HighScoreValue = myFont.render(str(HighScore),1,BLACK)
Warning = myFont.render("WARNING! ASTEROID FIELD INBOUND!",15,RED)
Background = pygame.image.load("./imgs/Background.png")

ADDASTEROID = pygame.USEREVENT + 1
pygame.time.set_timer(ADDASTEROID,int(rd.uniform(500,800)))

ADDOLD_SHIP = pygame.USEREVENT + 2
pygame.time.set_timer(ADDOLD_SHIP,12000)

ADDALIEN = pygame.USEREVENT + 3
pygame.time.set_timer(ADDALIEN,int(rd.uniform(500,800)))

Text_pop_up = True
ASTEROID_FIELD = pygame.USEREVENT + 4


player = Ship()

# Create groups to hold enemy sprites and all sprites
all_sprites = pygame.sprite.Group()
PlayerVar = pygame.sprite.GroupSingle()
asteroid_sprites = pygame.sprite.Group()
debris_sprites = pygame.sprite.Group()
pew_sprites = pygame.sprite.Group()
alien_sprites = pygame.sprite.Group()
# Add sprites to those groups
all_sprites.add(player)
PlayerVar.add(player)

# Adds sounds into game
explosion = pygame.mixer.Sound("./Sounds/boom.wav")
hurt = pygame.mixer.Sound("./Sounds/hurt.wav")
background = pygame.mixer.Sound("./Sounds/Background.wav")

# Sets sounds volume
explosion.set_volume(0.25)
hurt.set_volume(0.25)
background.set_volume(1.0)


# Runs the game loop
Game()
