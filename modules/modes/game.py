import operator
import random
import copy
import pygame
import pygame.constants as constants
import math

import modules.mode as mode
import modules.conf as conf

class Game(mode.Mode) :
	def __init__(self, screen) :
		self.screen = screen
		self.background = pygame.image.load(conf.settings['backgroundImage'])
		self.board = Board(conf.settings['boardPosition'])
		self.keys = [False, False, False]
		self.timePerUpdateMSecs = conf.settings['timePerUpdateMSecs']
		self.lastAnimTimeMSecs = pygame.time.get_ticks()

	def run(self) :
		self.update()
		self.screen.blit(self.background, (0,0))
		self.board.render(self.screen)

	def update(self) :
		curTime = pygame.time.get_ticks()
		numberOfFrames = int((curTime - self.lastAnimTimeMSecs) / self.timePerUpdateMSecs)
		if numberOfFrames < 1 :
			return
		self.lastAnimTimeMSecs = curTime

		for a in range(numberOfFrames):
			self.runActions()
			self.board.updateAnimation()

	def runActions(self) :
		if self.keys[conf.LEFT] :
			self.board.incAngle()
		if self.keys[conf.RIGHT] :
			self.board.decAngle()
		if self.keys[conf.FIRE] :
			self.board.throwBall()

	def processEvent(self, event) :
		if event.type == constants.KEYDOWN :
			if event.key == conf.player1Keys[conf.LEFT] :
				self.keys[conf.LEFT] = True
			if event.key == conf.player1Keys[conf.RIGHT] :
				self.keys[conf.RIGHT] = True
			if event.key == conf.player1Keys[conf.FIRE] :
				self.keys[conf.FIRE] = True

		if event.type == constants.KEYUP :
			if event.key == conf.player1Keys[conf.LEFT] :
				self.keys[conf.LEFT] = False
			if event.key == conf.player1Keys[conf.RIGHT] :
				self.keys[conf.RIGHT] = False
			if event.key == conf.player1Keys[conf.FIRE] :
				self.keys[conf.FIRE] = False


################################################################################
################################################################################
################################################################################


class Board(object) :
	def __init__(self, pos) :
		self.pos = pos
		self.size = conf.settings['boardSize']
		self.nextBallPos = [conf.settings['nextBallPosition'][0] + pos[0], conf.settings['nextBallPosition'][1] + pos[1] ]
		throwerPos = [conf.settings['throwerPosition'][0] + pos[0], conf.settings['throwerPosition'][1] + pos[1] ]
		self.thrower = Thrower(self.pos)
		self.balls = []
		self.throwAngle = 0
		self.thrownBall = None
		self.ball = Ball()
		self.ball.setCenterPos(self.thrower.getCenterPos())
		self.nextBall = Ball()
		self.nextBall.setCenterPos(self.nextBallPos)
		self.isTop8BallLine = True
		self.font = pygame.font.SysFont("Verdana, Arial, Courier New", 12)
		self.ballMatrix = [[None for i in range(conf.settings['maxBalls'][1])] for i in range(conf.settings['maxBalls'][0]+2)]
		self.animations = []

	def addToBallMatrix(self, ball) :
		pos = ball.getPosInBoard(self.pos, self.isTop8BallLine)
		self.ballMatrix[pos[0]][pos[1]] = ball
		sameColor = self.getBallsWithSameColor(ball.color, pos, [])
		if len(sameColor) >= 3 :
			self.removeFromBallMatrix(sameColor)
		looseBalls = self.getLooseBalls()
		self.removeFromBallMatrix(looseBalls)

		if len(sameColor) >= 3 :
			sameColor.extend(looseBalls)
			self.animations.append(BallFalling(sameColor))

	def getLooseBalls(self) :
		visitedBallsMatrix = [[False for i in range(conf.settings['maxBalls'][1])] for i in range(conf.settings['maxBalls'][0]+2)]
		for j in range(conf.settings['maxBalls'][1]) :
			ball = self.ballMatrix[0][j]
			if ball :
				self.visitBallMatrix(visitedBallsMatrix, [0, j])

		looseBalls = []
		for ball in self.balls :
			boardPos = ball.getPosInBoard(self.pos, self.isTop8BallLine)
			if not visitedBallsMatrix[boardPos[0]][boardPos[1]] :
				looseBalls.append(ball)

		return looseBalls

	def visitBallMatrix(self, visitedBallMatrix, pos) :
		for i in range(2) :
			if pos[i] < 0 or pos[i] >= conf.settings['maxBalls'][i] :
				return

		pi = int(pos[0])
		pj = int(pos[1])
		ball = self.ballMatrix[pi][pj]
		if not ball or visitedBallMatrix[pi][pj]:
			return

		visitedBallMatrix[pi][pj] = True
		if (self.isTop8BallLine and pi % 2 == 0) or (not self.isTop8BallLine and pi % 2 == 1) :
			for i in range(-1, 2) :
				for j in range(-1, 2) :
					if (i,j) != (0,0) and (i,j) != (-1,-1) and (i,j) != (+1, -1):
						self.visitBallMatrix(visitedBallMatrix, [pi+i, pj+j])
		else :
			for i in range(-1, 2) :
				for j in range(-1, 2) :
					if (i,j) != (0,0) and (i,j) != (-1,+1) and (i,j) != (+1, +1):
						self.visitBallMatrix(visitedBallMatrix, [pi+i, pj+j])


	def removeFromBallMatrix(self, balls) :
		for ball in balls :
			pos = ball.getPosInBoard(self.pos, self.isTop8BallLine)
			self.ballMatrix[pos[0]][pos[1]] = None
			try:
				self.balls.remove(ball)
			except:
				pass

	def getBallsWithSameColor(self, color, pos, ballsFound=[]) :
		for i in range(2) :
			if pos[i] < 0 or pos[i] >= conf.settings['maxBalls'][i] :
				return []

		pi = int(pos[0])
		pj = int(pos[1])
		ball = self.ballMatrix[pi][pj]
		if not ball or color != ball.color or ball in ballsFound:
			return []

		ballsFound.append(ball)
		if (self.isTop8BallLine and pi % 2 == 0) or (not self.isTop8BallLine and pi % 2 == 1) :
			for i in range(-1, 2) :
				for j in range(-1, 2) :
					if (i,j) != (0,0) and (i,j) != (-1,-1) and (i,j) != (+1, -1):
						self.getBallsWithSameColor(color, [pi+i, pj+j], ballsFound)
		else :
			for i in range(-1, 2) :
				for j in range(-1, 2) :
					if (i,j) != (0,0) and (i,j) != (-1,+1) and (i,j) != (+1, +1):
						self.getBallsWithSameColor(color, [pi+i, pj+j], ballsFound)

		return ballsFound

	def updateAnimation(self) :
		for anim in self.animations :
			if anim.isFinished():
				self.animations.remove(anim)
			else :
				anim.update()

		if self.thrownBall :
			ball = self.thrownBall
			ball.pos[0] = ball.pos[0] + 4*math.cos(self.throwAngle)
			ball.pos[1] = ball.pos[1] - 4*math.sin(self.throwAngle)

			if  ball.pos[0]  <= self.pos[0] :
				ball.pos[0] = self.pos[0] + 1
				self.throwAngle  = math.pi - self.throwAngle
			elif ball.pos[0] >= self.pos[0] -1  + self.size[0] - 2 * ball.radius :
				ball.pos[0] = self.pos[0] + self.size[0] - 2 * ball.radius
				self.throwAngle  = math.pi - self.throwAngle

			for b in self.balls :
				if ball.collides(b) :
					ball.roundPosAroundBall(b)
					self.thrownBall = None
					self.balls.append(ball)
					self.addToBallMatrix(ball)
					self.throwAngle = 0
					ball = None
					break

			if ball and ball.pos[1] <= self.pos[1] :
				ball.roundPosToBoardTop(self.pos, self.isTop8BallLine)
				self.thrownBall = None
				self.balls.append(ball)
				self.addToBallMatrix(ball)
				self.throwAngle = 0

	def render(self, screen) :
		self.thrower.render(screen)
		self.nextBall.render(screen)
		self.ball.render(screen)
		if self.thrownBall:
			self.thrownBall.render(screen)
		for ball in self.balls :
			ball.render(screen)
		for anim in self.animations:
			anim.render(screen)
		screen.blit(self.font.render("Thrower angle: " + str(self.thrower.angle/math.pi * 180), True, pygame.color.Color("yellow")), [30, 30])
		screen.blit(self.font.render("Number of balls: " + str(len(self.balls)), True, pygame.color.Color("yellow")), [30, 50])

	def incAngle(self) :
		self.thrower.incAngle()

	def decAngle(self) :
		self.thrower.decAngle()

	def throwBall(self) :
		if self.thrownBall :
			return
		self.throwAngle = self.thrower.angle
		self.thrownBall = self.ball
		self.ball= self.nextBall
		self.ball.setCenterPos(self.thrower.getCenterPos())
		self.nextBall = Ball()
		self.nextBall.setCenterPos(self.nextBallPos)


################################################################################
################################################################################
################################################################################


