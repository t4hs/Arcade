# Import modules
import pygame
import math
import random

pygame.init()

#Constants
# rgb colour codes
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
#Screen size
displayWidth = 1000
displayHeight = 800
#Game settings
playerSize = 15
forwardFriction = 0.5
backwardFriction = 0.2
playerMaxSpeed = 10
playerRotationSpeed = 10
bulletSpeed = 15
alienSpeed = 5
smallAlienAccuracy = 10

#Sounds
bigAlienSound = pygame.mixer.Sound("Sounds/Asteroids/bigAlien.wav")
extraLifeSound = pygame.mixer.Sound("Sounds/Asteroids/extraLife.wav")
fireSound = pygame.mixer.Sound("Sounds/Asteroids/fireSoundEffect.wav")
largeExplosionSound = pygame.mixer.Sound("Sounds/Asteroids/largeExplosion.wav")
mediumExplosionSound = pygame.mixer.Sound("Sounds/Asteroids/mediumExplosion.wav")
smallExplosionSound = pygame.mixer.Sound("Sounds/Asteroids/smallExplosion.wav")
smallAlienSound = pygame.mixer.Sound("Sounds/Asteroids/smallAlien.wav")
thrustSound = pygame.mixer.Sound("Sounds/Asteroids/thrustSoundEffect.wav")
thrustChannel = pygame.mixer.Channel(0)

#Window
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Asteroids")
timer = pygame.time.Clock()

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.horizontalSpeed = 0
        self.verticalSpeed = 0
        self.direction = -90
        self.rotationSpeed = 0
        self.thrust = False

    def updatePlayer(self):
        #Movement
        speed = math.sqrt(self.horizontalSpeed ** 2 + self.verticalSpeed ** 2)
        if self.thrust:
            thrustChannel.play(thrustSound)
            if speed + forwardFriction < playerMaxSpeed:
                self.horizontalSpeed += forwardFriction * math.cos(self.direction * math.pi / 180)
                self.verticalSpeed += forwardFriction * math.sin(self.direction * math.pi / 180)
            else:
                self.horizontalSpeed = playerMaxSpeed * math.cos(self.direction * math.pi / 180)
                self.verticalSpeed = playerMaxSpeed * math.sin(self.direction * math.pi / 180)
        else:
            if speed - backwardFriction > 0:
                changeInHorizontalSpeed = (backwardFriction * math.cos(self.verticalSpeed / self.horizontalSpeed))
                changeInVerticalSpeed = (backwardFriction * math.sin(self.verticalSpeed / self.horizontalSpeed))
                if self.horizontalSpeed != 0:
                    if changeInHorizontalSpeed / abs(changeInHorizontalSpeed) == self.horizontalSpeed / abs(
                            self.horizontalSpeed):
                        self.horizontalSpeed -= changeInHorizontalSpeed
                    else:
                        self.horizontalSpeed += changeInHorizontalSpeed
                if self.verticalSpeed != 0:
                    if changeInVerticalSpeed / abs(changeInVerticalSpeed) == self.verticalSpeed / abs(
                            self.verticalSpeed):
                        self.verticalSpeed -= changeInVerticalSpeed
                    else:
                        self.verticalSpeed += changeInVerticalSpeed
            else:
                self.horizontalSpeed = 0
                self.verticalSpeed = 0
        self.x += self.horizontalSpeed
        self.y += self.verticalSpeed

        #Wrap around window edges
        if self.x > displayWidth:
            self.x = 0
        elif self.x < 0:
            self.x = displayWidth
        elif self.y > displayHeight:
            self.y = 0
        elif self.y < 0:
            self.y = displayHeight

        #Rotate
        self.direction += self.rotationSpeed

    def drawPlayer(self):
        a = math.radians(self.direction)
        x = self.x
        y = self.y
        s = playerSize
        t = self.thrust
        #Draw player
        pygame.draw.line(gameDisplay, white,
                         (x - (s * math.sqrt(130) / 12) * math.cos(math.atan(7 / 9) + a),
                          y - (s * math.sqrt(130) / 12) * math.sin(math.atan(7 / 9) + a)),
                         (x + s * math.cos(a), y + s * math.sin(a)))

        pygame.draw.line(gameDisplay, white,
                         (x - (s * math.sqrt(130) / 12) * math.cos(math.atan(7 / 9) - a),
                          y + (s * math.sqrt(130) / 12) * math.sin(math.atan(7 / 9) - a)),
                         (x + s * math.cos(a), y + s * math.sin(a)))

        pygame.draw.line(gameDisplay, white,
                         (x - (s * math.sqrt(2) / 2) * math.cos(a + math.pi / 4),
                          y - (s * math.sqrt(2) / 2) * math.sin(a + math.pi / 4)),
                         (x - (s * math.sqrt(2) / 2) * math.cos(-a + math.pi / 4),
                          y + (s * math.sqrt(2) / 2) * math.sin(-a + math.pi / 4)))
        if t:
            pygame.draw.line(gameDisplay, white,
                             (x - s * math.cos(a),
                              y - s * math.sin(a)),
                             (x - (s * math.sqrt(5) / 4) * math.cos(a + math.pi / 6),
                              y - (s * math.sqrt(5) / 4) * math.sin(a + math.pi / 6)))
            pygame.draw.line(gameDisplay, white,
                             (x - s * math.cos(-a),
                              y + s * math.sin(-a)),
                             (x - (s * math.sqrt(5) / 4) * math.cos(-a + math.pi / 6),
                              y + (s * math.sqrt(5) / 4) * math.sin(-a + math.pi / 6)))

    def killPlayer(self):
        #Respawn position
        self.x = displayWidth / 2
        self.y = displayHeight / 2
        self.thrust = False
        self.direction = -90
        self.horizontalSpeed = 0
        self.verticalSpeed = 0

