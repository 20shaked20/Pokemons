import sys
from Ex4.client_python.game import game
from Ex4.DiGraph.GraphAlgo import GraphAlgo

INF = float("inf")


class Logic:
    """
    This class is responsible for how our agents will and try to capture the pokemon.
    it will use the graph implementation from our last Project in python.
    """

    def __init__(self, game: game):
        self.game = game

    def agent_path(self, agent, pokemons, assigned_pokemons, graph_algo: GraphAlgo, graph_json):
        min_dist = sys.float_info.max
        # chase_pokemon = None
        next = None
        src = agent.dest
        if agent.dest == -1:
            src = agent.src

        for pokemon in pokemons:
            print("ALL: ", assigned_pokemons)
            print("SINGLE: ", pokemon)
            # if pokemon in assigned_pokemons: continue
            pokemon_edge = self.game.misc.get_poke_edge(pokemon=pokemon, graph_json=graph_json,
                                                        g=graph_algo.get_graph())
            if src == pokemon_edge[1]:
                return pokemon_edge[0]
            else:
                path, curr_dist = self.game.graph_algo.dijkstra(src, pokemon_edge[1])
                if curr_dist < min_dist:
                    min_dist = curr_dist
                    next = path[1]
                    # chase_pokemon = pokemon
        # assigned_pokemons.append(chase_pokemon)
        return next
