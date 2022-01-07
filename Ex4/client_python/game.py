from types import SimpleNamespace

from Ex4.client_python.Misc import Misc
from client import Client
import json
from Ex4.Project.DiGraph.GraphAlgo import GraphAlgo

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'


class game:
    """
    This class is responsible for initialization of the game client, and some helping methods like scale.
    """

    def __init__(self):
        self.client = Client()
        self.client.start_connection(HOST, PORT)
        self.graph_algo = GraphAlgo()
        self.misc = Misc()
        self.pokemons = None
        self.graph_json = None
        self.info = None
        self.SIZE = 1280, 768
        self.start()

    def start(self):
        self.init_graph()
        self.init_pokemons()
        self.init_info()
        self.add_agents()
        self.set_nodes()
        self.client.start()

    def update_size(self, new_size):
        self.SIZE = new_size

    def init_info(self):
        tmp = self.client.get_info()
        self.info = json.loads(tmp, object_hook=lambda json_dict: SimpleNamespace(**json_dict)).GameServer
        return self.info

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
            return self.scale(data, 50, self.SIZE[0] - 50, data_prop[0], data_prop[2])
        if y:
            return self.scale(data, 50, self.SIZE[1] - 50, data_prop[1], data_prop[3])

    def add_agents(self):
        size = self.init_info()
        size = size.agents
        pokemons = self.init_pokemons()
        for i in range(0, size):
            mvp, x = self.misc.get_mvp(pokemons=pokemons, assigned_pokemons=[])
            print(x)
            edge = self.misc.get_poke_edge(pokemon=mvp, graph_json=self.graph_json,
                                           g=self.graph_algo.get_graph())
            pokemons.pop(x)
            self.client.add_agent("{\"id\":" + str(edge[1]) + "}")
