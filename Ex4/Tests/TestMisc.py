import json
import unittest
from types import SimpleNamespace
from Ex4.DiGraph.GraphAlgo import GraphAlgo

from Ex4.client_python.Misc import Misc


class MyTestCase(unittest.TestCase):

    def test_get_mvp(self):
        f = '{"Pokemons":[{"Pokemon":{"value":5.0}},{"Pokemon":{"value":9.0}},{"Pokemon":{"value":15.0}},{"Pokemon":{"value":20.0}}]}'
        pokemons = json.loads(f, object_hook=lambda d: SimpleNamespace(**d)).Pokemons
        print(pokemons)
        pokemons = [p.Pokemon for p in pokemons]
        print(pokemons)
        misc = Misc()
        p, p_id = misc.get_mvp(pokemons, [])
        self.assertEqual(p.value, 20)


if __name__ == '__main__':
    unittest.main()
