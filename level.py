import pygame
from tiles import Tile, Water, Lift, Button
from settings import tile_size
from player import Gepesz
from infos import Infos

class Level:
    button_pos_offset = 23
    BUTTON_SPEED = 3
    def __init__(self, level_data, surface, infos, gepesz):
        self.display_surface = surface
        self.tiles_dict = {}
        self.players = pygame.sprite.Group()  
        self.infos = infos  
        self.gepesz = gepesz  



        self.setup_level(level_data)

   

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        row_index = 0
        



        for row_index, row in enumerate(layout):
            for coll_index, cell in enumerate(row):
                if cell == "S":
                    x = coll_index * tile_size
                    y = row_index * tile_size
                    tile_X = Tile((x, y))
                    self.tiles.add(tile_X)  
                elif cell == "I":
                    x = coll_index * tile_size
                    y = row_index * tile_size
                    self.infos.rect.topleft = (x, y)  
                    self.players.add(self.infos)  
                elif cell == "G":
                    x = coll_index * tile_size
                    y = row_index * tile_size
                    self.gepesz.rect.topleft = (x, y)  
                    self.players.add(self.gepesz)  
                elif cell == "W":
                    x = coll_index * tile_size
                    y = row_index * tile_size
                    tile_X = Water((x, y))
                    self.tiles.add(tile_X)
                elif cell == "L":
                    x = coll_index * tile_size
                    y = row_index * tile_size
                    tile_X = Lift((x, y))
                    self.tiles.add(tile_X)    
                elif cell == "B":
                    x = coll_index * tile_size
                    y = row_index * tile_size + self.button_pos_offset
                    self.button = Button((x, y))
                    self.tiles.add(self.button)                      






    def run(self):
        self.players.update()
        self.players.draw(self.display_surface)
        self.horizontal_collision()
        self.vertical_collision()
        self.tiles.draw(self.display_surface)

    def horizontal_collision(self):
        for player in self.players:
            player.rect.x += player.direction.x * player.speed

            for sprite in self.tiles.sprites():
                if isinstance(sprite, Water):
                    continue
                if isinstance(sprite, Button):
                    if sprite.rect.colliderect(player.rect):
                        self.button.direction.y = 1
                        self.button.rect.y += self.button.direction.y
                if sprite.rect.colliderect(player.rect):
                    if player.direction.x < 0:
                        player.rect.left = sprite.rect.right
                    elif player.direction.x > 0:
                        player.rect.right = sprite.rect.left

    def vertical_collision(self):
        for player in self.players:
            player.apply_gravity()

            for sprite in self.tiles.sprites():
                if isinstance(sprite, Water):
                    continue
                if isinstance(sprite, Button):
                    if sprite.rect.colliderect(player.rect):
                        self.button.direction.y = 1
                        self.button.rect.y += self.button.direction.y
                if sprite.rect.colliderect(player.rect):
                    if player.direction.y > 0:
                        player.rect.bottom = sprite.rect.top
                        player.direction.y = 0
                        player.on_ground = True
                    elif player.direction.y < 0:
                        player.rect.top = sprite.rect.bottom
                        player.direction.y = 0
                        player.on_ceiling = True
        
        for player in self.players:
            if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
                player.on_ground = False
            if player.on_ceiling and player.direction.y > 0:
                player.on_ceiling = False
