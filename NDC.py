# Pyxel Studio
import pyxel
from random import *

tir_attente4 = 0
tir_attente5 = 0
tir_attente3 = 0
tir_attente2 = 0
tir_attente = 0
PLAYER_VITESSE = 2
score = 0
mort = False
WALLPAPER = True


class Player:
    def __init__(self):
        self.x = 120
        self.y = 120
        self.level = 1
        self.lifes = 4
        self.score = 0
        self.all_tir = []
        self.boost = False

    def deplacement(self):
        if (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q)) and self.x > 0:
            self.x -= PLAYER_VITESSE
        if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D)) and self.x + 16 < 256:
            self.x += PLAYER_VITESSE
        if (pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z)) and self.y > 0:
            self.y -= PLAYER_VITESSE
        if (pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S)) and self.y + 16 < 256:
            self.y += PLAYER_VITESSE + 0.5
    
    def soin(self):
        global tir_attente2
        if self.lifes != 5 and self.lifes > 0:
            if pyxel.frame_count - tir_attente2 >= -1:
                self.lifes += 1
                tir_attente2 = pyxel.frame_count + 600

    def tir(self):
        global tir_attente3
        if self.lifes > 0:
            if pyxel.frame_count - tir_attente3 >= -1:
                if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    pyxel.play(2, 1, 3)
                    if self.level == 2:
                        self.all_tir.append([self.x + 6, self.y])
                        self.all_tir.append([self.x - 6, self.y])
                        tir_attente3 = pyxel.frame_count + 10
                    elif self.boost:
                        self.all_tir.append([self.x, self.y])
                        tir_attente3 = pyxel.frame_count + 5
                    else:
                        self.all_tir.append([self.x, self.y])
                        tir_attente3 = pyxel.frame_count + 10

    def tirGestion(self):
        for tir in self.all_tir:
            if tir[1] + 16 < 0:
                self.all_tir.remove(tir)
            else:
                tir[1] -= 2 * PLAYER_VITESSE

    def update(self):
        self.deplacement()
        self.tir()
        self.tirGestion()
        self.soin()

    def draw(self):
        if self.boost:
            if self.level == 1:
                pyxel.blt(self.x, self.y, 0, 16, 32, 16, 16, 1)
            elif self.level == 2:
                pyxel.blt(self.x, self.y, 0, 80, 32, 16, 16, 1)
        else:
            if self.level == 1:
                pyxel.blt(self.x, self.y, 0, 16, 16, 16, 16, 1)
            elif self.level == 2:
                pyxel.blt(self.x, self.y, 0, 80, 16, 16, 16, 1)
        for tir in self.all_tir:
            pyxel.blt(tir[0], tir[1], 0, 0, 32, 16, 16, 1)


