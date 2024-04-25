import pygame, sys, os, math, random, time
from pygame.locals import *

##################################################
################## VARIABLES #####################
##################################################
winWidth = 900 #window width
winHeight = 600 #window height
backgroundX = -150
backgroundY = -150
intLevel = 1
intScore = 0
intCountdown = 4
playState = "menu"
bolBGOn = "true"
bolBGMove = "true"
pygame.init()
fpsClock=pygame.time.Clock()
winSurface = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption('Geometry Wars')
lstCheckBox = []
intCheckCount = 2

#################
#### PLAYER #####
#################
intWidth = 50 #player width
intSpeed = 5 #player speed
staHealth = 100
varHealth = staHealth

posX = winWidth / 2 #player x position
posY = winHeight / 2 #player y position
mouseX, mouseY = 0,0 #mouse positions

#################
#### BULLETS ####
#################
lstBullets = [] #list of bullets
bulletX, bulletY = posX, posY #bullet positions (origin of player)
mouseDown = 0 #tell if mouse down for shooting purposes

#################
##### BOMBS #####
#################
lstBombs = [] #list of bombs
bombCounter = 5
staDelay = 300 #static delay for bomb
varDelay = 0 #paceholder for variable bomb delay
staThickness = 5 #static thickness of bomb explosion
varThickness = staThickness #placeholder for variable explosion thickness

#################
#### ENEMIES ####
#################
lstGrunts = [] #list of enemies
gruntCount = 0
lstGravBalls = []
gravBallCount = 0

#################
#### COLORS #####
#################
clrBlack = pygame.Color(0, 0, 0)
clrWhite = pygame.Color(255, 255, 255)
clrPink = pygame.Color(255, 0, 255)
clrRed = pygame.Color(255, 0, 0)

#################
##### FONTS #####
#################
fntText = pygame.font.SysFont("consolas", 22)
fntOver = pygame.font.SysFont("consolas", 60)

#################
#### IMAGES #####
#################
BackgroundFile = os.path.join("data", "background.png")
imgBackground = pygame.image.load(BackgroundFile).convert_alpha()
BehindBackgroundFile = os.path.join("data", "background2.png")
imgBackgroundBehind = pygame.image.load(BehindBackgroundFile).convert_alpha()
ShipFile = os.path.join("data", "ship.png")
imgShip = pygame.image.load(ShipFile).convert_alpha()
GruntFile = os.path.join("data", "grunt.png")
imgGrunt = pygame.image.load(GruntFile).convert_alpha()
GravBallFile = os.path.join("data", "gravball.png")
imgGravBall = pygame.image.load(GravBallFile).convert_alpha()
GravBallBackFile = os.path.join("data", "gravballBack.png")
imgGravBallBack = pygame.image.load(GravBallBackFile).convert_alpha()

#################
##### AUDIO #####
#################

#################
#### CLASSES #####
#################

class clsBullet:
	def __init__(self, radius, x, y, color, speed, angle):
		self.radius = radius
		self.y = y
		self.x = x
		self.color = color
		self.speed = speed
		self.angle = angle
		self.speed = 15

	def shoot(self):
		self.xSpeed = math.sin(math.radians(self.angle + 90)) * self.speed
		self.ySpeed = math.cos(math.radians(self.angle + 90)) * self.speed
		self.x += int(self.xSpeed)
		self.y += int(self.ySpeed)

		pygame.draw.circle(winSurface, self.color, (self.x, self.y), self.radius)

		if self.x > winWidth:
			lstBullets.remove(self)
		elif self.x < 0:
			lstBullets.remove(self)
		elif self.y > winHeight:
			lstBullets.remove(self)
		elif self.y < 0:
			lstBullets.remove(self)

	def collide(self):
		global intScore
		for i in lstGrunts:
			self.distance = math.sqrt(((self.x - i.x) ** 2) + ((self.y - i.y) ** 2))
			if self.distance < (self.radius + i.radius):
				lstGrunts.remove(i)
				#lstBullets.remove(self) #WHY IS THIS BROKEN?
				intScore += 50

		for i in lstGravBalls:
			self.distance = math.sqrt(((self.x - i.x) ** 2) + ((self.y - i.y) ** 2))
			if self.distance < (self.radius + i.radius):
				i.health -= 1
				if i.width > 50:
					i.width -= 2
				if i.height > 50:
					i.height -= 2
				if i.health <= 0:
					i.dead = "true"
				#lstBullets.remove(self)
				intScore += 50

