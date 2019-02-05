import os
import time
import sys
import pygame
import pygame.constants as constants

import modules.conf as conf
import modules.modes.game as game


class Core (object) :
	def __init__(self) :
		pygame.init()
		#self.screen = pygame.display.set_mode(conf.settings['screenSize'], constants.ASYNCBLIT | constants.FULLSCREEN)
		self.screen = pygame.display.set_mode(conf.settings['screenSize'] )
		#pygame.mouse.set_visible(False)
		self.mode = game.Game(self.screen)
		self.count = 0
		self.initTime = 0

	def run(self) :
		initTime = 0
		timePerFrame = conf.settings['timePerFrameMSecs']
		self.initTime = pygame.time.get_ticks()
		while True :
			self.count = self.count + 1
			self.processUserInput()
			self.mode.run()
			pygame.display.flip()

			curTime = pygame.time.get_ticks()
			timeDiff = curTime - initTime
			if timeDiff <  timePerFrame:
				delay = timePerFrame - timeDiff
				realDelay = pygame.time.wait(delay)
			initTime = curTime


	def processUserInput(self) :
		for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == constants.K_ESCAPE) :
					currentTime = pygame.time.get_ticks()
					fps = self.count * 1000.0 / (currentTime - self.initTime)
					print("Framerate: ", fps, "fps")
					sys.exit()
				else :
					self.mode.processEvent(event)