#Class for shipwreck
class deadPlayer:
    def __init__(self, x, y, l):
        self.angle = random.randrange(0, 360) * math.pi / 180
        self.direction = random.randrange(0, 360) * math.pi / 180
        self.rotationSpeed = random.uniform(-0.25, 0.25)
        self.x = x
        self.y = y
        self.length = l
        self.speed = random.randint(2, 8)

    def updateDeadPlayer(self):
        pygame.draw.line(gameDisplay, white,
                         (self.x + self.length * math.cos(self.angle) / 2,
                          self.y + self.length * math.sin(self.angle) / 2),
                         (self.x - self.length * math.cos(self.angle) / 2,
                          self.y - self.length * math.sin(self.angle) / 2))
        self.angle += self.rotationSpeed
        self.x += self.speed * math.cos(self.direction)
        self.y += self.speed * math.sin(self.direction)

class Asteroid:
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        if t == "Large":
            self.size = 30
        elif t == "Normal":
            self.size = 20
        else:
            self.size = 10
        self.t = t

        #Randomize movement
        self.speed = random.uniform(1, (40 - self.size) * 4 / 15)
        self.dir = random.randrange(0, 360) * math.pi / 180

        # Draw Sprites
        circle = random.uniform(18, 36)
        dist = random.uniform(self.size / 2, self.size)
        self.vertices = []
        while circle < 360:
            self.vertices.append([dist, circle])
            dist = random.uniform(self.size / 2, self.size)
            circle += random.uniform(18, 36)

    def updateAsteroid(self):
        #Movement
        self.x += self.speed * math.cos(self.dir)
        self.y += self.speed * math.sin(self.dir)

        #Wrap around edges
        if self.x > displayWidth:
            self.x = 0
        elif self.x < 0:
            self.x = displayWidth
        elif self.y > displayHeight:
            self.y = 0
        elif self.y < 0:
            self.y = displayHeight

        #Draw asteroid
        for v in range(len(self.vertices)):
            if v == len(self.vertices) - 1:
                next_v = self.vertices[0]
            else:
                next_v = self.vertices[v + 1]
            this_v = self.vertices[v]
            pygame.draw.line(gameDisplay, white, (self.x + this_v[0] * math.cos(this_v[1] * math.pi / 180),
                                                  self.y + this_v[0] * math.sin(this_v[1] * math.pi / 180)),
                             (self.x + next_v[0] * math.cos(next_v[1] * math.pi / 180),
                              self.y + next_v[0] * math.sin(next_v[1] * math.pi / 180)))

class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.dir = direction
        self.life = 30

    def updateBullet(self):
        #Movement
        self.x += bulletSpeed * math.cos(self.dir * math.pi / 180)
        self.y += bulletSpeed * math.sin(self.dir * math.pi / 180)

        #Draw bullet
        pygame.draw.circle(gameDisplay, white, (int(self.x), int(self.y)), 3)

        #Wrap around window edges
        if self.x > displayWidth:
            self.x = 0
        elif self.x < 0:
            self.x = displayWidth
        elif self.y > displayHeight:
            self.y = 0
        elif self.y < 0:
            self.y = displayHeight
        self.life -= 1