class clsBomb:
	def __init__(self, radius, x, y, color):
		self.radius = radius
		self.y = y
		self.x = x
		self.color = color

	def explode(self):
		global varThickness, staThickness
		pygame.draw.circle(winSurface, self.color, (self.x, self.y), self.radius, int(varThickness))
		if varThickness < 30:
			varThickness += 1
		self.radius += 5
		if self.radius >= 300:
			lstBombs.remove(self)
			varThickness = staThickness

class clsGrunt:
	def __init__(self, radius, x, y, color):
		self.radius = radius
		self.x = x
		self.y = y
		self.color = color
		self.speed = 2

	def move(self):
		global posX, posY
		#rotate to player
		self.angle = abs(math.degrees(math.atan2(self.y-posY, self.x-posX)) - 180)
		imgGruntRotated = pygame.transform.rotate(imgGrunt, self.angle)
		width = pygame.Surface.get_width(imgGruntRotated)

		#follow player
		self.distance = math.sqrt(((self.x - posX) ** 2) + ((self.y - posY) ** 2))
		if self.distance > 0:
			self.xSpeed = math.sin(math.radians(self.angle + 90)) * self.speed
			self.ySpeed = math.cos(math.radians(self.angle + 90)) * self.speed
			self.x += int(self.xSpeed)
			self.y += int(self.ySpeed)

		#blit enemy
		winSurface.blit(imgGruntRotated,(self.x - (width / 2), self.y - (width / 2))) #blit ship

	def collide(self):
		global posX, posY, width, varHealth
		for i in lstBombs:
			self.distance = math.sqrt(((self.x - i.x) ** 2) + ((self.y - i.y) ** 2))
			if self.distance < (self.radius + i.radius):
				self.kill()

		self.distance = math.sqrt(((self.x - posX) ** 2) + ((self.y - posY) ** 2))
		if self.distance < (self.radius + 25):
			if varHealth > 0:
				varHealth -= 0.3
			else:
				varHealth = 0

	def kill(self):
		lstGrunts.remove(self)

class clsGravBall:
	def __init__(self, radius, x, y, width, height, color):
		self.radius = radius
		self.x = x
		self.y = y
		self.width = width
		self.height = width
		self.backWidth = width
		self.backHeight = height
		self.color = color
		self.speed = 2
		self.health = 300
		self.dead = "false"

	def grow(self):
		if self.backWidth <= 185:
			self.backWidth += 5
		elif self.backWidth <= 195:
			self.backWidth += 3
		elif self.backWidth <= 200:
			self.backWidth += 1
		if self.backHeight <= 185:
			self.backHeight += 5
		elif self.backHeight <= 195:
			self.backHeight += 3
		elif self.backHeight <= 200:
			self.backHeight += 1

		if self.width <= 85:
			self.width += 3
		elif self.width <= 95:
			self.width += 2
		elif self.width <= 100:
			self.width += 1
		if self.height <= 85:
			self.height += 3
		elif self.height <= 95:
			self.height += 2
		elif self.height <= 100:
			self.height += 1

		imgGravBallBackScaled = pygame.transform.scale(imgGravBallBack, (self.backWidth * 2, self.backHeight * 2))
		winSurface.blit(imgGravBallBackScaled,(self.x - (self.backWidth), self.y - (self.backHeight)))

		imgGravBallScaled = pygame.transform.scale(imgGravBall, (self.width, self.height))
		winSurface.blit(imgGravBallScaled,(self.x - (self.width / 2), self.y - (self.height / 2)))

	def gravitate(self):
		global posX, posY, width
		self.distance = math.sqrt(((self.x - posX) ** 2) + ((self.y - posY) ** 2))
		if self.distance > 0 and self.distance < 200:
			self.angle = abs(math.degrees(math.atan2(self.y-posY, self.x-posX)) - 180)
			self.xSpeed = math.sin(math.radians(self.angle + 90)) * self.speed
			self.ySpeed = math.cos(math.radians(self.angle + 90)) * self.speed
			posX -= int(self.xSpeed)
			posY -= int(self.ySpeed)

	def collide(self):
		global posX, posY, width, varHealth
		self.distance = math.sqrt(((self.x - posX) ** 2) + ((self.y - posY) ** 2))
		if self.distance < self.radius + 10:
			if varHealth > 0:
				varHealth -= 0.3
			else:
				varHealth = 0


	def implode(self):
		if self.backWidth >= 195:
			self.backWidth -= 1
		elif self.backWidth >= 185:
			self.backWidth -= 3
		elif self.backWidth > 6:
			self.backWidth -= 5

		if self.backHeight >= 195:
			self.backHeight -= 1
		elif self.backHeight >= 185:
			self.backHeight -= 3
		elif self.backHeight > 6:
			self.backHeight -= 5

		if self.width >= 95:
			self.width -= 1
		elif self.width >= 85:
			self.width -= 2
		elif self.width > 4:
			self.width -= 3

		if self.height >= 95:
			self.height -= 1
		elif self.height >= 85:
			self.height -= 2
		elif self.height > 4:
			self.height -= 3
		elif self.height > 0:
			lstGravBalls.remove(self)

		imgGravBallBackScaled = pygame.transform.scale(imgGravBallBack, (self.backWidth * 2, self.backHeight * 2))
		winSurface.blit(imgGravBallBackScaled,(self.x - (self.backWidth), self.y - (self.backHeight)))

		imgGravBallScaled = pygame.transform.scale(imgGravBall, (self.width, self.height))
		winSurface.blit(imgGravBallScaled,(self.x - (self.width / 2), self.y - (self.height / 2)))

