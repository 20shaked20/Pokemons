import copy
import json
import time
import sys
from collections import deque
from random import uniform
from typing import List

from Ex4.Project.DiGraph.DiGraph import DiGraph


INF = float("inf")


class GraphAlgo:

    def __init__(self, graph: DiGraph = None):  # actually its DiGraph.
        """
        This is the constructor of the graph
        :param graph: represents a DiGraph.
        """
        if graph is None:
            self.graph = DiGraph()
        else:
            self.graph = graph

    """This abstract class represents an interface of a graph."""

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

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        data = {"Edges": [], "Nodes": []}
        all_nodes = self.get_graph().get_all_v()
        for node in all_nodes:
            # key_list = list(all_nodes.keys())
            val_list = list(all_nodes.values())
            # print(val_list[node][0], ',' + val_list[node][1], ',', val_list[node][2])
            pos = str(val_list[node][0]) + ',' + str(val_list[node][1]) + ',' + str(val_list[node][2])
            data["Nodes"].append({
                'pos': pos,
                'id': node
            })
            # Iterate once over OUT-going edges
            edges = self.get_graph().all_out_edges_of_node(node)
            key_list = list(edges.keys())
            val_list = list(edges.values())
            for edge in edges:
                if not (edge in data["Edges"]):
                    data["Edges"].append({
                        'src': node,
                        'w': val_list[key_list.index(edge)],
                        'dest': edge
                    })

            # Then iterate once over IN-going edges
            edges = self.get_graph().all_in_edges_of_node(node)
            key_list = list(edges.keys())
            val_list = list(edges.values())
            for edge in edges:
                if not (edge in data["Edges"]):
                    data["Edges"].append({
                        'src': edge,
                        'w': val_list[key_list.index(edge)],
                        'dest': node
                    })
        # open(file_name, "x")  # cant "wx" - meaning create (x) + write (w), but just "w" will create if needed!
        json_file = open(str(file_name), "w")
        json_file.write(json.dumps(data, indent=4, ensure_ascii=False))
        return True
        """
        Explanation on values passed to json.dumps():
        indent = 4  -  activates pretty print if an integer is passed
        sort_keys = True  -  sorts the json 
        ensure_ascii = False  -  does not escape unicode characters to match ASCII 
        ( for example 'cost':'£4.00' becomes --> "cost": "\u00a34.00" if ensure_ascii=True )
        """

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        Approach:
        using a dictionary of each node distance from start node_id  and dictionary for previous updated node,
        At first we init a dictionary to unvisited all nodes, and every time we visit one update it to visited so we want need to revist it.
        each node is checked for its neighbours and calculates its distances while getting the best one we want.
        Accumulating the distance for each node untill we reach dest node and we stop checking.
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

        if dist_from_id1[id2] is INF or dist_from_id1[id2] <= 0:
            return INF, []

        return list(path), dist_from_id1[id2]

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
        Finds the shortest path that visits all the nodes in the list
        :param node_lst: A list of nodes id's
        :return: A list of the node id's in the path, and the overall distance (or cost/weight, etc...)
        """
        start_time = time.time()
        best_path = self.greedy_tsp(node_lst)
        if best_path is None:
            return None, -1
        temp_path = copy.deepcopy(best_path)
        best_cost = self.path_weight(temp_path)
        end_time = time.time()
        # print("Approximated a solution for TSP in:", end_time - start_time, "seconds with weight:", best_cost)
        return best_path, best_cost
        # return self.fixPath(node_lst, best_path), best_cost

    """
        START of TSP helper functions
    """

    def cost(self, node, neighbour):
        if node == neighbour:
            return 0.0
        neighbours = self.get_graph().all_out_edges_of_node(node)
        if len(neighbours) > 0:
            return neighbours.get(neighbour)
        return sys.float_info.max

    def path_weight(self, path: list[int]):
        path.reverse()
        ans = 0
        prev = path.pop()
        while path:
            next_n = path.pop()
            temp = self.cost(prev, next_n)
            ans += temp
            prev = next_n
        return ans

    def get_cheapest_neighbour(self, node):
        """
        This method find the cheapest neighbour of a node, and returns it.
        :param node: An integer for a node for which we want the cheapest neighbour
        :return: An int representing the cheapest neighbour node id, or -1 if no neighbours
        """
        neighbours = self.get_graph().all_out_edges_of_node(node)
        if len(neighbours) == 0:
            return -1
        best_cost = sys.float_info.max
        for neighbour in neighbours:
            cost = self.cost(node, neighbour)
            if cost < best_cost:
                best_cost = cost
                best_neighbour = neighbour
        return best_neighbour

    def greedy_tsp(self, cities: list[int]) -> List[int]:
        """
        This method heuristically computes a path for a variation on the TSP problem ( can repeat visits)
        :param cities: a list of nodes to visit
        :return: an ordered path of nodes representing a heuristically best route
        """
        curr_node = cities.pop()
        path = [curr_node]

        while len(cities) > 0:

            if len(cities) == 1:
                last_city = cities.pop()
                temp = self.shortest_path(path[-1], last_city)
                if temp[0] == INF:
                    return None
                path_to_rel = tuple(temp)
                path_to_rel = path_to_rel[0]
                path_to_rel.reverse()
                path_to_rel.pop()
                while path_to_rel:
                    t = path_to_rel.pop()
                    path.append(t)
                    if t in cities:
                        cities.remove(t)
                    if len(cities) == 0:
                        break
                # to_visit.remove(min(to_visit))
                continue  # fixed being stuck by plotting a path to a point in the list

            try:
                curr_node = self.get_cheapest_neighbour(path[-1])  # arr[-1] accesses last member of array
            except:
                curr_node = -1

            if curr_node in cities:
                cities.remove(curr_node)

            # exceptions : same solution, seperated for semantic reasons ( i.e. accessing path[-2] )

            # 1. no neighbours ( stuck )

            if curr_node == -1:
                temp = self.shortest_path(path[-1], cities.pop())
                if temp[0] == INF:
                    return None
                path_to_rel = tuple(temp)
                path_to_rel = path_to_rel[0]
                path_to_rel.reverse()
                path_to_rel.pop()
                while path_to_rel:
                    t = path_to_rel.pop()
                    path.append(t)
                    if t in cities:
                        cities.remove(t)
                    if len(cities) == 0:
                        break
                # to_visit.remove(min(to_visit))
                continue  # fixed being stuck by plotting a path to a point in the list

            # 2. looping ( repeating the same path )

            if len(path) >= 2:
                if path[-2] == curr_node:  # if we detect a loop, or we are stuck
                    # path_to_rel = self.shortest_path(path[-1], cities.pop())
                    temp = self.shortest_path(path[-1], cities.pop())
                    if temp[0] == INF:
                        return None
                    path_to_rel = tuple(temp)
                    path_to_rel: list = path_to_rel[0]  # this is a deque object
                    path_to_rel.reverse()
                    path_to_rel.pop()
                    while path_to_rel:
                        t = path_to_rel.pop()
                        path.append(t)
                        if t in cities:
                            cities.remove(t)
                        if len(cities) == 0:
                            break
                    # to_visit.remove(min(to_visit))
                    continue  # fixed being stuck by plotting a path to a point in the list

            # if all is 'right'

            path.append(curr_node)
        return path

    """
        END of TSP helper functions
    """

    def is_connected(self) -> bool:
        """
        private method that checks if the graph is strongly connected or not.
        :return: True if yes, false if not.
        """
        all_nodes = self.get_graph().get_all_v()
        for node in all_nodes:
            if not self.BFS_Helper(node):
                return False
        return True

    def BFS_Helper(self, node: int) -> bool:
        visited = {node}
        q = [node]
        while q:
            temp = q.pop()
            edges = self.get_graph().all_out_edges_of_node(temp)
            for edge in edges:
                if edge not in visited:
                    visited.add(edge)
                    q.append(edge)
        return len(visited) == len(self.get_graph().get_all_v())

    def centerPoint(self) -> (int, float):
        """
        Finds the node that has the shortest distance to it's farthest node.
        :return: The node id, min-maximum distance
        """
        if self.is_connected():
            min1 = sys.float_info.max
            node_id = -1
            for k in self.get_graph().get_all_v():
                curr_node = k
                max1 = sys.float_info.min
                for v in self.get_graph().get_all_v():
                    if v == k:  # same node, no need to check again.
                        continue
                    next_node = v
                    tmp_dijk = self.shortest_path(curr_node, next_node)
                    tmp = tmp_dijk[1]
                    if tmp_dijk[0] is not INF:
                        if tmp > max1:
                            max1 = tmp
                        if tmp > min1:
                            # we want Minimum of all maximums
                            break

                if min1 > max1:
                    min1 = max1
                    node_id = k

            return node_id, min1
        else:
            return False