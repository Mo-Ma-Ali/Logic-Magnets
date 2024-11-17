import pygame
import sys
from levels_data import levels 
from Search import Search
from copy import deepcopy
pygame.init()

# Constants
MENU_BACKGROUND = (60, 60, 60) 
WIDTH, HEIGHT = 800, 600  
GRID_COLUMNS = 5  
BUTTON_WIDTH, BUTTON_HEIGHT = 120, 60 
BUTTON_SPACING = 20  
BUTTON_COLOR = (0, 128, 128) 
WHITE = (255, 255, 255)
grid_color = (50, 44, 43)
highlight_color = (255, 255, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level Selection Menu")


in_menu = True
selected_level = None
counte = 0  

# Fonts
font = pygame.font.Font(None, 36)

def draw_menu(levels):

    screen.fill(MENU_BACKGROUND)
    title_font = pygame.font.Font(None, 48)
    title = title_font.render("Select a Level", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title, title_rect)

    button_font = pygame.font.Font(None, 36)
    start_x = (WIDTH - (GRID_COLUMNS * (BUTTON_WIDTH + BUTTON_SPACING) - BUTTON_SPACING)) // 2
    start_y = 200

    buttons = []
    for i, level in enumerate(levels):
        row, col = divmod(i, GRID_COLUMNS)
        x = start_x + col * (BUTTON_WIDTH + BUTTON_SPACING)
        y = start_y + row * (BUTTON_HEIGHT + BUTTON_SPACING)

        button_rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
        level_text = button_font.render(f"Level {i + 1}", True, (0, 0, 0))
        text_rect = level_text.get_rect(center=button_rect.center)
        screen.blit(level_text, text_rect)
        
        buttons.append((button_rect, i))
    pygame.display.flip()
    return buttons

class Grid:
    def __init__(self, cell_size, rows, cols):
        self.cell_size = cell_size
        self.rows = rows
        self.cols = cols

    def to_pixel(self, row, col):
        x = col * self.cell_size + self.cell_size / 2 + 50
        y = row * self.cell_size + self.cell_size / 2 + 50
        return pygame.Vector2(x, y)

    def draw_game(self):
        for row in range(self.rows):
            for col in range(self.cols):
                center = self.to_pixel(row, col)
                pygame.draw.circle(screen, grid_color, (int(center.x), int(center.y)), self.cell_size // 3, 0)

class Game:
    def __init__(self, level_data, grid,rows , cols):
        self.level_data = level_data
        self.grid = grid
        self.rows = rows
        self.cols = cols

    def load(self):
        global counte
        # counte = 0
        for hole_data in self.level_data[2]:
            hole_type, (row, col) = hole_data
            color = (20, 21, 15)
            center = self.grid.to_pixel(row, col)
            pygame.draw.circle(screen, color, (int(center.x), int(center.y)), self.grid.cell_size // 3,0)
        for ball_type, (row, col) in self.level_data[1]:
            color = (128, 61, 59) if ball_type == "Attract" else (30, 62, 98) if ball_type == "Hate" else (105, 117, 101)
            center = self.grid.to_pixel(row, col)
            pygame.draw.circle(screen, color, (int(center.x), int(center.y)), self.grid.cell_size // 4)
        # print ('sasa')
        
    def movement(self, new_row, new_col, ball_index):
        if self.level_data[3] >= counte:
            ball_type, _ = self.level_data[1][ball_index]
            if ball_type in ["Attract", "Hate"] and not self.position_occupied(new_row, new_col):
                self.level_data[1][ball_index] = (ball_type, (new_row, new_col))
                # self.load()
                self.do(new_row, new_col, ball_type)

    def do(self, new_row, new_col, moved_ball_type):
        in_line = []
        for i, (ball_type, (row, col)) in enumerate(self.level_data[1]):
            if (row == new_row or col == new_col) and (row != new_row or col != new_col):
                distance = abs(row - new_row) + abs(col - new_col)
                in_line.append((distance, i, ball_type, row, col))
        
        if moved_ball_type == "Attract":
            in_line.sort()
        elif moved_ball_type == "Hate":
            in_line.sort(reverse=True)

        for _, i, ball_type, row, col in in_line:
            if row == new_row:
                if moved_ball_type == "Attract":
                    if col < new_col and col + 1 < self.cols and not self.position_occupied(row, col + 1):
                        self.level_data[1][i] = (ball_type, (row, col + 1))
                    elif col > new_col and col - 1 >= 0 and not self.position_occupied(row, col - 1):
                        self.level_data[1][i] = (ball_type, (row, col - 1))
                elif moved_ball_type == "Hate":
                    if col < new_col and col - 1 >= 0 and not self.position_occupied(row, col - 1):
                        self.level_data[1][i] = (ball_type, (row, col - 1))
                    elif col > new_col and col + 1 < self.cols and not self.position_occupied(row, col + 1):
                        self.level_data[1][i] = (ball_type, (row, col + 1))

            elif col == new_col:
                if moved_ball_type == "Attract":
                    if row < new_row and row + 1 < self.rows and not self.position_occupied(row + 1, col):
                        self.level_data[1][i] = (ball_type, (row + 1, col))
                    elif row > new_row and row - 1 >= 0 and not self.position_occupied(row - 1, col):
                        self.level_data[1][i] = (ball_type, (row - 1, col))
                elif moved_ball_type == "Hate":
                    if row < new_row and row - 1 >= 0 and not self.position_occupied(row - 1, col):
                        self.level_data[1][i] = (ball_type, (row - 1, col))
                    elif row > new_row and row + 1 < self.rows and not self.position_occupied(row + 1, col):
                        self.level_data[1][i] = (ball_type, (row + 1, col))
    def position_occupied(self, row, col):
        return any(pos == (row, col) for _, pos in self.level_data[1])
    
    def win(self):
        if self.level_data[3] >= counte:
            matched_holes = set()
            
            for _, ball_pos in self.level_data[1]:
                for _, hole_pos in self.level_data[2]:
                    if ball_pos == hole_pos and hole_pos not in matched_holes:
                        matched_holes.add(hole_pos)
                        break 

            if len(matched_holes) == len(self.level_data[2]):
                winner = pygame.font.Font(None, 75)
                screen.blit(winner.render("You Win!", True, (0, 255, 0)), (self.rows + 50, self.cols + 50))
                return True
            elif self.level_data[3] - counte == 0:
                loser = pygame.font.Font(None, 75)
                screen.blit(loser.render("You Lost", True, (255, 0, 0)), (self.rows + 50, self.cols + 50))
        else:
            loser = pygame.font.Font(None, 75)
            screen.blit(loser.render("You Lost", True, (255, 0, 0)), (self.rows + 50, self.cols + 50))
 
def main():
    global in_menu, selected_level, counte,highlight_color
    running = True
    clock = pygame.time.Clock()
    level_buttons = draw_menu(levels)
    is_selected = False 
    is_moved = False
    row, col ,curCol,curRow = 0, 0 ,0 ,0
    ball_found = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif in_menu and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button_rect, level_index in level_buttons:
                    if button_rect.collidepoint(mouse_pos):
                        selected_level = level_index
                        in_menu = False
                        level_data = deepcopy(levels[selected_level])
                        width ,hight= WIDTH ,HEIGHT
                        rows, cols = level_data[4], level_data[5]
                        cell_size = min(width // cols, hight // rows)
                        screen = pygame.display.set_mode((cols * cell_size + 100, rows * cell_size + 100))
                        grid = Grid(cell_size, rows, cols)
                        game = Game(level_data, grid,rows , cols)
                        search = Search(grid, level_data,game)
                        break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    row = max(row - 1, 0)
                elif event.key == pygame.K_DOWN:
                    row = min(row + 1, rows - 1)
                elif event.key == pygame.K_LEFT:
                    col = max(col - 1, 0)
                elif event.key == pygame.K_RIGHT:
                    col = min(col + 1, cols - 1)
                elif event.key == pygame.K_SPACE:
                    is_selected = True
                elif event.key == pygame.K_e:
                    is_moved = True
                if event.key == pygame.K_b:
                    solution = search.BFS()
                if event.key == pygame.K_d:
                    solution = search.DFS()
                if event.key == pygame.K_u:
                    solution = search.UCS()
                if event.key == pygame.K_q:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    pygame.display.set_caption("Level Selection Menu")
                    game.load()
                    in_menu = True
                    counte = 0


        if in_menu:
            draw_menu(levels)
        else:
            screen.fill((175, 130, 96))
            grid.draw_game()
            if is_selected:
                curRow, curCol = row, col
                is_selected = False
            for i, (ball_type, (b_row, b_col)) in enumerate(game.level_data[1]):
                # print(is_selected , is_moved)
                if (curRow, curCol) == (row , col) and is_moved is True:
                    is_selected = False
                    is_moved = False
                if (curRow, curCol) == (b_row, b_col):
                    selected_ball_index = i
                    if ball_type != "Immobile" and is_moved and not game.position_occupied(row,col):
                        if counte < game.level_data[3]:
                            counte+=1
                            game.movement(row, col, selected_ball_index)
                            is_moved = False
                            is_selected = False
                    if ball_type != "Immobile":
                        ball_found = True

            highlight_color = grid_color if ball_found else highlight_color
            pygame.draw.rect(screen, highlight_color, pygame.Rect(col * cell_size + 50, row * cell_size + 50, cell_size, cell_size), 2)
            game.load()
            game.win()
            moves_text = font.render(f"Moves: {game.level_data[3] - counte}", True, (0, 0, 0))
            screen.blit(moves_text, (10, 10))
            pygame.display.flip()
        clock.tick(60)

main()