class clsCheckBox:
	def __init__ (self, checked, text, x, y):
		self.checked = checked
		self.text = text
		self.x = x
		self.y = y
		self.mouseX = 25
		self.mouseY = 25

	def check(self):
		pygame.draw.rect(winSurface, clrWhite, (self.x, self.y, 20, 20), 1)
		lblText = fntText.render(self.text, 1, clrWhite)
		winSurface.blit(lblText, (self.x + 30, self.y))
		if self.checked == "true":
			pygame.draw.rect(winSurface, clrWhite, (self.x, self.y, 20, 20), 0)
		elif self.checked == "false":
			pygame.draw.rect(winSurface, clrBlack, (self.x + 1, self.y + 1, 18, 18), 0)

	def switch(self):
		if self.mouseX >= self.x and self.mouseX <= self.x + 20 and self.mouseY >= self.y and self.mouseY <= self.y + 20:
			if self.checked == "true":
				self.checked = "false"
			elif self.checked == "false":
				self.checked = "true"

def fGruntSpawn():
	global gruntCount
	intSpawnNum = random.randint(0,3)
	if intSpawnNum == 0: #left side
		lstGrunts.append(clsGrunt(25, -50, random.randint(0,winHeight), clrRed))
		gruntCount += 1
	elif intSpawnNum == 1: #right side
		lstGrunts.append(clsGrunt(25, (winWidth + 50), random.randint(0,winHeight), clrRed))
		gruntCount += 1
	elif intSpawnNum == 2: #top
		lstGrunts.append(clsGrunt(25, random.randint(0, winWidth), -50, clrRed))
		gruntCount += 1
	elif intSpawnNum == 3: #bottom
		lstGrunts.append(clsGrunt(25, random.randint(0, winWidth), (winHeight + 50), clrRed))
		gruntCount += 1

def fGravBallSpawn():
	global gravBallCount
	lstGravBalls.append(clsGravBall(50, random.randint(0, winWidth), random.randint(0, winHeight), 0, 0, clrPink))
	gravBallCount += 1

