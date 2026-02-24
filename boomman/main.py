import time
import arcade 
from arcade import key
import random

from animation import Animate

SCREEN_WIDTH = 660
SCREEN_HEIGHT = 660
SCREEN_TITLE = "Bomberman"

CELL_WIDTH = 60
CELL_HEIGHT = 60

COLUMN_COUNT = SCREEN_WIDTH // CELL_WIDTH
ROW_COUNT = SCREEN_HEIGHT // CELL_HEIGHT


score_virtical = -1
class Game (arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
        
        self.power = 2

    def setup(self):
        self.dead_player_one = False
        self.dead_player_two = False
        self.gamever_bg = None
        self.gameover1 = arcade.load_texture("win/win1.png")
        self.gameover2 = arcade.load_texture("win/win2.png")
        self.go_rect = arcade.LBWH(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
        self.bg = arcade.load_texture('Blocks/BackgroundTile.png')
        self.solid_walls = arcade.SpriteList()
        self.boxes_list = arcade.SpriteList()
        self.player = Player()
        self.player2 = Player()
        self.flimes = arcade.SpriteList()
        
        
        for x in range(1, COLUMN_COUNT, 2):
            for y in range(1, COLUMN_COUNT,2):
                wall = Wall()
                wall.left = x*CELL_WIDTH
                wall.bottom = y*CELL_HEIGHT
                self.solid_walls.append(wall)

        clear_coords = [(0,0),(1,0),(2,0),(0,1),(0,2),(10,8),(10,9),(10,10),(9,10),(8,10)]
        for x in range(0, COLUMN_COUNT, ):
            for y in range(0, COLUMN_COUNT,):
                if x % 2 == 1 and  y % 2 == 1:
                    continue
                if (x,y) in clear_coords:
                    continue
                generation = random.randint(0, 3)
                if generation < 2:
                    continue
                box = Box()
                box.left = x*CELL_WIDTH
                box.bottom = y*CELL_HEIGHT
                print(box.bottom)
                self.boxes_list.append(box)
        self.player.position = arcade.Vec2(x= 630,y =630)
        self.player2.position = arcade.Vec2(CELL_HEIGHT,CELL_WIDTH)
            

    def on_update(self,delta):
        self.player.update_animation(delta/5)
        self.player.update()
        self.player2.update_animation(delta/5)
        self.player2.update()
        self.player.bombs.update()
        self.player2.bombs.update()
        self.flimes.update_animation(delta*150)
        self.player.bombs.update_animation(delta*150)
        self.player2.bombs.update_animation(delta*150)
        self.kill()
        
        
    def kill(self):
        if arcade.check_for_collision_with_list(self.player,windows.flimes):
            self.dead_player_one = True
            
        else:
            if arcade.check_for_collision_with_list(self.player2,windows.flimes):
                self.dead_player_two = True
                
    
        
            


    def draw_back(self):
        for x in range(COLUMN_COUNT):
            for y in range(COLUMN_COUNT):
                rect = arcade.XYWH(x*CELL_WIDTH,y*CELL_HEIGHT,CELL_WIDTH,CELL_HEIGHT, arcade.Vec2(0,0))
                arcade.draw_texture_rect(self.bg, rect)
        

    def on_draw(self):
        self.clear()
        self.draw_back()
        self.solid_walls.draw()
        self.boxes_list.draw()
        self.player.bombs.draw()
        self.player2.bombs.draw()
        arcade.draw_sprite(self.player)
        arcade.draw_sprite(self.player2)
        self.flimes.draw()
        if self.dead_player_two:
            windows.clear()
            arcade.draw_texture_rect(self.gameover2,self.go_rect)
            
        if self.dead_player_one:
            windows.clear()
            arcade.draw_texture_rect(self.gameover1,self.go_rect)
            


    def on_key_press(self,key,mod):
        if arcade.key.SPACE:
            pass
        if arcade.key.A == key:
            self.player.derection = 3
            self.player.change_x  = -2
            self.player.stop_animation = False
        if arcade.key.D == key:
            self.player.derection = 2
            self.player.change_x  = 2
            self.player.stop_animation = False
        if arcade.key.S == key:
            self.player.change_y  = -2
            self.player.derection = 1
            self.player.stop_animation = False
        if arcade.key.W == key:
            self.player.change_y  = 2
            self.player.derection = 0
            self.player.stop_animation = False
            
        if arcade.key.SPACE:
            pass
        if arcade.key.UP == key:
            self.player2.derection = 0
            self.player2.change_y  = 2
            self.player2.stop_animation = False
        if arcade.key.LEFT == key:
            self.player2.derection = 3
            self.player2.change_x  = -2
            self.player2.stop_animation = False
        if arcade.key.DOWN == key:
            self.player2.change_y  = -2
            self.player2.derection = 1
            self.player2.stop_animation = False
        if arcade.key.RIGHT == key:
            self.player2.change_x  = 2
            self.player2.derection = 2
            self.player2.stop_animation = False
        if arcade.key.G == key:
            self.player.spawn_bomb()
        if arcade.key.H == key:
            self.player2.spawn_bomb()
        
        self.player.update_sprite_list()        
        self.player2.update_sprite_list()  

    def on_key_release(self,key,mod):
        p1keys = [arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D] 
        p2keys = [arcade.key.UP, arcade.key.LEFT, arcade.key.DOWN, arcade.key.RIGHT] 
 
        if key in p2keys:
            self.player2.change_x = 0
            self.player2.change_y = 0
            self.player2.stop_animation = True
            
            
        if key in p1keys:
            self.player.change_x = 0
            self.player.change_y = 0
            self.player.stop_animation = True
class Flime(Animate):
    def __init__(self):
        super ().__init__("Flame/Flame_f00.png")
        for i in range(3):
            self.textures.append(arcade.load_texture(f'Flame/Flame_f0{i}.png'))
            

    
class Bombs(Animate):
    def __init__(self, power, player):
        super ().__init__('Bomb/Bomb_f00.png')
        for i in range(3):
            self.textures.append(arcade.load_texture(f'Bomb/Bomb_f0{i}.png'))
            
        self.timer = time.time()
        self.detonated = False
        
        self.power = power
        self.player = player
        
    def spawn_flime(self):
            
        dirs = [[-1,0],[0, 1],[1, 0],[0, -1], [0,0]]
        
        for dir in dirs: 
            print(self.power)
            for i in range(1, int(self.power)):
                x_dir = dir[0]
                y_dir = dir[1]
                
                flime =Flime()
                
                
                x_dir *= CELL_WIDTH * i
                y_dir *= CELL_HEIGHT * i
                
                flime.center_x = self.center_x + x_dir
                flime.center_y = self.center_y + y_dir
                coll_sprites = arcade.check_for_collision_with_list(flime,windows.boxes_list)
                coll_sprites_solid = arcade.check_for_collision_with_list(flime,windows.solid_walls)
                if len(coll_sprites_solid) > 0:
                    break
                
                windows.flimes.append(flime)
                self.player.stats['bomb_power'] += len(coll_sprites)/1
                print(self.power)

                
                for box in coll_sprites:
                    box.kill()
                    
                if  len(coll_sprites) > 0:
                    break

        
    def update(self, delta_time):
        self.update_animation(delta_time)
        
        if time.time()-self.timer >3 and not self.detonated:
            self.spawn_flime()
            self.kill()
            self.detonated =True
            
    

class Player (Animate):
    def __init__(self):
        super().__init__('Bomberman/Front/Bman_F_f00.png', 0.5)

        self.bombs = arcade.SpriteList()
        
        self.back_sprites = []
        self.front_sprites = []
        self.right_sprites = []
        self.left_sprites = []
        
        self.derection = 1
        
        self.stats = {
            "bomb_power":2
            
            
        }
        
        for i in range(8):
            self.back_sprites.append(arcade.load_texture(f'Bomberman/Back/Bman_B_f0{i}.png'))
            self.front_sprites.append(arcade.load_texture(f'Bomberman/Front/Bman_F_f0{i}.png'))
            self.right_sprites.append(arcade.load_texture(f'Bomberman/Side/Bman_S_f0{i}.png'))
            self.left_sprites.append(arcade.load_texture(f'Bomberman/Side/Bman_S_f0{i}.png').flip_horizontally())
            

            

    def update(self, delta_time = 1 / 60, *args, **kwargs):
        super().update(delta_time, *args, **kwargs)
        
        
        
    
        rar = arcade.check_for_collision_with_lists(self,[windows.boxes_list, windows.solid_walls])
        for box  in rar:
            
            if self.right > box.left and self.left < box.left:
                self.right = box.left

            elif self.left < box.right and self.right > box.right:
                self.left = box.right

            if self.bottom < box.top and self.top > box.top:
                self.bottom = box.top

            elif self.top > box.bottom and self.bottom < box.bottom:
                self.top = box.bottom
                
        if self.center_x > SCREEN_WIDTH:
            self.center_x = SCREEN_WIDTH
        elif self.center_x <0:
            self.center_x = 0 
        if self.center_y > SCREEN_HEIGHT:
            self.center_y = SCREEN_HEIGHT
        elif self.center_y <0:
            self.center_y = 0 
        

                

    def update_sprite_list(self):
        self.textures = (self.back_sprites,self.front_sprites,self.right_sprites,self.left_sprites)[self.derection]
        
    def spawn_bomb(self):
        get_x = self.center_x
        get_y = self.center_y
        bomb = Bombs(self.stats['bomb_power'], self)
        bomb.center_x = get_x//CELL_WIDTH * CELL_WIDTH + CELL_WIDTH/2
        bomb.center_y =  get_y//CELL_HEIGHT * CELL_HEIGHT + CELL_HEIGHT/2
        self.bombs.append(bomb)

class Wall(arcade.Sprite):
    def __init__(self, ):
        super().__init__('Blocks/SolidBlock.png')


class Box(arcade.Sprite):
    def __init__(self, ):
        super().__init__('Blocks/ExplodableBlock.png')
        
    

        
windows = Game()
windows.setup()
windows.run()