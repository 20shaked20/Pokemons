from types import SimpleNamespace
import json
from pygame import gfxdraw
import pygame
from pygame import *
from Ex4.client_python.game import game
from Ex4.client_python.Logic import Logic

# Globals:
RADIUS = 10
FONT = pygame.font.SysFont('Arial', 10, bold=True)


# TODO :
#  1. abs paths.
#  2. figure our what are up and down pokemons
#  note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
#  3. add different pokemon images ( randomizer )
#  4. consider creating & DO CREATE later :
#   A.Agent.py -> responsible for movement & creation
#   B.Pokemon.py -> responsible for creation of new pokemons & getting their before scale and after scale coordinates

class Arena:
    """
    This is the class where Arena is created, while generating pokemons and agents.
    also is responsible for agent movement.
    """

    def __init__(self):
        self.game = game()
        self.game.start()
        self.logic = Logic(self.game)
        self.agent_paths = {}

    def load_arena(self):
        while self.game.client.is_running() == 'true':
            pokemons = json.loads(self.game.client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
            pokemons = [p.Pokemon for p in pokemons]
            for p in pokemons:
                x, y, _ = p.pos.split(',')
                p.pos = SimpleNamespace(x=self.game.my_scale(
                    float(x), x=True), y=self.game.my_scale(float(y), y=True))
            agents = json.loads(self.game.client.get_agents(),
                                object_hook=lambda d: SimpleNamespace(**d)).Agents
            agents = [agent.Agent for agent in agents]
            for a in agents:
                x, y, _ = a.pos.split(',')
                a.pos = SimpleNamespace(x=self.game.my_scale(
                    float(x), x=True), y=self.game.my_scale(float(y), y=True))
            # check events
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

            # refresh surface
            bg = pygame.image.load('/Users/Shaked/PycharmProjects/Ex4-Pokemons/Ex4/Project/GUI/background.jpeg')
            self.game.screen.blit(bg, (0, 0))

            # draw edges
            for e in self.game.graph_json.Edges:
                # find the edge nodes
                src = next(n for n in self.game.graph_json.Nodes if n.id == e.src)
                dest = next(n for n in self.game.graph_json.Nodes if n.id == e.dest)

                # scaled positions
                src_x = self.game.my_scale(src.pos.x, x=True)
                src_y = self.game.my_scale(src.pos.y, y=True)
                dest_x = self.game.my_scale(dest.pos.x, x=True)
                dest_y = self.game.my_scale(dest.pos.y, y=True)

                # draw the line
                pygame.draw.line(self.game.screen, Color("BLACK"),
                                 (src_x, src_y), (dest_x, dest_y))
                # draw nodes
            for n in self.game.graph_json.Nodes:
                x = self.game.my_scale(n.pos.x, x=True)
                y = self.game.my_scale(n.pos.y, y=True)

                # it's just to get a nice anti-aliased circle
                gfxdraw.filled_circle(self.game.screen, int(x), int(y),
                                      RADIUS, Color(64, 80, 174))
                gfxdraw.aacircle(self.game.screen, int(x), int(y),
                                 RADIUS, Color(255, 255, 255))

                # draw the node id
                id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
                rects = id_srf.get_rect(center=(x, y))
                self.game.screen.blit(id_srf, rects)

            # draw agents / pokeballs
            for agent in agents:
                pokeball = pygame.image.load(
                    "/Users/Shaked/PycharmProjects/Ex4-Pokemons/Ex4/Project/GUI/pokeball.png")  # pokeball loader.
                self.game.screen.blit(pokeball, (int(agent.pos.x), int(agent.pos.y)))

            # draw pokemons
            for p in pokemons:
                pygame.draw.circle(self.game.screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)

            # update screen changes
            display.update()

            # refresh rate (fps)
            self.game.clock.tick(60)

            # choose next edge
            # our movement algo:
            for agent in agents:
                if agent.dest == -1:
                    if not self.agent_paths.get(agent.id):
                        self.agent_paths[agent.id] = self.logic.get_best_path(agent, self.game.graph_json,
                                                                              self.game.graph_algo.get_graph())
                        self.agent_paths[agent.id].reverse()
                    next_node = self.agent_paths.get(agent.id).pop()
                    print("PATH : ", self.agent_paths.get(agent.id))
                    self.game.client.choose_next_edge(
                        '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
                    ttl = self.game.client.time_to_end()
                    print(ttl, self.game.client.get_info())
                else:
                    self.game.client.move()
# game over:
