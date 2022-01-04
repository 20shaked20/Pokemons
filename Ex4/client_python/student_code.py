"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from Ex4.Project.DiGraph.DiGraph import DiGraph
from Ex4.Project.DiGraph.GraphAlgo import GraphAlgo

SIZE = 800, 480
RED = (255, 0, 0)
BLACK = (0, 0, 0)
PINK = (255, 200, 200)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
radius = 10
# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'

# START PYGAME:
pygame.init()
screen = pygame.display.set_mode(SIZE, depth=32, flags=16)  # 16 is resizable
pygame.display.set_caption("Pokemon")
FONT = pygame.font.SysFont('Arial', 10, bold=True)
clock = pygame.time.Clock()

"""
INTEGRATING OUR GRAPH WITH THE PROJECT:
"""

g = DiGraph()
agent_paths = {}


class game:

    def __init__(self):
        self.client = Client()
        self.client.start_connection(HOST, PORT)
        self.graph_algo = GraphAlgo(g)
        self.pokemons = None
        self.graph_json = None

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
            return self.scale(data, 50, screen.get_width() - 50, data_prop[0], data_prop[2])
        if y:
            return self.scale(data, 50, screen.get_height() - 50, data_prop[1], data_prop[3])

    def add_agents(self):
        self.client.add_agent("{\"id\":0}")
        # client.add_agent("{\"id\":1}")
        # client.add_agent("{\"id\":2}")
        # client.add_agent("{\"id\":3}")


# this command starts the server - the game is running now
game = game()
game.start()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""


# Start of helper methods and data structures

def get_mvp(pokemons):
    max_v = sys.float_info.min
    curr_pokemon = None
    for p in pokemons:
        if p.value > max_v:
            max_v = p.value
            curr_pokemon = p
    return p


def get_closest_poke(pokemons, agent):
    pass


def get_best_path(agent, g_easy, g: DiGraph, pokemons) -> list:
    """
    This method finds the best path for an agent in our 'game'
    :param agent: TODO: understand what data type an agent is + add hint
    :return: A path of integers representing the next set of nodes the agent will travel to
    """
    pokemons = game.init_pokemons()
    # chase_pokemon = get_mvp(pokemons)
    chase_pokemon = pokemons.pop()
    source = -1
    destination = -1
    eps = 0.00000001
    for edge in g_easy.Edges:
        src = g.get_all_v().get(edge.src)
        dest = g.get_all_v().get(edge.dest)
        if chase_pokemon.type < 0 and src < dest: continue
        if chase_pokemon.type > 0 and src > dest: continue
        a_p = [float(chase_pokemon.pos.x), float(chase_pokemon.pos.y)]  # x,y pokemon
        b_src = [float(src[0]), float(src[1])]  # x,y for src
        c_dst = [float(dest[0]), float(dest[1])]  # x,y for src

        bc = dist(b_src, c_dst)
        ba = dist(b_src, a_p)
        ca = dist(c_dst, a_p)

        da = ca + ba

        if abs(da - bc) <= eps:
            source = edge.src
            destination = edge.dest

    if chase_pokemon.type == 1:
        print(agent.src, source)
        ans = game.graph_algo.shortest_path(agent.src, source)[0]
        ans.append(destination)
        return ans

    else:
        print(agent.src, destination)
        ans = game.graph_algo.shortest_path(agent.src, destination)[0]
        ans.append(source)
        return ans


# End of helper methods and data structures

while game.client.is_running() == 'true':
    pokemons = json.loads(game.client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=game.my_scale(
            float(x), x=True), y=game.my_scale(float(y), y=True))
    agents = json.loads(game.client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    agent_paths = [] * len(agents)  # ADDED
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=game.my_scale(
            float(x), x=True), y=game.my_scale(float(y), y=True))
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    bg = pygame.image.load('/Users/Shaked/PycharmProjects/Ex4-Pokemons/Ex4/Project/GUI/background.jpeg')
    screen.blit(bg, (0, 0))

    # draw edges
    for e in game.graph_json.Edges:
        # find the edge nodes
        src = next(n for n in graph.Nodes if n.id == e.src)
        dest = next(n for n in graph.Nodes if n.id == e.dest)

        # scaled positions
        src_x = game.my_scale(src.pos.x, x=True)
        src_y = game.my_scale(src.pos.y, y=True)
        dest_x = game.my_scale(dest.pos.x, x=True)
        dest_y = game.my_scale(dest.pos.y, y=True)

        # draw the line
        pygame.draw.line(screen, Color("BLACK"),
                         (src_x, src_y), (dest_x, dest_y))
        # draw nodes
    for n in game.graph_json.Nodes:
        x = game.my_scale(n.pos.x, x=True)
        y = game.my_scale(n.pos.y, y=True)

        # it's just to get a nice anti-aliased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw agents / pokeballs
    for agent in agents:
        pokeball = pygame.image.load(
            "/Users/Shaked/PycharmProjects/Ex4-Pokemons/Ex4/Project/GUI/pokeball.png")  # pokeball loader.
        screen.blit(pokeball, (int(agent.pos.x), int(agent.pos.y)))

    # draw pokemons
    # TODO: below - also figure our what are up and down pokemons
    # note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    # choose next edge
    # our movement algo:

    for agent in agents:
        if agent.dest == -1:
            path = get_best_path(agent)
            assign_path(agent, path)  # TODO: this method might have to reverse the list!!!
            next_node = agent_paths[agent].pop()
            client.choose_next_edge(
                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            ttl = game.client.time_to_end()
            print(ttl, game.client.get_info())
        else:
            game.client.move()

    """ Original movement:
    for agent in agents:
        if agent.dest == -1:
            next_node = (agent.src - 1) % len(graph.Nodes)
            client.choose_next_edge(
                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())
    """

# game over:
