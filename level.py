from typing import List
import pygame
from pygame.sprite import Sprite
from tiles import Activate, Ajtó, Asztal, Barrier, Button, Csempe, Lift, Parketta, Platform, Switch, Szék, Tile, Water, Finished_check
from settings import HEIGHT, WIDTH, level_choice, level_map_1, level_map_2, level_map_3, level_map_4, level_map_5, level_map_6, level_map_7, level_map_8, level_map_9, tile_size
from player import Gepesz
from infos import Infos
from enemy import Enemy
from menu import Menu
from events import event_death
from timer import Scorer, Timer

class Level:
    button_pos_offset = 23
    BUTTON_SPEED = 3
    button_original_pos: int = 0
    button_onoff_infos: bool = False
    button_onoff_gepesz: bool = False
    full_lift: list[Lift] = []
    lift_original: int = 0
    switch_on: bool = False
    infos_alive: bool = True
    gepesz_alive: bool = True
    switch_pic: str = "graphics/temp/switch_off.png"
    lift_max: int = 0
    current_level: list[str] = level_choice
    background_image: str = "graphics/map/palyavalasztos(folyoso).png"
    infos_finished: bool = False
    gepesz_finished: bool = False
    enemy_facing_left: bool = True
    level_1_complete: bool = False
    level_2_complete: bool = False
    level_3_complete: bool = False
    level_4_complete: bool = False
    level_5_complete: bool = False
    level_6_complete: bool = False
    level_7_complete: bool = False
    level_8_complete: bool = False
    level_9_complete: bool = False
    game_finished: bool = False
    enemy: Enemy = Enemy((int(WIDTH / 2), int(HEIGHT / 2)))
    infos: Infos = Infos((int(WIDTH / 2), int(HEIGHT / 2 - 50)))
    gepesz: Gepesz = Gepesz((int(WIDTH / 2), int(HEIGHT / 2)))

    def __init__(self, surface: pygame.Surface, infos: Infos, gepesz: Gepesz, opp: Enemy , font: pygame.font.Font, clock: Timer, scorer: Scorer):
        self.display_surface = surface
        self.tiles_dict = {}
        self.players: pygame.sprite.Group[Sprite] = pygame.sprite.Group() # type: ignore
        self.infos: Infos = infos
        self.gepesz: Gepesz = gepesz
        self.enemy: Enemy = opp
        self.menu_object = Menu(surface)
        self.setup_level(self.current_level)
        self.game_font = font
        self.timer = clock
        self.scorer = scorer

    def setup_level(self, layout: List[str]):
        self.tiles: pygame.sprite.Group[Sprite] = pygame.sprite.Group() # type: ignore
        self.enemy.rect.topleft = (5000, 5000)
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
                    self.infos.save_original_pos((x, y))
                elif cell == "G":
                    x = coll_index * tile_size
                    y = row_index * tile_size
                    self.gepesz.rect.topleft = (x, y)
                    self.players.add(self.gepesz)
                    self.gepesz.save_original_pos((x, y))
                elif cell == "E":
                    x = coll_index * tile_size
                    y = row_index * tile_size - 33
                    self.enemy.rect.topleft = (x, y)
                    self.enemy.save_original_pos((x, y))
                elif cell == "W":
                    x = coll_index * tile_size
                    y = row_index * tile_size + 12
                    tile_X = Water((x, y))
                    self.tiles.add(tile_X)
                elif cell == "L":
                    x = coll_index * tile_size
                    y = row_index * tile_size
                    self.lift = Lift((x, y))
                    self.tiles.add(self.lift)
                    self.full_lift.append(self.lift)
                    self.lift_original = self.lift.rect.y
                elif cell == "B":
                    x = coll_index * tile_size
                    y = row_index * tile_size + self.button_pos_offset
                    self.button = Button((x, y))
                    self.tiles.add(self.button)
                    self.button_original_pos = self.button.rect.y
                elif cell == "K":
                    x = coll_index * tile_size
                    y = row_index * tile_size
                    self.switch = Switch((x, y), self.switch_pic)
                    self.tiles.add(self.switch)
                elif cell == "A":
                    x = coll_index * tile_size
                    y = row_index * tile_size
                    self.barrier = Barrier((x, y))
                    self.tiles.add(self.barrier)
                elif cell == "D":
                    x = coll_index * tile_size
                    y = row_index * tile_size
                    self.barrier = Asztal((x, y))
                    self.tiles.add(self.barrier)
                elif cell == "C":
                    x = coll_index * tile_size
                    y = row_index * tile_size
                    self.actiave = Activate((x, y))
                    self.tiles.add(self.actiave)
                elif cell == "T":
                    x = coll_index * tile_size
                    y = row_index * tile_size
                    self.csempe = Csempe((x, y))
                    self.tiles.add(self.csempe)
                elif cell == "P":
                    x = coll_index * tile_size
                    y = row_index * tile_size
                    self.parketta = Parketta((x, y))
                    self.tiles.add(self.parketta)
                elif cell == "s":
                    x = coll_index * tile_size
                    y = row_index * tile_size
                    self.szek = Szék((x, y))
                    self.tiles.add(self.szek)
                elif cell == "i":
                    x = coll_index * tile_size
                    y = row_index * tile_size
                    self.szek = Finished_check((x, y))
                    self.tiles.add(self.szek)
                elif cell == "F":
                    x = coll_index * tile_size
                    y = row_index * tile_size - 15
                    self.szek = Ajtó((x, y))
                    self.tiles.add(self.szek)
                elif cell == "H":
                    x = coll_index * tile_size
                    y = row_index * tile_size
                    self.platform = Platform((x, y))
                    self.tiles.add(self.platform)

    def level_reset(self):
        self.infos.rect.topleft = self.infos.original_pos
        self.gepesz.rect.topleft = self.gepesz.original_pos
        self.enemy.rect.topleft = self.enemy.original_pos
        self.switch_on = False
        self.switch_pic = "graphics/temp/switch_off.png"
        self.timer.reset_timer()
        self.setup_level(self.current_level)

    def home(self):
        self.setup_level(level_choice)
        self.timer.reset_timer()
        self.background_image = "graphics/map/palyavalasztos(folyoso).png"
        self.switch_on = False
        self.switch_pic = "graphics/temp/switch_off.png"
        self.current_level = level_choice
        self.enemy.rect.x = 10000
        self.infos_finished = False
        self.gepesz_finished = False

    def lift_up(self):
        for i in self.full_lift:
            if i.rect.y > self.lift_max:
                i.rect.y -= 4

    def lift_down(self):
        for i in self.full_lift:
            if self.lift_original > i.rect.y:
                i.rect.y += round(1.5)

    def run(self):
        self.infos.update()
        self.gepesz.update()
        self.players.draw(self.display_surface)
        self.enemy.draw(self.display_surface)
        self.horizontal_collision()
        self.vertical_collision()
        self.tiles.draw(self.display_surface)
        self.enemy_movement()
        self.map_choose()
        self.finish()
        self.enemy.change_image(self.enemy_facing_left)
        self.timer.time_print()
        if self.current_level == level_choice:
            self.lift_max = 450
            self.background_image = "graphics/map/palyavalasztos(folyoso).png"
        elif self.current_level == level_map_1:
            self.lift_max = 650
            self.background_image = "graphics/map/terem_hatter.png"
        elif self.current_level == level_map_3:
            self.lift_max = 257
        elif self.current_level == level_map_5:
            self.lift_max = 195
        elif self.current_level == level_map_7:
            self.lift_max = 610
            self.background_image = "graphics/map/jedlik_epulet.png"

        if not self.infos_alive or not self.gepesz_alive:
            pygame.event.post(pygame.event.Event(event_death))
        self.menu_object.delete_all()

    def pausemenu(self):
        self.menu_object.menudraw("pause")
        self.scorer.print_score()

    def deathmenu(self):
        self.menu_object.menudraw("death")
        self.timer.reset_timer()
        self.scorer.print_score()
        self.gepesz_alive = True
        self.infos_alive = True

    def endmenu(self):
        self.menu_object.menudraw("end")
        self.scorer.print_score()

    def screen_fill(self, screen: pygame.Surface, BACKGROUND: pygame.Surface):
        screen.blit(BACKGROUND, (0, 0))

    def enemy_movement(self):
        if self.enemy_facing_left:
            self.enemy.rect.x -= self.enemy.speed
        else:
            self.enemy.rect.x += self.enemy.speed
        for sprite in self.tiles.sprites():
            if isinstance(sprite, Barrier):
                if sprite.rect.colliderect(self.enemy.rect):
                    if self.enemy_facing_left:
                        self.enemy_facing_left = False
                    else:
                        self.enemy_facing_left = True
            if isinstance(sprite, Tile):
                if sprite.rect.colliderect(self.enemy.rect):
                    if self.enemy_facing_left:
                        self.enemy_facing_left = False
                    else:
                        self.enemy_facing_left = True

    def horizontal_collision(self):
        player_list: List[Gepesz|Infos] = self.players.sprites() # type: ignore
        for player in player_list:
            player.rect.x += int(player.direction.x * player.speed)

            for sprite in self.tiles.sprites():
                if isinstance(sprite, Water):
                    continue
                if isinstance(sprite, Barrier):
                    continue
                if isinstance(sprite, Ajtó):
                    continue
                if isinstance(sprite, Activate):
                    if sprite.rect.colliderect(player.rect):
                        self.setup_level(level_map_1)
                        self.current_level = level_map_1
                        self.background_image = "graphics/map/terem_hatter.png"

                if isinstance(sprite, Switch):
                    if sprite.rect.colliderect(player.rect):
                        if player.direction.x > 0 and player.rect.left < sprite.rect.left: # type: ignore
                            self.switch_on = True
                        elif player.direction.x < 0 and player.rect.right > sprite.rect.right: # type: ignore
                            self.switch_on = False
                            self.switch_pic = "graphics/temp/switch_off.png"
                        else:
                            self.switch_on = False
                    sprite.update_image(self.switch_on)
                player_list: List[Gepesz|Infos] = self.players.sprites() # type: ignore
                for other_player in player_list:
                    if other_player != player and player.rect.colliderect(other_player.rect):
                        if player.direction.x > 0:
                            player.rect.right = other_player.rect.left
                        elif player.direction.x < 0:
                            player.rect.left = other_player.rect.right
                if self.enemy.rect.colliderect(player.rect):
                    if player == self.infos:
                        self.infos_alive = False
                    elif player == self.gepesz:
                        self.gepesz_alive = False

                if sprite.rect.colliderect(player.rect): # type: ignore
                    if player.direction.x < 0:
                        player.rect.left = sprite.rect.right # type: ignore
                    elif player.direction.x > 0:
                        player.rect.right = sprite.rect.left # type: ignore

    def map_load(self):
        self.background_image = "graphics/map/terem_hatter.png"
        self.timer.reset_timer()

    def map_choose(self) -> None:
        player_list: List[Gepesz|Infos] = self.players.sprites() # type: ignore
        for player in player_list:
            if self.current_level == level_choice:
                keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and 108 < player.rect.x < 250 and 800 < player.rect.y < 900:
                    self.setup_level(level_map_1)
                    self.current_level = level_map_1
                    self.map_load()
                elif keys[pygame.K_SPACE] and 540 < player.rect.x < 680 and 680 < player.rect.y < 900:
                    self.setup_level(level_map_2)
                    self.current_level = level_map_2
                    self.map_load()
                elif keys[pygame.K_SPACE] and 990 < player.rect.x < 1130 and 680 < player.rect.y < 900:
                    self.setup_level(level_map_3)
                    self.current_level = level_map_3
                    self.map_load()
                elif keys[pygame.K_SPACE] and 1410 < player.rect.x < 1540 and 680 < player.rect.y < 900:
                    self.setup_level(level_map_4)
                    self.current_level = level_map_4
                    self.map_load()
                elif keys[pygame.K_SPACE] and 1580 < player.rect.x < 1730 and 220 < player.rect.y < 480:
                    self.setup_level(level_map_5)
                    self.current_level = level_map_5
                    self.map_load()
                elif keys[pygame.K_SPACE] and 1190 < player.rect.x < 1340 and 220 < player.rect.y < 480:
                    self.setup_level(level_map_6)
                    self.current_level = level_map_6
                    self.map_load()
                elif keys[pygame.K_SPACE] and 800 < player.rect.x < 940 and 220 < player.rect.y < 480:
                    self.setup_level(level_map_7)
                    self.current_level = level_map_7
                    self.map_load()
                elif keys[pygame.K_SPACE] and 430 < player.rect.x < 570 and 220 < player.rect.y < 480:
                    self.setup_level(level_map_8)
                    self.current_level = level_map_8
                    self.map_load()
                elif keys[pygame.K_SPACE] and 90 < player.rect.x < 230 and 220 < player.rect.y < 480:
                    self.setup_level(level_map_9)
                    self.current_level = level_map_9
                    self.background_image = "graphics/map/jedlik_epulet.png"

    def complete(self) -> None:
        if self.current_level == level_map_1:
            self.level_1_complete = True

        if self.current_level == level_map_2:
            self.level_2_complete = True

        if self.current_level == level_map_3:
            self.level_3_complete = True

        if self.current_level == level_map_4:
            self.level_4_complete = True

        if self.current_level == level_map_5:
            self.level_5_complete = True

        if self.current_level == level_map_6:
            self.level_6_complete = True

        if self.current_level == level_map_7:
            self.level_7_complete = True

        if self.current_level == level_map_8:
            self.level_8_complete = True

        if self.current_level == level_map_9:
            self.level_9_complete = True

        if self.level_1_complete and self.level_2_complete and self.level_3_complete and self.level_4_complete and self.level_5_complete and self.level_6_complete and self.level_7_complete and self.level_8_complete and self.level_9_complete:
            self.game_finished = True

    def finish(self) -> None:
        if self.infos_finished and self.gepesz_finished:
            self.complete()
            self.setup_level(level_choice)
            self.scorer.win(int(self.timer.current_time))
            self.timer.reset_timer()
            self.background_image = "graphics/map/palyavalasztos(folyoso).png"
            self.switch_on = False
            self.switch_pic = "graphics/temp/switch_off.png"
            self.current_level = level_choice
            self.enemy.rect.x = 10000
            self.infos_finished = False
            self.gepesz_finished = False

    def vertical_collision(self):
        player_list: List[Gepesz|Infos] = self.players.sprites() # type: ignore
        for player in player_list:
            player.apply_gravity()

            for sprite in self.tiles.sprites():
                if isinstance(sprite, Barrier):
                    continue
                if isinstance(sprite, Water):
                    if sprite.rect.colliderect(player.rect):
                        if player == self.infos:
                            self.infos_alive = False
                        elif player == self.gepesz:
                            self.gepesz_alive = False
                if isinstance(sprite, Ajtó):
                    continue
                if isinstance(sprite, Finished_check):
                    if sprite.rect.colliderect(self.infos.rect):
                        self.infos_finished = True
                    if sprite.rect.colliderect(self.gepesz.rect):
                        self.gepesz_finished = True

                if isinstance(sprite, Button):
                    if sprite.rect.colliderect(player.rect):
                        if player == self.infos:
                            self.button_onoff_infos = True
                        if player == self.gepesz:
                            self.button_onoff_gepesz = True
                    else:
                        if player == self.infos:
                            self.button_onoff_infos = False
                        if player == self.gepesz:
                            self.button_onoff_gepesz = False

                if sprite.rect.colliderect(player.rect): # type: ignore
                    if player.direction.y > 0:
                        player.rect.bottom = sprite.rect.top # type: ignore
                        player.direction.y = 0
                        player.on_ground = True
                    elif player.direction.y < 0:
                        player.rect.top = sprite.rect.bottom # type: ignore
                        player.direction.y = 0
                        player.on_ceiling = True

            for other_player in player_list:
                if other_player != player and player.rect.colliderect(other_player.rect):
                    if player.direction.y > 0:
                        player.rect.bottom = other_player.rect.top
                        player.direction.y = 0
                        player.on_ground = True
                    elif player.direction.y < 0:
                        player.rect.top = other_player.rect.bottom
                        player.direction.y = 0
                        player.on_ceiling = True
            if self.enemy.rect.colliderect(player.rect):
                self.enemy.rect.x = 10000
                self.scorer.add_score(50)

            if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
                player.on_ground = False
            if player.on_ceiling and player.direction.y > 0:
                player.on_ceiling = False

        if self.button_onoff_infos or self.button_onoff_gepesz:
            if self.button_onoff_infos or self.button_onoff_gepesz:
                self.button.rect.y += 2
            self.lift_up()
        elif self.switch_on:
            self.lift_up()
            if self.button_original_pos <= self.button.rect.y:
                self.button.rect.y -= 1
        else:
            if self.button_original_pos <= self.button.rect.y:
                self.button.rect.y -= 1
            else:
                self.lift_down()
