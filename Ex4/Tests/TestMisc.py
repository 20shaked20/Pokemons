import json
import unittest
from math import dist
from types import SimpleNamespace

from Ex4.client_python.Misc import Misc


class MyTestCase(unittest.TestCase):

    def test_get_mvp(self):
        f = '{"Pokemons":[{"Pokemon":{"value":5.0}},{"Pokemon":{"value":9.0}},{"Pokemon":{"value":15.0}},{"Pokemon":{"value":20.0}}]}'
        pokemons = json.loads(f, object_hook=lambda d: SimpleNamespace(**d)).Pokemons
        pokemons = [p.Pokemon for p in pokemons]
        misc = Misc()
        p, p_id = misc.get_mvp(pokemons, [])
        self.assertEqual(p.value, 20)

    def test_get_poke_edge(self):
        eps = 0.00000001

        src_x, src_y = 1, 3
        dest_x, dest_y = 5, 4
        poke_x, poke_y = 3, 3.5

        a_p = [float(poke_x), float(poke_y)]  # x,y pokemon
        b_src = [float(src_x), float(src_y)]  # x,y for src
        c_dst = [float(dest_x), float(dest_y)]  # x,y for dest

        bc = dist(b_src, c_dst)
        ba = dist(b_src, a_p)
        ca = dist(c_dst, a_p)

        da = ca + ba

        if abs(da - bc) <= eps:
            self.assertTrue(True)
        else:
            self.fail()

        src_x, src_y = 1, 3
        dest_x, dest_y = 5, 4
        poke_x, poke_y = 3, 3.5

        a_p = [float(poke_x), float(poke_y)]  # x,y pokemon
        b_src = [float(src_x), float(src_y)]  # x,y for src
        c_dst = [float(dest_x), float(dest_y)]  # x,y for dest

        bc = dist(b_src, c_dst)
        ba = dist(b_src, a_p)
        ca = dist(c_dst, a_p)

        da = ca + ba

        if abs(da - bc) <= eps:
            self.assertTrue(True)
        else:
            self.fail()




if __name__ == '__main__':
    unittest.main()