class Ennemies:
    def __init__(self):
        self.level = 1
        self.all_ennemies = []
        self.all_ennemies_tir = []

    def spawn(self):
        if pyxel.frame_count % 30 == 1:
            self.all_ennemies.append([randint(0, 240), 0, randint(0, 59), randint(1, 7), randint(100, 168)])

    def gestion(self):
        for ennemy in self.all_ennemies:
            if ennemy[3] == 7:
                ennemy[1] += 2
            elif ennemy[1] < ennemy[4] and ennemy[3] != 7:
                ennemy[1] += 1
                if pyxel.frame_count % 120 == ennemy[2]:
                    self.all_ennemies_tir.append([ennemy[0], ennemy[1],  self.tirDamage(ennemy[3])])
            elif pyxel.frame_count % 60 == ennemy[2]:  # va config cb de balle vba tirer chaque ennemie
                if ennemy[3] == 2:
                    self.all_ennemies_tir.append([ennemy[0] - 6, ennemy[1], self.tirDamage(ennemy[3])])
                    self.all_ennemies_tir.append([ennemy[0] + 6, ennemy[1], self.tirDamage(ennemy[3])])
                elif ennemy[3] == 4:
                    self.all_ennemies_tir.append([ennemy[0] - 6, ennemy[1], self.tirDamage(ennemy[3])])
                    self.all_ennemies_tir.append([ennemy[0] + 6, ennemy[1], self.tirDamage(ennemy[3])])
                elif ennemy[3] == 6:
                    self.all_ennemies_tir.append([ennemy[0], ennemy[1], self.tirDamage(ennemy[3])])
                    self.all_ennemies_tir.append([ennemy[0], ennemy[1] + 8, self.tirDamage(ennemy[3])])
                else:
                    self.all_ennemies_tir.append([ennemy[0], ennemy[1], self.tirDamage(ennemy[3])])
            elif ennemy[1] < 256 and pyxel.frame_count % 120 == ennemy[2]:
                self.all_ennemies_tir.append([ennemy[0], ennemy[1]])

    def tirDamage(self, ennemy):
        if ennemy == 1:
            return 1
        elif ennemy == 2:
            return 2
        elif ennemy == 3:
            return 1
        elif ennemy == 4:
            return 2
        elif ennemy == 5:
            return 2
        elif ennemy == 7:
            return 4
        elif ennemy == 6:
            return 4

    def ennemiesTirGestion(self):
        for tir in self.all_ennemies_tir:
            if tir[1] > 256:
                self.all_ennemies_tir.remove(tir)
            else:
                tir[1] += 2 * PLAYER_VITESSE

    def update(self):
        self.spawn()
        self.gestion()
        self.ennemiesTirGestion()

    def draw(self):

        for tir in self.all_ennemies_tir:
            pyxel.blt(tir[0], tir[1], 0, 0, 80, 16, 16, 1)

        for ennemy in self.all_ennemies:
            if ennemy[3] == 0:
                self.all_ennemies.remove(ennemy)
            if ennemy[3] == 1:
                pyxel.blt(ennemy[0], ennemy[1], 0, 96, 48, 16, 16, 1)
            elif ennemy[3] == 2:
                pyxel.blt(ennemy[0], ennemy[1], 0, 64, 48, 16, 16, 1)
            elif ennemy[3] == 3:
                pyxel.blt(ennemy[0], ennemy[1], 0, 80, 48, 16, 16, 1)
            elif ennemy[3] == 4:
                pyxel.blt(ennemy[0], ennemy[1], 0, 32, 48, 16, 16, 1)
            elif ennemy[3] == 5:
                pyxel.blt(ennemy[0], ennemy[1], 0, 48, 48, 16, 16, 1)
            elif ennemy[3] == 6:
                pyxel.blt(ennemy[0], ennemy[1], 0, 0, 48, 16, 16, 1)
            elif ennemy[3] == 7:
                pyxel.blt(ennemy[0], ennemy[1], 0, 16, 48, 16, 16, 1)


class Vaisseau:
    def __init__(self):
        self.life = 1000


class PowerUps:
    def __init__(self):
        self.type = ""
        self.all_powerups = []

    def spawn(self):
        if pyxel.frame_count % 300 == 1:
            self.all_powerups.append([randint(0, 248), randint(0, 242), randint(1, 2)])
            pyxel.play(2, 7, 5)

    def gestion(self):
        for powerup in self.all_powerups:
            powerup[1] += 1

    def update(self):
        self.spawn()
        self.gestion()

    def draw(self):
        for powerup in self.all_powerups:
            if powerup[2] == 1:
                pyxel.blt(powerup[0], powerup[1], 0, 64, 64, 8, 16, 1, 180)
            else:
                pyxel.blt(powerup[0], powerup[1], 0, 72, 64, 8, 16, 1, 180)


