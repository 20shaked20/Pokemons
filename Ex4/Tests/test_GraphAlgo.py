import copy
from unittest import TestCase
from Ex3.src.GraphInterface import GraphInterface
from Ex3.src.data.Project.DiGraph import DiGraph
from Ex3.src.data.Project.GraphAlgo import GraphAlgo
from Ex3.src.data.Project.Node import Node
from typing import List
import os


class TestGraphAlgo(TestCase):

    def setUp(self) -> None:
        nodes = {}
        g = DiGraph(nodes)
        path = "/Users/Shaked/PycharmProjects/DirectedWeigthedGraph_2/Ex3/data/100Nodes.json"
        # path = "C:/Users/yonar/PycharmProjects/DirectedWeigthedGraph_2/Ex3/data/A5.json"
        self.graph_algo = GraphAlgo(g)
        self.graph_algo.load_from_json(path)

    def test_get_graph(self):
        tmp_DiGraph = self.graph_algo.get_graph()
        self.assertEqual(self.graph_algo.get_graph(), tmp_DiGraph)

    def test_load_from_json(self):
        file_loc = "/Users/Shaked/PycharmProjects/DirectedWeigthedGraph_2/Ex3/data/100Nodes.json"
        # file_loc = "C:/Users/yonar/PycharmProjects/DirectedWeigthedGraph_2/Ex3/data/A5.json"
        self.assertEqual(self.graph_algo.load_from_json(file_loc), True)
        self.assertEqual(self.graph_algo.load_from_json("bla"), False))

    def test_dijkstra(self):
        print(self.graph_algo.dijkstra(0, 6))


