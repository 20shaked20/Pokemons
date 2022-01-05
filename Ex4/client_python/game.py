from types import SimpleNamespace
from client import Client
import json
import pygame
from Ex4.Project.DiGraph.DiGraph import DiGraph
from Ex4.Project.DiGraph.GraphAlgo import GraphAlgo

SIZE = 800, 480
# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'

g = DiGraph()


# TODO :
#  1. abs paths.

class game:
    """
    This class is responsible for initialization of the game client, and some helping methods like scale.
    """

    def __init__(self):
        self.client = Client()
        self.client.start_connection(HOST, PORT)
        self.graph_algo = GraphAlgo(g)
        self.screen = None
        self.clock = None
        self.pokemons = None
        self.graph_json = None
        self.pygame()

    def pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SIZE, depth=32, flags=16)  # 16 is resizable
        pygame.display.set_caption("Pokemon")
        self.clock = pygame.time.Clock()

    def start(self):
        self.init_graph()
        self.init_pokemons()
        self.set_nodes()
        self.add_agents()
        self.client.start()

    def init_pokemons(self):
        self.pokemons = json.loads(self.client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
        self.pokemons = [p.Pokemon for p in self.pokemons]
        for p in self.pokemons:
            x, y, _ = p.pos.split(',')
            p.pos = SimpleNamespace(x=float(x), y=float(y))
        return self.pokemons

    def init_graph(self):
        tmp = self.client.get_graph()
        self.graph_json = json.loads(tmp, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
        self.graph_algo.load_from_json(tmp)

    def set_nodes(self):
        for n in self.graph_json.Nodes:
            x, y, _ = n.pos.split(',')
            n.pos = SimpleNamespace(x=float(x), y=float(y))

    def get_data_proportions(self):
        # get data proportions
        min_x = min(list(self.graph_json.Nodes), key=lambda n: n.pos.x).pos.x
        min_y = min(list(self.graph_json.Nodes), key=lambda n: n.pos.y).pos.y
        max_x = max(list(self.graph_json.Nodes), key=lambda n: n.pos.x).pos.x
        max_y = max(list(self.graph_json.Nodes), key=lambda n: n.pos.y).pos.y
        return min_x, min_y, max_x, max_y

    def scale(self, data, min_screen, max_screen, min_data, max_data):
        """
        get the scaled data with proportions min_data, max_data
        relative to min and max screen dimensions
        """
        return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen

    # decorate scale with the correct values
    def my_scale(self, data, x=False, y=False):
        data_prop = self.get_data_proportions()
        if x:
            return self.scale(data, 50, self.screen.get_width() - 50, data_prop[0], data_prop[2])
        if y:
            return self.scale(data, 50, self.screen.get_height() - 50, data_prop[1], data_prop[3])

    def add_agents(self):
        self.client.add_agent("{\"id\":0}")
        # client.add_agent("{\"id\":1}")
        # client.add_agent("{\"id\":2}")
        # client.add_agent("{\"id\":3}")