class Game:
    def __init__(self):
        pyxel.init(256, 256, title="Nuit du Code")
        self.player = Player()
        self.ennemies = Ennemies()
        self.vaisseau = Vaisseau()
        self.powerUps = PowerUps()
        pyxel.load("3.pyxres")
        pyxel.play(0, 4, 31, True)
        pyxel.play(0, 6, 32, True)
        pyxel.run(self.update, self.draw)

    def commande(self):
        global WALLPAPER
        if pyxel.btnp(pyxel.KEY_U):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_N):
            WALLPAPER = not WALLPAPER
        if pyxel.btnp(pyxel.KEY_M):
            pyxel.stop()

    def receiveBonus(self):
        for powerup in self.powerUps.all_powerups:
            if self.player.x < powerup[0] + 16 and self.player.x + 16 > powerup[0] and self.player.y < powerup[
                1] + 16 and self.player.y + 16 > powerup[1]:
                self.powerUps.all_powerups.remove(powerup)
                pyxel.play(2, 3, 30)
                if powerup[2] == 1:
                    self.levelUp(pyxel.frame_count + 300)
                else:
                    self.speedUp(pyxel.frame_count + 300)

    def levelUp(self, time):
        global tir_attente4
        if time != 0:
            self.player.level = 2
        if pyxel.frame_count - tir_attente4 >= -1:
            self.player.level = 1
            tir_attente4 = 0
            tir_attente4 = pyxel.frame_count + 300

    def speedUp(self, time):
        global tir_attente5, PLAYER_VITESSE
        if time != 0:
            PLAYER_VITESSE = 4
            self.player.boost = True
        if pyxel.frame_count - tir_attente5 >= -1:
            PLAYER_VITESSE = 2
            self.player.boost = False
            tir_attente5 = 0
            tir_attente5 = pyxel.frame_count + 300

    def collisionTir(self):
        if self.player.lifes > 0:
            for tir in self.player.all_tir:
                for ennemy in self.ennemies.all_ennemies:  # change le type des ennemis quand ils meurt
                    if tir[0] < ennemy[0] + 16 and tir[0] + 16 > ennemy[0] and tir[1] < ennemy[1] + 16 and tir[1] + 16 > ennemy[1]:
                        pyxel.play(3, 5, 2)
                        if ennemy[3] == 2:
                            self.player.all_tir.remove(tir)
                            ennemy[3] = 1
                        elif ennemy[3] == 4:
                            self.player.all_tir.remove(tir)
                            ennemy[3] = 3
                        elif ennemy[3] == 6:
                            self.player.all_tir.remove(tir)
                            ennemy[3] = 5
                        else:
                            self.player.all_tir.remove(tir)
                            self.ennemies.all_ennemies.remove(ennemy)

    def collisionPlayer(self):
        for ennemy in self.ennemies.all_ennemies:
            if self.player.x < ennemy[0] + 16 and self.player.x + 16 > ennemy[0] and self.player.y < ennemy[1] + 16 and self.player.y + 16 > ennemy[1]:
                self.ennemies.all_ennemies.remove(ennemy)
                if self.player.lifes - self.ennemies.tirDamage(ennemy[3]) > 0:
                    self.player.lifes -= self.ennemies.tirDamage(ennemy[3])
                else:
                    self.player.lifes = 0

    def collisionPlayerTir(self):
        global tir_attente
        for tir in self.ennemies.all_ennemies_tir:
            if self.player.x < tir[0] + 16 and self.player.x + 16 > tir[0] and self.player.y < tir[1] + 16 and self.player.y + 16 > tir[1]:
                self.ennemies.all_ennemies_tir.remove(tir)
                if pyxel.frame_count - tir_attente >= -1:
                    tir_attente = pyxel.frame_count + 10
                    self.player.lifes -= 1

    def collisionTirVaisseau(self):
        for tir in self.ennemies.all_ennemies_tir:
            if tir[1] > 250:
                self.ennemies.all_ennemies_tir.remove(tir)
                self.vaisseau.life -= tir[2]

    def collisionEnnemy7Vaisseau(self):
        for ennemy in self.ennemies.all_ennemies:
            if ennemy[3] == 7:
                if ennemy[1] > 250:
                    self.ennemies.all_ennemies.remove(ennemy)
                    self.vaisseau.life -= 10

    def update(self):
        self.player.update()
        self.ennemies.update()
        self.collisionTir()
        self.collisionPlayer()
        self.collisionPlayerTir()
        self.collisionTirVaisseau()
        self.collisionEnnemy7Vaisseau()
        self.powerUps.update()
        self.receiveBonus()
        self.levelUp(0)
        self.speedUp(0)
        self.commande()

    def draw(self):
        global score, mort
        if self.player.lifes > 0 and self.vaisseau.life > 0:
            pyxel.cls(0)
            if WALLPAPER:
                pyxel.bltm(0, 0, 0, 0, 0, 256, 256)
            else:
                pyxel.bltm(255, 255, 0, 0, 0, 256, 256)
            self.ennemies.draw()
            self.powerUps.draw()
            pyxel.text(5, 5, "Player's Life:" + str(self.player.lifes), 7)
            pyxel.text(5, 15, "Ship's Life:" + str(self.vaisseau.life), 7)
            pyxel.text(5, 25 , "Score:" + str(pyxel.frame_count * 3 * self.player.lifes + self.vaisseau.life - 1000), 7)
            self.player.draw()
        else:
            pyxel.cls(0)
            mort = True

            if score == 0:
                score = pyxel.frame_count * 3 * (self.player.lifes+1 if self.player.lifes == 0 else self.player.lifes) + self.vaisseau.life - 1000
            pyxel.stop()

            pyxel.text(100, 120, "Vous avez echouer", 7)
            pyxel.text(110, 140, "Score: " + str(score), 7)
            pyxel.text(10, 10, "Vou pouvez relancer le jeu, l'humanite a peri...", 10)

Game()