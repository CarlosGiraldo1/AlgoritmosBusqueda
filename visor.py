import pygame
import time
from simpleai.search import  astar, depth_first, breadth_first
from algoritmos.a_star_Manhattan import A_Manhattan 
from algoritmos.amplitud import Amplitud 
from algoritmos.profundidad import Profundidad 
from algoritmos.a_star_Euclidea import A_Euclidea
from simpleai.search.viewers import BaseViewer

# map = [[' ',' ',' ',' ','T',' '],
#         [' ','#','#','#','#',' '],
#         [' ',' ',' ','P','#',' '],
#         [' ','#','#',' ',' ',' '],
#         [' ',' ',' ',' ',' ',' ']]

map = [[' ',' ',' ',' ',' ',' ',' ',' ','T',' ',' ',' ','#',' ',' ',' ','#',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#',' ',' ',' ','#',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ','#','#','#','#','#',' ',' ',' ','#','P','#',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#',' ',' ',' ',' ',' ','#',' ','#',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#',' ',' ',' ','#','#','#','#','#',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ','#',' ',' ',' ',' ','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ','#',' ',' ',' ',' ','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ','#',' ',' ',' ',' ','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ','#',' ',' ',' ',' ','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ','#',' ',' ',' ',' ','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ','#','#','#','#','#','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']]

COSTS = {
    "up": 5.0,
    "down": 1.0,
    "left": 1.0,
    "right": 1.0,
}

BARRIER = '#'
START = 'T'
END = 'P'
GAP = 30

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (64, 224, 250)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)



class Spot:
    def __init__(self, row, col, gap, total_rows, total_columns):
        self.row = row
        self.col = col
        self.x = row * gap
        self.y = col * gap
        self.color = WHITE
        self.neighbors = []
        self.gap = gap
        self.total_rows = total_rows
        self.total_columns = total_columns

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == BLUE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = BLUE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.y, self.x, self.gap, self.gap))



def make_grid(rows, columns, gap):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(columns):
            spot = Spot(i, j, gap, rows, columns)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, columns, gap):

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (columns*gap, i * gap))
        for j in range(columns):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, rows*gap))


def draw(win, grid, rows, columns, gap):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, columns, gap)
    pygame.display.update()



def searchInfo (problem,result,use_viewer):
    def getTotalCost (problem,result):
        originState = problem.initial_state
        totalCost = 0
        for action,endingState in result.path():
            if action is not None:
                totalCost += problem.cost(originState,action,endingState)
                originState = endingState
        return totalCost

    
    res = "Total length of solution: {0}\n".format(len(result.path()))
    res += "Total cost of solution: {0}\n".format(getTotalCost(problem,result))
        
    if use_viewer:
        stats = [{'name': stat.replace('_', ' '), 'value': value}
                         for stat, value in list(use_viewer.stats.items())]
        
        for s in stats:
            res+= '{0}: {1}\n'.format(s['name'],s['value'])
    return res

def initialize_map(rows, columns, map, grid):
    for i in range(rows):
        for j in range(columns):
            if (map[i][j]==BARRIER):
                grid[i][j].make_barrier()

            if (map[i][j]==START):
                start = grid[i][j]
                start.make_start()

            if (map[i][j]==END):
                end = grid[i][j]
                end.make_end()

    return [start, end]


def main(gap, map, costs):
    rows = len(map)
    columns = len(map[0])

    heigth = gap * rows
    width = gap * columns

    pygame.display.set_caption("Path Finding Algorithm")
    win = pygame.display.set_mode((width, heigth))

    grid = make_grid(rows, columns, gap)
    start, end = initialize_map(rows, columns, map, grid)

    run = True
    while run:

        draw(win, grid, rows, columns, gap)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and start and end:
                    run = False

                if event.key == pygame.K_1 and start and end:
                    grid = make_grid(rows, columns, gap)
                    start, end = initialize_map(rows, columns, map, grid)
                    draw(win, grid, rows, columns, gap)

                    problem = A_Manhattan(map, lambda: draw(win, grid, rows, columns, gap), grid, BARRIER, START, END, costs)
                    used_viewer=BaseViewer() 

                    time1 = time.time()
                    result = astar(problem, graph_search=True, viewer=used_viewer)
                    time2 = time.time()

                    info=searchInfo(problem,result,used_viewer)
                    print('A* Manhattan')
                    print([i[1] for i in result.path()])
                    print('Time: ' + str(time2-time1))
                    print(info)
                    
                    for p in result.path():
                        if ((grid[p[1][0]][p[1][1]]!=start) & (grid[p[1][0]][p[1][1]]!=end)) :
                            grid[p[1][0]][p[1][1]].make_path()

                if event.key == pygame.K_2 and start and end:
                    grid = make_grid(rows, columns, gap)
                    start, end = initialize_map(rows, columns, map, grid)
                    draw(win, grid, rows, columns, gap)

                    problem = A_Euclidea(map, lambda: draw(win, grid, rows, columns, gap), grid, BARRIER, START, END, costs)
                    used_viewer=BaseViewer() 

                    time1 = time.time()
                    result = astar(problem, graph_search=True, viewer=used_viewer)
                    time2 = time.time()
                    
                    info=searchInfo(problem,result,used_viewer)
                    print('A* Euclidea')
                    print([i[1] for i in result.path()])
                    print('Time: ' + str(time2-time1))
                    print(info)

                    for p in result.path():
                        if ((grid[p[1][0]][p[1][1]]!=start) & (grid[p[1][0]][p[1][1]]!=end)) :
                            grid[p[1][0]][p[1][1]].make_path()

                if event.key == pygame.K_3 and start and end:
                    grid = make_grid(rows, columns, gap)
                    start, end = initialize_map(rows, columns, map, grid)
                    draw(win, grid, rows, columns, gap)

                    problem = Amplitud(map, lambda: draw(win, grid, rows, columns, gap), grid, BARRIER, START, END, costs)
                    used_viewer=BaseViewer() 

                    time1 = time.time()
                    result = breadth_first(problem, graph_search=True, viewer=used_viewer)
                    time2 = time.time()

                    info=searchInfo(problem,result,used_viewer)
                    print('Amplitud')
                    print([i[1] for i in result.path()])
                    print('Time: ' + str(time2-time1))
                    print(info)

                    for p in result.path():
                        if ((grid[p[1][0]][p[1][1]]!=start) & (grid[p[1][0]][p[1][1]]!=end)) :
                            grid[p[1][0]][p[1][1]].make_path()

                if event.key == pygame.K_4 and start and end:
                    grid = make_grid(rows, columns, gap)
                    start, end = initialize_map(rows, columns, map, grid)
                    draw(win, grid, rows, columns, gap)

                    problem = Profundidad(map, lambda: draw(win, grid, rows, columns, gap), grid, BARRIER, START, END, costs)
                    used_viewer=BaseViewer() 

                    time1 = time.time()
                    result = depth_first(problem, graph_search=True, viewer=used_viewer)
                    time2 = time.time()
                    
                    info=searchInfo(problem,result,used_viewer)
                    print('Profundidad')
                    print([i[1] for i in result.path()])
                    print('Time: ' + str(time2-time1))
                    print(info)

                    for p in result.path():
                        if ((grid[p[1][0]][p[1][1]]!=start) & (grid[p[1][0]][p[1][1]]!=end)) :
                            grid[p[1][0]][p[1][1]].make_path()

                if event.key == pygame.K_c:
                    grid = make_grid(rows, columns, gap)
                    start, end = initialize_map(rows, columns, map, grid)
                    draw(win, grid, rows, columns, gap)

    pygame.quit()


main(GAP, map, COSTS)