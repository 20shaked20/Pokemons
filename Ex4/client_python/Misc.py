import sys
from math import dist

from Ex4.Project.DiGraph.DiGraph import DiGraph

INF = float("inf")


class Misc:
    """
    A class containing common helper methods
    """

    def __init__(self):
        pass

    def is_assigned(self, pokemon, assigned_pokemons):
        for p in assigned_pokemons:
            if p is not None:
                if p.pos.x == pokemon.pos.x and p.pos.y == pokemon.pos.y:
                    return True
        return False

    def get_mvp(self, pokemons, assigned_pokemons):
        max_v = sys.float_info.min
        poke_id = 0
        i = 0
        curr_pokemon = None
        for p in pokemons:
            if p.value > max_v and not self.is_assigned(p, assigned_pokemons):
                max_v = p.value
                curr_pokemon = p
                poke_id = i
            i += 1
        # pokemons.remove(curr_pokemon)
        return curr_pokemon, poke_id

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
            # if pokemon.type == 1:
            return source, destination
            # else:
            #     return destination, source
