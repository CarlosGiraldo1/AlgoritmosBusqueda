from simpleai.search import SearchProblem, breadth_first
import pygame

# map = [[' ',' ',' ',' ','T',' '],
#         [' ','#','#','#','#',' '],
#         [' ',' ',' ','P','#',' '],
#         [' ','#','#',' ',' ',' '],
#         [' ',' ',' ',' ',' ',' ']]


class Amplitud(SearchProblem):

    def __init__(self, map, draw, grid, code_barrier, code_start, code_end, costs):

        self.initial_state = None
        self.draw= draw
        self.grid = grid
        self.code_barrier = code_barrier
        self.code_start = code_start
        self.code_end = code_end
        self.costs = costs

        for i, row in enumerate(map):
            for j, coor in enumerate(row):
                if coor == self.code_start :
                    self.initial_state = (i,j)
                    break

        SearchProblem.__init__(self,self.initial_state)

        self.goal = None
        for i, row in enumerate(map):
            for j, coor in enumerate(row):
                if coor == self.code_end:
                    self.goal = (i,j)
                    break

        self.map = map
        self.y = len(map)
        self.x = len(map[0]) 
        self.open_set = {self.initial_state, self.goal}

    #es_valido = lambda self, coordenada, state: (0<=coordenada[0]<self.y) & (0<=coordenada[1]<self.x) & (state[coordenada[0]][coordenada[1]]!='#')
    def es_valido(self, coordenada) : 
        if ((0<=coordenada[0]<self.y) & (0<=coordenada[1]<self.x)): 
            if (self.map[coordenada[0]][coordenada[1]]!=self.code_barrier):
                return True
            else:
                return False
        return False


    def actions(self, state):
        if ((state != self.goal) & (not self.goal is None) & (not state is None)):
            #resp = [(state[0]+1,state[1]), (state[0]-1,state[1]), (state[0],state[1]+1), (state[0],state[1]-1)] # 5a
            resp = [(state[0]+1,state[1]), (state[0],state[1]-1), (state[0],state[1]+1), (state[0]-1,state[1])] # 5b
            resp_filtered = [i for i in resp if self.es_valido(i)]
            
            for s in resp_filtered:
                if s not in self.open_set:
                    self.open_set.add(s)
                    self.grid[s[0]][s[1]].make_open()
            self.draw()
            return resp_filtered

        else:
            return []

    def result(self, state, action):
        return action

    def is_goal(self, state):
        if ((state != self.goal) & (state != self.initial_state)) :
            self.grid[state[0]][state[1]].make_closed()
            self.draw()
        return state == self.goal

    def cost(self, state, action, state2):
        if (state2[0]>state[0]):
            return self.costs['down']
        if (state2[0]<state[0]):
            return self.costs['up']
        if (state2[1]>state[1]):
            return self.costs['right']
        if (state2[1]<state[1]):
            return self.costs['left']

        return 1


# problem = Amplitud(map)
# result = breadth_first(problem)

# print(problem.initial_state)
# print(result.state)
# print(result.path())
# print(len(result.path())-1)