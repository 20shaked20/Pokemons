"""
 * Authors - Yonatan Ratner & Shaked Levi
 * Date - 5.1.2022
"""
import sys
from Ex4.client_python.game import game
from Ex4.DiGraph.GraphAlgo import GraphAlgo


class Logic:
    """
    This class is responsible for how our agents will and try to capture the pokemon.
    it will use the graph implementation from our last Project in python.
    """

    def __init__(self, game: game):
        self.game = game

    def agent_path(self, agent, pokemons, graph_algo: GraphAlgo, graph_json):
        """
        This method is using the dijkstra method we implemented in the last assignment to generate the best given path for our agent.
        what we did was to only assign the first node of the dijkstra path because we wanted our agent to move in single ticks.
        this way we can make sure if another agents picks up a pokemon our agent wont force going to it and will change course.
        """
        min_dist = sys.float_info.max
        next = None
        src = agent.dest
        if agent.dest == -1:
            src = agent.src

        for pokemon in pokemons:
            pokemon_edge = self.game.misc.get_poke_edge(pokemon=pokemon, graph_json=graph_json,
                                                        g=graph_algo.get_graph())
            if src == pokemon_edge[1]:
                return pokemon_edge[0]
            else:
                # dijkstra is a tuple of ( Path, weight )
                dijkstra = self.game.graph_algo.dijkstra(src, pokemon_edge[1])
                if dijkstra[1] < min_dist:
                    min_dist = dijkstra[1]
                    next = dijkstra[0][1]
        return next
