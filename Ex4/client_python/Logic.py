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

    def is_assigned(self, pokemon, assigned_pokemons):
        for p in assigned_pokemons:
            if p is not None:
                if p.pos.x == pokemon.pos.x and p.pos.y == pokemon.pos.y:
                    return True
        return False

    def get_mvp(self, pokemons, assigned_pokemons):
        max_v = sys.float_info.min
        curr_pokemon = None
        for p in pokemons:
            if p.value > max_v and not self.is_assigned(p, assigned_pokemons):
                max_v = p.value
                curr_pokemon = p
        # pokemons.remove(curr_pokemon)
        return curr_pokemon

    def get_closest_poke(self, pokemons, agent):
        pass

    def get_poke_in_radius(self, agent, pokemons, assigned_pokemons, radius: int, graph_json, g: DiGraph):
        best = 10  # we want less than 4 nodes away from agent's src anyway.
        best_pokemon = None
        for p in pokemons:
            if not self.is_assigned(p, assigned_pokemons):
                src_dest_tuple = self.get_poke_edge(p, graph_json, g)
                if src_dest_tuple is None:
                    continue
                source, destination = src_dest_tuple
                if p.type == 1:
                    path = self.game.graph_algo.dijkstra(agent.src, destination)[0]
                    if path == INF:
                        continue
                    # print(path)
                    if len(path) < radius and len(path) < best:
                        best = len(path)
                        best_pokemon = p
                else:
                    path = self.game.graph_algo.dijkstra(agent.src, source)[0]
                    if path == INF:
                        continue
                    # print(path)
                    if len(path) < radius and len(path) < best:
                        best = len(path)
                        best_pokemon = p
        return best_pokemon

    def get_poke_edge(self, pokemon, graph_json, g: DiGraph) -> (int, int):
        source = -1
        destination = -1
        eps = 0.00000001
        if pokemon is not None:
            for edge in graph_json.Edges:
                src = g.get_all_v().get(edge.src)
                dest = g.get_all_v().get(edge.dest)
                if pokemon.type < 0 and src < dest: continue
                if pokemon.type > 0 and src > dest: continue
                a_p = [float(pokemon.pos.x), float(pokemon.pos.y)]  # x,y pokemon
                b_src = [float(src[0]), float(src[1])]  # x,y for src
                c_dst = [float(dest[0]), float(dest[1])]  # x,y for src

                bc = dist(b_src, c_dst)
                ba = dist(b_src, a_p)
                ca = dist(c_dst, a_p)

                da = ca + ba

                if abs(da - bc) <= eps:
                    source = edge.src
                    destination = edge.dest
            return source, destination

    def get_cut(self):
        # TODO: figure out how to get strongly connected NODE cuts
        pass

    def get_best_path(self, agent, graph_json, g: DiGraph, assigned_pokemons) -> (list, object):
        """
        This method finds the best path for an agent in our 'game'
        :param agent:
        :return: A path of integers representing the next set of nodes the agent will travel to
        """
        pokemons = self.game.init_pokemons()
        radius: int = 4
        if pokemons is not None:
            # chase_pokemon = self.get_mvp(pokemons, assigned_pokemons)
            chase_pokemon = self.get_poke_in_radius(agent,pokemons,assigned_pokemons,radius, graph_json, g)
            if chase_pokemon is None:
                chase_pokemon = self.get_mvp(pokemons, assigned_pokemons)
            # print("SRC DEST", self.get_poke_edge(chase_pokemon, graph_json, g))
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