class Saucer:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.state = "Dead"
        self.type = "Large"
        self.directionChoice = ()
        self.bullets = []
        self.cooldown = 0
        self.bulletDirection = 0
        self.soundDelay = 0

    def updateSaucer(self):
        #Movement
        self.x += alienSpeed * math.cos(self.direction * math.pi / 180)
        self.y += alienSpeed * math.sin(self.direction * math.pi / 180)

        #Randomize direction
        if random.randrange(0, 100) == 1:
            self.direction = random.choice(self.directionChoice)

        #Wrap around window edges
        if self.y < 0:
            self.y = displayHeight
        elif self.y > displayHeight:
            self.y = 0
        if self.x < 0 or self.x > displayWidth:
            self.state = "Dead"

        #Fire
        if self.type == "Large":
            self.bulletDirection = random.randint(0, 360)
        if self.cooldown == 0:
            self.bullets.append(Bullet(self.x, self.y, self.bulletDirection))
            self.cooldown = 30
        else:
            self.cooldown -= 1

        #Sound
        if self.type == "Large":
            pygame.mixer.Sound.play(bigAlienSound)
        else:
            pygame.mixer.Sound.play(smallAlienSound)

    def createSaucer(self):
        # Create saucer
        self.state = "Alive"
        #Set random position
        self.x = random.choice((0, displayWidth))
        self.y = random.randint(0, displayHeight)

        #Randomize type
        if random.randint(0, 1) == 0:
            self.type = "Large"
            self.size = 20
        else:
            self.type = "Small"
            self.size = 10

        #Randomize direction
        if self.x == 0:
            self.direction = 0
            self.directionChoice = (0, 45, -45)
        else:
            self.direction = 180
            self.directionChoice = (180, 135, -135)

        #Reset bullet cooldown
        self.cooldown = 0

    def drawSaucer(self):
        pygame.draw.polygon(gameDisplay, white,
                            ((self.x + self.size, self.y),
                             (self.x + self.size / 2, self.y + self.size / 3),
                             (self.x - self.size / 2, self.y + self.size / 3),
                             (self.x - self.size, self.y),
                             (self.x - self.size / 2, self.y - self.size / 3),
                             (self.x + self.size / 2, self.y - self.size / 3)), 1)
        pygame.draw.line(gameDisplay, white,
                         (self.x - self.size, self.y),
                         (self.x + self.size, self.y))
        pygame.draw.polygon(gameDisplay, white,
                            ((self.x - self.size / 2, self.y - self.size / 3),
                             (self.x - self.size / 3, self.y - 2 * self.size / 3),
                             (self.x + self.size / 3, self.y - 2 * self.size / 3),
                             (self.x + self.size / 2, self.y - self.size / 3)), 1)




def drawText(msg, color, x, y, size, centered=True):
    #Style text
    font = pygame.font.SysFont("Calibri", size)
    textSurface = font.render(msg, True, color)

    #Centre text
    if centered:
        rect = textSurface.get_rect(center=(x, y))
    else:
        rect = pygame.Rect(x, y, 0, 0)

    #Output text
    gameDisplay.blit(textSurface, rect)


#Collision detection
def isColliding(x, y, xTo, yTo, size):
    if x > xTo - size and x < xTo + size and y > yTo - size and y < yTo + size:
        return True
    return False

