import threading
import pygame, random, sys, re, time, numpy as np
import tkinter as tk
from knight_hunting import sub_game as game1
from cheems import  sub_game as game2
from keras.models import load_model
import gensim.models.keyedvectors as keyedvectors

userdata = []
pow = []
MOD = int(1e9) + 9277


def prep_hash():
	BASE = 256
	MAX = 320

	global pow, MOD

	pow.append(1)
	for i in range(1, MAX):
		pow.append(pow[i - 1] * BASE % MOD)

def trans_list(data):
	global userdata
	for line in data:
		number = ""
		tmp = []
		for i in range(0, len(line)):
			if line[i] == '\n':
				break
			if line[i] == ' ':
				tmp.append(number)
				number = ""
			else: 
				number += line[i]
		userdata.append(tmp)

def trans_str():
	info = str("")
	for i in userdata:
		tmp = str("")
		for j in i:
			tmp += str(j) + ' '
		info += tmp
		info += '\n'
	file = open("./asset/data/userdata.txt", "w")
	file.write(info)
	file.close()

try:
	# file = open("./asset/data/userdata.txt", "a")
	# file.close()
	file = open("./asset/data/userdata.txt", "r+")
	data = file.readlines()
	trans_list(data)
	file.close()
except FileNotFoundError:
	print("File not Found.")
	exit()	

# --------------------------------------------------------------------------------

# FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Define Colors
GREEN = (13, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 3, 3)
GRAY = (80, 80, 80)
WHITE = (255, 255, 255)

play = None
pos = 0
history = []

# --------------------------------------------------------------------------------

def get_data_playing():
	global userdata, history

	if (len(userdata[pos]) < 4):
		userdata[pos].append(0)
		userdata[pos].append(0)
		return

	for i in range(5, len(userdata[pos]), 3):
		history.append([userdata[pos][i], userdata[pos][i + 1], userdata[pos][i + 2]])

def save_data_playing(gold, items, history):
	global userdata, pos
	
	userdata[pos][3] = gold
	userdata[pos][4] = items
	while len(userdata[pos]) > 5:
		userdata[pos].pop()
	for i in range(len(history) - 1, -1, -1):
		userdata[pos].insert(5, history[i][2])
		userdata[pos].insert(5, history[i][1])
		userdata[pos].insert(5, history[i][0])
	
	trans_str()

