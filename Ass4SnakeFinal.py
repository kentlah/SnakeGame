import pygame
import sys
import random
from pygame.locals import *

# Initialise pygame
pygame.init()

# set height and width of game window
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# define the colours used in the game
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# create a clock to control frame rate for the game
clock = pygame.time.Clock()

# defining the snake
class Snake:
    def __init__(self):
        #initialise the snake, run reset so we have a fresh canvas to work with
        self.reset()

    def reset(self):
        # resests the snake properties to default
        self.position = [random.randrange(1, (SCREEN_WIDTH // 10)) * 10, random.randrange(1, (SCREEN_HEIGHT // 10)) * 10]
        self.body = [self.position[:]]
        self.direction = "RIGHT"
        self.change_to = self.direction
        self.speed = 10
        self.length = 1

    def change_dir_to(self, dir):
        #change the snakes direction if it's not opposite to current direction (so it can't go back on itself)
        opposite_directions = {"RIGHT": "LEFT", "LEFT": "RIGHT", "UP": "DOWN", "DOWN": "UP"}
        if dir != opposite_directions.get(self.direction):
            self.direction = dir

    def move(self, food_pos):
        # Move the snake by one "block" in it's current direction
        if self.direction == "RIGHT":
            self.position[0] += 10
        elif self.direction == "LEFT":
            self.position[0] -= 10
        elif self.direction == "UP":
            self.position[1] -= 10
        elif self.direction == "DOWN":
            self.position[1] += 10

        #insert new position at the begining of the body list
        self.body.insert(0, list(self.position))
        if self.position == food_pos:
            return True
        else:
            #remove the last part of the snakes body
            self.body.pop()
            return False

    def check_collision(self, game):
        # check if snake has collided with anything (wall or itself)
        if not game.options['borders']:
             # Allow snake to wrap around the screen if borders are off
            self.position[0] %= SCREEN_WIDTH
            self.position[1] %= SCREEN_HEIGHT
        elif self.position[0] >= SCREEN_WIDTH or self.position[0] < 0 or self.position[1] >= SCREEN_HEIGHT or self.position[1] < 0:
            return True
        for block in self.body[1:]:
            if self.position == block:
                return True
        return False

    def get_head_pos(self):
        # Return the current position of the snake's head
        return self.position

    def get_body(self):
        # Return the list representing the snake's body
        return self.body

    def increase_speed(self):
        # Increase the snake's speed and length after eating
        self.speed += 1 if self.speed < 30 else 0
        self.length += 1

#Define the worm class (snake food)
class Worm:
    def __init__(self):
        # Initialise the worm's properties
        self.spawn_worm()

    def spawn_worm(self):
        # Randomly place the worm on the screen
        self.position = [random.randrange(1, (SCREEN_WIDTH // 10)) * 10, random.randrange(1, (SCREEN_HEIGHT // 10)) * 10]
        self.spawn_time = pygame.time.get_ticks()

#This is the game class - controls game logic and state
class Game:
    def __init__(self):
        # Initialise game settings and state
        self.font = pygame.font.SysFont('arial', 25)
        self.debug_font = pygame.font.SysFont('Consolas', 20)
        self.reset_game()
        self.paused = False

        # Game options that can be toggled in the menu
        self.options = {
            "borders": True,
            "score": True,
            "worm_timer": False,
            "increase_speed": False
        }

        # Debug mode for in game debugging - F5 to enable in game
        self.debug_mode = False

    def reset_game(self):
        # reset everything for a new game
        self.snake = Snake()
        self.worm = Worm()
        self.score = 0

    def toggle_debug(self):
        #toggles debug mode
        self.debug_mode = not self.debug_mode

    def draw_game_over(self):
        #game over screen - gives options to quit, continue, etc
        screen.fill(BLACK)
        game_over_text = self.font.render("Game Over", True, WHITE)
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        continue_text = self.font.render("Click to continue, or press escape to quit.", True, WHITE)

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT // 1.5))
        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    waiting_for_input = False
                    self.main_menu()
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                    
    def display_pause_message(self):
        #displays the pause screen
        pause_text = self.font.render("Game Paused. Press P to continue...", True, WHITE)
        screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.update()                
                    
                    
    def run(self):
        #main game loop
        self.reset_game()  # Reset the game state each time `run` is called
        running = True
        worm_timer = 10000  # 10 seconds

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key in (K_UP, K_w):
                        self.snake.change_dir_to("UP")
                    elif event.key in (K_DOWN, K_s):
                        self.snake.change_dir_to("DOWN")
                    elif event.key in (K_LEFT, K_a):
                        self.snake.change_dir_to("LEFT")
                    elif event.key in (K_RIGHT, K_d):
                        self.snake.change_dir_to("RIGHT")
                    elif event.key == K_F5:
                        self.toggle_debug()
                    elif event.key == K_ESCAPE:
                        self.main_menu()
                        #pygame.quit() ## Rather than quit and exit, ESC in game returns to main menu
                        #sys.exit()
                    elif event.key == K_p:
                        self.paused = not self.paused #added 01/04
                        
            if not self.paused:
                 ####  moving game logic within pause
                if self.snake.move(self.worm.position):
                    self.score += 10
                    self.worm.spawn_worm()
                    if self.options['increase_speed']:
                        self.snake.increase_speed()

                worm_timer_expired = pygame.time.get_ticks() - self.worm.spawn_time > worm_timer
                if self.options['worm_timer'] and worm_timer_expired:
                    self.worm.spawn_worm()
                    if len(self.snake.body) > 3:
                        self.snake.body.pop()
                    else:
                        running = False

                if self.snake.check_collision(self):
                    running = False
                ######
            else:
                self.display_pause_message()
                continue #removing this causes pause message not to display
                
                
            screen.fill(BLACK)
            for pos in self.snake.body:
                pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
            pygame.draw.rect(screen, RED, pygame.Rect(self.worm.position[0], self.worm.position[1], 10, 10))

            if self.options["score"]:
                score_text = self.font.render(f'Score: {self.score}', True, WHITE)
                screen.blit(score_text, (5, 5))

            if self.debug_mode:
                debug_info = [
                    f"Worm Pos: {self.worm.position}",
                    f"Head Pos: {self.snake.get_head_pos()}",
                    f"Speed: {self.snake.speed}",
                    f"Worm Timer: {(worm_timer - (pygame.time.get_ticks() - self.worm.spawn_time)) // 1000}s",
                    f"Length: {len(self.snake.body)}"
                ]
                for i, info in enumerate(debug_info):
                    text_surf = self.debug_font.render(info, True, WHITE)
                    screen.blit(text_surf, (5, 30 + i * 20))

            pygame.display.flip()
            clock.tick(self.snake.speed)

        self.draw_game_over()

    def draw_menu(self, selected_option, option_names):
        """Draw the menu screen."""
        screen.fill(BLACK)
        menu_title = self.font.render('Snake Game Menu', True, WHITE)
        screen.blit(menu_title, (SCREEN_WIDTH // 2 - menu_title.get_width() // 2, 20))
        
        for i, option in enumerate(option_names + ["Start Game"]):  # Add "Start Game" option
            option_state = 'On' if self.options.get(option, '') else 'Off'
            text = f'{option.capitalize()}: {option_state}' if option in self.options else option
            color = GREEN if i == selected_option else WHITE
            menu_option = self.font.render(text, True, color)
            screen.blit(menu_option, (SCREEN_WIDTH // 2 - menu_option.get_width() // 2, 100 + i * 30))
        
        pygame.display.update()

    def main_menu(self):
        """Show the main menu."""
        selected_option = 0
        option_names = list(self.options.keys())
        
        while True:
            self.draw_menu(selected_option, option_names)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    #if event.key == pygame.K_UP:
                    if event.key in (K_UP, K_w):
                        selected_option = (selected_option - 1) % (len(self.options) + 1)
                    elif event.key in (K_DOWN, K_s):
                        selected_option = (selected_option + 1) % (len(self.options) + 1)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == len(option_names):  # If "Start Game" is selected
                            self.run()
                        else:  # Toggle the selected option
                            option = option_names[selected_option]
                            self.options[option] = not self.options[option]
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            clock.tick(15)

if __name__ == "__main__":
    game = Game()
    game.main_menu()