class Ball(object) :
	def __init__(self, pos = [0,0]) :
#debug
		self.color = random.randint(0, len(conf.settings['ballImage'])-1)
		self.ballImage = conf.settings['ballImage'][self.color]
		self.radius = conf.settings['ballRadius']
		self.pos = copy.copy(pos)
		self.boardPos = [-1, -1]

	def setCenterPos(self, pos) :
		for a in range(2) :
			self.pos[a] = pos[a] - self.radius

	def centerDistance(self, ball) :
		a = self.pos[0] - ball.pos[0]
		b = self.pos[1] - ball.pos[1]
		return math.sqrt(a**2 + b**2)

	def collides(self, ball) :
		return self.centerDistance(ball) <  self.radius + self.radius - 4

	def render(self, screen) :
		screen.blit(self.ballImage[1], self.pos)

	def roundPosAroundBall(self, ball) :
		a = float(self.pos[0] - ball.pos[0])
		b = float(self.pos[1] - ball.pos[1])
		beta = math.acos(a / math.sqrt(a**2 + b**2))
		piThirds = math.pi / 3.0
		beta = piThirds * math.floor(0.5 + beta/piThirds)
		if self.pos[1] < ball.pos[1] :
				beta = - beta
		self.pos[0] = 2 * self.radius * math.cos(beta) + ball.pos[0]
		self.pos[1] = 2 * self.radius * math.sin(beta) + ball.pos[1]


	def roundPosToBoardTop(self, offsetPos = (0,0) , isTop8BallLine = True) :
		[i, j] = self.getPosInBoard(offsetPos, isTop8BallLine)

		if isTop8BallLine :
			compensation = 0
		else :
			compensation = self.radius

		self.pos[0] = int(j * self.radius * 2.0 + compensation)
		self.pos[1] = int(i * math.sin(math.pi/3.0) * self.radius * 2.0)

		self.pos[0] = offsetPos[0] + self.pos[0]
		self.pos[1] = offsetPos[1] + self.pos[1]

	def getPosInBoard(self, offsetPos = (0, 0), isTop8BallLine = True) :
		x = self.pos[0] - offsetPos[0]
		y = self.pos[1] - offsetPos[1]

		i = math.floor(0.5 + y / (math.sin(math.pi/3.0) * self.radius * 2.0))
		if (isTop8BallLine and i % 2 == 0) or (not isTop8BallLine and i % 2 == 1) :
			compensation = 0
		else :
			compensation = - self.radius
		j = math.floor(0.5 + (x - compensation)  / (self.radius * 2.0))

		return [int(i),int(j)]


################################################################################
################################################################################
################################################################################


class Thrower(object) :
	def __init__(self, offsetPos) :
		self.size = conf.settings['throwerSize']
		self.pos = [offsetPos[0] + conf.settings['throwerPosition'][0], offsetPos[1] + conf.settings['throwerPosition'][1] ]
		self.angle = math.pi / 2
		self.angleInc = math.pi / 180
		self.image = conf.settings['throwerImage']

	def render(self, screen) :
		screen.blit(self.image[int(self.angle*180/math.pi)], self.pos)

	def incAngle(self) :
		self.angle = self.angle + self.angleInc
		if self.angle >  math.pi - 3*self.angleInc :
			self.angle = math.pi - 3*self.angleInc

	def decAngle(self) :
		self.angle = self.angle - self.angleInc
		if self.angle <  3*self.angleInc :
			self.angle = 3*self.angleInc

	def getCenterPos(self) :
		return [self.pos[0] + self.size[0]/2, self.pos[1] + self.size[1] / 2]

################################################################################
################################################################################
################################################################################

class Animation(object) :
	def __init__(self):
		pass

	def render(self, screen) :
		pass

	def update(self) :
		pass

	def isFinished(self):
		return True

################################################################################
################################################################################
################################################################################

class BallFalling(Animation) :
	def __init__(self, balls) :
		self.balls = copy.copy(balls)
		self.maxHeight = conf.settings["screenSize"][1]
		self.speed = 0
		self.acceleration = 0.2

	def render(self, screen) :
		for ball in self.balls :
			ball.render(screen)

	def update(self) :
		self.speed = self.speed + self.acceleration
		for ball in self.balls :
			ball.pos[1] = ball.pos[1]+int(self.speed)

	def isFinished(self) :
		for ball in self.balls :
			if ball.pos[1] < self.maxHeight :
				return False
		return True

################################################################################
################################################################################
################################################################################

class ReceivedBall(Animation) :
	def __init__(self) :
		pass

	def render(self, screen) :
		pass

	def update(self) :
		pass

	def isFinished(self) :
		return True