def game_frame():
	# Create Display Surface(SCALE = 16 / 9)


	class Button():
		def __init__(self, x, y, image, scale):
			width = image.get_width()
			height = image.get_height()
			self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
			self.rect = self.image.get_rect()
			self.rect.center = (x, y)
			self.pos_unhover = (x, y)
			self.pos_hover = (x, y - 3)
			self.origin_rect = self.image.get_rect()
			self.origin_rect.center = (x, y)
		
		def draw(self, surface):
			surface.blit(self.image, self.rect)
			pos = pygame.mouse.get_pos()
			if self.origin_rect.collidepoint(pos):
				self.rect.center = self.pos_hover
			else:
				self.rect.center = self.pos_unhover


	class Thumb_nail():
		def __init__(self, x, y, image, circle = False):
			width = image.get_width()
			height = image.get_height()
			self.image = pygame.transform.scale(image, (width, height))
			self.rect = self.image.get_rect()
			self.rect.topleft = (x, y)
			self.pos_unhover = (x, y)
			self.pos_hover = (x, y + 30)
			self.click = False
			self.origin_rect = self.image.get_rect()
			self.origin_rect.center = (x, y)
			self.circle = circle
		
		def draw(self, surface):
			surface.blit(self.image, self.rect)
			pos = pygame.mouse.get_pos()
			if self.origin_rect.collidepoint(pos) or self.click:
				if not self.circle:
					self.rect.center = self.pos_hover
				else:
					pygame.draw.circle(surface, GREEN, (self.rect.centerx
					                                    , self.rect.bottom + 20.0 / 1200 * my_game.WINDOW_WIDTH)
					                   , 10.0 / 1200 * my_game.WINDOW_WIDTH)
			else:
				self.rect.center = self.pos_unhover


	class Item_skill(pygame.sprite.Sprite):
		def __init__(self, type, index, image, group, player):
			super().__init__()
			self.index = index
			self.type = type
			self.image = image
			self.item_group = group
			self.rect = self.image.get_rect()
			self.player = player
			self.rect.centery = player.rect.centery
			self.rect.left = player.rect.right
			distance = my_game.map_rect.right - player.rect.right
			if player.running == False:
				self.remove(group)
			if distance > 200:
				self.rect.x += random.randint(100
											, min(500, int(distance - self.image.get_width())))
		
		def update(self):
			if not self.player.running:
				self.remove(self.item_group)
			if my_game.scroll_map_bool:
				self.rect.x -= my_game.scroll_map
			if pygame.sprite.collide_rect(self, self.player):
				# Set timeskill
				if self.type == 1:
					self.player.speed_up_time += FPS  # one second
				elif self.type == 2:
					self.player.slow_down_time += FPS  # three seconds
				elif self.type == 3:
					self.player.positionx += 150  #
					if self.player.rect.right + 150 >= my_game.map_rect.right and \
						my_game.map_rect.right > my_game.WINDOW_WIDTH:
						self.player.win_absolute = True
					self.player.pos_tele = self.player.rect.topleft
					self.player.tele_frame = 5
				elif self.type == 4:
					self.player.reverse_time += FPS
				elif self.type == 5:
					self.player.pos_tele = self.player.rect.topleft
					self.player.tele_frame = 5
					self.player.rect.right = my_game.map_rect.right
					if my_game.map_rect.right > my_game.WINDOW_WIDTH:
						self.player.win_absolute = True
					
				elif self.type == 6:
					self.player.positionx = my_game.map_rect.left
					self.player.pos_tele = self.player.rect.topleft
					self.player.tele_frame = 5
				self.remove(self.item_group)
				if my_game.music:
					my_game.collect_sound.play()
	
	class Text:
		def __init__(self, text, font, x, y, center = False, color = YELLOW, hover = True):
			self.text = text
			self.font = font
			self.color = color
			self.font = font
			self.text_surface = self.font.render(self.text, True, self.color)
			self.text_rect = self.text_surface.get_rect()
			self.text_rect.topleft = (x, y)
			self.need_hover = hover
			if center:
				self.text_rect.center = (x, y)
			self.hover = False
			self.click = False
		
		def draw(self, surface):
			if self.need_hover:
				if self.hover:
					self.color = GREEN
				elif self.click:
					self.color = GREEN
				else:
					self.color = YELLOW
			
			self.text_surface = self.font.render(self.text, True, self.color)
			
			surface.blit(self.text_surface, self.text_rect)


	class Game():
		def __init__(self, gold, items, history):
			#Load variable
			self.has_load_map = False
			self.has_load_bet = False
			self.has_load_set = False
			self.has_load_skill = False
			self.has_load_shop = False
			# display value
			self.WINDOW_WIDTH = 1200
			self.WINDOW_HEIGHT = 675
			self.display_surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
			
			self.scroll = 0
			self.direction_scroll = 1
			
			self.user_name =  str(userdata[pos][0])
			
			# sound
			self.collect_sound = pygame.mixer.Sound("./asset/music/collect_music.wav")
			self.race_music = pygame.mixer.Sound("./asset/music/race_music.mp3")
			self.yeah_sound = pygame.mixer.Sound("./asset/music/yeah.wav")
			
			# Game Value, SET in TEXT file
			self.gold = int(gold)
			self.map = 1
			self.set = 1
			self.bet = 1
			self.rank = []
			self.history = history
			self.own_item = int(items)
			
			#font text
			self.show_text_chat = u""
			
			#setting variable
			self.music = True
		
		def main(self):
			# Music
			self.menu_music = pygame.mixer.Sound("./asset/music/menu_music.mp3")
			self.menu_music.set_volume(.2)
			self.show_main_menu()
		
		def load_map(self):
			# load show map
			self.map_thumbnail_images = []
			for i in range(1, 7):
				image = pygame.image.load(f"./asset/map/showmap{i}.png")
				image = pygame.transform.scale(image, (int(0.271 * self.WINDOW_WIDTH), int(0.271 * self.WINDOW_HEIGHT)))
				self.map_thumbnail_images.append(image)
			
			self.map_thumbnail = []
			# Chua te hard code
			for i in range(6):
				if i <= 2:
					self.map_thumbnail.append(
						Button(int(i * (self.map_thumbnail_images[i].get_width() + 0.040 * self.WINDOW_WIDTH)
								+ 0.051 * self.WINDOW_WIDTH + self.map_thumbnail_images[i].get_width() / 2),
							int(0.314 * self.WINDOW_HEIGHT)
							, self.map_thumbnail_images[i], 1))
				else:
					self.map_thumbnail.append(
						Button(int((i - 3) * (self.map_thumbnail_images[i].get_width() + 0.040 * self.WINDOW_WIDTH)
								+ 0.051 * self.WINDOW_WIDTH + self.map_thumbnail_images[i].get_width() / 2),
							int((0.314 + 0.377) * self.WINDOW_HEIGHT), self.map_thumbnail_images[i], 1))
			self.has_load_map = True
		
		def load_set(self):
			# Load show set
			images = []
			for i in range(6):
				image = pygame.image.load(f"./asset/set/set_avt/all_set_{i + 1}.png")
				image = pygame.transform.scale(image,
											(int(0.286 * self.WINDOW_HEIGHT), int(0.286 * self.WINDOW_HEIGHT)))
				images.append(image)
			
			self.sets_thumbnail = []
			# Chua te hard code
			for i in range(6):
				if i <= 2:
					self.sets_thumbnail.append(
						Button(int(0.192 * self.WINDOW_WIDTH + i * (0.16 + 0.146) * self.WINDOW_WIDTH)
							, int(0.317 * self.WINDOW_HEIGHT), images[i], 1))
				else:
					self.sets_thumbnail.append(
						Button(int(0.192 * self.WINDOW_WIDTH + (i - 3) * (0.16 + 0.146) * self.WINDOW_WIDTH)
							, int(0.7196 * self.WINDOW_HEIGHT), images[i], 1))
			
			# Load Item image
			image = pygame.image.load("./asset/image/lucky_box.png")
			scale = image.get_width() / image.get_height()
			self.item_image = pygame.transform.scale(image, (
				int(scale * self.WINDOW_HEIGHT * 0.11), int(self.WINDOW_HEIGHT * 0.11)))
			self.has_load_set = True
		
		def load_bet(self):
			# Load betting
			self.all_bet_thumbnail_images = []
			for k in range(6):
				temp = []
				for i in range(5):
					image = pygame.image.load(f'./asset/set/set_avt/{k + 1}{i + 1}.png')
					scale = image.get_height() / image.get_width()
					image = pygame.transform.scale(image,
												(int(0.10 * self.WINDOW_WIDTH),
													int(0.10 * self.WINDOW_WIDTH * scale)))
					temp.append(image)
				self.all_bet_thumbnail_images.append(temp)
			self.has_load_bet = True
		
		def load_skill(self):
			self.speed_up_frame = []
			for i in range(8):
				image = pygame.image.load(f"./asset/effectskill/speedup/{i+1}.png")
				scale = image.get_width() / image.get_height()
				image = pygame.transform.scale(image , (self.WINDOW_HEIGHT * 0.3 * scale, self.WINDOW_HEIGHT * 0.11))
				self.speed_up_frame.append(image)
			
			self.slow_down_frame = []
			for i in range(8):
				image = pygame.image.load(f"./asset/effectskill/speeddown/{i + 1}.png")
				scale = image.get_width() / image.get_height()
				image = pygame.transform.scale(image, (self.WINDOW_HEIGHT * 0.3 * scale, self.WINDOW_HEIGHT * 0.11))
				self.slow_down_frame.append(image)
			
			self.reverse_frame = []
			for i in range(9):
				image = pygame.image.load(f"./asset/effectskill/return/{i + 1}.png")
				scale = image.get_width() / image.get_height()
				image = pygame.transform.scale(image, (self.WINDOW_HEIGHT * 0.3 * scale, self.WINDOW_HEIGHT * 0.11))
				self.reverse_frame.append(image)
				
			self.tele_frame = []
			for i in range(5):
				image = pygame.image.load(f"./asset/effectskill/teleport/{i + 1}.png")
				scale = image.get_width() / image.get_height()
				image = pygame.transform.scale(image, (self.WINDOW_HEIGHT * 0.2 * scale, self.WINDOW_HEIGHT * 0.11))
				self.tele_frame.append(image)
				
			#finish
			self.has_load_skill = True
		def load_race(self):

			# Set back map
			self.backmap = pygame.image.load(f"./asset/map/backmap{self.map}.jpg")
			scale = self.backmap.get_width() / self.backmap.get_height()
			self.backmap = pygame.transform.scale(self.backmap, (self.WINDOW_HEIGHT * scale, self.WINDOW_HEIGHT))
			self.backmap_rect = self.backmap.get_rect()
			self.backmap_rect.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2)
			
			#load
			image = pygame.image.load(f"./asset/image/lucky_box.png")
			scale = image.get_width() / image.get_height()
			image = pygame.transform.scale(image, (self.WINDOW_HEIGHT*0.12 * scale, self.WINDOW_HEIGHT*0.12))
			self.use_item_button = Button((1-0.084)* self.WINDOW_WIDTH, (1-0.12)*self.WINDOW_HEIGHT,image , 1)

			# Add Character
			self.player_group = pygame.sprite.Group()
			for i in range(1, 6):
				player = Player(i, 0, self.WINDOW_HEIGHT * 0.263 + (i - 1) * self.WINDOW_HEIGHT * 0.174, self.player_group)
				self.player_group.add(player)
				if i == self.bet:
					self.user_player = player
			self.has_load_player = True
		
		def load_shop(self):
			# text shop button
			image = pygame.image.load("./asset/image/shop.png")
			scale = image.get_width() / image.get_height()
			self.shop_text = pygame.transform.scale(image,
			                                        (self.WINDOW_HEIGHT * 0.13 * scale, self.WINDOW_HEIGHT * 0.13))
			# buy now button
			image = pygame.image.load("./asset/button/button_buy_now.png")
			scale = image.get_width() / image.get_height()
			self.buy_button_actived = pygame.transform.scale(image, (self.WINDOW_HEIGHT // 8 * scale
			                                                         , self.WINDOW_HEIGHT // 8))
			image = pygame.image.load("./asset/button/button_buy_now_unactive.png")
			self.buy_button_unactived = pygame.transform.scale(image,
			                                                   (self.WINDOW_HEIGHT // 8 * scale,
			                                                    self.WINDOW_HEIGHT // 8))
			# coin
			image = pygame.image.load("./asset/image/coin.png")
			scale = image.get_width() / image.get_height()
			self.coin = pygame.transform.scale(image, (self.WINDOW_HEIGHT * 0.1 * scale, self.WINDOW_HEIGHT * 0.1))
			
			self.has_load_shop = True
		
		def show_main_menu(self):
			if not self.has_load_map:
				self.load_map_thread = threading.Thread(target=self.load_map)
				self.load_map_thread.start()
			if not self.has_load_set:
				self.load_set_thread = threading.Thread(target=self.load_set)
				self.load_set_thread.start()
			if not self.has_load_bet:
				self.load_bet_thread = threading.Thread(target=self.load_bet)
				self.load_bet_thread.start()
			if not self.has_load_skill:
				self.load_skill_thread = threading.Thread(target=self.load_skill)
				self.load_skill_thread.start()
			if not self.has_load_shop:
				self.load_shop_thread = threading.Thread(target=self.load_shop)
				self.load_shop_thread.start()
				
			# Load background
			image = pygame.image.load("./asset/image/back.webp").convert()
			scale = int(image.get_width() / image.get_height())
			self.back_ground_image = pygame.transform.scale(image, (int(self.WINDOW_HEIGHT * scale), self.WINDOW_HEIGHT))
			
			# Button menu
			#new game button
			image = pygame.image.load("./asset/button/button_new-game.png")
			scale = image.get_width() / image.get_height()
			image = pygame.transform.scale(image, (self.WINDOW_HEIGHT* 0.11 * scale, self.WINDOW_HEIGHT * 0.11))
			start_button = Button(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT* 0.28,
								image, 1)
			#settings button
			image = pygame.image.load("./asset/button/button_settings.png")
			scale = image.get_width() / image.get_height()
			image = pygame.transform.scale(image, (self.WINDOW_HEIGHT * 0.11 * scale, self.WINDOW_HEIGHT * 0.11))
			setting_button = Button(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT * 0.443 ,
									image, 1)
			
			#shop button
			image = pygame.image.load("./asset/button/button_shop.png")
			scale = image.get_width() / image.get_height()
			image = pygame.transform.scale(image, (self.WINDOW_HEIGHT * 0.11 * scale, self.WINDOW_HEIGHT * 0.11))
			shop_button = Button(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT * 0.6,
			                        image, 1)
			
			#help button
			image = pygame.image.load("./asset/button/button_help.png")
			scale = image.get_height() / image.get_width()
			image = pygame.transform.scale(image, (int(0.15 * self.WINDOW_WIDTH)
			                                       , int(scale * 0.15 * self.WINDOW_WIDTH)))
			
			help_button = Button(int((1 - 0.07) * self.WINDOW_WIDTH)
			                     , int(0.92 * self.WINDOW_HEIGHT), image, 1)
			
			#User button
			image = pygame.image.load("./asset/button/button_user.png")
			scale = image.get_height() / image.get_width()
			image = pygame.transform.scale(image, (int(0.15 * self.WINDOW_WIDTH)
			                                       , int(scale * 0.15 * self.WINDOW_WIDTH)))
			
			user_button = Button(int((0.03 + 0.075) * self.WINDOW_WIDTH)
			                     , int(0.88 * self.WINDOW_HEIGHT), image, 1)
			
			#Mini game button
			image = pygame.image.load("./asset/button/button_minigame.png")
			scale = image.get_width() / image.get_height()
			image = pygame.transform.scale(image, (self.WINDOW_HEIGHT * 0.11 * scale, self.WINDOW_HEIGHT * 0.11))
			mini_game_button = Button(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT * 0.76,
			                        image, 1)
			#game_text
			image = pygame.image.load("./asset/image/lifeislie.png")
			scale = image.get_width() / image.get_height()
			life_is_lie = pygame.transform.scale(image, (self.WINDOW_HEIGHT * 0.13 * scale, self.WINDOW_HEIGHT * 0.13))
			life_is_lie_rect = life_is_lie.get_rect()
			life_is_lie_rect.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT//10)
			
			# Font (Set here because the height can be change from the settings options)
			self.font32 = pygame.font.Font("./asset/font/font1.ttf", self.WINDOW_WIDTH // 32 + 1)
			self.font19 = pygame.font.Font("./asset/font/aachenb.ttf", self.WINDOW_WIDTH // 64 + 1)
			self.font17 = pygame.font.Font("./asset/font/aachenb.ttf", self.WINDOW_WIDTH // 71 + 1)
			self.font64 = pygame.font.Font("./asset/font/aachenb.ttf", self.WINDOW_WIDTH // 25 + 1)
			
			self.menu_music.stop()
			if self.music:
				self.menu_music.play(-1)
			
			main_menu_run = True
			while main_menu_run:
				self.show_back_ground()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					# CHECK CLICK BUTTON
					if event.type == pygame.MOUSEBUTTONDOWN:
						pos = pygame.mouse.get_pos()
						if start_button.rect.collidepoint(pos):
							if self.has_load_map:
								self.start_new_round()
						if help_button.rect.collidepoint(pos):
							self.show_help()
						if shop_button.rect.collidepoint(pos):
							if self.has_load_shop:
								self.show_shop()
						if setting_button.rect.collidepoint(pos):
							self.show_setting()
						if mini_game_button.rect.collidepoint(pos):
							self.show_minigame()
						if user_button.rect.collidepoint(pos):
							self.show_user()
						
				start_button.draw(self.display_surface)
				setting_button.draw(self.display_surface)
				help_button.draw(self.display_surface)
				shop_button.draw(self.display_surface)
				mini_game_button.draw(self.display_surface)
				user_button.draw(self.display_surface)
				
				self.display_surface.blit(life_is_lie, life_is_lie_rect)
				pygame.display.update()
				clock.tick(FPS)
		
		def show_help(self):
			
			# GO BACK BUTTON
			image = pygame.image.load("./asset/button/go_back_button.png")
			scale = image.get_width() / image.get_height()
			image = pygame.transform.scale(image,
			                               (int(0.0688 * self.WINDOW_HEIGHT * scale), int(0.0688 * self.WINDOW_HEIGHT)))
			go_back_button = Button(int(0.051 * self.WINDOW_WIDTH + image.get_width() / 2),
			                        int(0.075 * self.WINDOW_HEIGHT),
			                        image, 1)
			image = pygame.image.load("./asset/image/help.png")
			help_image = pygame.transform.scale(image, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
			
			helping = True
			while helping:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						pos = pygame.mouse.get_pos()
						# Check click Map
						if go_back_button.rect.collidepoint(pos):
							helping = False
						
				self.show_back_ground()
				#show the help
				self.display_surface.blit(help_image, (0,0))
				# DRAW BUTTON
				go_back_button.draw(self.display_surface)
				pygame.display.update()
				clock.tick(FPS)
		
		def show_user(self):
			
			# GO BACK BUTTON
			image = pygame.image.load("./asset/button/go_back_button.png")
			scale = image.get_width() / image.get_height()
			image = pygame.transform.scale(image,
			                               (int(0.0688 * self.WINDOW_HEIGHT * scale), int(0.0688 * self.WINDOW_HEIGHT)))
			go_back_button = Button(int(0.051 * self.WINDOW_WIDTH + image.get_width() / 2),
			                        int(0.075 * self.WINDOW_HEIGHT),
			                        image, 1)
			
			user_image = pygame.image.load("./asset/image/user_page.png")
			user_image = pygame.transform.scale(user_image, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
			
			#load history [self.bet, self.map_length, sign * self.bet_money]
			type_map = ["SHORT MAP", "MEDIUM MAP", "LONG MAP"]
			history_text = []
			dis = self.WINDOW_WIDTH // 32 + 1
			for i , item in enumerate(self.history):
				temp = []
				temp.append(Text(f"{abs(int(item[2]))}", self.font32 ,int(.13 * self.WINDOW_WIDTH)
				                 ,int( (0.33 + i * 0.06) * self.WINDOW_HEIGHT + i * dis ), center=True,hover=False))
				
				temp.append(Text(f"{type_map[int(item[1])-2]}", self.font32, int(.4 * self.WINDOW_WIDTH)
				                 , int((0.33 + i * 0.06) * self.WINDOW_HEIGHT + i * dis), center=True,hover=False))
				
				temp.append(Text(f" {item[0]}", self.font32, int(.64 * self.WINDOW_WIDTH)
				                 , int((0.33 + i * 0.06) * self.WINDOW_HEIGHT + i * dis), center=True,hover=False))
				if (int(item[2]) > 0):
					temp.append(Text(f"+{item[2]}", self.font32, int(.86 * self.WINDOW_WIDTH)
				                 , int((0.33 + i * 0.06) * self.WINDOW_HEIGHT + i * dis), center=True, color=GREEN
					                 ,hover=False))
				else:
					temp.append(Text(f"{item[2]}", self.font32, int(.86 * self.WINDOW_WIDTH)
					                 , int((0.33 + i * 0.06) * self.WINDOW_HEIGHT + i * dis), center=True,
					                 color=RED,hover=False))
				history_text.append(temp)
			helping = True
			while helping:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						pos = pygame.mouse.get_pos()
						# Check click Map
						if go_back_button.rect.collidepoint(pos):
							helping = False
				
				self.show_back_ground()
				
				#Draw the history skeletons
				
				self.display_surface.blit(user_image, (0 ,0))
				for grp in history_text:
					for item in grp:
						item.draw(self.display_surface)
				# DRAW BUTTON
				go_back_button.draw(self.display_surface)
				pygame.display.update()
				clock.tick(FPS)
		
		def show_minigame(self):
			
			# GO BACK BUTTON
			image = pygame.image.load("./asset/button/go_back_button.png")
			scale = image.get_width() / image.get_height()
			image = pygame.transform.scale(image,
			                               (int(0.0688 * self.WINDOW_HEIGHT * scale), int(0.0688 * self.WINDOW_HEIGHT)))
			go_back_button = Button(int(0.051 * self.WINDOW_WIDTH + image.get_width() / 2),
			                        int(0.075 * self.WINDOW_HEIGHT),
			                        image, 1)
			#button start game
			image = pygame.image.load("./asset/button/button_start.png")
			scale = image.get_width() / image.get_height()
			image = pygame.transform.scale(image , (self.WINDOW_HEIGHT * .12 * scale, self.WINDOW_HEIGHT * .12))
			left_button = Button(int(0.26 * self.WINDOW_WIDTH), int(self.WINDOW_HEIGHT * .84) ,image , 1)
			right_button = Button(int(0.73 * self.WINDOW_WIDTH), int(self.WINDOW_HEIGHT * .84) ,image , 1)
			
			
			#image mini game
			image = pygame.image.load("./asset/image/minigame1.png")
			scale = image.get_width() / image.get_height()
			knight_image = pygame.transform.scale(image,(int(self.WINDOW_HEIGHT * 0.45 * scale)
			                                             , int(self.WINDOW_HEIGHT * 0.45) ) )
			knight_image_rect = knight_image.get_rect()
			knight_image_rect.center = (0.26 * self.WINDOW_WIDTH, self.WINDOW_HEIGHT *0.4)
			
			image = pygame.image.load("./asset/image/minigame2.png")
			scale = image.get_width() / image.get_height()
			cheems_image = pygame.transform.scale(image,(int(self.WINDOW_HEIGHT * 0.45 * scale)
			                                             , int(self.WINDOW_HEIGHT * 0.45) ) )
			cheems_image_rect = cheems_image.get_rect()
			cheems_image_rect.center = (0.73 * self.WINDOW_WIDTH, self.WINDOW_HEIGHT *0.4)
			
			playing = True
			while playing:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						pos = pygame.mouse.get_pos()
						# Check click Map
						if go_back_button.rect.collidepoint(pos):
							playing = False
						#Check click game 1
						if left_button.rect.collidepoint(pos):
							self.menu_music.stop()
							self.gold = game1(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.display_surface, self.gold, self.music)
							save_data_playing(self.gold, self.own_item, self.history)
							if self.music:
								self.menu_music.play(-1)
						#CHeck click game 2
						if right_button.rect.collidepoint(pos):
							self.menu_music.stop()
							self.gold = game2(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.gold, self.music)
							save_data_playing(self.gold, self.own_item, self.history)
							if self.music:
								self.menu_music.play(-1)
				self.show_back_ground()
				#blit game image
				self.display_surface.blit(knight_image, knight_image_rect)
				self.display_surface.blit(cheems_image, cheems_image_rect)
				
				# DRAW BUTTON
				go_back_button.draw(self.display_surface)
				left_button.draw(self.display_surface)
				right_button.draw(self.display_surface)
				pygame.display.update()
				clock.tick(FPS)
		
		def show_shop(self):
			# GO BACK BUTTON
			image = pygame.image.load("./asset/button/go_back_button.png")
			scale = image.get_width() / image.get_height()
			image = pygame.transform.scale(image,
			                               (int(0.0688 * self.WINDOW_HEIGHT * scale), int(0.0688 * self.WINDOW_HEIGHT)))
			go_back_button = Button(int(0.051 * self.WINDOW_WIDTH + image.get_width() / 2),
			                        int(0.075 * self.WINDOW_HEIGHT),
			                        image, 1)
			
			
			
			# buy variable
			can_buy = self.gold >= 500 and self.own_item <= 2
			
			#buy now
			
			if can_buy:
				buy_button = Button(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT*0.84, self.buy_button_actived, 1)
			else:
				buy_button = Button(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT*0.84, self.buy_button_unactived, 1)

			#lucky box
			image = pygame.image.load("./asset/image/gift_box.png")
			scale = image.get_width() / image.get_height()
			gift_box = pygame.transform.scale(image, (self.WINDOW_HEIGHT *0.45 * scale, self.WINDOW_HEIGHT*0.45))
			gift_box_rect = gift_box.get_rect()
			gift_box_rect.center = (self.WINDOW_WIDTH //2, self.WINDOW_HEIGHT *0.3)
			
			#coin
			
			coin_rect = self.coin.get_rect()
			coin_rect.centery = self.WINDOW_HEIGHT * 0.6
			coin_rect.left = self.WINDOW_WIDTH // 2.7
			
			# user gold text
			gold_text = self.font64.render(f'{self.gold}', True, YELLOW)
			gold_text_rect = gold_text.get_rect()
			gold_text_rect.centery = self.WINDOW_HEIGHT * 0.6
			gold_text_rect.left = coin_rect.right + self.WINDOW_WIDTH * (20.0 / 1200)
			
			price = max(self.gold // 10, 500)
			price_text = self.font64.render(f'-{price}', True, RED)
			price_text_rect = price_text.get_rect()
			price_text_rect.topleft = gold_text_rect.bottomleft
			price_text_rect.y += self.WINDOW_HEIGHT * (25.0 / 675)
			
			# shop text
			shop_text_rect = self.shop_text.get_rect()
			shop_text_rect.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 10)
			
			#owner items text
			item_count = self.font64.render(f"X {self.own_item}", True ,GREEN)
			item_count_rect = item_count.get_rect()
			item_count_rect.centery = gift_box_rect.centery + self.WINDOW_HEIGHT * (15.0 / 675)
			item_count_rect.left = gift_box_rect.right
			
			#sound
			buy_item_sound = pygame.mixer.Sound("./asset/music/buy_item_sound.wav")
			
			
			
			shopping = True
			while shopping:
				can_buy = self.gold >= price and self.own_item <= 2
				if can_buy:
					buy_button.image = self.buy_button_actived
				else:
					buy_button.image = self.buy_button_unactived
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						save_data_playing(self.gold, self.own_item, self.history)
						pygame.quit()
						sys.exit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						pos = pygame.mouse.get_pos()
						# Check click Map
						if go_back_button.rect.collidepoint(pos):
							shopping = False
						if buy_button.rect.collidepoint(pos):
							if can_buy:
								self.gold -= price
								self.own_item += 1
								if self.music:
									buy_item_sound.play()
				
				self.show_back_ground()
				# DRAW BUTTON
				go_back_button.draw(self.display_surface)
				buy_button.draw(self.display_surface)
				
				#shop text
				self.display_surface.blit(self.shop_text, shop_text_rect)
				
				
				#User gold text
				gold_text = self.font64.render(f'{self.gold}', True, YELLOW) #rerender the gold text
				price = max((self.gold // 1000) * 100, 500)
				price_text = self.font64.render(f'-{price}', True, RED) #rerender price
				if self.own_item == 3:
					item_count = self.font64.render(f"X {self.own_item} (MAX)", True, GREEN) #rerender the items
				else:
					item_count = self.font64.render(f"X {self.own_item}", True, GREEN)  # rerender the items
				self.display_surface.blit(gold_text, gold_text_rect)
				self.display_surface.blit(price_text, price_text_rect)
				self.display_surface.blit(item_count, item_count_rect)
				# lucky box and coin
				self.display_surface.blit(gift_box, gift_box_rect)
				self.display_surface.blit(self.coin, coin_rect)
				
				pygame.display.update()
				clock.tick(FPS)
			
			save_data_playing(self.gold, self.own_item, self.history)
				
		def show_back_ground(self):
			if self.scroll <= 0:
				self.direction_scroll = 1
			if self.scroll >= self.back_ground_image.get_width() - self.WINDOW_WIDTH:
				self.direction_scroll = -1
			self.scroll += self.direction_scroll * .5 * my_game.WINDOW_WIDTH * 1.0 / 1200
			self.display_surface.blit(self.back_ground_image, (-self.scroll, 0))
		
		def start_new_round(self):
			self.show_map()
		
		def show_setting(self):
			
			image = pygame.image.load("./asset/button/go_back_button.png")
			scale = image.get_width() / image.get_height()
			image = pygame.transform.scale(image,
										(int(0.0688 * self.WINDOW_HEIGHT * scale), int(0.0688 * self.WINDOW_HEIGHT)))
			# GO BACK BUTTON
			go_back_button = Button(int(0.051 * self.WINDOW_WIDTH + image.get_width() / 2), int(0.075 * self.WINDOW_HEIGHT),
									image, 1)
			
			# setting option button
			image = pygame.image.load("./asset/button/button_resolution.png")
			scale = image.get_width() / image.get_height()
			image = pygame.transform.scale(image,
										(self.WINDOW_HEIGHT // 10 * scale, self.WINDOW_HEIGHT // 10))
			resolution_button = Button(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT * 0.52, image, 1)
			
			image1 = pygame.image.load("./asset/button/button_music.png")
			image2 = pygame.image.load("./asset/button/button_music_off.png")
			scale = image.get_width() / image.get_height()
			music_actived = pygame.transform.scale(image1,
			                               (self.WINDOW_HEIGHT // 10 * scale, self.WINDOW_HEIGHT // 10))
			music_unactived = pygame.transform.scale(image2,
			                                      (self.WINDOW_HEIGHT // 10 * scale, self.WINDOW_HEIGHT // 10))
			if self.music:
				music_button = Button(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT * 0.357 , music_actived , 1)
			else:
				music_button = Button(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT * 0.357 , music_unactived , 1)

			
			setting = True
			while setting:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						pos = pygame.mouse.get_pos()
						# Check click Map
						if go_back_button.rect.collidepoint(pos):
							setting = False
						if resolution_button.rect.collidepoint(pos):
							self.show_resolution()
						if music_button.rect.collidepoint(pos):
							if self.music:
								self.music = False
								music_button.image = music_unactived
								self.menu_music.stop()
							else:
								self.music = True
								music_button.image = music_actived
								self.menu_music.play(-1)
				
				self.show_back_ground()
				# DRAW BUTTON
				go_back_button.draw(self.display_surface)
				resolution_button.draw(self.display_surface)
				music_button.draw(self.display_surface)
				pygame.display.update()
				clock.tick(FPS)
		
		def show_resolution(self):
			# resolution option button
			image = pygame.image.load("./asset/button/800x450.png")
			scale = image.get_width() / image.get_height()
			image = pygame.transform.scale(image, (self.WINDOW_HEIGHT // 10 * scale, self.WINDOW_HEIGHT // 10))
			btn_800x450 = Button(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 3, image, 1)
			
			image = pygame.image.load("./asset/button/1200x675.png")
			image = pygame.transform.scale(image, (self.WINDOW_HEIGHT // 10 * scale, self.WINDOW_HEIGHT // 10))
			btn_1200x675 = Button(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 3 + self.WINDOW_HEIGHT // 6, image, 1)
			
			
			# GO BACK BUTTON
			image = pygame.image.load("./asset/button/go_back_button.png")
			scale = image.get_width() / image.get_height()
			image = pygame.transform.scale(image,
										(int(0.0688 * self.WINDOW_HEIGHT * scale), int(0.0688 * self.WINDOW_HEIGHT)))
			go_back_button = Button(int(0.051 * self.WINDOW_WIDTH + image.get_width() / 2), int(0.075 * self.WINDOW_HEIGHT),
									image, 1)
			resulutioning = True
			while resulutioning:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						pos = pygame.mouse.get_pos()
						# Check click Map
						if go_back_button.rect.collidepoint(pos):
							resulutioning = False
						if btn_800x450.rect.collidepoint(pos):
							self.WINDOW_WIDTH = 800
							self.WINDOW_HEIGHT = 450
							self.display_surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
							self.has_load_bet = False
							self.has_load_map = False
							self.has_load_set = False
							self.has_load_shop = False
							self.show_main_menu()
						
						if btn_1200x675.rect.collidepoint(pos):
							self.WINDOW_WIDTH = 1200
							self.WINDOW_HEIGHT = 675
							self.display_surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
							self.has_load_bet = False
							self.has_load_map = False
							self.has_load_set = False
							self.has_load_shop = False
							self.show_main_menu()
				self.show_back_ground()
				# DRAW BUTTON
				go_back_button.draw(self.display_surface)
				btn_800x450.draw(self.display_surface)
				btn_1200x675.draw(self.display_surface)
				pygame.display.update()
				clock.tick(FPS)
		
		def comment_embedding(self, comment):
			max_seq = 200
			embedding_size = 12
			model_embedding = keyedvectors.KeyedVectors.load('./asset./AI/word_fasttext.model')
    
			word_labels = []
			for word in list(model_embedding.key_to_index.keys()):
				word_labels.append(word)
        
			matrix = np.zeros((max_seq, embedding_size))
			words = comment.split()
			lencmt = len(words)

			for i in range(max_seq):
				indexword = i % lencmt
				if (max_seq - i < lencmt):
					break
				if (words[indexword] in word_labels):
					matrix[i] = model_embedding[words[indexword]]
			matrix = np.array(matrix)
			return matrix

		def preprocess_data(self, comments):
			# Lower case
			comments = comments.lower()
			# Look for one or more characters between 0-9
			comments = re.compile('[0-9]+').sub(' ', comments)
			# Look for strings starting with http:// or https://
			comments = re.compile('(http|https)://[^\s]*').sub(' ', comments)
			# Look for strings with @ in the middle
			comments = re.compile('[^\s]+@[^\s]+').sub(' ', comments)
			# Handle $ sign
			comments = re.compile('[$]+').sub(' ', comments)
			# get rid of repeat letters
			temp = " "
			for letter in comments:
				if (letter != temp[-1]):
					temp += letter
			comments = temp
			# get rid of any punctuation
			comments = re.split('[ #%^&*@$/#.-:&*+=\[\]?!(){},\'">_<;%\n\r\t\|]', comments)
			# remove any empty word string
			comments = [word for word in comments if len(word) > 0]
			comments = " ".join(comments)
    
			return comments

		def AI_evaluate(self, comments):
			model_sentiment = load_model("./asset./AI/models.h5")
			comments = self.preprocess_data(comments)
			if comments == "":
				return 1

			maxtrix_embedding = np.expand_dims(self.comment_embedding(comments), axis=0)
			maxtrix_embedding = np.expand_dims(maxtrix_embedding, axis=3)

			result = model_sentiment.predict(maxtrix_embedding)
			result = result[:,:2]

			result = np.argmax(result)
			print("Label predict: ", result)
			#0 là tiêu cực
			#1 là tích cực
		
			return result
		
		def show_bet(self):
			self.load_race_thread = threading.Thread(target=self.load_race)
			self.load_race_thread.start()
			# Load betting
			self.bet_thumbnail_images = self.all_bet_thumbnail_images[self.set - 1]
			self.bet_thumbnails = []
			for i in range(5):
				thumbnail = Thumb_nail(int(((0.15 + i * (0.1525 + 0.063 / 2)) * self.WINDOW_WIDTH))
									, int(0.195 * self.WINDOW_HEIGHT), self.bet_thumbnail_images[i], circle=True)
				self.bet_thumbnails.append(thumbnail)
			# Load Text
			gold_text = self.font32.render(f'Gold:  {self.gold}', True, YELLOW)
			gold_text_rect = gold_text.get_rect()
			gold_text_rect.topleft = (0.15 * self.WINDOW_WIDTH, int(0.62 * self.WINDOW_HEIGHT))
			
			user_text = f"{min(100, self.gold // 2)}"
			
			bet_text = self.font32.render(f' BET: {user_text}', True, YELLOW)
			bet_text_rect = bet_text.get_rect()
			bet_text_rect.topleft = (int(0.15 * self.WINDOW_WIDTH), int(0.7 * self.WINDOW_HEIGHT))
			
			text_box = pygame.Rect(int(0.15 * self.WINDOW_WIDTH), int(0.7 * self.WINDOW_HEIGHT), self.WINDOW_WIDTH // 3,
								self.WINDOW_HEIGHT // 10)
			color = YELLOW
			active = False
			error = False
			
			bet_text_rect.centery = 0.7 * self.WINDOW_HEIGHT + text_box.h / 2
			
			# Play button
			image = pygame.image.load("./asset/button/play_now_button.png")
			scale = image.get_width() / image.get_height()
			image = pygame.transform.scale(image, (scale * self.WINDOW_HEIGHT * 0.1, self.WINDOW_HEIGHT * 0.1))
			play_button = Button(int(0.8 * self.WINDOW_WIDTH), int(0.72 * self.WINDOW_HEIGHT), image, 1)
			
			# Go back button
			image = pygame.image.load("./asset/button/go_back_button.png")
			scale = image.get_width() / image.get_height()
			image = pygame.transform.scale(image,
										(int(0.0688 * self.WINDOW_HEIGHT * scale), int(0.0688 * self.WINDOW_HEIGHT)))
			go_back_button = Button(int(0.051 * self.WINDOW_WIDTH + image.get_width() / 2), int(0.075 * self.WINDOW_HEIGHT),
									image, 1)
			dis = 15.0 / 1200 * self.WINDOW_WIDTH
			dis_ = 15.0 / 675 * self.WINDOW_HEIGHT
			short_map = Text("SHORT MAP", self.font32,text_box.right + dis , gold_text_rect.top - dis_)
			medium_map = Text("MEDIUM MAP", self.font32, text_box.right + dis , short_map.text_rect.bottom + dis_)
			medium_map.click = True
			long_map = Text("LONG MAP", self.font32, text_box.right + dis, medium_map.text_rect.bottom + dis_)
			map_choose = [short_map, medium_map, long_map]
			
			# User click the thumnail
			have_click = False
			
			betting = True
			while betting:
				if have_click == False:
					for i in range(5):
						if self.bet_thumbnails[i].click:
							have_click = True
							break
				
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if event.type == pygame.MOUSEMOTION:
						pos = pygame.mouse.get_pos()
						for map in map_choose:
							if map.text_rect.collidepoint(pos):
								map.hover = True
							else:
								map.hover = False
					
					if event.type == pygame.MOUSEBUTTONDOWN:
						pos = pygame.mouse.get_pos()
						#Check click map choose
						for map in map_choose:
							if map.text_rect.collidepoint(pos):
								map.click = True
								for submap in map_choose:
									if submap != map:
										submap.click = False
						# Check click GO BaCK
						if go_back_button.rect.collidepoint(pos):
							betting = False
						# CHeck click thumbnail
						for i in range(5):
							if self.bet_thumbnails[i].rect.collidepoint(pos):
								self.bet_thumbnails[i].click = True
								for j in range(5):
									if j == i:
										continue
									self.bet_thumbnails[j].click = False
						# Check Click Box
						if text_box.collidepoint(pos):
							active = True
						else:
							active = False
						
						# Check click play_now
						if play_button.rect.collidepoint(pos):
							if not error and have_click:
								for i in range(5):
									if self.bet_thumbnails[i].click == True:
										self.bet = i + 1
										break
								self.bet_money = int(user_text)
								for i in range(3):
									if map_choose[i].click == True:
										self.map_length = i + 2
										break
								self.race()
					
					if event.type == pygame.KEYDOWN:
						if active:
							if event.key == pygame.K_BACKSPACE:
								user_text = user_text[0: -1]
							else:
								if len(user_text) <= 10 and event.unicode.isdigit():
									user_text += event.unicode
								elif event.key == pygame.K_RETURN:
									if not error and have_click:
										self.bet_money = int(user_text)
										for i in range(3):
											if map_choose[i].click == True:
												self.map_length = i + 2
												break
										self.race()
				
				# Check error
				error = (len(user_text) >= 11) or (not user_text.isdigit()) or (int(user_text) <= 0) or (
					int(user_text) > self.gold)
				self.show_back_ground()
				# Draw character
				for i in range(5):
					self.bet_thumbnails[i].draw(self.display_surface)
				# DRAW BUTTON
				go_back_button.draw(self.display_surface)
				play_button.draw(self.display_surface)
				
				# CHECK COLORS OF THE BOX
				if active:
					if error:
						color = RED
					else:
						color = GREEN
				else:
					color = YELLOW
				
				gold_text = self.font32.render(f'Gold:  {self.gold}', True, YELLOW)  # Update HUD
				bet_text = self.font32.render(f' BET: {user_text}', True, color)  # Update HUD
				self.display_surface.blit(gold_text, gold_text_rect)
				self.display_surface.blit(bet_text, bet_text_rect)
				for map in map_choose:
					map.draw(self.display_surface)
				pygame.draw.rect(self.display_surface, color, text_box, 3)
				
				pygame.display.update()
				clock.tick(FPS)
		
		def show_map(self):
			
			# GO BACK BUTTON
			image = pygame.image.load("./asset/button/go_back_button.png")
			scale = image.get_width() / image.get_height()
			image = pygame.transform.scale(image,
										(int(0.0688 * self.WINDOW_HEIGHT * scale), int(0.0688 * self.WINDOW_HEIGHT)))
			go_back_button = Button(int(0.051 * self.WINDOW_WIDTH + image.get_width() / 2), int(0.075 * self.WINDOW_HEIGHT),
									image, 1)
			mapping = True
			while mapping:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						pos = pygame.mouse.get_pos()
						# Check click Map
						for i in range(6):
							if self.map_thumbnail[i].rect.collidepoint(pos):
								self.map = i + 1
								self.show_set()
						if go_back_button.rect.collidepoint(pos):
							mapping = False
				
				self.show_back_ground()
				# DRAW BUTTON
				for i in range(6):
					self.map_thumbnail[i].draw(self.display_surface)
				
				go_back_button.draw(self.display_surface)
				pygame.display.update()
				clock.tick(FPS)
		
		def show_set(self):
			
			# Set button
			image = pygame.image.load("./asset/button/go_back_button.png")
			scale = image.get_width() / image.get_height()
			image = pygame.transform.scale(image,
										(int(0.0688 * self.WINDOW_HEIGHT * scale), int(0.0688 * self.WINDOW_HEIGHT)))
			# GO BACK BUTTON
			
			go_back_button = Button(int(0.051 * self.WINDOW_WIDTH + image.get_width() / 2), int(0.075 * self.WINDOW_HEIGHT),
									image, 1)
			chosing_set = True
			while chosing_set:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						pos = pygame.mouse.get_pos()
						# Check click GO BaCK
						if go_back_button.rect.collidepoint(pos):
							chosing_set = False
						# Check chosing set
						for i in range(6):
							if self.sets_thumbnail[i].rect.collidepoint(pos):
								self.set = i + 1
								self.show_bet()
				self.show_back_ground()
				# DRAW BUTTON
				for i in range(6):
					self.sets_thumbnail[i].draw(self.display_surface)
				go_back_button.draw(self.display_surface)
				pygame.display.update()
				clock.tick(FPS)
		
		def show_victory(self):
			#Load AI_evaluate response(khoảng 5s)
			negative = pygame.transform.scale(pygame.image.load(f"./asset/image/negative.png")
											, (int(self.WINDOW_WIDTH * 0.3), int(self.WINDOW_HEIGHT * 0.17)))
			positive = pygame.transform.scale(pygame.image.load(f"./asset/image/positive.png")
											, (int(self.WINDOW_WIDTH * 0.3), int(self.WINDOW_HEIGHT * 0.17)))
			response = self.AI_evaluate(self.user_text)
			self.user_text = u""
			self.show_text_chat = u""

			# cong tien
			if self.bet == self.rank[0].index:
				self.gold += self.bet_money * (self.map_length - 1)
				sign = 1
			else:
				self.gold -= self.bet_money
				sign = -1
				
			#data variable-Save vo data nhe (self.gold, self.history)
			if len(self.history) >= 7:
				self.history.pop()
			self.history.insert(0,  [self.bet, self.map_length, sign * self.bet_money * (self.map_length - 1)])
			
			save_data_playing(self.gold, self.own_item, self.history)

			self.load_race_thread.join()
			self.race_music.stop()
			show_vic_music = pygame.mixer.Sound("./asset/music/show_vic.wav")
			if self.music:
				show_vic_music.play(-1)
			image = pygame.image.load("./asset/image/show_vic.png")
			self.victory_image = pygame.transform.scale(image, (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
			
			image = pygame.image.load("./asset/button/play_now_button.png")
			scale = image.get_height() / image.get_width()
			image = pygame.transform.scale(image, (int(0.15 * self.WINDOW_WIDTH)
			                                       , int(scale * 0.15 * self.WINDOW_WIDTH)))
			
			play_button = Button( int( (1 - 0.03 - 0.075) * self.WINDOW_WIDTH)
			                     ,int(0.88 * self.WINDOW_HEIGHT) , image, 1)

			
			
			player = self.rank[0]
			scale = player.image.get_height() / player.image.get_width()
			for image in player.frame:
				image = pygame.transform.scale(image,
											(int(0.25 * self.WINDOW_HEIGHT), int(0.25 * self.WINDOW_HEIGHT * scale)))
			player.rect = player.image.get_rect()
			player.rect.bottom = 0.66 * self.WINDOW_HEIGHT
			player.rect.centerx = 0.5 * self.WINDOW_WIDTH
			
			player = self.rank[1]
			for image in player.frame:
				image = pygame.transform.scale(image,
											(int(0.2 * self.WINDOW_HEIGHT), int(0.2 * self.WINDOW_HEIGHT * scale)))
			player.rect = player.image.get_rect()
			player.rect.bottom = 0.62 * self.WINDOW_HEIGHT
			player.rect.centerx = 0.3 * self.WINDOW_WIDTH
			
			player = self.rank[2]
			for image in player.frame:
				image = pygame.transform.scale(image,
											(int(0.2 * self.WINDOW_HEIGHT), int(0.2 * self.WINDOW_HEIGHT * scale)))
			player.rect = player.image.get_rect()
			player.rect.bottom = 0.62 * self.WINDOW_HEIGHT
			player.rect.centerx = 0.67 * self.WINDOW_WIDTH
			
			player = self.rank[3]
			for image in player.frame:
				image = pygame.transform.scale(image,
											(int(0.14 * self.WINDOW_HEIGHT), int(0.14 * self.WINDOW_HEIGHT * scale)))
			player.rect = player.image.get_rect()
			player.rect.bottom = 0.5 * self.WINDOW_HEIGHT
			player.rect.centerx = 0.82 * self.WINDOW_WIDTH
			
			player = self.rank[4]
			for image in player.frame:
				image = pygame.transform.scale(image,
											(int(0.14 * self.WINDOW_HEIGHT), int(0.14 * self.WINDOW_HEIGHT * scale)))
			player.rect = player.image.get_rect()
			player.rect.bottom = 0.5 * self.WINDOW_HEIGHT
			player.rect.centerx = 0.15 * self.WINDOW_WIDTH
			
			gold_box = self.font32.render(f'GOLD: {self.gold}', True, YELLOW)
			gold_box_rect = gold_box.get_rect()
			gold_box_rect.topleft = (int(self.WINDOW_WIDTH * 0.03), int(self.WINDOW_HEIGHT * 0.75))
			
			if self.bet == self.rank[0].index:
				bet_box = self.font32.render(f'+ {self.bet_money * (self.map_length - 1)}', True, GREEN)
			else:
				bet_box = self.font32.render(f'- {self.bet_money}', True, RED)
				
			bet_box_rect = bet_box.get_rect()
			bet_box_rect.topleft = (
				int(self.WINDOW_WIDTH * 0.03), int(self.WINDOW_HEIGHT * 0.75) + gold_box_rect.height)
			
			showing = True
			while showing:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						pos = pygame.mouse.get_pos()
						
						# Click play again
						if play_button.rect.collidepoint(pos):							
							show_vic_music.stop()
							self.rank = []
							self.show_main_menu()
				
				self.display_surface.blit(self.victory_image, (0, 0))
				play_button.draw(self.display_surface)
				for player in self.rank:
					player.animate(.2)
				self.player_group.draw(self.display_surface)
				
				# show money

				self.display_surface.blit(gold_box, gold_box_rect)
				

				self.display_surface.blit(bet_box, bet_box_rect)
				
				#AI_evaluate response
				if response == 1: #tich cực (cho bản AI_evaluate6, 7)
					self.display_surface.blit(positive, (0, 0))
				else:
					self.display_surface.blit(negative, (0, 0))

				# DRAW BUTTON
				pygame.display.update()
				clock.tick(FPS)
		
		def show_HUD(self):
			pass
		
		def count_down(self):
			num3_image = pygame.transform.scale(pygame.image.load("./asset/image/num3.png"),
												(self.WINDOW_WIDTH // 2, self.WINDOW_WIDTH // 2))
			num2_image = pygame.transform.scale(pygame.image.load("./asset/image/num2.png"),
												(self.WINDOW_WIDTH // 2, self.WINDOW_WIDTH // 2))
			num1_image = pygame.transform.scale(pygame.image.load("./asset/image/num1.png"),
												(self.WINDOW_WIDTH // 2, self.WINDOW_WIDTH // 2))
			rect = num3_image.get_rect()
			rect.center = (self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2)
			
			music = pygame.mixer.Sound("./asset/music/count_down_music.mp3")
			
			frame_count = 0
			time = 3
			if self.music:
				music.play()
			while True:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
				frame_count += 1
				if frame_count == FPS / 10:
					frame_count = 0
					time -= 0.1
				self.display_surface.fill(BLACK)
				if time > 2:
					self.display_surface.blit(num3_image, rect)
				if time <= 2 and time > 1:
					self.display_surface.blit(num2_image, rect)
				if time <= 1 and time > 0:
					self.display_surface.blit(num1_image, rect)
				if time <= 0:
					break
				clock.tick(FPS)
				pygame.display.update()
		
		def blit_text(self, surface, text, pos, font, background_color=None, color=pygame.Color('black')):
			if self.map == 2 or self.map == 3 or self.map == 4 or self.map == 5:
				color = WHITE
			x, y = pos
			for line in text.splitlines():
				word_surface = font.render(line, 1, color, background_color)
				word_width, word_height = word_surface.get_size()
				surface.blit(word_surface, (x, y))
				y += word_height  # Start on new row
		
		def show_chat(self, *comments):
			if str(comments) == "('',)":  # đưa vào chuỗi rỗng
				self.blit_text(self.display_surface, self.show_text_chat,
							(int(self.WINDOW_WIDTH * 0.05), int(self.WINDOW_HEIGHT * 0.02)), self.font17)
				return 0
			elif len(comments) > 0:
				if self.show_text_chat.count("\n") >= 4:
					self.show_text_chat = self.show_text_chat[self.show_text_chat.find("\n") + 1:]
				self.show_text_chat += self.user_name + ": "+ str(comments)[2:-3] + "\n"
			else:
				temp = random.randint(1, 15)
				switcher = {
					1: 'Chỉ cần bạn có mặt, thắng thua không quan trọng',
					2: '@@',
					3: 'Xin lỗi tôi mệt rồi',
					4: 'Thanks',
					5: 'Bạn chơi hay quá! Đúng là bạn thân của tớ',
					6: 'Chỉ cần bạn có mặt, thắng thua không quan trọng',
					7: 'Ước được thua',
					8: 'Thôi gg đi',
					9: 'kkk',
					10: 'Thua đi nhá',
					11: '0949365JKL kb zalo t đón',
					12: 'Ping cao quá',
					13: 'Tao troll thôi',
					14: 'Chỉ cần bạn có mặt, thắng thua không quan trọng',
					15: 'Hello bạn!',
				}
				if self.show_text_chat.count("\n") >= 4:
					self.show_text_chat = self.show_text_chat[self.show_text_chat.find("\n") + 1:]
				self.show_text_chat += "Chat Bot " + str(random.randint(1, 4)) + ": " + switcher.get(temp) + "\n"
			
			self.blit_text(self.display_surface, self.show_text_chat,
						(int(self.WINDOW_WIDTH * 0.05), int(self.WINDOW_HEIGHT * 0.02)), self.font17)
		
		def remove_Vietnamese_letter(self, s):
			s = re.sub('[áàảãạăắằẳẵặâấầẩẫậ]', 'a', s)
			s = re.sub('[ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬ]', 'A', s)
			s = re.sub('[éèẻẽẹêếềểễệ]', 'e', s)
			s = re.sub('[ÉÈẺẼẸÊẾỀỂỄỆ]', 'E', s)
			s = re.sub('[óòỏõọôốồổỗộơớờởỡợ]', 'o', s)
			s = re.sub('[ÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢ]', 'O', s)
			s = re.sub('[íìỉĩị]', 'i', s)
			s = re.sub('[ÍÌỈĨỊ]', 'I', s)
			s = re.sub('[úùủũụưứừửữự]', 'u', s)
			s = re.sub('[ÚÙỦŨỤƯỨỪỬỮỰ]', 'U', s)
			s = re.sub('[ýỳỷỹỵ]', 'y', s)
			s = re.sub('[ÝỲỶỸỴ]', 'Y', s)
			s = re.sub('đ', 'd', s)
			s = re.sub('Đ', 'D', s)
			return s
		
		
		def race(self):
			# time
			self.time = 0
			self.frame_count = 0
			self.menu_music.stop()
			# text variable
			racing = True
			active = False
			user_text = u""
			user_text_temp = u""
			self.user_text = u""  # AI_evaluate
			box_chat = pygame.transform.scale(pygame.image.load(f"./asset/image/box_chat.png")
											, (int(self.WINDOW_WIDTH * 0.3), int(self.WINDOW_HEIGHT * 0.15)))
			
			# Item
			item_group = pygame.sprite.Group()
			
			# scroll variables
			self.scroll_map = int(2 * my_game.WINDOW_WIDTH / 1200 * 1.0)
			self.scroll_map_bool = True
			
			# Set n road continous
			self.road = pygame.transform.scale(pygame.image.load(f"./asset/map/{self.map}-{self.map_length}.png"),
			                                   (self.WINDOW_WIDTH * self.map_length, self.WINDOW_HEIGHT))
			self.map_rect = self.road.get_rect()
			self.map_rect.topleft = (0, 0)
			
			# count down
			self.count_down()
			if self.music:
				self.race_music.play()
			
			# text box
			text_box = self.font19.render(f'Chat: {user_text}', True, BLACK)
			text_box_rect = text_box.get_rect()
			text_box_rect.topleft = (int(self.WINDOW_WIDTH * 0.73), int(self.WINDOW_HEIGHT * 0.05))
			
			text_chat_rect = pygame.Rect(int(self.WINDOW_WIDTH * 0.73), int(self.WINDOW_HEIGHT * 0.026),
										self.WINDOW_WIDTH // 4, self.WINDOW_HEIGHT // 12)  # để nhận biết nhấp chuột
			
			text_box_rect.centery = 0.02 * self.WINDOW_HEIGHT + text_chat_rect.h // 2
			self.list_choice = [1,2,3,4,5]
			
			#use item variable
			can_uses = self.own_item > 0
			#player bet
			for player in self.player_group.sprites():
				if player.index == self.bet:
					self.user_player = player
					break
			
			
			# Main loop
			while racing:
				print(self.time)
				# if all player get the race, show victory
				if len(self.rank) == 5:
					self.show_victory()
				# 1 Tang toc , 2 giam toc 3.dich chuyen 4. Quay lui 5. CHay ve dich 6 di ve nha
				if random.randint(0, 1000) >= 996:
					type = random.choices([1, 2, 3, 4, 5, 6], weights=[0.3, 0.3, .05, 0.3, .001, .001])[0]
					if len(self.list_choice)  == 0:
						self.list_choice = [1,2,3,4,5]
					random.shuffle(self.list_choice)
					index = self.list_choice.pop()

					for player in self.player_group.sprites():
						if player.index == index:
							if player.running == False:
								break
							else:
								item = Item_skill(type, index, self.item_image, item_group, player)
								item_group.add(item)
				
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						pos = pygame.mouse.get_pos()
						# Check Click Box chat
						if text_chat_rect.collidepoint(pos):
							active = True
						else:
							active = False
						
						if self.use_item_button.rect.collidepoint(pos) and can_uses:
							can_uses = False
							self.own_item -= 1
							# 1 Tang toc , 2 giam toc 3.dich chuyen 4. Quay lui 5. CHay ve dich 6 di ve nha
							type = random.choices([1,3,5], weights=[0.5, 1-0.5-0.001,.001])[0]
							# Set timeskill
							if type == 1:
								self.user_player.speed_up_time += FPS  # one second
							elif type == 3:
								self.user_player.positionx += 150  #
								if self.user_player.rect.right + 150 >= self.map_rect.right and \
									self.map_rect.right > self.WINDOW_WIDTH:
									self.user_player.win_absolute = True
								self.user_player.pos_tele = self.user_player.rect.topleft
								self.user_player.tele_frame = 5
							
							elif type == 5:
								self.user_player.pos_tele = self.player.rect.topleft
								self.user_player.tele_frame = 5
								self.user_player.rect.right = self.map_rect.right
								if self.map_rect.right > self.WINDOW_WIDTH:
									self.player.win_absolute = True
							if self.music:
								my_game.collect_sound.play()
				
					
					if event.type == pygame.KEYDOWN and active:
						if event.key == pygame.K_BACKSPACE:
							# Go dau tieng viet
							if event.unicode.isalpha():
								# d + d
								if self.remove_Vietnamese_letter(user_text).rfind(
									self.remove_Vietnamese_letter(event.unicode)) == len(user_text) - 1:
									user_text = user_text[: -1] + event.unicode
								# du + d
								elif self.remove_Vietnamese_letter(user_text).rfind(
									self.remove_Vietnamese_letter(event.unicode)) == len(user_text) - 2:
									user_text = user_text[:-2] + event.unicode + user_text[-1] * 2
								# day + d
								elif self.remove_Vietnamese_letter(user_text).rfind(
									self.remove_Vietnamese_letter(event.unicode)) == len(user_text) - 3:
									user_text = user_text[:-3] + event.unicode + user_text[-2:] * 2
								# dung + d
								elif self.remove_Vietnamese_letter(user_text).rfind(
									self.remove_Vietnamese_letter(event.unicode)) == len(user_text) - 4:
									user_text = user_text[:-4] + event.unicode + user_text[-3:] * 2
								# duong + d
								elif self.remove_Vietnamese_letter(user_text).rfind(
									self.remove_Vietnamese_letter(event.unicode)) == len(user_text) - 5:
									user_text = user_text[:-5] + event.unicode + user_text[-4:] * 2
								
								if event.unicode == "ư" and user_text.rfind("ư") + 1 <= len(user_text) - 1:
									if user_text[user_text.rfind("ư") + 1] == "o":
										vi_tri = user_text.rfind("ư") + 1
										user_text = list(user_text)
										user_text[vi_tri] = "ơ"
										user_text = ''.join(user_text)
								continue
							else:
								user_text = user_text[: -1]
								continue
						
						if len(user_text) <= 70:
							user_text += event.unicode
						
						if event.key == pygame.K_RETURN:
							user_text_temp = user_text
							user_text = u""
				
				# time getting
				self.frame_count += 1
				if self.frame_count == FPS:
					self.time += 1
					self.frame_count = 0
				
				# Show Back map
				self.display_surface.blit(self.backmap, self.backmap_rect)
				
				# BOX CHAT
				text_box = self.font19.render(f'Chat: {user_text}', True, BLACK)  # rerender hud
				
				# Checck color of the box
				if active:
					color = GRAY
				else:
					color = BLACK
				
				self.display_surface.blit(box_chat, (int(self.WINDOW_WIDTH * 0.7), 0))
				try:
					if len(user_text) <= 22:
						text_box = self.font19.render(f'Chat: {user_text}', True, color)
					else:
						text_box = self.font19.render(f'Chat: {user_text[len(user_text) - 22:]}', True, color)
					self.display_surface.blit(text_box, text_box_rect)
				except ValueError:
					pass
				
				# Scroll the road
				if self.scroll_map_bool:
					self.map_rect.x -= self.scroll_map
				
				# Blit the road
				self.display_surface.blit(self.road, self.map_rect)
				
				# Run the player
				self.player_group.update()
				self.player_group.draw(self.display_surface)
				
				# BLit the item
				item_group.update()
				item_group.draw(self.display_surface)
				#Blit the use item button
				if can_uses:
					self.use_item_button.draw(self.display_surface)
				
				# Show chat
				if (random.randint(0, 1000) >= 998):
					self.show_chat()
				
				if user_text_temp != "":
					self.user_text += user_text_temp[:-1] + " "  # AI_evaluate
					self.show_chat(user_text_temp[:-1] + " ")
					user_text_temp = ""
				else:
					self.show_chat("")
				
				pygame.display.update()
				clock.tick(FPS)


	class Player(pygame.sprite.Sprite):
		def __init__(self, index, x, y, group):
			super().__init__()
			self.index = index
			self.origin_speed = random.uniform(.1, .3) * my_game.WINDOW_WIDTH * 1.0 / 1200
			self.animate_fps = .3
			self.running = True
			self.win_absolute = False
			self.has_boost = False
			self.group = group
			self.speed = self.origin_speed
			self.origin_frame = []
			self.speed_up_time = self.reverse_time = self.slow_down_time = 0
			
			
			for i in range(9):
				image = pygame.image.load(f"./asset/set/set{my_game.set}/{self.index}/{i + 1}.png")
				scale = image.get_width() / image.get_height()
				self.origin_frame.append(
					pygame.transform.scale(image,
										(int(my_game.WINDOW_HEIGHT * 0.15 * scale), int(my_game.WINDOW_HEIGHT * 0.15))))
			
			self.flip_frame = []
			for i in range(9):
				self.flip_frame.append(pygame.transform.flip(self.origin_frame[i], True, False))
			
			self.frame = self.origin_frame
			self.current_frame = 0
			self.image = self.frame[self.current_frame]
			self.rect = self.image.get_rect()
			self.rect.bottomleft = (x, y)
			self.positionx = x
			
			#tele variable
			self.pos_tele = (0, 0)
			self.tele_frame = 0
			# variable for celebartion
			self.is_cele = False
			self.origin_x = x
			self.origin_y = y
			self.cele = -2
			# Mui ten
			self.mui_ten = pygame.transform.scale(pygame.image.load(f"./asset/image/mui_ten.png")
												, (int(my_game.WINDOW_WIDTH * 0.025), int(my_game.WINDOW_HEIGHT * 0.045)))
		
		def skill(self):
			# UU tien phep quay lui, neu gap quay lui xoa het phep con lai
			if self.reverse_time > 0:
				self.speed_up_time = self.slow_down_time = 0
				self.reverse_time -= 1
				self.speed = -2 * my_game.WINDOW_WIDTH * 1.0 / 1200
				self.frame = self.flip_frame
				my_game.display_surface.blit(my_game.reverse_frame[int(self.current_frame)],self.rect.topleft)
			else:
				self.speed = self.origin_speed
				self.frame = self.origin_frame
			# Phep nao gap sau thi lay phep do, khong cong tru toc do
			if self.speed_up_time + self.slow_down_time == 0:
				if self.reverse_time == 0:
					self.speed = self.origin_speed
			
			elif self.speed_up_time > self.slow_down_time and self.speed_up_time > 0:
				self.speed = self.origin_speed + 2 * my_game.WINDOW_WIDTH * 1.0 / 1200
				self.slow_down_time = 0
				self.speed_up_time -= 1
				my_game.display_surface.blit(my_game.speed_up_frame[int(abs(self.current_frame-1))]
											,self.rect.topleft)

			
			elif self.speed_up_time < self.slow_down_time and self.slow_down_time > 0:
				self.speed = self.origin_speed - 2 * my_game.WINDOW_WIDTH * 1.0 / 1200
				self.slow_down_time -= 1
				self.speed_up_time = 0
				my_game.display_surface.blit(my_game.slow_down_frame[int(abs(self.current_frame - 1))]
											, self.rect.topleft)
			
			if self.tele_frame > 0:
				my_game.display_surface.blit(my_game.tele_frame[int(5 - self.tele_frame)]
											, self.pos_tele)
				self.tele_frame -= .2
		def update(self):
			self.skill()
			if self.is_cele:
				self.celebrate()
			if self.rect.right >= my_game.map_rect.right:
				self.rect.right = my_game.map_rect.right
				if self not in my_game.rank:
					if len(my_game.rank) == 0:
						if my_game.music:
							my_game.yeah_sound.play()
						self.is_cele = True
					self.get_race()
			
			if self.win_absolute and my_game.scroll_map_bool:
				self.rect.x -= my_game.scroll_map
			
			if self.running:
				self.positionx += self.speed
				self.rect.x = int(self.positionx)
				self.animate(self.animate_fps)
			
			# draw mui ten
			if self.index == my_game.bet:
				my_game.display_surface.blit(self.mui_ten, (int(self.rect.left * 0.93) - 10, int(self.rect.top)))
		
		def get_race(self):
			# win absolute la dich chuyen thang ve dich, nen khong can ngung man hinh - > may con kia chay bthg
			if not self.win_absolute:
				self.running = False
				my_game.rank.append(self)
				if my_game.map_rect.right <= my_game.WINDOW_WIDTH:
					my_game.scroll_map = 0
					my_game.scroll_map_bool = False
				for player in self.group.sprites():
					if player == self:
						continue
					if not player.has_boost:
						player.origin_speed += 2 * my_game.WINDOW_WIDTH * 1.0 / 1200
						player.has_boost = True
			else:
				self.running = False
				my_game.rank.append(self)
		
		def animate(self, fps):
			self.current_frame += fps
			if self.current_frame >= 8:
				self.current_frame = 0
			self.image = self.frame[int(self.current_frame)]
		
		def celebrate(self):
			self.rect.bottom += self.cele
			
			if self.rect.bottom >= self.origin_y:
				if self.cele > 0:
					self.cele *= -1
			
			if self.rect.bottom <= self.origin_y - 40:
				if self.cele < 0:
					self.cele *= -1

	pygame.init()
	pygame.display.set_caption("Life is lie")
	logo = pygame.image.load("./asset/image/logo.png")
	pygame.display.set_icon(logo)

	global userdata, pos, history
	my_game = Game(userdata[pos][3], userdata[pos][4], history)
	my_game.main()
	

# --------------------------------------------------------------------------------

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 675

root = tk.Tk()

root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{int(root.winfo_screenwidth()/2 - WINDOW_WIDTH/2)}+{int(root.winfo_screenheight()/2 - WINDOW_HEIGHT/2)}")
root.resizable(False, False)
root.iconbitmap("./asset/image/logo.ico")
root.title("Life is lie")

login_bg = tk.PhotoImage(file="./asset/image/login_bg.png")
signup_bg = tk.PhotoImage(file="./asset/image/signup_bg.png")
reset_password_bg = tk.PhotoImage(file="./asset/image/reset_password_bg.png")

show = tk.PhotoImage(file="./asset/image/show.png")
hide = tk.PhotoImage(file="./asset/image/hide.png")
go_back = tk.PhotoImage(file="./asset/image/go_back.png")
go_to_singup = tk.PhotoImage(file="./asset/image/go_to_signup.png")
forgot_password = tk.PhotoImage(file="./asset/image/forgot_password.png")

required_username = tk.PhotoImage(file="./asset/error/required_username.png")
find_username = tk.PhotoImage(file="./asset/error/find_username.png")
begin_username = tk.PhotoImage(file="./asset/error/begin_username.png")
invalid_username = tk.PhotoImage(file="./asset/error/invalid_username.png")
username_limit = tk.PhotoImage(file="./asset/error/username_limit.png")
username_existed = tk.PhotoImage(file="./asset/error/username_existed.png")

required_password_login = tk.PhotoImage(file="./asset/error/required_password_login.png")
required_password = tk.PhotoImage(file="./asset/error/required_password.png")
invalid_password = tk.PhotoImage(file="./asset/error/invalid_password.png")
password_limit = tk.PhotoImage(file="./asset/error/password_limit.png")
match_password = tk.PhotoImage(file="./asset/error/match_password.png")

required_repassword = tk.PhotoImage(file="./asset/error/required_repassword.png")
match_repassword = tk.PhotoImage(file="./asset/error/match_repassword.png")

required_email = tk.PhotoImage(file="./asset/error/required_email.png")
invalid_email = tk.PhotoImage(file="./asset/error/invalid_email.png")
email_existed = tk.PhotoImage(file="./asset/error/email_existed.png")
find_email = tk.PhotoImage(file="./asset/error/find_email.png")

# --------------------------------------------------------------------------------

def delete_errors(*error):
	for i in error:
		i.place_forget()

def reset_state(*state):
	for i in state:
		i.config(image=hide)

def change_frame(src, des, *text):
	for i in text:
		i.delete(0, "end")
	src.forget()
	des.pack(expand=True, fill="both")

def show_password(state, entry):
	state.config(image=show)
	entry.config(show="")
	state.config(command=lambda: hide_password(state, entry))

def hide_password(state, entry):
	state.config(image=hide)
	entry.config(show="•")
	state.config(command=lambda: show_password(state, entry))

def invalid_letter(letter):
	return not(
			(letter >= '0' and letter <= '9')
			or (letter >= 'A' and letter <= 'Z')
			or (letter >= 'a' and letter <= 'z'))

def pos_user(email):
	global userdata

	l = int(0)
	r = len(userdata) - 1
	mid = int((r + l) / 2)
	
	if (r < 0): 
		return -1

	while (True):
		if l + 1 >= r:
			if int(userdata[r][1]) <= email:
				return r + 1
			if int(userdata[l][1]) > email:
				return l
			return r
		if int(userdata[mid][1]) > email:
			r = int(mid)
		else:
			l = int(mid) + 1
		mid = int((r + l) / 2)

def get_hash(s, capital = 0):
	hashS = 0
	for i in range(0, len(s)):
		tmp = hashS
		if s[i] <= 'Z':
			hashS = (tmp + (ord(s[i]) + capital) * pow[i]) % MOD
		else:
			hashS = (tmp + ord(s[i]) * pow[i]) % MOD
		
	return hashS

# -------------------- SIGN UP --------------------
class signup():  
	def __init__(self) -> None:		
		global log_in
		
		self.frame = tk.Frame(root, width=1200, height=675)
		
		tk.Label(self.frame, image=signup_bg).place(x=0,y=0)

		# username
		self.username_entry = tk.Entry(self.frame, font=("Calibri", 14), fg="#646060")
		self.username_entry.focus()
		self.username_entry.place(x=776, y=155, width=366, height=36)

		# email
		self.email_entry = tk.Entry(self.frame, font=("Calibri", 14), fg="#646060")
		self.email_entry.place(x=776, y=255, width=366, height=36)

		# password
		self.password_entry = tk.Entry(self.frame, font=("Calibri", 14), show="•", fg="#646060")
		self.password_entry.place(x=776, y=355, width=366, height=36)
		self.password_state = tk.Button(
			self.frame, 
			image=hide, 
			bd=0, 
			bg="white", 
			activebackground="white", 
			cursor="hand2", 
			command=lambda: show_password(self.password_state, self.password_entry))
		self.password_state.place(x=1100, y=363)
		
		# confirm password
		self.repassword_entry = tk.Entry(self.frame, font=("Calibri", 14), show="•", fg="#646060")
		self.repassword_entry.place(x=776, y=455, width=366, height=36)
		self.repassword_state = tk.Button(
			self.frame, 
			image=hide, 
			bd=0, 
			bg="white", 
			activebackground="white", 
			cursor="hand2", 
			command=lambda: show_password(self.repassword_state, self.repassword_entry))
		self.repassword_state.place(x=1100, y=463)

		# sign up
		self.signup_button = tk.Button(
			self.frame, 
			text="Sign up", 
			font=("Calibri", 25, "bold"), 
			bd=1,
			fg="#ffd300",
			activeforeground="#ffd300",
			bg="#ff1309",
			activebackground="#ff1309",
			cursor="hand2", 
			command=self.process
			)
		self.signup_button.place(x=776, y=535, height=48, width=364)

		# go to log in
		self.go_to_login_button = tk.Button(
			self.frame,
			image=go_back,
			bd=0,
			bg="#aadcfe",
			activebackground="#aadcfe",
			cursor="hand2", 
			command=lambda: [delete_errors(self.required_username_error, self.begin_username_error, self.invalid_username_error, self.username_existed_error, self.username_limit_error, 
										self.required_email_error, self.invalid_email_error, self.email_existed_error,
										self.required_password_error, self.invalid_password_error, self.password_limit_error,
										self.required_repassword_error, self.match_repassword_error),
							reset_state(self.password_state, self.repassword_state),
							change_frame(self.frame, log_in.frame, self.username_entry, self.email_entry, self.password_entry, self.repassword_entry)])
		self.go_to_login_button.place(x=741, y=625)	

		# errors messages
		self.required_username_error = tk.Label(self.frame, image=required_username, bd=1, bg="#aadcfe")
		self.begin_username_error = tk.Label(self.frame, image=begin_username, bd=1, bg="#aadcfe")
		self.invalid_username_error = tk.Label(self.frame, image=invalid_username, bd=1, bg="#aadcfe")
		self.username_existed_error = tk.Label(self.frame, image=username_existed, bd=1, bg="#aadcfe")	
		self.username_limit_error = tk.Label(self.frame, image=username_limit, bd=1, bg="#aadcfe")

		self.required_email_error = tk.Label(self.frame, image=required_email, bd=1, bg="#aadcfe")
		self.invalid_email_error = tk.Label(self.frame, image=invalid_email, bd=1, bg="#aadcfe")
		self.email_existed_error = tk.Label(self.frame, image=email_existed, bd=1, bg="#aadcfe")

		self.required_password_error = tk.Label(self.frame, image=required_password, bd=1, bg="#aadcfe")
		self.invalid_password_error = tk.Label(self.frame, image=invalid_password, bd=1, bg="#aadcfe")
		self.password_limit_error = tk.Label(self.frame, image=password_limit, bd=1, bg="#aadcfe")

		self.required_repassword_error = tk.Label(self.frame, image=required_repassword, bd=1, bg="#aadcfe")
		self.match_repassword_error = tk.Label(self.frame, image=match_repassword, bd=1, bg="#aadcfe")

	def process(self):		
		global userdata, log_in
		
		self.username = self.username_entry.get()
		self.required_username_error.place_forget()
		self.begin_username_error.place_forget()
		self.username_limit_error.place_forget()
		self.invalid_username_error.place_forget()
		self.username_existed_error.place_forget()

		self.email = self.email_entry.get()
		self.required_email_error.place_forget()
		self.invalid_email_error.place_forget()
		self.email_existed_error.place_forget()

		self.password = self.password_entry.get()
		self.required_password_error.place_forget()
		self.password_limit_error.place_forget()
		self.invalid_password_error.place_forget()

		self.repassword = self.repassword_entry.get()
		self.required_repassword_error.place_forget()
		self.match_repassword_error.place_forget()

		# username
		if len(self.username) <= 0:
			self.required_username_error.place(x=773, y=193)
			return None
		if len(self.username) > 32:
			self.username_limit_error.place(x=773, y=196)
			return None
		for i in range(0, len(self.username)):
			if invalid_letter(self.username[i]):
				self.invalid_username_error.place(x=773, y=196)
				return None
		if self.username[0] < 'A':
			self.begin_username_error.place(x=773, y=196)
			return None
		if (len(userdata) > 0):
			for i in userdata:
				if i[0] == self.username:
					self.username_existed_error.place(x=773, y=196)
					return None
		
		# email
		check = False
		if len(self.email) <= 0 or len(self.email) > 320:
			self.required_email_error.place(x=773, y=296)
			return None
		for i in range(0, len(self.email)):
			if (invalid_letter(self.email[i]) 
				and not (self.email[i] == '-' or self.email[i] == '_' 
						or ((self.email[i] == '.' or self.email[i] == '@') and i > 0))
				or i > 64):
				self.invalid_email_error.place(x=773, y=296)
				return None
			if  ((self.email[i] == '-' or self.email[i] == '_' or self.email[i] == '.' or self.email[i] == '@')
					and i > 0 and (self.email[i] == self.email[i - 1] or i + 1 == len(self.email))):
				self.invalid_email_error.place(x=773, y=296)
				return None
			if self.email[i] == '@':
				if (len(self.email) - i > 255):
					self.invalid_email_error.place(x=773, y=296)
					return None
				check = True
				exist_letter = False
				i += 1
				if (invalid_letter(self.email[i])):
					self.invalid_email_error.place(x=773, y=296)
					return None
				i += 1
				while i < len(self.email):
					if (invalid_letter(self.email[i]) 
							and not ((self.email[i] == '-' or self.email[i] == '.') 
									and self.email[i] != self.email[i - 1] and i + 1 < len(self.email))):
						self.invalid_email_error.place(x=773, y=296)
						return None
					exist_letter |= self.email[i] >= 'A'
					i += 1
				i -= 1
				while i >= 3 and self.email[i] != '.' and self.email[i] != '@': 
					i -= 1
					exist_letter |= (self.email[i] >= 'A')
				if (i <= 2 or len(self.email) - i - 1 < 2 or self.email[i] != '.' or not exist_letter):
					self.invalid_email_error.place(x=773, y=296)
					return None
				break
		if not check:
			self.invalid_email_error.place(x=773, y=296)
			return None
		self.email_code = get_hash(self.email_entry.get(), 32)
		self.pos = pos_user(self.email_code)
		if (self.pos > 0 and self.email_code == int(userdata[self.pos - 1][1])):
			self.email_existed_error.place(x=773, y=296)
			return None

		# password
		if len(self.password) <= 0:
			self.required_password_error.place(x=773, y=396)
			return None
		if len(self.password) > 16 or len(self.password) < 8:
			self.password_limit_error.place(x=773, y=396)
			return None
		for i in self.password:
			if invalid_letter(i):
				self.invalid_password_error.place(x=773, y=396)
				return None
		
		# confirm password
		if len(self.repassword) <= 0:
			self.required_repassword_error.place(x=773, y=496)
			return None
		if len(self.repassword) != len(self.password) or self.repassword != self.password:
			self.match_repassword_error.place(x=773, y=496)
			return None
		
		# sign up success
		global pos
		pos = self.pos - 1
		userdata.insert(pos, [self.username , self.email_code, get_hash(self.password)])
		trans_str()
		
		delete_errors(self.required_username_error, self.begin_username_error, self.invalid_username_error, self.username_existed_error, self.username_limit_error, 
					self.required_email_error, self.invalid_email_error, self.email_existed_error,
					self.required_password_error, self.invalid_password_error, self.password_limit_error,
					self.required_repassword_error, self.match_repassword_error)
		reset_state(self.password_state, self.repassword_state)
		change_frame(self.frame, log_in.frame, self.username_entry, self.email_entry, self.password_entry, self.repassword_entry)

# -------------------- LOG IN --------------------
class login():
	def __init__(self) -> None:
		self.frame = tk.Frame(root, width=1200, height=675)
		
		tk.Label(self.frame, image=login_bg).place(x=0,y=0)

		# username
		self.username_entry = tk.Entry(self.frame, font=("Calibri", 14), fg="#646060")
		self.username_entry.focus()
		self.username_entry.place(x=776, y=155, width=366, height=36)

		# password
		self.password_entry = tk.Entry(self.frame, font=("Calibri", 14), show="•", fg="#646060")
		self.password_entry.place(x=776, y=255, width=366, height=36)
		self.password_state = tk.Button(
			self.frame, 
			image=hide, 
			bd=0, 
			bg="white", 
			activebackground="white", 
			cursor="hand2", 
			command=lambda: show_password(self.password_state, self.password_entry))
		self.password_state.place(x=1100, y=263)

		# log in
		self.login_button = tk.Button(
			self.frame, 
			text="Log in", 
			font=("Calibri", 25, "bold"), 
			bd=1,
			fg="#ffd300",
			activeforeground="#ffd300",
			bg="#ff1309",
			activebackground="#ff1309",
			cursor="hand2", 
			command=self.process
			)
		self.login_button.place(x=776, y=335, height=48, width=364)

		# forgot password
		self.reset_pass = reset_password()
		self.forget_password_button = tk.Button(
			self.frame, 
			image=forgot_password,
			bd=0,
			bg="#aadcfe",
			activebackground="#aadcfe",
			cursor="hand2",
			command=lambda: [delete_errors(self.required_username_error, self.find_username_error,
										self.required_password_error, self.match_password_error),
							reset_state(self.password_state),
							change_frame(self.frame, self.reset_pass.frame, self.username_entry, self.password_entry)])
		self.forget_password_button.place(x=865, y=402)
		# go to sign up
		self.sign_up = signup()
		self.go_to_signup_button = tk.Button(
			self.frame, 
			image=go_to_singup,
			bd=0,
			bg="#aadcfe",
			activebackground="#aadcfe",
			cursor="hand2", 
			command=lambda: [delete_errors(self.required_username_error, self.find_username_error,
										self.required_password_error, self.match_password_error),
							reset_state(self.password_state),
							change_frame(self.frame, self.sign_up.frame, self.username_entry, self.password_entry)])
		self.go_to_signup_button.place(x=828, y=434)

		# errors messages
		self.required_username_error = tk.Label(self.frame, image=required_username, bd=1, bg="#aadcfe")
		self.find_username_error = tk.Label(self.frame, image=find_username, bd=1, bg="#aadcfe")
		self.required_password_error = tk.Label(self.frame, image=required_password_login, bd=1, bg="#aadcfe")
		self.match_password_error = tk.Label(self.frame, image=match_password, bd=1, bg="#aadcfe")


	def process(self):
		global userdata

		self.required_username_error.place_forget()
		self.find_username_error.place_forget()
		self.required_password_error.place_forget()
		self.match_password_error.place_forget()

		if len(self.username_entry.get()) <= 0:
			self.required_username_error.place(x=773, y=193)
			return None
		
		self.pos = -1
		for i in range(0, len(userdata)):
			if (userdata[i][0] == self.username_entry.get()):
				self.pos = i
				break
		if self.pos < 0:
			self.find_username_error.place(x=773, y=196)
			return None

		if len(self.password_entry.get()) <= 0:
			self.required_password_error.place(x=774, y=296)
			return None

		if get_hash(self.password_entry.get()) != int(userdata[self.pos][2]):
			self.match_password_error.place(x=773, y=296)
			return None

		# login in successful
		self.play_game()
	
	def play_game(self):
		global pos
		pos = self.pos
		file.close()
		root.destroy()
		get_data_playing()
		global play
		play = game_frame()

class reset_password:
	def __init__(self):
		global log_in
		
		self.frame = tk.Frame(root, width=1200, height=675)
		
		tk.Label(self.frame, image=reset_password_bg).place(x=0,y=0)

		# username
		self.username_entry = tk.Entry(self.frame, font=("Calibri", 14), fg="#646060")
		self.username_entry.focus()
		self.username_entry.place(x=776, y=155, width=366, height=36)

		# email
		self.email_entry = tk.Entry(self.frame, font=("Calibri", 14), fg="#646060")
		self.email_entry.place(x=776, y=255, width=366, height=36)

		# password
		self.password_entry = tk.Entry(self.frame, font=("Calibri", 14), show="•", fg="#646060")
		self.password_entry.place(x=776, y=355, width=366, height=36)
		self.password_state = tk.Button(
			self.frame, 
			image=hide, 
			bd=0, 
			bg="white", 
			activebackground="white", 
			cursor="hand2", 
			command=lambda: show_password(self.password_state, self.password_entry))
		self.password_state.place(x=1100, y=363)
		
		# confirm password
		self.repassword_entry = tk.Entry(self.frame, font=("Calibri", 14), show="•", fg="#646060")
		self.repassword_entry.place(x=776, y=455, width=366, height=36)
		self.repassword_state = tk.Button(
			self.frame, 
			image=hide, 
			bd=0, 
			bg="white", 
			activebackground="white", 
			cursor="hand2", 
			command=lambda: show_password(self.repassword_state, self.repassword_entry))
		self.repassword_state.place(x=1100, y=463)

		# reset password
		self.reset_password_button = tk.Button(
			self.frame, 
			text="Reset password", 
			font=("Calibri", 25, "bold"), 
			bd=1,
			fg="#ffd300",
			activeforeground="#ffd300",
			bg="#ff1309",
			activebackground="#ff1309",
			cursor="hand2", 
			command=self.process
			)
		self.reset_password_button.place(x=776, y=535, height=48, width=364)

		# go to log in
		self.go_to_login_button = tk.Button(
			self.frame,
			image=go_back,
			bd=0,
			bg="#aadcfe",
			activebackground="#aadcfe",
			cursor="hand2", 
			command=lambda: [delete_errors(self.required_username_error, self.find_username_error,
										self.required_email_error, self.find_email_error,
										self.required_password_error, self.invalid_password_error, self.password_limit_error,
										self.required_repassword_error, self.match_repassword_error),
							reset_state(self.password_state, self.repassword_state),
							change_frame(self.frame, log_in.frame, self.username_entry, self.email_entry, self.password_entry, self.repassword_entry)])
		self.go_to_login_button.place(x=741, y=625)	

		# errors messages
		self.required_username_error = tk.Label(self.frame, image=required_username, bd=1, bg="#aadcfe")
		self.find_username_error = tk.Label(self.frame, image=find_username, bd=1, bg="#aadcfe")
		
		self.required_email_error = tk.Label(self.frame, image=required_email, bd=1, bg="#aadcfe")
		self.find_email_error = tk.Label(self.frame, image=find_email, bd=1, bg="#aadcfe")

		self.required_password_error = tk.Label(self.frame, image=required_password, bd=1, bg="#aadcfe")
		self.invalid_password_error = tk.Label(self.frame, image=invalid_password, bd=1, bg="#aadcfe")
		self.password_limit_error = tk.Label(self.frame, image=password_limit, bd=1, bg="#aadcfe")

		self.required_repassword_error = tk.Label(self.frame, image=required_repassword, bd=1, bg="#aadcfe")
		self.match_repassword_error = tk.Label(self.frame, image=match_repassword, bd=1, bg="#aadcfe")
	
	def process(self):
		global userdata, log_in, info

		self.required_username_error.place_forget()
		self.find_username_error.place_forget()
		self.required_email_error.place_forget()
		self.find_email_error.place_forget()
		self.required_password_error.place_forget()
		self.password_limit_error.place_forget()
		self.invalid_password_error.place_forget()
		self.required_repassword_error.place_forget()
		self.match_repassword_error.place_forget()

		# username
		if len(self.username_entry.get()) <= 0:
			self.required_username_error.place(x=773, y=193)
			return None

		self.pos = -1
		for i in range(0, len(userdata)):
			if userdata[i][0] == self.username_entry.get():
				self.pos = i
				break
		if self.pos < 0:
			self.find_username_error.place(x=773, y=196)
			return None

		# email
		if len(self.email_entry.get()) <= 0:
			self.required_email_error.place(x=773, y=296)
			return None
		self.email_code = get_hash(self.email_entry.get(), 32)
		if (int(userdata[self.pos][1]) != self.email_code):
			self.find_email_error.place(x=773, y=296)
			return None

		# password
		self.password = self.password_entry.get()
		if len(self.password) <= 0:
			self.required_password_error.place(x=773, y=396)
			return None
		if len(self.password) > 16 or len(self.password) < 8:
			self.password_limit_error.place(x=773, y=396)
			return None
		for i in self.password:
			if invalid_letter(i):
				self.invalid_password_error.place(x=773, y=396)
				return None
		
		# confirm password
		self.repassword = self.repassword_entry.get()
		if len(self.repassword) <= 0:
			self.required_repassword_error.place(x=773, y=496)
			return None
		self.password_code = get_hash(self.password)
		if len(self.repassword) != len(self.password) or self.password_code != get_hash(self.repassword):
			self.match_repassword_error.place(x=773, y=496)
			return None
		
		# reset password
		userdata[self.pos - 1][2] = self.password_code
		trans_str()

		delete_errors(self.required_username_error, self.find_username_error,
					self.required_email_error, self.find_email_error,
					self.required_password_error, self.password_limit_error, self.invalid_password_error,
					self.required_repassword_error, self.match_repassword_error)
		reset_state(self.password_state, self.repassword_state)
		change_frame(self.frame, log_in.frame, self.username_entry, self.email_entry, self.password_entry, self.repassword_entry),

# --------------------------------------------------------------------------------

prep_hash()
log_in = login()
log_in.frame.pack(expand=True, fill="both")

root.mainloop()