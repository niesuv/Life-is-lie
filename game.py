import pygame, sys
import login

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Muahaha')
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

# Display some text
font = pygame.font.Font(None, 36)
text = font.render("Hello There", 1, (10, 10, 10))
textpos = text.get_rect()
textpos.centerx = background.get_rect().centerx
background.blit(text, textpos)

# Blit everything to the screen
screen.blit(background, (0, 0))
pygame.display.flip()

# Event loop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			pos = login.log()
			print(pos)
			if pos < 0:
				pygame.quit()
				sys.exit()
		

	screen.blit(background, (0, 0))
	pygame.display.flip()