while True:
	if playState == "menu":
		winSurface.fill(clrBlack) #fill black
		lblTitle = fntOver.render("GEOMETRY WARS", 1, clrWhite)
		winSurface.blit(lblTitle, (winWidth / 2 - 220, winHeight / 2 - 150))
		lblPlay = fntText.render("Press enter to play", 1, clrWhite)
		winSurface.blit(lblPlay, (winWidth / 2 - 120, winHeight / 2 - 80))
		lblWASD = fntText.render("WASD to move, Space for bomb", 1, clrWhite)
		winSurface.blit(lblWASD, (winWidth / 2 - 180, winHeight / 2 - 40))
		lblMouse = fntText.render("Move mouse to aim, click to shoot", 1, clrWhite)
		winSurface.blit(lblMouse, (winWidth / 2 - 210, winHeight / 2))

		if intCheckCount == 2:
			lstCheckBox.append(clsCheckBox("true", "Enable background", winWidth / 2 - 120, winHeight / 2 + 100))
			intCheckCount -= 1
		elif intCheckCount == 1:
			lstCheckBox.append(clsCheckBox("true", "Move background", winWidth / 2 - 120, winHeight / 2 + 140))
			intCheckCount -= 1

		keys = pygame.key.get_pressed()
		if keys[pygame.K_RETURN]: #left
			playState = "play"
		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN: #mouse down
				mouseDown = 1
				for i in lstCheckBox:
					i.mouseX, i.mouseY = pygame.mouse.get_pos()
					i.switch()
			elif event.type == MOUSEBUTTONUP: #mouse up
				mouseDown = 0
			if event.type == pygame.QUIT: #quit
				pygame.quit()
				sys.exit()

		if intCheckCount == 0:
			for i in lstCheckBox:
				i.check()
			if lstCheckBox[0].checked == "true":
				bolBGOn = "true"
			elif lstCheckBox[0].checked == "false":
				bolBGOn = "false"
			if lstCheckBox[1].checked == "true":
				bolBGMove = "true"
			if lstCheckBox[1].checked == "false":
				bolBGMove = "false"


	if playState == "dead":
		winSurface.fill(clrBlack) #fill black
		lblDead = fntOver.render("YOU DIED!", 1, clrWhite)
		winSurface.blit(lblDead, (winWidth / 2 - 155, winHeight / 2 - 150))
		lblReplay = fntText.render("Press enter to restart", 1, clrWhite)
		winSurface.blit(lblReplay, (winWidth / 2 - 140, winHeight / 2 - 80))
		lblReplay = fntText.render("Press M to go to menu", 1, clrWhite)
		winSurface.blit(lblReplay, (winWidth / 2 - 135, winHeight / 2 - 50))

		keys = pygame.key.get_pressed()
		if keys[pygame.K_RETURN]: #left
			lstGrunts = []
			lstGravBalls = []
			lstBullets = []
			lstBombs = []
			varHealth = staHealth
			posX = winWidth / 2 #player x position
			posY = winHeight / 2 #player y position
			intLevel = 1
			intScore = 0
			gruntCount = 0
			gravBallCount = 0
			playState = "play"
		if keys[pygame.K_m]: #left
			lstGrunts = []
			lstGravBalls = []
			lstBullets = []
			lstBombs = []
			varHealth = staHealth
			posX = winWidth / 2 #player x position
			posY = winHeight / 2 #player y position
			intLevel = 1
			intScore = 0
			gruntCount = 0
			gravBallCount = 0
			playState = "menu"
		for event in pygame.event.get():
			if event.type == pygame.QUIT: #quit
				pygame.quit()
				sys.exit()

	if playState == "play":
		winSurface.fill(clrBlack) #fill black
		if bolBGOn == "true":
			winSurface.blit(imgBackgroundBehind,(backgroundX / 2, backgroundY / 2)) #blit background image
			winSurface.blit(imgBackground,(backgroundX, backgroundY)) #blit background image

		for event in pygame.event.get():
			if event.type == MOUSEBUTTONDOWN: #mouse down
				mouseDown = 1
			elif event.type == MOUSEBUTTONUP: #mouse up
				mouseDown = 0
			if event.type == pygame.QUIT: #quit
				pygame.quit()
				sys.exit()

		#wall collision
		if posY > (winHeight - 25): # topddd
			posY -= intSpeed
		if posY < (0 + 25): #bottom
			posY += intSpeed
		if posX > (winWidth - 25): #right
			posX -= intSpeed
		if posX < (0 + 25): #left
			posX += intSpeed

		#tell if mousedown (1 = true, 0 = false, 2+ = delay)
		if mouseDown == 1:
			lstBullets.append(clsBullet(5, posX, posY, clrWhite, 8, intAngle)) #append new bullet to list
			mouseDown = 5
		elif mouseDown > 1:
			mouseDown -= 1

		#check keys
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_m]: #left
				lstGrunts = []
				lstGravBalls = []
				lstBullets = []
				lstBombs = []
				varHealth = staHealth
				posX = winWidth / 2 #player x position
				posY = winHeight / 2 #player y position
				intLevel = 1
				intScore = 0
				gruntCount = 0
				gravBallCount = 0
				playState = "menu"
		if keystate[pygame.K_a]: #left
			posX -= intSpeed
			if bolBGMove == "true":
				backgroundX -= intSpeed - 6
		if keystate[pygame.K_d]: #right
			posX += intSpeed
			if bolBGMove == "true":
				backgroundX += intSpeed - 6
		if keystate[pygame.K_w]: #up
			posY -= intSpeed
			if bolBGMove == "true":
				backgroundY -= intSpeed - 6
		if keystate[pygame.K_s]: #down
			posY += intSpeed
			if bolBGMove == "true":
				backgroundY += intSpeed - 6
		if keystate[pygame.K_SPACE]: #bomb
			if varDelay == 0:
				if bombCounter > 0:
					lstBombs.append(clsBomb(5, posX, posY, clrPink))
					varDelay = staDelay
					bombCounter -= 1
		if varDelay > 0:
			varDelay -= 1

		#level counter
		if intLevel == 1:
			while gruntCount < 6:
				fGruntSpawn()
			while gravBallCount < 1:
				fGravBallSpawn()
			if lstGrunts == [] and len(lstGravBalls) < 2:
				gruntCount = 0
				gravBallCount = 0
				intLevel = 2
		elif intLevel == 2:
			while gruntCount < 9:
				fGruntSpawn()
			while gravBallCount < 2:
				fGravBallSpawn()
			if lstGrunts == [] and len(lstGravBalls) < 2:
				gruntCount = 0
				gravBallCount = 0
				intLevel = 3
		elif intLevel == 3:
			while gruntCount < 12:
				fGruntSpawn()
			while gravBallCount < 3:
				fGravBallSpawn()
			if lstGrunts == [] and len(lstGravBalls) < 2:
				gruntCount = 0
				gravBallCount = 0
				intLevel = 1

		#call shoot from Bullet class
		for i in lstGravBalls:
			if i.dead == "false":
				i.grow()
				i.gravitate()
				i.collide()
			elif i.dead == "true":
				i.implode()
		for i in lstBombs:
			i.explode()
		for i in lstBullets:
			i.shoot()
			i.collide()
		for i in lstGrunts:
			i.collide()
			i.move()

		#get mouse position for angle, rotate ship continuously
		mouseX, mouseY = pygame.mouse.get_pos()
		intAngle = abs(math.degrees(math.atan2(posY-mouseY, posX-mouseX)) - 180)
		imgShipRotated = pygame.transform.rotate(imgShip, intAngle)
		width = pygame.Surface.get_width(imgShipRotated)
		winSurface.blit(imgShipRotated,(posX - (width / 2), posY - (width / 2))) #blit ship

		#information labels
		lblHealth = fntText.render("Health:" + str(round(varHealth, 0))[:-2], 1, clrWhite)
		winSurface.blit(lblHealth, (10, 10))
		pygame.draw.rect(winSurface, clrWhite, (150, 10, (staHealth * 3), 20), 1) #bomb cooldown outline
		pygame.draw.rect(winSurface, clrWhite, (150, 10, (varHealth * 3), 20), 0) #bomb cooldown

		lblBombs = fntText.render("Bombs: " + str(bombCounter), 1, clrWhite)
		winSurface.blit(lblBombs, (10, 40))
		pygame.draw.rect(winSurface, clrWhite, (150, 40, staDelay, 20), 1) #bomb cooldown outline
		pygame.draw.rect(winSurface, clrWhite, (150, 40, varDelay, 20), 0) #bomb cooldown

		lblLevel = fntText.render("Level:" + str(intLevel), 1, clrWhite)
		winSurface.blit(lblLevel, (500, 10))

		lblScore = fntText.render("Score:" + str(intScore), 1, clrWhite)
		winSurface.blit(lblScore, (500, 40))

		if varHealth <= 0:
			playState = "dead"

	fpsClock.tick(60)
	pygame.display.update()