import pygame

# Tile size
TILE_SIZE = 32
bg_scroll = 0
TILE_TYPES = 21
screen_scroll =0

width = 800
height = 650
win = pygame.display.set_mode((width, height))
#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'scripts/img/Tile/{x}.png')
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)

class World():
	def __init__(self):
		self.obstacle_list = []

	def process_data(self, data):
		self.level_length = len(data[0])
		#iterate through each value in level data file
		for y, row in enumerate(data):
			for x, tile in enumerate(row):
				if tile >= 0:
					img = img_list[tile]
					img_rect = img.get_rect()
					img_rect.x = x * TILE_SIZE
					img_rect.y = y * TILE_SIZE
					tile_data = (img, img_rect)
					if tile >= 0 and tile <= 8:
						self.obstacle_list.append(tile_data)

	def draw(self):
		for tile in self.obstacle_list:
			tile[1][0] += screen_scroll
			win.blit(tile[0], tile[1])