import pygame
import random
from dino_runner.utils.constants import *
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.text_utils import draw_message_component
from dino_runner.components.powerups.power_up_manager import PowerUpManager
from dino_runner.components.powerups.desacelerar_manager import DesacelerarManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.score = 0
        self.death_count = 0
        self.game_speed = 20
        self.x_nuvem = SCREEN_WIDTH
        self.y_nuvem = random.randint(100, 230)
        self.x_meteor = random.randint(40, 600)
        self.y_meteor = - 300 - random.randint(10, 200)
        self.x_meteor2 = random.randint(40, 600)
        self.y_meteor2 = -80 - random.randint(100, 200)
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.x_sol = -90
        self.y_sol = 200
        self.x_lua = -84
        self.y_lua = 200
        self.player = Dinosaur()
        self.desdel = DesacelerarManager()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.desdel.reset_des()
        self.game_speed = 20
        self.score = 0
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self.score, self.game_speed, self.player)
        self.desdel.update(self, self.score)
    
    def update_score(self):
        self.score += 0.25
        if self.score % 20 == 0 and self.score < 200:
            self.game_speed += 1.5
        if self.score > 100:
            self.score += 0.25
        if self.score > 300:
            self.score += 0.5
            if self.score % 50 == 0 and self.score > 300:
                self.game_speed += 2
        if self.game_speed >= 53:
            self.game_speed = 53

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        if  self.x_sol >= SCREEN_WIDTH:
            self.screen.fill((0, 0, 0))
        if self.x_lua >= SCREEN_WIDTH:
            self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        self.desdel.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()
    


    def draw_background(self):
        self.screen.blit(SOL, (self.x_sol, self.y_sol))      
        self.screen.blit(LUA, (self.x_lua, self.y_lua))        

        if self.x_sol < SCREEN_WIDTH:
            self.x_lua = -84
            self.y_lua = 200
            self.x_sol += 1
            self.y_sol -= 0.20
            if self.x_sol > SCREEN_WIDTH/2: 
                self.y_sol += 0.40

        elif self.x_sol >= SCREEN_WIDTH:
            self.x_lua += 1
            self.y_lua -= 0.20
            if self.x_lua >= SCREEN_WIDTH:
                self.x_sol = - 100
                self.x_sol = 200
            if self.x_lua > SCREEN_WIDTH / 2:
                self.y_lua += 0.40

        if self.score > 200:
            self.screen.blit(METEOR, (self.x_meteor, self.y_meteor))
            self.screen.blit(METEOR,  (self.x_meteor2, self.y_meteor2))
            if self.y_meteor >= 340:
                self.screen.blit(METEOR ,(self.x_meteor, self.y_meteor))
                self.y_meteor = -100
                self.x_meteor = random.randint(0, 800)
            if self.y_meteor2 >= 340:
                self.screen.blit(METEOR ,(self.x_meteor2, self.y_meteor2))
                self.y_meteor2 = -100
                self.x_meteor2 = random.randint(0, 800)
            self.y_meteor2 += 2
            self.x_meteor2 += 1
            self.y_meteor += 2
            self.x_meteor += 1

        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG,(image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
    
        cloud_width = CLOUD.get_width()
        self.screen.blit(CLOUD, (self.x_nuvem, self.y_nuvem))
        if self.x_nuvem <= -cloud_width:
            self.screen.blit(CLOUD, (self.x_nuvem, self.y_nuvem))
            self.x_nuvem = SCREEN_WIDTH
        self.x_nuvem -= 2        

    def draw_score(self):
        draw_message_component(
            f"Score: {int(self.score)}",
            self.screen,
            pos_x_center=1000,
            pos_y_center=50,
        )
        if self.x_sol >= SCREEN_WIDTH:
            draw_message_component(
                f"score: {int(self.score)}",
                self.screen,
                font_color = (255, 255, 255),
                pos_x_center=1000,
                pos_y_center=50
            )        

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round(self.player.power_up_time / 1000 - pygame.time.get_ticks() / 1000, 2)
            if time_to_show >= 0 and self.x_sol < SCREEN_WIDTH:
                draw_message_component(
                    f"{self.player.type.capitalize()} enable for {time_to_show} seconds",
                    self.screen,
                    font_size = 18, 
                    pos_x_center = 500,
                    pos_y_center = 40
                )
            elif time_to_show >= 0 and self.x_sol >=  SCREEN_WIDTH:
                draw_message_component(
                    f"{self.player.type.capitalize()} enable for {time_to_show} seconds",
                    self.screen,
                    font_color = (255, 255, 255),
                    font_size = 18, 
                    pos_x_center = 500,
                    pos_y_center = 40
                )
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        self.x_sol = -84
        self.y_sol = 200
        self.x_lua = -90
        self.y_lua = 200
        self.x_nuvem = SCREEN_WIDTH
        self.y_meteor = 0 - random.randint(100, 1000)

        if self.death_count == 0:
            draw_message_component("press any key to start", self.screen) 
        else:          
            gameover = pygame.image.load(os.path.join(IMG_DIR, 'Other/GameOver.png'))
            self.screen.blit(gameover, (half_screen_width - 180, half_screen_height - 230))  
            draw_message_component("pres any key to restart", self.screen, pos_y_center=half_screen_height + 140)
            draw_message_component(
                f"Your score: {int(self.score)}",
                self.screen,
                pos_y_center=half_screen_height - 150,
            )
            draw_message_component(
                f"Death count: {self.death_count}",
                self.screen, 
                pos_y_center=half_screen_height - 100
            )
            self.screen.blit(ICON, (half_screen_width - 40, half_screen_height - 30))
            

        pygame.display.flip()

        self.handle_events_on_menu()