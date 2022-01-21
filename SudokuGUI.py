import pygame
pygame.font.init()
from solver import solve, is_valid, find_empty, generator
import time
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (128,128,128)
DARK_PURPLE = (195, 127, 219)
LIGHT_PURPLE = (224, 180, 240)
# TODO make the size of the grid optional 6x6 , 9x9, 12x12

class Grid:

    board=generator()

    def __init__(self, rows, cols, width, height, win):
            self.rows = rows
            self.cols = cols
            self.width = width
            self.height = height
            self.squares = [[Square(self.board[i][j], i , j , self.width , self.height) for i in range(self.rows)] for j in range(self.cols)]
            self.selected_pos= None
            self.ngrid=None
            self.wrong=0
            self.win = win
            for i in range(rows):
                for j in range(cols):
                    if self.squares[i][j]!=0:
                        self.squares[i][j].fixed=True


    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / self.cols
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 3
            else:
                thick = 1
            pygame.draw.line(win, BLACK, (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, BLACK, (i * gap, 0), (i * gap, self.height), thick) 

        # Draw Squares
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].draw_square(win)
        
        
    
    def sketch_temp(self, val):
        row, col = self.selected_pos
        self.squares[row][col].set_temp(val)
            
    def update_grid(self):
        self.ngrid = [[self.squares[j][i].value for i in range(self.rows)] for j in range(self.cols)]
        return(self.ngrid)

    def place_val(self, val, pos):
        row, col = pos
        if self.squares[row][col].value == 0 :
            if not(is_valid(self.board, val, (row, col))):
                self.wrong=+1
            self.squares[row][col].set_val(val)
            self.squares[row][col].set_temp(0)
            self.update_grid()
            

    def click(self, pos):
        if pos[0]<self.width and pos[1]<self.height:
            gap = self.width / self.cols
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        

    def move(self, pos, dir):
        row, col = pos
        
        if dir=="r" and col+1 < self.cols:
            self.select((row, col+1))
        if dir=="l" and col-1 > -1:
            self.select((row, col-1))                
        if dir=="u" and row-1 > -1:
            self.select((row-1, col))
        if dir=="d" and row+1 < self.rows:
            self.select((row+1, col))


    def select(self, pos):
        row, col = pos
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].selected=False

        self.squares[row][col].selected=True
        self.selected_pos = (row , col)

    def clear(self):
        row, col = self.selected_pos
        self.squares[row][col].temp=0

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.squares[i][j].value == 0:
                    return False
        return True

    def solve_gui(self):
        self.update_grid()
        pos = find_empty(self.ngrid)
        if pos==(-1,-1):
            return True
        else:
            row, col = pos

        for i in range(1, 10):
            if is_valid(self.ngrid, i, (row, col)):
                self.ngrid[row][col] = i
                self.squares[row][col].set_val(i)
                self.squares[row][col].draw_change(self.win, True)
                self.update_grid()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

        
                self.ngrid[row][col] = 0
                self.squares[row][col].set_val(0)
                self.update_grid()
                self.squares[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)
                
        return False

class Square:
    rows=9
    cols=9
    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.temp = 0
        self.selected = False
        self.fixed = False

    def draw_square(self, win):
        # Draws numbers in the square 
        fnt1 = pygame.font.SysFont("comicsans", 40)
        fnt2 = pygame.font.SysFont("comicsans", 20)

        gap = self.width / 9
        x = self.row * gap
        y = self.col * gap

        if self.temp != 0 and self.value == 0:
            text = fnt2.render(str(self.temp), 1, GREY)
            win.blit(text, (x+5, y+5))

        elif self.value != 0:
            text = fnt1.render(str(self.value), 1, BLACK)
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, RED, (x,y, gap ,gap), 3)
        
    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.row * gap
        y = self.col * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)


    
    def set_val(self, val):
        self.value=val
    
    def set_temp(self, temp):
        self.temp=temp

def redraw_window( win, grid, time, result, pos):
        # Draw time
        win.fill(WHITE)
        time_fnt = pygame.font.SysFont("comicsans", 30)
        time_text = time_fnt.render("Time: " + format_time(time), 1,BLACK)
        win.blit(time_text, (540 - 170, 550))
        # draw button
        button_fnt = pygame.font.SysFont("comicsans", 20)
        if 200 <= pos[0] <= 200+140 and 550 <= pos[1] <= 550+40:
            pygame.draw.rect(win,LIGHT_PURPLE,[200,550,100,40])
        else:
            pygame.draw.rect(win,DARK_PURPLE,[200,550,100,40])
        button_text=button_fnt.render("FINISH", 1 , BLACK)
        win.blit(button_text, (210,555))
        
        # draw board
        grid.draw(win)

        # draw result
        if(result!=None):
            win.blit(result, (10, 550))


def format_time(secs):
    sec = secs%60
    minute = secs//60
    

    mat = " " + str(minute) + ":" + str(sec)
    return mat

def select_button(pos):
    if 200 <= pos[0] <= 200+100 and 550 <= pos[1] <= 550+40:
        return True
    else:
        
        return False
      

def main():
    
    win = pygame.display.set_mode((540,600))
    icon = pygame.image.load('icon.png')
    pygame.display.set_caption("Sudoku")
    pygame.display.set_icon(icon)
    run = True
    key = None
    grid = Grid(9 ,9 , 540, 540, win)
    start = time.time()
    result=None
    while run:
        pos = pygame.mouse.get_pos()
        play_time=round(time.time()-start)
        win.fill(WHITE)
        grid.draw(win)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE or event.key == pygame.K_KP_PERIOD:
                    grid.clear()
                    key=None
                if event.key == pygame.K_RIGHT:
                    grid.move(grid.selected_pos, "r")
                if event.key == pygame.K_LEFT:
                    grid.move(grid.selected_pos, "l")
                if event.key == pygame.K_UP:
                    grid.move(grid.selected_pos, "u")
                if event.key == pygame.K_DOWN:
                    grid.move(grid.selected_pos, "d")
                                            
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    i, j = grid.selected_pos
                    key=grid.squares[i][j].temp
                    if key != 0:
                        grid.place_val( key,(i,j))

                if event.key == pygame.K_SPACE:
                    grid.solve_gui()
                    button_fnt = pygame.font.SysFont("comicsans", 15)
                    button_text=button_fnt.render("PLAY AGAIN", 1 , BLACK)
                    win.blit(button_text, (210,555))
                    if(select_button(pos)):
                        run = False




            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if(select_button(pos)):
                    result_fnt = pygame.font.SysFont("comicsans", 20)
                    if grid.is_finished():
                        for i in range(grid.rows):
                            for j in range(grid.cols):
                                grid.place_val( grid.squares[i][j].temp,(i, j))
                        if grid.wrong>0:
                            result = result_fnt.render("TRY AGAIN", 1 , RED)
                        else:
                            result = result_fnt.render("WELL DONE!", 1 , GREEN)
                        win.blit(result, (10, 550))
                    else:
                        result = result_fnt.render("some tiles is empty!", 1 , BLACK)

                if grid.click(pos):
                    row, col = grid.click(pos)
                    grid.select((row,col))
                
                

        if grid.selected_pos and key != None:
            grid.sketch_temp( key )
            key=None
            

        redraw_window(win, grid, play_time, result, pos)
    
        pygame.display.update()

main()

