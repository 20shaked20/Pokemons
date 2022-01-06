from types import SimpleNamespace
import json
from pygame import gfxdraw
import pygame
from pygame import *
from Ex4.client_python.game import game
from Ex4.client_python.Logic import Logic
import os

# Globals:
RADIUS = 10
SIZE = 1280, 768


class Arena:
    """
    This is the class where Arena is created, while generating pokemons and agents.
    also is responsible for agent movement.
    """

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pokemon")
        parent_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        self.images_path = parent_path + "/imgs/"
        self.game = game()
        self.game.start()
        self.logic = Logic(self.game)
        self.agent_paths = {}
        self.assigned_pokemons = []
        self.agents = []
        self.delay = 0
        self.screen = pygame.display.set_mode((SIZE[0], SIZE[1]), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.clock = pygame.time.Clock()
        self.FONT = pygame.font.SysFont('Arial', 10, bold=True)
        self.start_time = self.game.client.time_to_end()
        self.load_arena()

    def game_over(self):
        self.game.client.stop()
        save_info = self.game.client.get_info()
        # self.game.client.stop_connection()
        # pygame.quit()
        # exit(0)

    def draw_stop_button(self):
        text = "stop"
        font = pygame.font.Font(None, 32)
        txt_surface = font.render(text, True, 'BLACK')
        input_box = pygame.Rect(150, 10, 130, 32)
        light_color = (170, 170, 170)
        dark_color = 'BLACK'
        self.screen.blit(txt_surface, (191, 15))
        pygame.draw.rect(self.screen, dark_color, input_box, 2)

    def draw_timer(self):
        text = str(pygame.time.get_ticks() / 1000) + "/" + str(round(float(self.start_time) / 1000))
        font = pygame.font.Font(None, 32)
        txt_surface = font.render(text, True, 'BLACK')
        input_box = pygame.Rect(10, 10, 130, 32)
        self.screen.blit(txt_surface, (15, 15))
        pygame.draw.rect(self.screen, 'BLACK', input_box, 2)

    def draw_moves(self):
        info = self.game.init_info()
        text = ' Moves: ' + str(info.moves)
        font = pygame.font.Font(None, 32)
        txt_surface = font.render(text, True, 'BLACK')
        input_box = pygame.Rect(10, 45, 130, 32)
        self.screen.blit(txt_surface, (10, 50))
        pygame.draw.rect(self.screen, 'BLACK', input_box, 2)

    def draw_score(self):
        info = self.game.init_info()
        text = ' Score: ' + str(info.grade)
        font = pygame.font.Font(None, 32)
        txt_surface = font.render(text, True, 'BLACK')
        input_box = pygame.Rect(10, 80, 130, 32)
        self.screen.blit(txt_surface, (10, 85))
        pygame.draw.rect(self.screen, 'BLACK', input_box, 2)

    def draw_edges(self):
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
            pygame.draw.line(self.screen, Color("BLACK"),
                             (src_x, src_y), (dest_x, dest_y))

    def draw_nodes(self):
        for n in self.game.graph_json.Nodes:
            x = self.game.my_scale(n.pos.x, x=True)
            y = self.game.my_scale(n.pos.y, y=True)

            # it's just to get a nice anti-aliased circle
            gfxdraw.filled_circle(self.screen, int(x), int(y),
                                  RADIUS, Color(64, 80, 174))
            gfxdraw.aacircle(self.screen, int(x), int(y),
                             RADIUS, Color(255, 255, 255))

            # draw the node id
            id_srf = self.FONT.render(str(n.id), True, Color(255, 255, 255))
            rects = id_srf.get_rect(center=(x, y))
            self.screen.blit(id_srf, rects)

    def draw_agents(self):
        self.agents = json.loads(self.game.client.get_agents(),
                                 object_hook=lambda d: SimpleNamespace(**d)).Agents
        self.agents = [agent.Agent for agent in self.agents]
        for a in self.agents:
            x, y, _ = a.pos.split(',')
            a.pos = SimpleNamespace(x=self.game.my_scale(
                float(x), x=True), y=self.game.my_scale(float(y), y=True))
        for agent in self.agents:
            pokeball = pygame.image.load(self.images_path + "agents/Agent" + str(agent.id) + ".png")
            self.screen.blit(pokeball, (int(agent.pos.x - 10), int(agent.pos.y - 10)))

    def draw_pokemons(self):
        pokemons = json.loads(self.game.client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
        pokemons = [p.Pokemon for p in pokemons]
        for p in pokemons:
            x, y, _ = p.pos.split(',')
            p.pos = SimpleNamespace(x=self.game.my_scale(
                float(x), x=True), y=self.game.my_scale(float(y), y=True))
        for p in pokemons:
            val = int((p.value % 7))
            if val == 0:
                val += 1
            poke = pygame.image.load(self.images_path + "pokemons/" + str(val) + ".png")
            self.screen.blit(poke, (int(p.pos.x - 10), int(p.pos.y - 10)))

    def load_arena(self):
        while self.game.client.is_running() == 'true':
            self.delay += 1
            bg = pygame.image.load(self.images_path + "background.jpeg")
            # '/Users/Shaked/PycharmProjects/Ex4-Pokemons/Ex4/imgs/background.jpeg')
            # self.screen.blit(bg, (0, 0))
            self.screen.blit(pygame.transform.scale(bg, (SIZE[0], SIZE[1])), (0, 0))

            # check events
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                elif events.type == VIDEORESIZE:
                    self.screen = pygame.display.set_mode(
                        events.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
                    self.game.update_size(events.dict['size'])
                    self.screen.blit(pygame.transform.scale(bg, events.dict['size']), (0, 0))
                    pygame.display.flip()
                elif events.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if 150 <= mouse[0] <= 150 + 130 and 10 <= mouse[1] <= 32:
                        self.game_over()
            if self.delay > 5:
                self.game.client.move()
                self.delay = 0
            # refresh surface
            self.draw_stop_button()
            self.draw_timer()
            self.draw_moves()
            self.draw_score()
            # draw edges
            self.draw_edges()
            # draw nodes
            self.draw_nodes()
            # draw agents / pokeballs
            self.draw_agents()
            # draw pokemons
            self.draw_pokemons()
            # update screen changes
            display.update()
            self.unthreaded_agents()

    def unthreaded_agents(self):
        for agent in self.agents:
            if agent.dest == -1:
                curr_pokemons = self.game.init_pokemons()
                next_node = self.logic.agent_path(agent=agent, pokemons=curr_pokemons,
                                                  assigned_pokemons=self.assigned_pokemons,
                                                  graph_algo=self.game.graph_algo, graph_json=self.game.graph_json)
                print("NEXT NODE : ", next_node)
                self.game.client.choose_next_edge(
                    '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
                ttl = self.game.client.time_to_end()
                print(ttl, self.game.client.get_info())


# game over:
