import pygame,random,sys


#FPS and clock
FPS = 60
clock = pygame.time.Clock()
#Define Colors
GREEN = (10, 50, 10)
BLACK = (0,0,0)

#Create Display Surface(SCALE = 16 / 9)
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 675

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def draw(self, surface):
		surface.blit(self.image, self.rect)


class Game():
    def __init__(self):
        self.scroll = 0
        self.direction_scroll = 1
        #Get BACKGROUND
        image = pygame.image.load("./asset/image/back.webp").convert()
        scale = int( image.get_width() / image.get_height() )
        self.back_ground_image = pygame.transform.scale(image, (int(WINDOW_HEIGHT * scale), WINDOW_HEIGHT))
        #Game Value, SET in TEXT file
        self.gold = 1000
        self.map = 1
        self.set = 1
        self.bet = 1
        self.history = []




    def main(self):
        running = True
        while running:
            #Check close
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.show_main_menu()
            clock.tick(FPS)


    def show_main_menu(self):
        self.menu_music = pygame.mixer.Sound("./asset/music/menu_music.mp3")
        start_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3,
                                     pygame.image.load("./asset/button/start_button.png"), 0.2)
        setting_button = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 100,
                                     pygame.image.load("./asset/button/setting_button.png"), 0.2)
        main_menu_run = True
        self.menu_music.play(-1)
        while main_menu_run:
            self.show_back_ground()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #CHECK CLICK BUTTON
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if start_button.rect.collidepoint(pos):
                        self.start_new_round()
            start_button.draw(display_surface)
            setting_button.draw(display_surface)
            pygame.display.update()
            clock.tick(FPS)

    def show_back_ground(self):
        if self.scroll <= 0:
            self.direction_scroll = 1
        if self.scroll >= self.back_ground_image.get_width() - WINDOW_WIDTH:
            self.direction_scroll = -1
        self.scroll += self.direction_scroll*.5
        display_surface.blit(self.back_ground_image,(-self.scroll,0))


    def start_new_round(self):
        self.show_map()
        self.race()

    def show_setting(self):
        pass

    def show_bet(self):
        pass

    def show_map(self):
        #SET BUTTON
        image = pygame.image.load("./asset/map/map1.png")
        scale = image.get_width() / image.get_height()
        image = pygame.transform.scale(image, (300 * scale, 300))
        map_button1 = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, image, 1)

        mapping = True
        while mapping:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if map_button1.rect.collidepoint(pos):
                        self.map = 1
                        mapping = False
            display_surface.fill(BLACK)
            map_button1.draw(display_surface)
            pygame.display.update()
            clock.tick(FPS)

    def show_set(self):
        pass

    def show_victory(self):
        pass

    def race(self):
        self.menu_music.stop()
        racing = True
        map = pygame.transform.scale(pygame.image.load(f"./asset/map/map{self.map}.png"),(WINDOW_WIDTH,WINDOW_HEIGHT))
        player_group = pygame.sprite.Group()
        for i in range(1,6):
            player = Player(i,0,WINDOW_HEIGHT*0.412 + (i-1)*WINDOW_HEIGHT*0.113)
            player_group.add(player)

        while racing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

            display_surface.blit(map, (0,0))
            player_group.update()
            player_group.draw(display_surface)
            pygame.display.update()
            clock.tick(FPS)

class Player(pygame.sprite.Sprite):
    def __init__(self, index, x , y):
        super().__init__()
        self.index = index
        self.speed = random.randint(1,3)
        self.animate_fps = .2
        self.frame = []
        for i in range(9):
            image = pygame.image.load(f"./asset/set/1/{i+1}.png")
            self.frame.append(pygame.transform.scale(image, (50,60)))

        self.current_frame = 0
        self.image = self.frame[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)



    def update(self):
        if self.rect.right <= WINDOW_WIDTH:
            self.rect.x += self.speed
            self.animate(self.animate_fps)

    def animate(self,fps):
        self.current_frame += fps
        if self.current_frame >= 8:
            self.current_frame = 0
        self.image = self.frame[int(self.current_frame)]



pygame.init()
my_game = Game()
my_game.main()
