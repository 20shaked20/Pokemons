import sys
import time

import pygame
import math
from tkinter import *

from Ex4.Project.DiGraph.GraphAlgo import GraphAlgo
from Ex4.Project.DiGraph.DiGraph import DiGraph

SIZE = 800, 480
RED = (255, 0, 0)
BLACK = (0, 0, 0)
PINK = (255, 200, 200)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

"""
LEGACY CLASS, not using!!! moved to work on gui via matplotlib.
"""


# TODO:
#   1. fix arrows.

class GraphGui:

    def __init__(self, graph_algo: GraphAlgo):
        self.graph_algo = graph_algo
        self.nodesX = {}
        self.nodesY = {}
        self.login = Tk()
        self.user_name = StringVar()  # used for login
        self.password = StringVar()  # used for login
        self.login_lables()
        self.login.mainloop()

    def home_screen(self):
        users = {'John': 'id', 'Shaked': '318985165', '1': '1'}
        username = self.user_name.get()
        print(username)
        passwd = self.password.get()
        if username in users:
            if users[username] == passwd:
                label4 = Label(self.login, text="Game loading... ", width=25, font=("arial", 40, "bold"))
                label4.place(x=0, y=400)
                time.sleep(1)
                self.play_game()

            else:  # incorrect id
                label4 = Label(self.login, text="Wrong id's enter again", width=25, font=("arial", 40, "bold"))
                label4.place(x=0, y=400)

    def login_lables(self):
        self.login.title("Game Login")
        self.login.minsize(SIZE[0], SIZE[1])
        self.login.maxsize(SIZE[0], SIZE[1])
        label1 = Label(self.login, text=" Game Login ", fg="black", font=("new times roman", 40, "bold"))
        label1.place(x=250, y=15)

        label2 = Label(self.login, text="Username :", font=("arial", 16, "bold"))
        label2.place(x=144, y=150)

        textBox1 = Entry(self.login, textvar=self.user_name, width=30, font=("arial", 16, "bold"))
        textBox1.place(x=290, y=150)

        label3 = Label(self.login, text="Password :", font=("arial", 16, "bold"))
        label3.place(x=150, y=250)

        textBox2 = Entry(self.login, textvar=self.password, width=30, font=("arial", 16, "bold"))
        textBox2.place(x=290, y=250)

        button1 = Button(self.login, text="   Login   ", fg="black", bg="white", relief="raised",
                         font=("arial", 16, "bold"),
                         command=self.play_game)
        button1.place(x=335, y=340)

    def play_game(self):
        pygame.init()
        self.login.withdraw()
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption("Pokemon")
        self.play_music()
        self.update_x_y_pos()
        self.run()

    def run(self):
        bg = pygame.image.load('background.jpeg')
        running = True
        while running:
            self.screen.fill('WHITE')
            self.screen.blit(bg, (0, 0))
            self.draw_line_arrows()
            self.draw_pokeballs()  # creates pokeballs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                pygame.display.update()

    def draw_pokeballs(self):
        """
        This method initializes the ui.
        i'e -> creates objects ( lines, elevators, floors... )
        """
        nodes = self.graph_algo.get_graph().get_all_v()
        pokeball = pygame.image.load("pokeball.png")  # pokeball loader.
        for k in nodes:
            curr_x = self.nodesX[k]
            curr_y = self.nodesY[k]
            update_pos = (curr_x, curr_y)
            self.screen.blit(pokeball, (update_pos[0] - 5, update_pos[1] - 5))

    def draw_line_arrows(self):
        nodes = self.graph_algo.get_graph().get_all_v()
        for k in nodes:
            out_edge = self.graph_algo.get_graph().all_out_edges_of_node(k)
            start = [self.nodesX[k], self.nodesY[k]]
            for v in out_edge:
                end = [self.nodesX[v], self.nodesY[v]]
                pygame.draw.line(self.screen, 'BLACK', start, end, 2)
                # self.draw_arrow(BLACK, start, end)

    def play_music(self):
        file = 'theme_song.mp3'
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1)  # If the loops is -1 then the music will repeat indefinitely.

    def update_x_y_pos(self):
        minX = sys.float_info.max
        minY = sys.float_info.max
        maxX = sys.float_info.min
        maxY = sys.float_info.min

        nodes = self.graph_algo.get_graph().get_all_v()

        for k in nodes:
            curr_pos = nodes[k]
            x = float(curr_pos[0])
            y = float(curr_pos[1])
            minX = min(minX, x)
            minY = min(minY, y)
            maxX = max(maxX, x)
            maxY = max(maxY, y)

        X_Scaling = SIZE[0] / (maxX - minX) * 0.9
        Y_Scaling = SIZE[1] / (maxY - minY) * 0.9

        for k in nodes:
            curr_id = k
            curr_pos = nodes[k]
            x = (float(curr_pos[0]) - minX) * X_Scaling + 10
            y = (float(curr_pos[1]) - minY) * Y_Scaling + 30

            self.nodesX[curr_id] = int(x)
            self.nodesY[curr_id] = int(y)

    def draw_arrow(self, colour, start, end):  # start = [x,y] end = [x,y]
        pygame.draw.line(self.screen, colour, start, end, 2)
        rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 90
        pygame.draw.polygon(self.screen, BLACK, (
            (end[0] - 5 * math.sin(math.radians(rotation)), end[1] - 5 * math.cos(math.radians(rotation))),
            (
                end[0] + 30 * math.sin(math.radians(rotation - 120)),
                end[1] + 30 * math.cos(math.radians(rotation - 120))),
            (end[0] + 30 * math.sin(math.radians(rotation + 120)),
             end[1] + 30 * math.cos(math.radians(rotation + 120)))))


if __name__ == '__main__':
    nodes = {}
    graph = DiGraph(nodes)
    graph_algo = GraphAlgo()
    graph_algo.load_from_json("/Users/Shaked/PycharmProjects/DirectedWeigthedGraph_2/Ex3/data/A0.json")
    run = GraphGui(graph_algo)
