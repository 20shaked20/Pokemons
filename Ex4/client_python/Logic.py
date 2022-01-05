import sys
from math import dist
from Ex4.Project.DiGraph.DiGraph import DiGraph
from Ex4.client_python.game import game

INF = float("inf")


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
        if pokemons is not None:
            chase_pokemon = self.get_mvp(pokemons, assigned_pokemons)
            # chase_pokemon = pokemons.pop()
            print("SRC DEST", self.get_poke_edge(chase_pokemon, graph_json, g))
            src_dest_tuple = self.get_poke_edge(chase_pokemon, graph_json, g)
            if src_dest_tuple is None:
                for node in g.all_out_edges_of_node(agent.src):
                    return [node], None
            source, destination = src_dest_tuple

            if chase_pokemon.type == 1:
                # print(agent.src, destination)
                ans = self.game.graph_algo.dijkstra(agent.src, destination)[0]
                if ans == INF:
                    return [source], chase_pokemon
                if isinstance(ans, list):
                    ans.reverse()
                    return ans, chase_pokemon
                return [ans], chase_pokemon

            else:
                # print(agent.src, source)
                ans = self.game.graph_algo.dijkstra(agent.src, source)[0]
                if ans == INF:
                    return [destination], chase_pokemon
                if isinstance(ans, list):
                    ans.reverse()
                    return ans, chase_pokemon
                return [ans], chase_pokemon
