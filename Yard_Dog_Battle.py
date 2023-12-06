import pygame
import random
import math
from utils import make_background, Player



pygame.mixer.init()
background_music = pygame.mixer.Sound("assets/Intergalactic-Odyssey.wav")
background_music.set_volume(0.4)
background_music.play(-1)


class Game:
    def __init__(self):
        pygame.init()

        pygame.mixer.init()

        self.player1_position = (185, 120)
        self.player2_position = (555, 360)
        self.score_value = 0

        self.bulletimg = pygame.image.load("assets/bullets.png")
        self.bulletx = 0
        self.bullety = 0
        self.bullet_x_change = 0
        self.bullet_y_change = 5
        self.bullet_state = 'ready'

        self.shooting_sound= pygame.mixer.Sound("assets/shooting.wav")
        self.shooting_sound.set_volume(0.5)

        self.bounds_reached_count = 0
        self.player_lives = 3

        # Load background music



        self.img = pygame.image.load('assets/seamless-grass.jpg')
        self.menu_img = pygame.image.load('assets/forest2.png')

        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        self.player1 = Player("assets/squirrel.png", 185, 120)
        self.player2 = Player("assets/squirrel.png", 555, 360)

        self.enemyimg = []
        self.enemyx = []
        self.enemyy = []
        self.enemy_x_change = []
        self.enemy_y_change = []
        self.num_enemies = 6

        # Initialize mixer for sound




        for _ in range(self.num_enemies):
            self.enemyimg.append(pygame.image.load("assets/A_squirrel.png"))
            self.enemyx.append(random.randint(0,768))
            self.enemyy.append(random.randint(0,150))
            self.enemy_x_change.append(1)
            self.enemy_y_change.append(40)

        self.bullets = []


        self.score_value = 0
        self.font = pygame.font.Font('assets/black-crayon/Black Crayon.ttf', 32)
        self.scoretext_x = 10
        self.scoretext_y = 10

        self.game_state = "MENU"

        self.total_game_time = 0  # Total elapsed time in milliseconds
        self.time_limit = 60000





            # Load more game state variables as needed

            # Update the game screen with loaded positions and values
            # ... (your code to update positions and values)

    def reset_game(self):
        self.bounds_reached_count = 0
        self.player_lives = 3
    def save_scores(self, score):
        self.scores.append(score)
        save_score(score)
    def fire_bullet(self, player):
        if self.bullet_state == "ready":
            self.bulletx = player.x
            self.bullety = player.y
            self.bullet_state = 'fire'
    def handle_input(self, event):
        if self.game_state == "MENU":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_state = "PLAYING"
                elif event.key == pygame.K_q:  # Press 'Q' to quit in the main menu
                    pygame.quit()
                    sys.exit()
        elif self.game_state == "PLAYING":

            if event.type == pygame.KEYDOWN:
                # Player 1 controls
                if event.key == pygame.K_LEFT:
                    self.player1.x_change = -2

                # ... (other player 1 controls)
                if event.key == pygame.K_RIGHT:
                    self.player1.x_change = 2

                if event.key == pygame.K_UP:
                    self.player1.y_change= -2

                if event.key == pygame.K_DOWN:
                    self.player1.y_change = 2

                # Player 2 controls
                if event.key == pygame.K_a:
                    self.player2.x_change = -2


                if event.key == pygame.K_d:
                    self.player2.x_change = 2


                if event.key == pygame.K_w:
                    self.player2.y_change = -2


                if event.key == pygame.K_s:
                    self.player2.y_change = 2


                # ... (other player 2 controls)

                # Player 1 fire
                elif event.key == pygame.K_SPACE:
                    self.fire_bullet(self.player1)
                    self.shooting_sound.play()


                # Player 2 fire
                elif event.key == pygame.K_e:
                    self.fire_bullet(self.player2)

            elif event.type == pygame.KEYUP:
                # ... (your existing key release handling)
                if event.key == pygame.K_LEFT:
                    self.player1.x_change = 0
                # ... (other player 1 controls)
                if event.key == pygame.K_RIGHT:
                    self.player1.x_change = 0

                if event.key == pygame.K_UP:
                    self.player1.y_change = 0

                if event.key == pygame.K_DOWN:
                    self.player1.y_change = 0
                # Player 2 controls
                if event.key == pygame.K_a:
                    self.player2.x_change = 0

                if event.key == pygame.K_d:
                    self.player2.x_change = 0

                if event.key == pygame.K_w:
                    self.player2.y_change = 0

                if event.key == pygame.K_s:
                    self.player2.y_change = 0


    def update_game_state(self):

        dt = self.clock.tick(60)  # Get the time passed since the last frame in milliseconds
        self.total_game_time += dt


        if self.game_state == "PLAYING":
            for i in range(self.num_enemies):
                if self.enemyy[i] > 200:
                    self.enemyy[i] = 0
                    self.bounds_reached_count += 1

                    if self.bounds_reached_count >= 1:
                        self.player_lives -= 1

                    # Check if the game should end


                self.enemyx[i] += self.enemy_x_change[i]
                if self.enemyx[i] <= 0:
                    self.enemy_x_change[i] = 1
                    self.enemyy[i] += self.enemy_y_change[i]
                elif self.enemyx[i] >= 768:
                    self.enemy_x_change[i] = -1
                    self.enemyy[i] += self.enemy_y_change[i]

                if self.collision(self.enemyx[i], self.enemyy[i]):
                    self.bullety = 480
                    self.bullet_state = "ready"
                    self.score_value += 1
                    print(self.score_value)
                    self.enemyx[i] = random.randint(0,768)
                    self.enemyy[i] = random.randint(0,150)



            if self.player_lives <= 0 or self.total_game_time >= self.time_limit:
                self.game_state = 'GAME_OVER'

            if self.score_value == 10:
                self.player_lives = 3
            # Player movement
            self.player1.move()
            self.player2.move()

            # Bullet movement
            if self.bullety <= 0:
                self.bullety = 480
                self.bullet_state = 'ready'

            if self.bullet_state == 'fire':
                self.bullety -= self.bullet_y_change


    def draw_game(self):
        self.screen.fill((0, 0, 0))





        if self.game_state == "MENU":
            self.screen.blit(self.menu_img,(0,0))
            self.draw_menu()
        elif self.game_state == "PLAYING":
            self.screen.blit(self.img, (0, 0))
            self.draw_playing()
        elif self.game_state == "GAME_OVER":
            self.draw_game_over()



        pygame.display.flip()
        self.clock.tick(30)

    def draw_menu(self):
        menu_font = pygame.font.Font('assets/black-crayon/Black Crayon.ttf', 64)
        instruction_font = pygame.font.Font('assets/black-crayon/Black Crayon.ttf', 32)

        title_text = menu_font.render("Yard Dog Battle", True, (255, 255, 255))
        self.screen.blit(title_text, (200, 100))

        instruction_text = instruction_font.render("Press Enter to Start", True, (255, 255, 255))
        self.screen.blit(instruction_text, (250, 300))

        quit_text = instruction_font.render("Press Q to Quit", True, (255, 255, 255))
        self.screen.blit(quit_text, (300, 400))



    def draw_playing(self):
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)


        for i in range(self.num_enemies):
            self.enemy(self.enemyx[i], self.enemyy[i], i)

        if self.bullet_state == 'fire':
            self.screen.blit(self.bulletimg, (self.bulletx + 8, self.bullety + 5))
        # Adjust to draw from the correct player

        self.show_score()

    def draw_game_over(self):
        over_text = self.font.render('GAME OVER', True, (255, 255, 255))
        self.screen.blit(over_text, (200, 250))

    def show_score(self):
        score_text = self.font.render("Score:" + str(self.score_value), True, (225, 255, 255))
        self.screen.blit(score_text, (self.scoretext_x, self.scoretext_y))

        lives_text = self.font.render(f"Player Lives: {self.player_lives} ",
                                      True, (225, 255, 255))
        self.screen.blit(lives_text, (self.scoretext_x, self.scoretext_y + 40))

        time_text = self.font.render(f"Time:{self.total_game_time}",True, (255,255,255))
        self.screen.blit(time_text, (500, 0))
    def draw_bullet(self):
        self.screen.blit(self.bulletimg, self.bulletx, self.bullety)
    def enemy(self, x, y, i):
        self.screen.blit(self.enemyimg[i], (x, y))

    def collision(self, enemyx, enemyy):
        distance = math.sqrt((math.pow(enemyx - self.bulletx, 2)) + (math.pow(enemyy - self.bullety, 2)))
        return distance < 13

    def run(self):

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                self.handle_input(event)





            make_background(self.screen)
            self.update_game_state()
            self.draw_game()



        pygame.mixer.quit()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game_instance = Game()
    game_instance.run()