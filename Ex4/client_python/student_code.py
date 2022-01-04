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

client = Client()
client.start_connection(HOST, PORT)

pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))

print(pokemons)

graph_json = client.get_graph()

"""
INTEGRATING OUR GRAPH WITH THE PROJECT:
"""

g = DiGraph()
graph_algo = GraphAlgo(g)
graph_algo.load_from_json(graph_json)
print(graph_algo.get_graph())


for n in g_easy.Nodes:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))

# get data proportions
min_x = min(list(g_easy.Nodes), key=lambda n: n.pos.x).pos.x
min_y = min(list(g_easy.Nodes), key=lambda n: n.pos.y).pos.y
max_x = max(list(g_easy.Nodes), key=lambda n: n.pos.x).pos.x
max_y = max(list(g_easy.Nodes), key=lambda n: n.pos.y).pos.y


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimensions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values


def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


radius = 10

client.add_agent("{\"id\":0}")
# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":3}")

# this command starts the server - the game is running now
client.start()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""

# Start of helper methods and data structures
agent_paths = {}


# pokemon_imgs = []
# for i in range(0,10):
#     pokemon_imgs.append()


def get_best_path(agent, g_easy, g: DiGraph, pokemons) -> list:
    """
    This method finds the best path for an agent in our 'game'
    :param agent: TODO: understand what data type an agent is + add hint
    :return: A path of integers representing the next set of nodes the agent will travel to
    """
    pokemons = json.loads(client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=float(x), y=float(y))
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
        # print(abs(da - bc))

        if abs(da - bc) <= eps:
            source = edge.src
            destination = edge.dest

    if chase_pokemon.type == 1:
        print(agent.src, source)
        ans = graph_algo.shortest_path(agent.src, source)[0]
        ans.append(destination)
        return ans

    else:
        print(agent.src, destination)
        ans = graph_algo.shortest_path(agent.src, destination)[0]
        ans.append(source)
        return ans


# End of helper methods and data structures

while client.is_running() == 'true':
    pokemons = json.loads(client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    agent_paths = [] * len(agents)  # ADDED
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    bg = pygame.image.load('/Users/Shaked/PycharmProjects/Ex4-Pokemons/Ex4/Project/GUI/background.jpeg')
    screen.blit(bg, (0, 0))

    # draw edges
    for e in g_easy.Edges:
        # find the edge nodes
        src = next(n for n in graph.Nodes if n.id == e.src)
        dest = next(n for n in graph.Nodes if n.id == e.dest)

        # scaled positions
        src_x = my_scale(src.pos.x, x=True)
        src_y = my_scale(src.pos.y, y=True)
        dest_x = my_scale(dest.pos.x, x=True)
        dest_y = my_scale(dest.pos.y, y=True)

        # draw the line
        pygame.draw.line(screen, Color("BLACK"),
                         (src_x, src_y), (dest_x, dest_y))
        # draw nodes
    for n in g_easy.Nodes:
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)

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
            ttl = client.time_to_end()
            print(ttl, client.get_info())
        else:
            next_node = agent_paths[agent].pop()
            client.choose_next_edge(
                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())

    """ Original movement:
    for agent in agents:
        if agent.dest == -1:
            next_node = (agent.src - 1) % len(graph.Nodes)
            client.choose_next_edge(
                '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())
    """

    client.move()
# game over:
