import pygame
from pygame import mixer
import sys
import random
from math import sin,cos
pygame.init()

class Player:
	def __init__(self,x,y,state,frame,health,vulnerable):
		self.x = x
		self.y = y
		self.state = state
		self.frame = frame
		self.health = health
		self.vulnerable = vulnerable
	def draw_player(self):
		screen.blit(playerstates[self.state][self.frame],(self.x,self.y))
	def draw_player_u(self):
		screen.blit(playerstates[self.state][self.frame],(self.x,self.y-200))

enemy_key = {
	69: ['x','y','directionspeed;(-1 is left)','enemy_type','internal_timer','health','vulnerable?'],
	0: [-40,100,1,'rattata',0,3,1],
	1: [-40,50,2,'pidgey',0,1,1],
	2: [400,100,-1,'rattata',0,3,1],
	3: [400,50,-2,'pidgey',0,1,1],
	4: [-40,300,1,'rattata',0,3,1],
	5: [-40,250,2,'pidgey',0,1,1],
	6: [400,300,-1,'rattata',0,3,1],
	7: [400,250,-2,'pidgey',0,1,1]
}

def fire_bullets(x,y):
	bullet_list.append([x,y+12,player.state])
def update_bullets():
	for idx,bullet in enumerate(bullet_list):
		if bullet[2] == 0:
			bullet[0]-=10
		elif bullet[2] == 1:
			bullet[0]+=10
		if bullet[0] < -5 or bullet[0] > 405:
			bullet_list.pop(idx)

def draw_bullets():
	for bullet in bullet_list:
		screen.blit(bullets,(bullet[0],bullet[1]))

def show_score(x,y):
	screen.blit(text_surface,(x,y))

def generate_enemy(time):
#	print(int(200*(0.995**(time/1000))))
	randomgenerated = random.randint(1,int(80*(0.997**(time/1000))))
#	print(randomgenerated)
	if randomgenerated == 1:
#		print('enemy_summoned')
		enemy_type = random.randint(0,7)
		list_of_enemies.append(enemy_key[enemy_type])
#		print(enemy_key[enemy_type])
#		print(enemy_key)
#		print(list_of_enemies)
def update_enemy(post100):
	list_of_killed = []
	for idx,enemy in enumerate(list_of_enemies):
		enemy[0] += enemy[2]
		enemy[4] += 1
		if enemy[3] == 'pidgey':
			if not post100:enemy[1]+= cos(enemy[4]/15)/2
			elif post100: enemy[1] += sin(enemy[4]/15)
		if enemy[6] >= 1:
			for idx2,bullet in enumerate(bullet_list):
				if (bullet[0] <= enemy[0]+40 and bullet[0] >= enemy[0]-10) and (bullet[1] >= enemy[1]-10 and bullet[1] <= enemy[1]+40):
					bullet_list.pop(idx2)
					enemy[5] -= 1
					enemy[6] = 0

		else:
			enemy[6] += 0.15



		if enemy[0] > 405 or enemy[0] < -45:
			list_of_enemies.pop(idx)
		if enemy[5] <= 0:
			list_of_enemies.pop(idx)
			list_of_killed.append(1)
	return len(list_of_killed)
def draw_enemy():
	for enemy in list_of_enemies:
		if enemy[3] == 'pidgey': indexuno = 1
		elif enemy[3] == 'rattata': indexuno = 0
		if enemy[2] > 0: indexdos = 1
		elif enemy[2] < 0: indexdos = 0
		screen.blit(enemystates[indexuno][indexdos],(enemy[0],enemy[1]))

def takedamage():
	damagetaken = 0
	if player.vulnerable >= 1:
		for enemy in list_of_enemies:
			if (player.x >= enemy[0]-32 and player.x <= enemy[0]+40) and ((player.y >= enemy[1]-40 and player.y <= enemy[1]+32) or (player.y-200 >= enemy[1]-40 and player.y-200 <= enemy[1]+32)):
#				print('collision')
				damagetaken += 1
				soundeffects[3].play()
				player.vulnerable = 0
	else:
		player.vulnerable += 0.02
	return damagetaken


