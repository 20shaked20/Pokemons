import json
from collections import deque
from random import uniform
from Ex4.Project.DiGraph.DiGraph import DiGraph

INF = float("inf")


class GraphAlgo:
    """
    This class is used for algorithm on the graph.
    """

    def __init__(self, graph: DiGraph = None):  # actually its DiGraph.
        """
        This is the constructor of the graph
        :param graph: represents a DiGraph.
        """
        if graph is None:
            self.graph = DiGraph()
        else:
            self.graph = graph

    def get_graph(self) -> DiGraph:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """
        try:
            _dict = json.loads(file_name)
            edges = _dict["Edges"]
            nodes = _dict["Nodes"]

            # NODE Creation:
            xyz_tuple = None  # standard position
            key = "pos"
            for k in nodes:
                if key in k:
                    curr_pos = k["pos"]
                    xyz_split = curr_pos.split(",")
                    xyz_tuple = tuple(xyz_split)
                    curr_id = k["id"]
                    self.graph.add_node(curr_id, xyz_tuple)
                else:
                    xyz_tuple = (uniform(0.0, 100.0), uniform(0.0, 100.0), 0.0)  # in case it has
                    curr_id = k["id"]
                    self.graph.add_node(curr_id, xyz_tuple)

            # EDGES Creation:
            for k in edges:
                curr_src = k["src"]
                curr_weight = k["w"]
                curr_dest = k["dest"]
                self.graph.add_edge(curr_src, curr_dest, curr_weight)
            return True
        except FileNotFoundError:
            return False

    def dijkstra(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        Approach:
        using a dictionary of each node distance from start node_id  and dictionary for previous updated node,
        At first we init a dictionary to unvisited all nodes, and every time we visit one update it to visited so we want need to revisit it.
        each node is checked for its neighbours and calculates its distances while getting the best one we want.
        Accumulating the distance for each node until we reach dest node and we stop checking.
        after that, in order to return the list of the nodes, we used deque to traverse backwards in our path using the 'previous node'
        dictionary, by that we achieved saving the path from id1 - id2.
        Notes:
        If there is no path between id1 and id2, or one of them do not exist the function returns (float('inf'),[])
        More info:
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        """
        if self.get_graph().get_all_v().get(id1) is None or self.get_graph().get_all_v().get(id2) is None:
            return INF, []
        unvisited_nodes = self.get_graph().get_all_v()

        # Creating a dictionary of each node's distance from start_node(id1).
        # it will be updated using relaxation on each traverse
        dist_from_id1 = {}
        for node in self.get_graph().get_all_v():
            if node == id1:
                dist_from_id1[node] = 0
            else:
                dist_from_id1[node] = INF

        # Initialize previous_node, the dictionary that maps each node to the
        # node it was visited from when the shortest path to it was found.
        previous_node = {node: None for node in self.get_graph().get_all_v()}

        while unvisited_nodes:
            # Set current_node to the unvisited node with the shortest distance
            # calculated so far.
            current_node = min(
                unvisited_nodes, key=lambda node: dist_from_id1[node]
            )
            unvisited_nodes.pop(current_node)

            # if there's a node that is not connected to our node, its value is INF.
            # no reason to keep checking because we can't traverse any further.
            if dist_from_id1[current_node] == INF:
                break

            # this is the relaxation process, checks if there's a shorter way to reach a neighbour,
            for k in self.get_graph().all_out_edges_of_node(current_node):
                distance = self.get_graph().all_out_edges_of_node(current_node)[k]
                neighbor = k
                new_path = dist_from_id1[current_node] + distance
                if new_path < dist_from_id1[neighbor]:
                    dist_from_id1[neighbor] = new_path
                    previous_node[neighbor] = current_node

            if current_node == id2:  # src = dest, we reached the end, finished with loop.
                break

        # To build the path to be returned,
        # we iterate back from the nodes, to get the path. using likewise "parent array"
        path = deque()
        current_node = id2
        while previous_node[current_node] is not None:
            path.appendleft(current_node)
            current_node = previous_node[current_node]
        path.appendleft(id1)

        return list(path), dist_from_id1[id2]