def gameLoop(startingState):
    #variables
    gameState = startingState
    playerState = "Alive"
    playerBlink = 0
    playerPieces = []
    playerDyingDelay = 0
    playerInvisible = 0
    nextLevelDelay = 0
    bulletCapacity = 4
    bullets = []
    asteroids = []
    stage = 3
    score = 0
    live = 2
    oneUpMultiplier = 1
    playOneUpSFX = 0
    intensity = 0
    hyperspace = 0
    player = Player(displayWidth / 2, displayHeight / 2)
    alien = Saucer()

    #Main
    while gameState != "Exit":
        #Menu
        while gameState == "Menu":
            gameDisplay.fill(black)
            drawText("ASTEROIDS", white, displayWidth / 2, displayHeight / 2, 100)
            drawText("Press any key to START", white, displayWidth / 2, displayHeight / 2 + 100, 50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameState = "Exit"
                if event.type == pygame.KEYDOWN:
                    gameState = "Playing"
            pygame.display.update()
            timer.tick(5)

        #Input handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "Exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.thrust = True
                if event.key == pygame.K_LEFT:
                    player.rotationSpeed = -playerRotationSpeed
                if event.key == pygame.K_RIGHT:
                    player.rotationSpeed = playerRotationSpeed
                if event.key == pygame.K_SPACE and playerDyingDelay == 0 and len(bullets) < bulletCapacity:
                    bullets.append(Bullet(player.x, player.y, player.direction))
                    # Play SFX
                    pygame.mixer.Sound.play(fireSound)
                if gameState == "Game Over":
                    if event.key == pygame.K_r:
                        gameState = "Exit"
                        gameLoop("Playing")
                if event.key == pygame.K_LSHIFT:
                    hyperspace = 30
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.thrust = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.rotationSpeed = 0

        player.updatePlayer()

        #check invisibility
        if playerInvisible != 0:
            playerInvisible -= 1
        elif hyperspace == 0:
            playerState = "Alive"

        #Paint over display
        gameDisplay.fill(black)

        #Hyperspace
        if hyperspace != 0:
            playerState = "Died"
            hyperspace -= 1
            if hyperspace == 1:
                player.x = random.randrange(0, displayWidth)
                player.y = random.randrange(0, displayHeight)

        #Asteroid player collision detection
        for a in asteroids:
            a.updateAsteroid()
            if playerState != "Died":
                if isColliding(player.x, player.y, a.x, a.y, a.size):
                    #Shipwreck
                    playerPieces.append(
                        deadPlayer(player.x, player.y, 5 * playerSize / (2 * math.cos(math.atan(1 / 3)))))
                    playerPieces.append(
                        deadPlayer(player.x, player.y, 5 * playerSize / (2 * math.cos(math.atan(1 / 3)))))
                    playerPieces.append(deadPlayer(player.x, player.y, playerSize))

                    #Kill player
                    playerState = "Died"
                    playerDyingDelay = 30
                    playerInvisible = 120
                    player.killPlayer()

                    if live != 0:
                        live -= 1
                    else:
                        gameState = "Game Over"

                    #Half asteroid
                    if a.t == "Large":
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        score += 20
                        pygame.mixer.Sound.play(largeExplosionSound)
                    elif a.t == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        score += 50
                        pygame.mixer.Sound.play(mediumExplosionSound)
                    else:
                        score += 100
                        pygame.mixer.Sound.play(smallExplosionSound)
                    asteroids.remove(a)

        #Update Shipwreck
        for f in playerPieces:
            f.updateDeadPlayer()
            if f.x > displayWidth or f.x < 0 or f.y > displayHeight or f.y < 0:
                playerPieces.remove(f)

        #Update level
        if len(asteroids) == 0 and alien.state == "Dead":
            if nextLevelDelay < 30:
                nextLevelDelay += 1
            else:
                stage += 1
                intensity = 0
                #Spawn asteroids
                for i in range(stage):
                    xTo = displayWidth / 2
                    yTo = displayHeight / 2
                    while xTo - displayWidth / 2 < displayWidth / 4 and yTo - displayHeight / 2 < displayHeight / 4:
                        xTo = random.randrange(0, displayWidth)
                        yTo = random.randrange(0, displayHeight)
                    asteroids.append(Asteroid(xTo, yTo, "Large"))
                nextLevelDelay = 0

        #Update intensity
        if intensity < stage * 450:
            intensity += 1

        #Aliens
        if alien.state == "Dead":
            if random.randint(0, 6000) <= (intensity * 2) / (stage * 9) and nextLevelDelay == 0:
                alien.createSaucer()
                #Remove big aliens
                if score >= 40000:
                    alien.type = "Small"
        else:
            #Alien aiming
            acc = smallAlienAccuracy * 4 / stage
            alien.bulletDirection = math.degrees(
                math.atan2(-alien.y + player.y, -alien.x + player.x) + math.radians(random.uniform(acc, -acc)))

            alien.updateSaucer()
            alien.drawSaucer()

            #Alien asteroid collision deteection
            for a in asteroids:
                if isColliding(alien.x, alien.y, a.x, a.y, a.size + alien.size):
                    alien.state = "Dead"

                    #Half asteroid
                    if a.t == "Large":
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        pygame.mixer.Sound.play(largeExplosionSound)
                    elif a.t == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        pygame.mixer.Sound.play(mediumExplosionSound)
                    else:
                        pygame.mixer.Sound.play(smallExplosionSound)
                    asteroids.remove(a)

            #Alien bullet collison detection
            for b in bullets:
                if isColliding(b.x, b.y, alien.x, alien.y, alien.size):
                    # Add points
                    if alien.type == "Large":
                        score += 200
                    else:
                        score += 1000

                    alien.state = "Dead"
                    pygame.mixer.Sound.play(largeExplosionSound)
                    bullets.remove(b)

            #Alien player collision detection
            if isColliding(alien.x, alien.y, player.x, player.y, alien.size):
                if playerState != "Died":
                    #Shipwreck
                    playerPieces.append(
                        deadPlayer(player.x, player.y, 5 * playerSize / (2 * math.cos(math.atan(1 / 3)))))
                    playerPieces.append(
                        deadPlayer(player.x, player.y, 5 * playerSize / (2 * math.cos(math.atan(1 / 3)))))
                    playerPieces.append(deadPlayer(player.x, player.y, playerSize))

                    # Kill player
                    playerState = "Died"
                    playerDyingDelay = 30
                    playerInvisible = 120
                    player.killPlayer()

                    if live != 0:
                        live -= 1
                    else:
                        gameState = "Game Over"

                    pygame.mixer.Sound.play(largeExplosionSound)

            #Alien fire
            for b in alien.bullets:
                b.updateBullet()

                #Alien bullet asteroid collision detection
                for a in asteroids:
                    if isColliding(b.x, b.y, a.x, a.y, a.size):
                        #Half asteroid
                        if a.t == "Large":
                            asteroids.append(Asteroid(a.x, a.y, "Normal"))
                            asteroids.append(Asteroid(a.x, a.y, "Normal"))
                            pygame.mixer.Sound.play(largeExplosionSound)
                        elif a.t == "Normal":
                            asteroids.append(Asteroid(a.x, a.y, "Small"))
                            asteroids.append(Asteroid(a.x, a.y, "Small"))
                            pygame.mixer.Sound.play(largeExplosionSound)
                        else:
                            pygame.mixer.Sound.play(largeExplosionSound)

                        #Remove asteroid and bullet
                        asteroids.remove(a)
                        alien.bullets.remove(b)

                        break

                #Alien bullet player collision detection
                if isColliding(player.x, player.y, b.x, b.y, 5):
                    if playerState != "Died":
                        #Shipwreck
                        playerPieces.append(
                            deadPlayer(player.x, player.y, 5 * playerSize / (2 * math.cos(math.atan(1 / 3)))))
                        playerPieces.append(
                            deadPlayer(player.x, player.y, 5 * playerSize / (2 * math.cos(math.atan(1 / 3)))))
                        playerPieces.append(deadPlayer(player.x, player.y, playerSize))

                        # Kill player
                        playerState = "Died"
                        playerDyingDelay = 30
                        playerInvisible = 120
                        player.killPlayer()

                        if live != 0:
                            live -= 1
                        else:
                            gameState = "Game Over"

                        pygame.mixer.Sound.play(largeExplosionSound)
                        alien.bullets.remove(b)

                if b.life <= 0:
                    try:
                        alien.bullets.remove(b)
                    except ValueError:
                        continue

        # Bullets
        for b in bullets:
            #Update bullets
            b.updateBullet()

            #bullet asteroid collision detection
            for a in asteroids:
                if b.x > a.x - a.size and b.x < a.x + a.size and b.y > a.y - a.size and b.y < a.y + a.size:
                    #Half asteroid
                    if a.t == "Large":
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        asteroids.append(Asteroid(a.x, a.y, "Normal"))
                        score += 20
                        pygame.mixer.Sound.play(largeExplosionSound)
                    elif a.t == "Normal":
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        asteroids.append(Asteroid(a.x, a.y, "Small"))
                        score += 50
                        pygame.mixer.Sound.play(mediumExplosionSound)
                    else:
                        score += 100
                        pygame.mixer.Sound.play(smallExplosionSound)
                    asteroids.remove(a)
                    bullets.remove(b)
                    break

            # Destroying bullets
            if b.life <= 0:
                try:
                    bullets.remove(b)
                except ValueError:
                    continue

        #1 up
        if score > oneUpMultiplier * 10000:
            oneUpMultiplier += 1
            live += 1
            playOneUpSFX = 60
        #Sound
        if playOneUpSFX > 0:
            playOneUpSFX -= 1
            pygame.mixer.Sound.play(extraLifeSound, 60)

        #Draw player
        if gameState != "Game Over":
            if playerState == "Died":
                if hyperspace == 0:
                    if playerDyingDelay == 0:
                        if playerBlink < 5:
                            if playerBlink == 0:
                                playerBlink = 10
                            else:
                                player.drawPlayer()
                        playerBlink -= 1
                    else:
                        playerDyingDelay -= 1
            else:
                player.drawPlayer()
        else:
            drawText("Game Over", white, displayWidth / 2, displayHeight / 2, 100)
            drawText("Press \"R\" to restart!", white, displayWidth / 2, displayHeight / 2 + 100, 50)
            live = -1

        #Draw score
        drawText(str(score), white, 60, 20, 40, False)

        #Draw Lives
        for l in range(live + 1):
            Player(75 + l * 25, 75).drawPlayer()

        #Update screen
        pygame.display.update()

        #Tick fps
        timer.tick(30)

#Start game
gameLoop("Menu")

#End game
pygame.quit()
quit()
