# tile_collision.py
import csv

import pygame

# Tile size and tile types
TILE_SIZE = 32
SOLID_TILES = [2]  # List of tile types that are solid (e.g., Box tile type is 2)

# Tile collision check function
def check_tile_collision(player, tile_map):
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    # Check for tile collisions (solid tiles)
    for row in range(len(tile_map)):
        for col in range(len(tile_map[row])):
            tile = tile_map[row][col]
            if tile in SOLID_TILES:  # Solid tile
                tile_rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if player_rect.colliderect(tile_rect):

                        return True  # Collision detected
    return False  # No collision

# Function to load the tile map from CSV
def load_tile_map(filename="level1_data.csv"):
    """
    Load a tile map from a CSV file. Each tile is represented by an integer.
    """
    tile_map = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            tile_map.append([int(cell) for cell in row])
    return tile_map

# Function to draw the tile map on the screen
def draw_tile_map(tile_map, win, water_tile, box):
    """
    Draw the tile map using the provided tile images.
    """
    for row in range(len(tile_map)):
        for col in range(len(tile_map[row])):
            tile = tile_map[row][col]
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            
            # Draw the correct tile based on its value
            if tile == 1:
                win.blit(water_tile, (x, y))
            elif tile == 2:
                win.blit(box, (x, y))
            else:
                pass  # For empty or non-solid tiles, you can add grass or background tiles
