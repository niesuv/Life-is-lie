from turtle import window_width
import pygame, random, sys, re
import numpy as np

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
	
	def draw(self, surface):
		surface.blit(self.image, self.rect)
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			self.rect.center = self.pos_hover
		else:
			self.rect.center = self.pos_unhover


class Thumb_nail():
	def __init__(self, x, y, image):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (width, height))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.pos_unhover = (x, y)
		self.pos_hover = (x, y + 30)
		self.click = False
	
	def draw(self, surface):
		surface.blit(self.image, self.rect)
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos) or self.click:
			self.rect.center = self.pos_hover
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
		self.rect.topleft = player.rect.topright
		distance = my_game.map_rects[my_game.map_length - 1].right - player.rect.right
		if player.running == False:
			self.remove(group)
		if distance > 200:
			self.rect.x += random.randint(100
			                              ,min(500, int(distance - self.image.get_width())) )
	
	def update(self):
		if not self.player.running:
			self.remove(self.item_group)
		if my_game.scroll_map_bool:
			self.rect.x -= my_game.scroll_map
		if pygame.sprite.collide_rect(self,self.player):
			#Set timeskill
			if self.type == 1:
				self.player.speed_up_time += FPS  #one second
			elif self.type == 2:
				self.player.slow_down_time += FPS  #three seconds
			elif self.type == 3:
				self.player.positionx += 150 #tele300 pixel
				if self.player.rect.right + 150 >= my_game.map_rects[my_game.map_length - 1].right and my_game.map_rects[my_game.map_length - 1].right > my_game.WINDOW_WIDTH:
					self.player.win_absolute = True
			elif self.type == 4:
				self.player.reverse_time += FPS
			elif self.type == 5:
				self.player.rect.right = my_game.map_rects[my_game.map_length - 1].right
				if my_game.map_rects[my_game.map_length - 1].right > my_game.WINDOW_WIDTH:
					self.player.win_absolute = True
			elif self.type == 6:
				self.player.positionx = my_game.map_rects[0].left
			self.remove(self.item_group)
			my_game.collect_sound.play()
			


class Game():
	def __init__(self):
		#display value
		self.WINDOW_WIDTH = 1200
		self.WINDOW_HEIGHT = 675
		
		self.display_surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
		
		self.scroll = 0
		self.direction_scroll = 1
		self.time = 0
		self.frame_count = 0
		
		
		# Font
		self.font32 = pygame.font.Font("./asset/font/font1.ttf", self.WINDOW_WIDTH // 32 + 1)
		
		#sound
		self.collect_sound = pygame.mixer.Sound("./asset/music/collect_music.wav")
		self.race_music = pygame.mixer.Sound("./asset/music/race_music.mp3")
		self.yeah_sound = pygame.mixer.Sound("./asset/music/yeah.wav")
		
		# Item image
		self.item_image = []
		for i in range(6):
			image = pygame.image.load(f"./asset/skill/{i + 1}.png")
			scale = image.get_width() / image.get_height()
			self.item_image.append(
				pygame.transform.scale(image, (int(scale * self.WINDOW_HEIGHT * 0.15), int(self.WINDOW_HEIGHT * 0.15))))
		
		
		# Game Value, SET in TEXT file
		self.gold = 1000
		self.map = 1
		self.set = 1
		self.bet = 1
		self.rank = []
		self.history = []
		self.show_text_chat = u""
		self.font19 = pygame.font.Font("./asset/font/aachenb.ttf", self.WINDOW_WIDTH // 64 + 1)
		self.font17 = pygame.font.Font("./asset/font/aachenb.ttf", self.WINDOW_WIDTH // 71 + 1)
	
	
	
	def main(self):
		# Music
		self.menu_music = pygame.mixer.Sound("./asset/music/menu_music.mp3")
		self.menu_music.set_volume(.2)
		self.show_main_menu()
	
	def show_main_menu(self):
		#Load background
		image = pygame.image.load("./asset/image/back.webp").convert()
		scale = int(image.get_width() / image.get_height())
		self.back_ground_image = pygame.transform.scale(image, (int(self.WINDOW_HEIGHT * scale), self.WINDOW_HEIGHT))
		
		# Button menu
		image = pygame.image.load("./asset/button/start_button.png")
		scale = image.get_width() / image.get_height()
		image = pygame.transform.scale(image, (self.WINDOW_HEIGHT // 8 * scale,self.WINDOW_HEIGHT // 8))
		start_button = Button(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 3,
		                      image, 1)
		image = pygame.image.load("./asset/button/setting_button.png")
		scale = image.get_width() / image.get_height()
		image = pygame.transform.scale(image, (self.WINDOW_HEIGHT // 8 * scale, self.WINDOW_HEIGHT // 8))
		
		setting_button = Button(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 3 + 100,
		                        image, 1)
		
		self.menu_music.stop()
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
						self.start_new_round()
					
					if setting_button.rect.collidepoint(pos):
						self.show_setting()
			
			start_button.draw(self.display_surface)
			setting_button.draw(self.display_surface)
			pygame.display.update()
			clock.tick(FPS)
	
	def show_back_ground(self):
		if self.scroll <= 0:
			self.direction_scroll = 1
		if self.scroll >= self.back_ground_image.get_width() - self.WINDOW_WIDTH:
			self.direction_scroll = -1
		self.scroll += self.direction_scroll * .5 * my_game.WINDOW_WIDTH * 1.0  / 1200
		self.display_surface.blit(self.back_ground_image, (-self.scroll, 0))
	
	def start_new_round(self):
		self.show_map()
	
	def show_setting(self):

		image = pygame.image.load("./asset/button/go_back_button.png")
		scale = image.get_width() / image.get_height()
		image = pygame.transform.scale(image, (int(0.0688 * self.WINDOW_HEIGHT * scale), int(0.0688 * self.WINDOW_HEIGHT)))
		# GO BACK BUTTON
		go_back_button = Button(int(0.051 * self.WINDOW_WIDTH + image.get_width() / 2), int(0.075 * self.WINDOW_HEIGHT), image, 1)
		
		#setting option button
		image = pygame.image.load("./asset/button/resolution_button'.png")
		scale = image.get_width() / image.get_height()
		image = pygame.transform.scale(image,
		                               (self.WINDOW_HEIGHT //10 * scale, self.WINDOW_HEIGHT //10))
		resolution_button = Button(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 3, image, 1)
		
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
						
					
			self.show_back_ground()
			# DRAW BUTTON
			go_back_button.draw(self.display_surface)
			resolution_button.draw(self.display_surface)
			pygame.display.update()
			clock.tick(FPS)
	
	def show_resolution(self):
		# resolution option button
		image = pygame.image.load("./asset/button/600x330.png")
		scale = image.get_width() / image.get_height()
		image = pygame.transform.scale(image,(self.WINDOW_HEIGHT // 10 * scale, self.WINDOW_HEIGHT // 10))
		btn_600x330 = Button(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 3, image, 1)
		
		image = pygame.image.load("./asset/button/800x450.png")
		image = pygame.transform.scale(image, (self.WINDOW_HEIGHT // 10 * scale, self.WINDOW_HEIGHT // 10))
		btn_800x450 = Button(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 3 + self.WINDOW_HEIGHT//6, image, 1)
		
		image = pygame.image.load("./asset/button/1200x675.png")
		image = pygame.transform.scale(image, (self.WINDOW_HEIGHT // 10 * scale, self.WINDOW_HEIGHT // 10))
		btn_1200x675 = Button(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 3 + 2*self.WINDOW_HEIGHT//6, image, 1)
		
		image = pygame.image.load("./asset/button/1600x900.png")
		image = pygame.transform.scale(image, (self.WINDOW_HEIGHT // 10 * scale, self.WINDOW_HEIGHT // 10))
		btn_1600x900 = Button(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 3 + 3*self.WINDOW_HEIGHT//6, image, 1)
		
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
					if btn_600x330.rect.collidepoint(pos):
						self.WINDOW_WIDTH = 600
						self.WINDOW_HEIGHT = 337
						self.display_surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
						self.show_main_menu()
					
					if btn_800x450.rect.collidepoint(pos):
						self.WINDOW_WIDTH = 800
						self.WINDOW_HEIGHT = 450
						self.display_surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
						self.show_main_menu()
					
					if btn_1600x900.rect.collidepoint(pos):
						self.WINDOW_WIDTH = 1600
						self.WINDOW_HEIGHT = 900
						self.display_surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
						self.show_main_menu()
						
					if btn_1200x675.rect.collidepoint(pos):
						self.WINDOW_WIDTH = 1200
						self.WINDOW_HEIGHT = 675
						self.display_surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
						self.show_main_menu()
			self.show_back_ground()
			# DRAW BUTTON
			go_back_button.draw(self.display_surface)
			btn_600x330.draw(self.display_surface)
			btn_800x450.draw(self.display_surface)
			btn_1200x675.draw(self.display_surface)
			btn_1600x900.draw(self.display_surface)
			pygame.display.update()
			clock.tick(FPS)
	
	def preprocess_data(self, comments):

		# get rid of "train"
		comments = comments.replace("train", " ")
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

		return comments

	def sigmoid(self, z):
		return(1 / (1 + np.exp(-z)))

	def AI_evaluate(self, comments):
		#Load vocabList and theta
		vocabList = open("./asset/AI/vocabulary.txt",  encoding="utf8")
		vocabList = str(vocabList.read()).split("\n")
		theta = np.loadtxt('./asset/AI/optimizedTheta.txt')

		#Digitize data
		n = len(vocabList)  #numbers of features 
		word_indices = [0 for i in range(n)]
		comments = self.preprocess_data(comments)

		for i in range(n):
			if vocabList[i] in comments:
				word_indices[i] += 1

		#Output 
		#print(self.sigmoid(np.array(word_indices) @ theta.T))
		if len(comments) == 0:
			print(u"\nBạn muốn nói gì sao?\n")
		elif (self.sigmoid(np.array(word_indices) @ theta.T)) >= (0.5 + 10e-6) or ("chó" in comments) or ("lỗi" in comments):
			print(u"\nBạn hẳn đã có một ngày không tốt!\nHãy để Silly Squad giúp bạn nhé!\n")
		else:
			print(u"\nCảm ơn bạn đã tham gia trò chơi Silly Squad <3\n")

	def show_bet(self):
		# Load Text
		gold_text = self.font32.render(f'Gold:  {self.gold}', True, YELLOW)
		gold_text_rect = gold_text.get_rect()
		gold_text_rect.topleft = (0.15 * self.WINDOW_WIDTH, int(0.62 * self.WINDOW_HEIGHT))
		
		user_text = "100"
		
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
		
		# Load thumbnail
		self.bet_thumbnail_images = []
		for i in range(5):
			image = pygame.image.load(f'./asset/set/set_avt/{self.set}{i + 1}.png')
			scale = image.get_height() / image.get_width()
			image = pygame.transform.scale(image, (int(0.1525 * self.WINDOW_WIDTH), int(0.1525 * self.WINDOW_WIDTH * scale)))
			self.bet_thumbnail_images.append(image)
		
		self.bet_thumbnails = []
		for i in range(5):
			thumbnail = Thumb_nail(int(((0.15 + i * (0.1525 + 0.063 / 2)) * self.WINDOW_WIDTH))
			                       , int(0.195 * self.WINDOW_HEIGHT), self.bet_thumbnail_images[i])
			self.bet_thumbnails.append(thumbnail)
		
		# Go back button
		image = pygame.image.load("./asset/button/go_back_button.png")
		scale = image.get_width() / image.get_height()
		image = pygame.transform.scale(image, (int(0.0688 * self.WINDOW_HEIGHT * scale), int(0.0688 * self.WINDOW_HEIGHT)))
		go_back_button = Button(int(0.051 * self.WINDOW_WIDTH + image.get_width() / 2), int(0.075 * self.WINDOW_HEIGHT), image, 1)
		
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
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
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
					
					# CHeck click play_now
					if play_button.rect.collidepoint(pos):
						if not error and have_click:
							for i in range(5):
								if self.bet_thumbnails[i].click == True:
									self.bet = i + 1
									break
							self.bet_money = int(user_text)
							self.race()
				
				if event.type == pygame.KEYDOWN:
					if active:
						if event.key == pygame.K_BACKSPACE:
							user_text = user_text[0: -1]
						else:
							if len(user_text) <= 12:
								user_text += event.unicode
			
			# Check error
			error = (len(user_text) >= 13) or (not user_text.isdigit()) or (int(user_text) <= 0) or (
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
			pygame.draw.rect(self.display_surface, color, text_box, 3)
			
			pygame.display.update()
			clock.tick(FPS)
	
	def show_map(self):
		# SET BUTTON
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
		# GO BACK BUTTON
		image = pygame.image.load("./asset/button/go_back_button.png")
		scale = image.get_width() / image.get_height()
		image = pygame.transform.scale(image, (int(0.0688 * self.WINDOW_HEIGHT * scale), int(0.0688 * self.WINDOW_HEIGHT)))
		go_back_button = Button(int(0.051 * self.WINDOW_WIDTH + image.get_width() / 2), int(0.075 * self.WINDOW_HEIGHT), image, 1)
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
		# Lay ra anh thumbnail
		images = []
		for i in range(4):
			image = pygame.image.load(f"./asset/set/set_avt/all_set{i+1}.png")
			image = pygame.transform.scale(image, (int(0.286 * self.WINDOW_HEIGHT), int(0.286 * self.WINDOW_HEIGHT)))
			images.append(image)
		self.sets_thumbnail = []
		# Chua te hard code
		for i in range(4):
			if i <= 2:
				self.sets_thumbnail.append(Button(int(0.192 * self.WINDOW_WIDTH + i * (0.16 + 0.146) * self.WINDOW_WIDTH)
				                                  , int(0.317 * self.WINDOW_HEIGHT), images[i], 1))
			else:
				self.sets_thumbnail.append(Button(int(0.192 * self.WINDOW_WIDTH + (i - 3) * (0.16 + 0.146) * self.WINDOW_WIDTH)
				                                  , int(0.7196 * self.WINDOW_HEIGHT), images[i], 1))
		# Set button
		image = pygame.image.load("./asset/button/go_back_button.png")
		scale = image.get_width() / image.get_height()
		image = pygame.transform.scale(image, (int(0.0688 * self.WINDOW_HEIGHT * scale), int(0.0688 * self.WINDOW_HEIGHT)))
		# GO BACK BUTTON
		
		go_back_button = Button(int(0.051 * self.WINDOW_WIDTH + image.get_width() / 2), int(0.075 * self.WINDOW_HEIGHT), image, 1)
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
					for i in range(4):
						if self.sets_thumbnail[i].rect.collidepoint(pos):
							self.set = i + 1
							self.show_bet()
			self.show_back_ground()
			# DRAW BUTTON
			for i in range(4):
				self.sets_thumbnail[i].draw(self.display_surface)
			go_back_button.draw(self.display_surface)
			pygame.display.update()
			clock.tick(FPS)
	
	def show_victory(self):
		self.race_music.stop()
		show_vic_music = pygame.mixer.Sound("./asset/music/show_vic.wav")
		show_vic_music.play(-1)
		image = pygame.image.load("./asset/image/show_vic.png")
		self.victory_image = pygame.transform.scale(image, (self.WINDOW_WIDTH,self.WINDOW_HEIGHT))
		
		image = pygame.image.load("./asset/button/play_now_button.png")
		scale = image.get_height() / image.get_width()
		image = pygame.transform.scale(image, (int(0.15 * self.WINDOW_WIDTH), int(scale * 0.15 * self.WINDOW_WIDTH)))
		play_button = Button(int(0.8 * self.WINDOW_WIDTH), int(0.72 * self.WINDOW_HEIGHT), image, 1)
		play_button.rect.bottomright = (self.WINDOW_WIDTH - 10, self.WINDOW_HEIGHT - 10)
		
		player = self.rank[0]
		scale = player.image.get_height() / player.image.get_width()
		for image in player.frame:
			image = pygame.transform.scale(image, (int(0.25 * self.WINDOW_HEIGHT), int(0.25 * self.WINDOW_HEIGHT * scale)))
		player.rect = player.image.get_rect()
		player.rect.bottom = 0.66 * self.WINDOW_HEIGHT
		player.rect.centerx = 0.5 * self.WINDOW_WIDTH

		
		player = self.rank[1]
		for image in player.frame:
			image = pygame.transform.scale(image, (int(0.2 * self.WINDOW_HEIGHT), int(0.2 * self.WINDOW_HEIGHT * scale)))
		player.rect = player.image.get_rect()
		player.rect.bottom = 0.62 * self.WINDOW_HEIGHT
		player.rect.centerx = 0.3 * self.WINDOW_WIDTH

		
		player = self.rank[2]
		for image in player.frame:
			image = pygame.transform.scale(image, (int(0.2 * self.WINDOW_HEIGHT), int(0.2 * self.WINDOW_HEIGHT * scale)))
		player.rect = player.image.get_rect()
		player.rect.bottom = 0.62 * self.WINDOW_HEIGHT
		player.rect.centerx = 0.67 * self.WINDOW_WIDTH

		
		player = self.rank[3]
		for image in player.frame:
			image = pygame.transform.scale(image, (int(0.14 * self.WINDOW_HEIGHT), int(0.14 * self.WINDOW_HEIGHT * scale)))
		player.rect = player.image.get_rect()
		player.rect.bottom = 0.5 * self.WINDOW_HEIGHT
		player.rect.centerx = 0.82 * self.WINDOW_WIDTH

		
		player = self.rank[4]
		for image in player.frame:
			image = pygame.transform.scale(image, (int(0.14 * self.WINDOW_HEIGHT), int(0.14 * self.WINDOW_HEIGHT * scale)))
		player.rect = player.image.get_rect()
		player.rect.bottom = 0.5 * self.WINDOW_HEIGHT
		player.rect.centerx = 0.15 * self.WINDOW_WIDTH
		
		#cong tien
		if self.bet == self.rank[0].index:
			self.gold += self.bet_money
		else:
			self.gold -= self.bet_money
		
		showing = True
		while showing:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					
					#Click play again
					if play_button.rect.collidepoint(pos):
						self.AI_evaluate(self.user_text)
						self.user_text = u""
						self.show_text_chat = u""
						show_vic_music.stop()
						self.rank = []
						self.show_main_menu()
						
			self.display_surface.blit(self.victory_image,(0,0))
			play_button.draw(self.display_surface)
			for player in self.rank:
				player.animate(.2)
			self.player_group.draw(self.display_surface)

			#show money
			gold_box = self.font32.render(f'GOLD: {self.gold}', True, YELLOW) 
			gold_box_rect = gold_box.get_rect()
			gold_box_rect.topleft = (int(self.WINDOW_WIDTH*0.03), int(self.WINDOW_HEIGHT*0.75) )
			self.display_surface.blit(gold_box, gold_box_rect)

			if self.bet == self.rank[0].index: 
				bet_box = self.font32.render(f'+ {self.bet_money}', True, GREEN) 
			else: 
				bet_box = self.font32.render(f'- {self.bet_money}', True, RED) 
			bet_box_rect = bet_box.get_rect()
			bet_box_rect.topleft = (int(self.WINDOW_WIDTH*0.03), int(self.WINDOW_HEIGHT*0.75) + gold_box_rect.height)
			self.display_surface.blit(bet_box, bet_box_rect)

			# DRAW BUTTON
			pygame.display.update()
			clock.tick(FPS)
	
	def show_HUD(self):
		pass
	
	def count_down(self):
		num3_image = pygame.transform.scale(pygame.image.load("./asset/image/num3.png"),(self.WINDOW_WIDTH//2, self.WINDOW_WIDTH//2))
		num2_image = pygame.transform.scale(pygame.image.load("./asset/image/num2.png"),(self.WINDOW_WIDTH//2, self.WINDOW_WIDTH//2))
		num1_image = pygame.transform.scale(pygame.image.load("./asset/image/num1.png"),(self.WINDOW_WIDTH//2, self.WINDOW_WIDTH//2))
		rect = num3_image.get_rect()
		rect.center = (self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT //2)
		
		music = pygame.mixer.Sound("./asset/music/count_down_music.mp3")
		
		frame_count = 0
		time = 3
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

	def blit_text(self, surface, text, pos, font, background_color = None, color=pygame.Color('black')):
		if self.map == 2 or self.map == 3 or self.map == 4:
			color = WHITE
		x, y = pos
		for line in text.splitlines():
			word_surface = font.render(line, 1, color, background_color) 
			word_width, word_height = word_surface.get_size() 
			surface.blit(word_surface, (x, y))
			y += word_height  # Start on new row

	def show_chat(self, *comments):
		if str(comments) == "('',)": #đưa vào chuỗi rỗng
			self.blit_text(self.display_surface, self.show_text_chat,(int(self.WINDOW_WIDTH*0.05), int(self.WINDOW_HEIGHT*0.02) ) , self.font17)
			return 0
		elif len(comments) > 0:
			if self.show_text_chat.count("\n") >= 4:
				self.show_text_chat = self.show_text_chat[self.show_text_chat.find("\n")+1 :]
			self.show_text_chat +=  "User_name: " + str(comments)[2:-3] + "\n"  #self.user_name + str(comments)[2:-3] + "\n"
		else:
			temp = random.randint(1, 15)
			switcher={
			1:'Chỉ cần bạn có mặt, thắng thua không quan trọng',
			2:'@@',
			3:'Xin lỗi tôi mệt rồi',
			4:'Thanks',
			5:'Bạn chơi hay quá! Đúng là bạn thân của tớ',
			6:'Chỉ cần bạn có mặt, thắng thua không quan trọng',
			7:'Ước được thua',
			8:'Thôi gg đi',
			9:'kkk',
			10:'Thua đi nhá',
			11:'0949365JKL kb zalo t đón',
			12:'Ping cao quá',
			13:'Tao troll thôi',
			14:'Chỉ cần bạn có mặt, thắng thua không quan trọng',
			15:'Hello bạn!',
			}
			if self.show_text_chat.count("\n") >= 4:
				self.show_text_chat = self.show_text_chat[self.show_text_chat.find("\n")+1 :]
			self.show_text_chat += "Chat Bot " + str(random.randint(1, 4)) + ": " +switcher.get(temp) + "\n"

		self.blit_text(self.display_surface, self.show_text_chat,(int(self.WINDOW_WIDTH*0.05), int(self.WINDOW_HEIGHT*0.02) ) , self.font17)

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
		self.menu_music.stop()
		self.map_length = 4
		racing = True
		active = False
		user_text = u""
		user_text_temp = u""
		self.user_text = u"" #AI_evaluate
		box_chat = pygame.transform.scale(pygame.image.load(f"./asset/image/box_chat.png")
		                                  , ( int(self.WINDOW_WIDTH*0.3), int(self.WINDOW_HEIGHT*0.15) ) )
		
		#Set n road continous
		map = pygame.transform.scale(pygame.image.load(f"./asset/map/{self.map}.png"), (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
		last_map = pygame.transform.scale(pygame.image.load(f"./asset/map/{self.map}.1.png"), (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
		self.map_rects = []
		for i in range(self.map_length):
			rect = map.get_rect()
			if i > 0:
				rect.topleft = self.map_rects[i-1].topright
			else:
				rect.topleft = (0, 0)
			self.map_rects.append(rect)		

		#Set back map
		backmap = pygame.image.load(f"./asset/map/backmap{self.map}.jpg")
		scale = backmap.get_width() / backmap.get_height()
		backmap = pygame.transform.scale(backmap, (self.WINDOW_HEIGHT * scale, self.WINDOW_HEIGHT))
		backmap_rect = backmap.get_rect()
		backmap_rect.center = (self.WINDOW_WIDTH //2 , self.WINDOW_HEIGHT // 2)
		self.player_group = pygame.sprite.Group()

		#Item
		item_group = pygame.sprite.Group()

		#Add Character
		for i in range(1, 6):
			player = Player(i, 0, self.WINDOW_HEIGHT * 0.263 + (i - 1) * self.WINDOW_HEIGHT * 0.174,self.player_group)
			self.player_group.add(player)

		#scroll variables
		self.scroll_map = int(2 * my_game.WINDOW_WIDTH   / 1200 * 1.0)
		self.scroll_map_bool = True
		
		#count down

		self.count_down()
		self.race_music.play()
		
		#text box
		text_box = self.font19.render(f'Chat: {user_text}', True, BLACK)
		text_box_rect = text_box.get_rect()
		text_box_rect.topleft = (int(self.WINDOW_WIDTH * 0.73), int(self.WINDOW_HEIGHT * 0.05))
		
		text_chat_rect = pygame.Rect(int(self.WINDOW_WIDTH * 0.73), int(self.WINDOW_HEIGHT * 0.026),
		                             self.WINDOW_WIDTH // 4, self.WINDOW_HEIGHT // 12)  # để nhận biết nhấp chuột
		
		text_box_rect.centery = 0.02 * self.WINDOW_HEIGHT + text_chat_rect.h // 2
		
		#Main loop
		while racing:
			print(self.time)
			
			#if all player get the race, show victory
			if len(self.rank) == 5:
				self.show_victory()
			# 1 Tang toc , 2 giam toc 3.dich chuyen 4. Quay lui 5. CHay ve dich 6 di ve nha
			if random.randint(0,1000) >= 995:
				type = random.choices([1,2,3,4,5,6], weights=[0.3, 0.3, .05 , 0.3, .001, .001])[0]
				index = random.randint(1,7)
				for player in self.player_group.sprites():
					if player.index == index:
						if player.running == False:
							break
						else:
							item = Item_skill(type,index,self.item_image[type -1],item_group,player)
							item_group.add(item)
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					#Check Click Box chat
					if text_chat_rect.collidepoint(pos):
						active = True
					else:
						active = False					

				if event.type == pygame.KEYDOWN:                  
					if event.key == pygame.K_BACKSPACE:
						#Go dau tieng viet
						if event.unicode.isalpha():
							#d + d
							if self.remove_Vietnamese_letter(user_text).rfind(self.remove_Vietnamese_letter(event.unicode)) == len(user_text) - 1:
								user_text = user_text[: -1] + event.unicode
							#du + d
							elif self.remove_Vietnamese_letter(user_text).rfind(self.remove_Vietnamese_letter(event.unicode)) == len(user_text) - 2:
								user_text = user_text[:-2] + event.unicode + user_text[-1] * 2
							#day + d
							elif self.remove_Vietnamese_letter(user_text).rfind(self.remove_Vietnamese_letter(event.unicode)) == len(user_text) - 3:
								user_text = user_text[:-3] + event.unicode + user_text[-2:] * 2
							#dung + d
							elif self.remove_Vietnamese_letter(user_text).rfind(self.remove_Vietnamese_letter(event.unicode)) == len(user_text) - 4:
								user_text = user_text[:-4] + event.unicode + user_text[-3:] * 2
							#duong + d
							elif self.remove_Vietnamese_letter(user_text).rfind(self.remove_Vietnamese_letter(event.unicode)) == len(user_text) - 5:
								user_text = user_text[:-5] + event.unicode + user_text[-4:] * 2
							
							if event.unicode == "ư" and user_text.rfind("ư") + 1 <= len(user_text) - 1:
								if user_text[user_text.rfind("ư") + 1] == "o":
									list(user_text)[user_text.rfind("ư") + 1] = "ơ" 
									user_text = ''.join(user_text)
							continue
						else:
							user_text = user_text[: -1]
							continue

					if len(user_text) <= 70:
						user_text += event.unicode

					if  event.key == pygame.K_RETURN:
						user_text_temp = user_text
						user_text = u""

			#time getting
			self.frame_count+= 1
			if self.frame_count == FPS:
				self.time += 1
				self.frame_count = 0
			
			#Show Back map
			self.display_surface.blit(backmap, backmap_rect)
			
			#BOX CHAT
			text_box = self.font19.render(f'Chat: {user_text}', True, BLACK) #rerender hud

			#Checck color of the box
			if active:
				color = GRAY
			else:
				color = BLACK

			self.display_surface.blit(box_chat, ( int(self.WINDOW_WIDTH*0.7), 0) )
			try:
				if len(user_text) <= 22: 
					text_box = self.font19.render(f'Chat: {user_text}', True, color) 
				else:
					text_box = self.font19.render(f'Chat: {user_text[len(user_text)-22:]}', True, color)
				self.display_surface.blit(text_box, text_box_rect)
			except ValueError:
				pass

			#Scroll the road
			for i in range(self.map_length):
				self.map_rects[i].x -= self.scroll_map
				
			# Blit the road
			for i in range(self.map_length):
				if self.map_rects[i].left <= self.WINDOW_WIDTH or self.map_rects[i].right >= 0:
					if i != self.map_length - 1:
						self.display_surface.blit(map, self.map_rects[i])
					else:
						self.display_surface.blit(last_map, self.map_rects[i])
			
			# Run the player
			self.player_group.update()
			self.player_group.draw(self.display_surface)
			
			
			#BLit the item
			item_group.update()
			item_group.draw(self.display_surface)

			#Show chat
			if (random.randint(0,1000) >= 998):
				self.show_chat()

			if user_text_temp != "":
				self.user_text += user_text_temp[:-1] + " " #AI_evaluate
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
		self.origin_speed = random.uniform(.1, .3) * my_game.WINDOW_WIDTH * 1.0  / 1200
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
				pygame.transform.scale(image, (int(my_game.WINDOW_HEIGHT * 0.15 * scale), int(my_game.WINDOW_HEIGHT * 0.15))))
		
		self.flip_frame = []
		for i in range(9):
			self.flip_frame.append(pygame.transform.flip(self.origin_frame[i],True, False))
			
		self.frame = self.origin_frame
		self.current_frame = 0
		self.image = self.frame[self.current_frame]
		self.rect = self.image.get_rect()
		self.rect.bottomleft = (x, y)
		self.positionx = x
		
		#variable for celebartion
		self.is_cele = False
		self.origin_x = x
		self.origin_y = y
		self.cele = -2
		#Mui ten
		self.mui_ten = pygame.transform.scale(pygame.image.load(f"./asset/image/mui_ten.png")
	                                      , (int(my_game.WINDOW_WIDTH * 0.025), int(my_game.WINDOW_HEIGHT * 0.045)))
	def skill(self):
		#UU tien phep quay lui, neu gap quay lui xoa het phep con lai
		if self.reverse_time > 0:
			self.speed_up_time = self.slow_down_time = 0
			self.reverse_time -= 1
			self.speed = -2 * my_game.WINDOW_WIDTH * 1.0  / 1200
			self.frame = self.flip_frame
		else:
			self.speed = self.origin_speed
			self.frame = self.origin_frame
		#Phep nao gap sau thi lay phep do, khong cong tru toc do
		if self.speed_up_time + self.slow_down_time == 0:
			if self.reverse_time == 0:
				self.speed = self.origin_speed
		
		elif self.speed_up_time > self.slow_down_time and self.speed_up_time > 0:
			self.speed = self.origin_speed + 2 * my_game.WINDOW_WIDTH *1.0  / 1200
			self.slow_down_time = 0
			self.speed_up_time -= 1
		
		elif self.speed_up_time < self.slow_down_time and self.slow_down_time > 0:
			self.speed = self.origin_speed - 2 * my_game.WINDOW_WIDTH *1.0  / 1200
			self.slow_down_time -= 1
			self.speed_up_time = 0
		
	
	def update(self):
		self.skill()
		if self.is_cele:
			self.celebrate()
		if self.rect.right >= my_game.map_rects[my_game.map_length-1].right:
			self.rect.right = my_game.map_rects[my_game.map_length-1].right
			if self not in my_game.rank:
				if len(my_game.rank) == 0:
					my_game.yeah_sound.play()
					self.is_cele = True
				self.get_race()
			
		if self.win_absolute and my_game.scroll_map_bool:
			self.rect.x -= my_game.scroll_map
		
		if self.running:
			self.positionx += self.speed
			self.rect.x = int(self.positionx)
			self.animate(self.animate_fps)
		
		#draw mui ten
		if self.index == my_game.bet:
			my_game.display_surface.blit(self.mui_ten, ( int(self.rect.left * 0.93) - 30, int(self.rect.top)  ) )

	def get_race(self):
		#win absolute la dich chuyen thang ve dich, nen khong can ngung man hinh - > may con kia chay bthg
		if not self.win_absolute:
			self.running = False
			my_game.rank.append(self)
			if my_game.map_rects[my_game.map_length-1].right <= my_game.WINDOW_WIDTH:
				my_game.scroll_map = 0
				my_game.scroll_map_bool = False
			for player in self.group.sprites():
				if player == self :
					continue
				if not player.has_boost:
					player.origin_speed += 2 * my_game.WINDOW_WIDTH * 1.0  / 1200
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
my_game = Game()
my_game.main()
