"""
 * Authors - Yonatan Ratner & Shaked Levi
 * Date - 5.1.2022
"""
import threading
from types import SimpleNamespace
import json
from pygame import gfxdraw
import pygame
from pygame import *
from game import game
from Logic import Logic
from Misc import Misc
import os
from RunServerScript import RunServerScript
import time

# Globals:
RADIUS = 10
SIZE = 1280, 768


class Arena:
    """
    This is the class where Arena is created, while generating pokemons and agents.
    also is responsible for agent movement.
    """

    def __init__(self, case: int):
        self.case = case
        pygame.init()
        pygame.display.set_caption("Pokemon Level: " + str(case))
        self.server_script = RunServerScript()
        self.t = threading.Thread(target=self.server_script.server_activate, daemon=True, args=[int(case)])
        self.t.start()
        time.sleep(1)
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
        parent_path = Misc.resource_path(relative_path='data')
        self.images_path = parent_path + "/imgs/"
        self.game = game()
        self.game.start()
        self.logic = Logic(self.game)
        self.agent_paths = {}
        self.assigned_pokemons = []
        self.agents = []
        self.screen = pygame.display.set_mode((SIZE[0], SIZE[1]), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.clock = pygame.time.Clock()
        self.FONT = pygame.font.SysFont('Arial', 10, bold=True)
        self.start_time = self.game.client.time_to_end()
        self.load_arena()

    def game_over(self):
        """
        When the game ends, this method is applied making sure we stop the game and server.
        """
        pygame.quit()
        self.game.client.stop()
        self.game.client.stop_connection()
        exit(0)

    def pause(self):
        """
        method for the pause button.
        """
        self.game.client.stop_connection()

    def draw_stop_button(self):
        """
        Method for drawing the stop button.
        """
        text = "stop"
        font = pygame.font.Font(None, 32)
        txt_surface = font.render(text, True, 'BLACK')
        input_box = pygame.Rect(150, 10, 130, 32)
        dark_color = 'BLACK'
        self.screen.blit(txt_surface, (191, 15))
        pygame.draw.rect(self.screen, dark_color, input_box, 2)

    def draw_timer(self):
        """
        Method for drawing the timer label
        """
        text = str(pygame.time.get_ticks() / 1000) + "/" + str(round(float(self.start_time) / 1000))
        font = pygame.font.Font(None, 32)
        txt_surface = font.render(text, True, 'BLACK')
        input_box = pygame.Rect(10, 10, 130, 32)
        self.screen.blit(txt_surface, (15, 15))
        pygame.draw.rect(self.screen, 'BLACK', input_box, 2)

    def draw_moves(self):
        """
        Method for drawing the moves label
        """
        info = self.game.init_info()
        text = ' Moves: ' + str(info.moves)
        font = pygame.font.Font(None, 32)
        txt_surface = font.render(text, True, 'BLACK')
        input_box = pygame.Rect(10, 45, 130, 32)
        self.screen.blit(txt_surface, (10, 50))
        pygame.draw.rect(self.screen, 'BLACK', input_box, 2)

    def draw_score(self):
        """
        Method for drawing the score label
        """
        info = self.game.init_info()
        text = ' Score: ' + str(info.grade)
        font = pygame.font.Font(None, 32)
        txt_surface = font.render(text, True, 'BLACK')
        input_box = pygame.Rect(10, 80, 130, 32)
        self.screen.blit(txt_surface, (10, 85))
        pygame.draw.rect(self.screen, 'BLACK', input_box, 2)

    def draw_edges(self):
        """
        Method for drawing the edges of the graph
        """
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
        """
        Method for drawing the nodes of the graph.
        """
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
        """
        Method for drawing the agents, it changes accordingly to the agent current position
        """
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
        """
        Method for drawing the pokemons that appear in the graph, each time new pokemon pops it will draw him.
        """
        pokemons = json.loads(self.game.client.get_pokemons(), object_hook=lambda d: SimpleNamespace(**d)).Pokemons
        pokemons = [p.Pokemon for p in pokemons]
        for p in pokemons:
            x, y, _ = p.pos.split(',')
            p.pos = SimpleNamespace(x=self.game.my_scale(
                float(x), x=True), y=self.game.my_scale(float(y), y=True))
        for p in pokemons:
            # we used the % here, in order to make sure our pokemon stays the same.
            # the module number is changeable to the amount of pokemons you use
            val = int((p.value % 7))
            if val == 0:
                val += 1
            poke = pygame.image.load(self.images_path + "pokemons/" + str(val) + ".png")
            if p.type == 1:  # up pokemon
                plus = pygame.image.load(self.images_path + "pokemons/+.png")
                self.screen.blit(plus, (int(p.pos.x - 10), int(p.pos.y - 30)))
                self.screen.blit(poke, (int(p.pos.x - 10), int(p.pos.y - 10)))
            if p.type == -1:  # down pokemon
                minus = pygame.image.load(self.images_path + "pokemons/-.png")
                self.screen.blit(minus, (int(p.pos.x - 10), int(p.pos.y - 15)))
                self.screen.blit(poke, (int(p.pos.x - 10), int(p.pos.y - 10)))

    def load_arena(self):
        """
        this method is responsible for creating and loading the arena into view.
        it constantly reloads it self and draws the new pokemons and the current location of the agents.
        we used a delay of 6 sec to make sure our movement occurs 10 to sec, so it will fit the 300 moves in 30 sec.
        obviously reaching a perfect 300 moves in 30 sec is far from reality because of other methods loading and taking some weight on the program.
        """
        while self.game.client.is_running() == 'true':
            bg = pygame.image.load(self.images_path + "background.jpeg")
            self.screen.blit(pygame.transform.scale(bg, (SIZE[0], SIZE[1])), (0, 0))
            self.clock.tick(60)
            time.sleep(0.075)  # used to reduce n.o of movement to be exactly under 600/300 for each case
            self.game.client.move()

            if round(pygame.time.get_ticks() / 1000) >= round(float(self.start_time) / 1000):
                self.game_over()
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
                    mouse_ = pygame.mouse.get_pos()
                    if 150 <= mouse_[0] <= 150 + 130 and 10 <= mouse_[1] <= 32:
                        self.pause()

            # refresh surface
            self.draw_stop_button()
            self.draw_timer()
            self.draw_moves()
            self.draw_score()
            self.draw_edges()
            self.draw_nodes()
            self.draw_agents()
            self.draw_pokemons()
            display.update()

            self.agent_movement()

    def agent_movement(self):
        """
        This method is responsible for agent movement.
        """
        for agent in self.agents:
            if agent.dest == -1:
                curr_pokemons = self.game.init_pokemons()
                next_node = self.logic.agent_path(agent=agent, pokemons=curr_pokemons,
                                                  graph_algo=self.game.graph_algo, graph_json=self.game.graph_json)
                print("NEXT NODE : ", next_node)
                self.game.client.choose_next_edge(
                    '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
                ttl = self.game.client.time_to_end()
                print(ttl, self.game.client.get_info())

# game over:
