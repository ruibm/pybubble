import pygame.constants as constants
import pygame.image as image


LEFT=0
RIGHT=1
FIRE=2

player1Keys = [constants.K_LEFT, constants.K_RIGHT, constants.K_SPACE]
player2Keys = [constants.K_a, constants.K_d, constants.K_LCTRL]

settings = dict()
settings['backgroundImage'] = "images/background.png"
settings['screenSize'] = [640, 480]
settings['ballRadius'] = 15
settings['boardPosition'] = [200, 60]
settings['boardSize'] = [240, 350]
settings['maxBalls'] = [11, 8]
settings['throwerPosition'] = [70, 264]
settings['throwerSize'] = [ 100, 100]
settings['timePerUpdateMSecs'] = int(1000.0 / 120.0)
settings['timePerFrameMSecs'] = int(1000.0 / 30.0)
settings['nextBallPosition'] = [27, 324]

settings['ballImage'] = []
settings['ballImage'].append(("blue", image.load("images/blue_ball.png")))
settings['ballImage'].append(("red", image.load("images/red_ball.png")))
settings['ballImage'].append(("orange", image.load("images/orange_ball.png")))
settings['ballImage'].append(("pink", image.load("images/pink_ball.png")))
settings['ballImage'].append(("black", image.load("images/black_ball.png")))
settings['ballImage'].append(("grey", image.load("images/grey_ball.png")))
settings['ballImage'].append(("green", image.load("images/green_ball.png")))
settings['ballImage'].append(("yellow", image.load("images/yellow_ball.png")))
# for img in settings['ballImage'] :
# 	img[1].set_colorkey(0xFFFFFF)

settings['throwerImage'] = [None]
for angle in range(1, 180):
  # settings['throwerImage'].append(image.load("images/green_ball.png"))
	settings['throwerImage'].append(image.load("images/thrower_" + str(angle) + ".png"))
	# settings['throwerImage'][angle].set_colorkey(0xFFFFFF)
