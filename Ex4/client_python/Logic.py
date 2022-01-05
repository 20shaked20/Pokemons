import sys
from math import dist
from Ex4.Project.DiGraph.DiGraph import DiGraph
from Ex4.client_python.game import game


# TODO :
#  1. abs paths.
#  2. understand what data type an agent is + add hint

class Logic:
    """
    This class is responsible for how our agents will and try to capture the pokemon.
    it will use the graph implementation from our last Project in python.
    """

    def __init__(self, game: game):
        self.game = game

    def get_mvp(self, pokemons) -> object:
        max_v = sys.float_info.min
        curr_pokemon = None
        for p in pokemons:
            if p.value > max_v:
                max_v = p.value
                curr_pokemon = p
        return curr_pokemon

    def get_closest_poke(self, pokemons, agent):
        pass

    def get_best_path(self, agent, graph_json, g: DiGraph) -> list:
        """
        This method finds the best path for an agent in our 'game'
        :param agent:
        :return: A path of integers representing the next set of nodes the agent will travel to
        """
        pokemons = self.game.init_pokemons()
        # chase_pokemon = get_mvp(pokemons)
        chase_pokemon = pokemons.pop()
        source = -1
        destination = -1
        eps = 0.00000001
        for edge in graph_json.Edges:
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
            ans = self.game.graph_algo.dijkstra(agent.src, source)[0]
            ans.append(destination)
            return ans

        else:
            print(agent.src, destination)
            ans = self.game.graph_algo.dijkstra(agent.src, destination)[0]
            ans.append(source)
            return ans
