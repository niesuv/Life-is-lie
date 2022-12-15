import pygame, random, sys, re

# FPS and clock
FPS = 60
clock = pygame.time.Clock()
# Define Colors
GREEN = (13, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 3, 3)
WHITE = (255, 255, 255)

# Create Display Surface(SCALE = 16 / 9)
WINDOW_WIDTH =  1200
WINDOW_HEIGHT = 675

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


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
		self.image = pygame.transform.scale(image,( width, height) )
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.pos_unhover = (x, y)
		self.pos_hover = (x, y - 10)
		self.click = False
		
	def draw(self, surface):
		surface.blit(self.image, self.rect)
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos) or self.click:
			self.rect.center = self.pos_hover
		else:
			self.rect.center = self.pos_unhover


class Game():
	def __init__(self):
		self.scroll = 0
		self.direction_scroll = 1
		# Get BACKGROUND
		image = pygame.image.load("./asset/image/back.webp").convert()
		scale = int(image.get_width() / image.get_height())
		self.back_ground_image = pygame.transform.scale(image, (int(WINDOW_HEIGHT * scale), WINDOW_HEIGHT))
		
		#Font
		self.font32 = pygame.font.Font("./asset/font/font1.ttf",32)
		
		# Game Value, SET in TEXT file
		self.gold = 1000
		self.map = 1
		self.set = 1
		self.bet = 1
		self.history = []
	
	def main(self):
		running = True
		while running:
			# Check close
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				self.show_main_menu()
			clock.tick(FPS)
	
	def show_main_menu(self):
		# Music
		self.menu_music = pygame.mixer.Sound("./asset/music/menu_music.mp3")
		self.menu_music.set_volume(.2)
		# Button menu
		start_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3,
		                      pygame.image.load("./asset/button/start_button.png"), 0.2)
		setting_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 130,
		                        pygame.image.load("./asset/button/setting_button.png"), 0.2)
		
		
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
			
			start_button.draw(display_surface)
			setting_button.draw(display_surface)
			pygame.display.update()
			clock.tick(FPS)
	
	def show_back_ground(self):
		if self.scroll <= 0:
			self.direction_scroll = 1
		if self.scroll >= self.back_ground_image.get_width() - WINDOW_WIDTH:
			self.direction_scroll = -1
		self.scroll += self.direction_scroll * .5
		display_surface.blit(self.back_ground_image, (-self.scroll, 0))
	
	def start_new_round(self):
		self.show_map()
	
	def show_setting(self):
		#Set button
		image = pygame.image.load("./asset/button/go_back_button.png")
		scale = image.get_width() / image.get_height()
		image = pygame.transform.scale(image, (int(0.0688 * WINDOW_HEIGHT * scale), int(0.0688 * WINDOW_HEIGHT)))
		# GO BACK BUTTON
		go_back_button = Button(int(0.051 * WINDOW_WIDTH + image.get_width() / 2), int(0.075 * WINDOW_HEIGHT), image, 1)
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
			
			self.show_back_ground()
			# DRAW BUTTON
			go_back_button.draw(display_surface)
			pygame.display.update()
			clock.tick(FPS)
	
	def show_bet(self):
		#Load Text
		gold_text = self.font32.render(f'Gold:  {self.gold}', True, YELLOW)
		gold_text_rect = gold_text.get_rect()
		gold_text_rect.topleft = ( 0.15*WINDOW_WIDTH,int(0.62 * WINDOW_HEIGHT))
		
		user_text = ""
		
		bet_text = self.font32.render(f' BET: {user_text}', True, YELLOW)
		bet_text_rect = bet_text.get_rect()
		bet_text_rect.topleft = ( int(0.15*WINDOW_WIDTH),  int(0.7 * WINDOW_HEIGHT))
		
		text_box = pygame.Rect(int(0.15*WINDOW_WIDTH) , int(0.7 * WINDOW_HEIGHT) , WINDOW_WIDTH //3 , WINDOW_HEIGHT//10 )
		color = YELLOW
		active = False
		error = False
		
		bet_text_rect.centery = 0.7 * WINDOW_HEIGHT + text_box.h / 2
		
		#Play button
		image = pygame.image.load("./asset/button/play_now_button.png")
		scale =image.get_height()/ image.get_width()
		image = pygame.transform.scale(image, (int(0.33 * WINDOW_WIDTH), int(scale * 0.33 * WINDOW_WIDTH)))
		play_button = Button(int(0.8*WINDOW_WIDTH),int(0.72 * WINDOW_HEIGHT),image, 1)
		
		#Load thumbnail
		self.bet_thumbnail_images = []
		for i in range(5):
			image = pygame.image.load(f'./asset/set/set_avt/1{i+1}.png')
			scale = image.get_height() / image.get_width()
			image = pygame.transform.scale(image, (int(0.1525 * WINDOW_WIDTH), int (0.1525 * WINDOW_WIDTH * scale)))
			self.bet_thumbnail_images.append(image)
		
		self.bet_thumbnails = []
		for i in range(5):
			thumbnail = Thumb_nail(int(( (0.15 + i*(0.1525 +0.063/2)) * WINDOW_WIDTH))
			                       ,int(0.195*WINDOW_HEIGHT),self.bet_thumbnail_images[i])
			self.bet_thumbnails.append(thumbnail)
		
		#Go back button
		image = pygame.image.load("./asset/button/go_back_button.png")
		scale = image.get_width() / image.get_height()
		image = pygame.transform.scale(image,( int(0.0688 * WINDOW_HEIGHT * scale) ,int(0.0688 * WINDOW_HEIGHT) ))
		go_back_button = Button(int(0.051 * WINDOW_WIDTH + image.get_width() / 2), int(0.075 * WINDOW_HEIGHT), image, 1)
		
		#User click the thumnail
		have_click = False
		betting  = True
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
					#CHeck click thumbnail
					for i in range(5):
						if self.bet_thumbnails[i].rect.collidepoint(pos):
							self.bet_thumbnails[i].click = True
							for j in range(5):
								if j == i:
									continue
								self.bet_thumbnails[j].click = False
					#Check Click Box
					if text_box.collidepoint(pos):
						active = True
					else:
						active = False
						
					#CHeck click play_now
					if play_button.rect.collidepoint(pos):
						if not error and have_click:
							self.race()
							
						
				if event.type == pygame.KEYDOWN:
					if active:
						if event.key == pygame.K_BACKSPACE:
							user_text = user_text[0 : -1]
						else:
							if len(user_text) <= 12:
								user_text += event.unicode
								
			#Check error
			error = (len(user_text) >= 13) or (not user_text.isdigit()) or (int(user_text) <=0) or ( int(user_text) > self.gold)
			self.show_back_ground()
			#Draw character
			for i in range(5):
				self.bet_thumbnails[i].draw(display_surface)
			# DRAW BUTTON
			go_back_button.draw(display_surface)
			play_button.draw(display_surface)
			
			#CHECK COLORS OF THE BOX
			if active:
				if error:
					color = RED
				else:
					color = GREEN
			else:
				color = YELLOW
			
			gold_text = self.font32.render(f'Gold:  {self.gold}', True, YELLOW) #Update HUD
			bet_text = self.font32.render(f' BET: {user_text}', True, color) #Update HUD
			display_surface.blit(gold_text, gold_text_rect)
			display_surface.blit(bet_text, bet_text_rect)
			pygame.draw.rect(display_surface, color, text_box , 3 )
			
			pygame.display.update()
			clock.tick(FPS)
			

			
			
	def show_map(self):
		# SET BUTTON
		self.map_thumbnail_images = []
		for i in range(1,7):
			image = pygame.image.load(f"./asset/map/showmap{i}.png")
			image = pygame.transform.scale(image, (int(0.271 * WINDOW_WIDTH),int(0.271 * WINDOW_HEIGHT)))
			self.map_thumbnail_images.append(image)
		
		self.map_thumbnail = []
		#Chua te hard code
		for i in range(6):
			if i <= 2:
				self.map_thumbnail.append(Button(int(i*(self.map_thumbnail_images[i].get_width() + 0.040 * WINDOW_WIDTH )
				                          + 0.051 * WINDOW_WIDTH + self.map_thumbnail_images[i].get_width() / 2)  ,int(0.314 * WINDOW_HEIGHT)
				                      ,self.map_thumbnail_images[i],1))
			else:
				self.map_thumbnail.append(Button(int((i-3)*(self.map_thumbnail_images[i].get_width() + 0.040 * WINDOW_WIDTH )
				                          + 0.051 * WINDOW_WIDTH + self.map_thumbnail_images[i].get_width() / 2),
				                      int((0.314 +0.377) * WINDOW_HEIGHT ),self.map_thumbnail_images[i],1 ))
		# GO BACK BUTTON
		image = pygame.image.load("./asset/button/go_back_button.png")
		scale = image.get_width() / image.get_height()
		image = pygame.transform.scale(image, (int(0.0688 * WINDOW_HEIGHT * scale),int(0.0688 * WINDOW_HEIGHT)))
		go_back_button = Button(int(0.051*WINDOW_WIDTH + image.get_width() / 2), int(0.075*WINDOW_HEIGHT),image, 1)
		mapping = True
		while mapping:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					#Check click Map
					for i in range(6):
						if self.map_thumbnail[i].rect.collidepoint(pos):
							self.map = i+1
							self.show_set()
					if go_back_button.rect.collidepoint(pos):
						mapping = False
						
			self.show_back_ground()
			#DRAW BUTTON
			for i in range(6):
				self.map_thumbnail[i].draw(display_surface)
				
			go_back_button.draw(display_surface)
			pygame.display.update()
			clock.tick(FPS)
	
	def show_set(self):
		#Lay ra anh thumbnail
		image = pygame.image.load(f"./asset/set/set_avt/all_set1.png")
		image = pygame.transform.scale(image, (int(0.286 * WINDOW_HEIGHT), int(0.286 * WINDOW_HEIGHT)))
		images = [image, image, image, image, image]
		self.sets_thumbnail = []
		# Chua te hard code
		for i in range(5):
			if i <= 2:
				self.sets_thumbnail.append(Button(int(0.192 * WINDOW_WIDTH + i * (0.16 + 0.146)*WINDOW_WIDTH)
				                        ,int(0.317 * WINDOW_HEIGHT),images[i],1))
			else:
				self.sets_thumbnail.append(Button(int(0.192 * WINDOW_WIDTH + (i-3) * (0.16 + 0.146) * WINDOW_WIDTH)
				                       , int(0.7196 * WINDOW_HEIGHT), images[i], 1))
		# Set button
		image = pygame.image.load("./asset/button/go_back_button.png")
		scale = image.get_width() / image.get_height()
		image = pygame.transform.scale(image, (int(0.0688 * WINDOW_HEIGHT * scale), int(0.0688 * WINDOW_HEIGHT)))
		# GO BACK BUTTON
		
		
		go_back_button = Button(int(0.051 * WINDOW_WIDTH + image.get_width() / 2), int(0.075 * WINDOW_HEIGHT), image, 1)
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
					#Check chosing set
					for i in range(5):
						if self.sets_thumbnail[i].rect.collidepoint(pos):
							self.set = i + 1
							self.show_bet()
			self.show_back_ground()
			# DRAW BUTTON
			for i in range(5):
				self.sets_thumbnail[i].draw(display_surface)
			go_back_button.draw(display_surface)
			pygame.display.update()
			clock.tick(FPS)
		
	
	def show_victory(self):
		pass
	
	def show_HUD(self):
		pass

	def show_box_chat(self, active): ################################
		color = BLACK
		user_text = ""

		self.font32 = pygame.font.Font("./asset/font/font1.ttf", 15)
		text_box = self.font32.render(f'Chat: {user_text}', True, BLACK) #bet_text
		text_box_rect = text_box.get_rect()
		text_box_rect.topleft = (int(WINDOW_WIDTH*0.73), int(WINDOW_HEIGHT*0.05) ) 
		
		text_chat = pygame.Rect(int(WINDOW_WIDTH*0.73), int(WINDOW_HEIGHT*0.026) , WINDOW_WIDTH // 4 , WINDOW_HEIGHT // 12 ) #text_box
		
		text_box_rect.centery = 0.02 * WINDOW_HEIGHT + text_chat.h // 2  
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				#Check Click Box
				if text_chat.collidepoint(pos):
					active = True
				else:
					active = False					
				print(active)
			if event.type == pygame.KEYDOWN:
				if active:
					if event.key == pygame.K_BACKSPACE:
						user_text = user_text[0 : -1]
					elif len(user_text) <= 20:
						print("xx")
						user_text += event.unicode
						print(user_text)
		
			
		#CHECK COLORS OF THE BOX
		if active:
			color = GREEN
		else:
			color = BLACK
		
		text_box = self.font32.render(f'Nhap chat: {user_text}', True, color) #update HUD
		display_surface.blit(text_box, text_box_rect)
		pygame.draw.rect(display_surface, color, text_chat , 3 ) ############s#bỏ

		return active



	
	def race(self):
		self.menu_music.stop()
		racing = True
		map = pygame.transform.scale(pygame.image.load(f"./asset/map/map{self.map}.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
		box_chat = pygame.transform.scale(pygame.image.load(f"./asset/image/box_chat.png"), ( int(WINDOW_WIDTH*0.3), int(WINDOW_HEIGHT*0.15) ) )
		backmap = pygame.image.load(f"./asset/map/backmap{self.map}.jpg")
		scale = backmap.get_width() / backmap.get_height()
		backmap = pygame.transform.scale(backmap,(WINDOW_HEIGHT * scale,WINDOW_HEIGHT))
		player_group = pygame.sprite.Group()
		for i in range(1, 6):
			player = Player(i, 0, WINDOW_HEIGHT * 0.263351 + (i - 1) * WINDOW_HEIGHT * 0.17407407407)
			player_group.add(player)
		scroll = 0
		mouse_click = False
		while racing:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				#if event.type == pygame.MOUSEBUTTONDOWN:
					#pos = pygame.mouse.get_pos()

			#Scroll the back_ground behide
			scroll += 1
			if scroll >= backmap.get_width():
				scroll = 0
			for i in range(3):
				display_surface.blit(backmap,(i * backmap.get_width() - scroll, 0))
				
			#Box chat
			#print(mouse_click, "ttttt")
			display_surface.blit(box_chat, ( int(WINDOW_WIDTH*0.7), 0) ) 
			mouse_click = self.show_box_chat(mouse_click)
			#print(mouse_click, "yyy")
			#Blit the road
			display_surface.blit(map, (0, 0))
			
		
			#Run the player
			player_group.update()
			player_group.draw(display_surface)
			
			#Blit the HUD
			self.show_HUD()
			
			pygame.display.update()
			clock.tick(FPS)
			


class Player(pygame.sprite.Sprite):
	def __init__(self, index, x, y):
		super().__init__()
		self.index = index
		self.speed = random.uniform(1,2)
		self.animate_fps = .3
		self.frame = []
		for i in range(9):
			image = pygame.image.load(f"./asset/set/set{my_game.set}/{self.index}/{i + 1}.png")
			scale = image.get_width() / image.get_height()
			self.frame.append(pygame.transform.scale(image, (int(WINDOW_HEIGHT*0.15*scale), int(WINDOW_HEIGHT*0.15))))
		
		self.current_frame = 0
		self.image = self.frame[self.current_frame]
		self.rect = self.image.get_rect()
		self.rect.bottomleft = (x, y)
		self.positonx = x
	
	def update(self):
		if self.rect.right <= WINDOW_WIDTH:
			self.positonx += self.speed
			self.rect.x = int(self.positonx)
			self.animate(self.animate_fps)
	
	def animate(self, fps):
		self.current_frame += fps
		if self.current_frame >= 8:
			self.current_frame = 0
		self.image = self.frame[int(self.current_frame)]
	
	

pygame.init()
my_game = Game()
my_game.main()
