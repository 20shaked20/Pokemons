import sys
import time

import pygame
import math

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
        self.screen = None
        self.play_game()

    def play_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE, depth=32, flags=16)  # 16 is resizable
        pygame.display.set_caption("Pokemon")
        # self.play_music()
        self.update_x_y_pos()
        self.run()

    def run(self):
        bg = pygame.image.load('/Users/Shaked/PycharmProjects/Ex4-Pokemons/Ex4/Project/GUI/background.jpeg')
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
        pokeball = pygame.image.load("/Users/Shaked/PycharmProjects/Ex4-Pokemons/Ex4/Project/GUI/pokeball.png")  # pokeball loader.
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


if __name__ == '__main__':
    nodes = {}
    graph = DiGraph(nodes)
    graph_algo = GraphAlgo()
    graph_algo.load_from_json("/Users/Shaked/PycharmProjects/DirectedWeigthedGraph_2/Ex3/data/A0.json")
    run = GraphGui(graph_algo)