screen = pygame.display.set_mode((400,400))
pygame.display.set_caption("Pika.2 release 1.0")
icon = pygame.image.load('pstateleft.png')
playerstates = [[pygame.image.load('pstateleft.png'),pygame.image.load('pstateleft2.png')],[pygame.image.load('pstateright.png'),pygame.image.load('pstateright2.png')]]
ground = pygame.image.load('ground.png')
bgsky = [pygame.image.load('bg.png'),pygame.image.load('bg2.png'),pygame.image.load('bg3.png'),pygame.image.load('bg4.png'),pygame.image.load('bg5.png'),pygame.image.load('bg6.png'), pygame.image.load('bg7.png'),pygame.image.load('bg8.png'),pygame.image.load('bg9.png'),pygame.image.load('bg10.png')]
title_card = pygame.image.load('titlecard.png')
bullets = pygame.image.load('zapparticle1.png')
enemystates = [[pygame.image.load('rattataleft.png'),pygame.image.load('rattataright.png')],[pygame.image.load('pidgeyleft.png'),pygame.image.load('pidgeyright.png')]]
soundeffects = [pygame.mixer.Sound('soundeffect1.wav'),pygame.mixer.Sound('zap.wav'),pygame.mixer.Sound('jumpy.wav'),pygame.mixer.Sound('hit.wav')]
hearts = [pygame.image.load('0hearts.png'),pygame.image.load('1heart.png'),pygame.image.load('2hearts.png'),pygame.image.load('3hearts.png')]
mixer.music.load('bgmusic.mp3')
mixer.music.play(-1)
pygame.display.set_icon(icon)
player = Player(100,308,1,0,3,1)
FPS = 60
clock = pygame.time.Clock()
player_speed = 4
pygame.font.init()
score = 0
score_font = pygame.font.Font('8bit.ttf',14)
text_surface = score_font.render('SCORE: ' +str(score),False,(255,255,255))

while True:
	is_title_card = True
	while is_title_card:
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						soundeffects[0].play()
						is_title_card = False
		screen.blit(title_card,(0,0))
		show_score(10,0)
#		print(pygame.mouse.get_pos())
		pygame.display.update()


	moving_left = False
	moving_right = False
	is_jumping = False
	initial_time = pygame.time.get_ticks()
	bullet_list = []
	list_of_enemies = []
	list_of_hostile_projectiles = []
	game_running = True
	summon_enemies = False
	player.health = 3
	score = 0
	player = Player(100,308,1,0,3,1)
	morethancien = False
	rat_health = 2
	bird_health = 1
	while game_running:
		enemy_key = {
			69: ['x','y','directionspeed;(-1 is left)','enemy_type','internal_timer','health','vulnerable?'],
			0: [-40,100,1,'rattata',0,rat_health,True],
			1: [-40,50,2,'pidgey',0,bird_health,True],
			2: [400,100,-1,'rattata',0,rat_health,True],
			3: [400,50,-2,'pidgey',0,bird_health,True],
			4: [-40,300,1,'rattata',0,rat_health,True],
			5: [-40,250,2,'pidgey',0,bird_health,True],
			6: [400,300,-1,'rattata',0,rat_health,True],
			7: [400,250,-2,'pidgey',0,bird_health,True]
		}
		game_timer = pygame.time.get_ticks() - initial_time

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()


			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					player.state = 0
					moving_left = True
				if event.key == pygame.K_RIGHT:
					player.state = 1
					moving_right = True
				if event.key == pygame.K_UP:
					if not is_jumping:
						soundeffects[2].play()
						jumpt_0 = game_timer
						is_jumping = True
				if event.key == pygame.K_DOWN:
					soundeffects[1].play()
					fire_bullets(player.x,player.y)
					fire_bullets(player.x,player.y-200)
#				if event.key == pygame.K_e:
#					score += 1
#					print(score)
				if event.key == pygame.K_SPACE:
					if not (is_jumping or moving_left or moving_right):
						player.y = 318
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					moving_left = False
				if event.key == pygame.K_RIGHT:
					moving_right = False
				if event.key == pygame.K_SPACE:
					player.y = 308

		if moving_left:
			player.x -= player_speed
			if player.x < 0:
				player.x += player_speed
			player.frame = int(game_timer/200)%2
		if moving_right:
			player.x += player_speed
			if player.x > 368:
				player.x -= player_speed
			player.frame = int(game_timer/200)%2
		if not (moving_right or moving_left):
			player.frame = 0


		if is_jumping:
			if (game_timer - jumpt_0) < 500:
				player.y = 308 + 1200*((game_timer - jumpt_0)/1000)**2 - 600*((game_timer - jumpt_0)/1000)
			else:
				player.y = 308
				is_jumping = False

		if game_timer > 5000:
			summon_enemies = True
		

		if player.health <= 0:
			game_running = False

		screen.fill((255,255,255))

		screen.blit(bgsky[int(score/20)%len(bgsky)],(0,0))
		screen.blit(bgsky[int(score/20)%len(bgsky)],(0,200))
		screen.blit(ground,(0,0))
		screen.blit(ground,(0,-200))
		screen.blit(hearts[player.health],(250,0))

		update_bullets()
		draw_bullets()
		if score >= 20:
			rat_health = 3
		if score >= 60:
			morethancien = True
		if score >= 120:
			rat_health = 4
		if score >= 160:
			bird_health = 2
		if summon_enemies:
			generate_enemy(game_timer)
			score += update_enemy(morethancien)
			draw_enemy()
			player.health -= takedamage()

		player.draw_player()
		player.draw_player_u()

		text_surface = score_font.render('SCORE: ' +str(score),False,(255,255,200))
		show_score(10,0)


#		print(pygame.mouse.get_pos())
#		print(bullet_list)
#		print(list_of_enemies)


		pygame.display.update()
		clock.tick(FPS)

