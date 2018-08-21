from unittest import TestCase
import Initializer as ini
import networkx as nx


class TestMake_random_topology(TestCase):

    def test_make_random_topology(self):

        random_graph = ini.make_random_topology(300, 3)
        self.assertTrue(random_graph, type(random_graph) == nx.Graph)

class Test_find_subgraph(TestCase):
    def test_find_subgraph(self):

        random_graph = ini.make_random_topology(400,3)
        subgraph = ini.find_subgraph(random_graph)
        self.assertTrue(subgraph, type(subgraph) == list)

class Test_find_storage_capacity(TestCase):
    def test_find_storage_capacity(self):

        random_graph = ini.make_random_topology(400,3)
        subgraph = ini.find_subgraph(random_graph)
        storage_capacity = ini.find_storage_capacity(random_graph, subgraph)
        self.assertTrue(storage_capacity, type(storage_capacity) == list)

class Test_subgraph_capacity_sum(TestCase):
    def test_subgraph_sum(self):

        random_graph = ini.make_random_topology(400,3)
        subgraph = ini.find_subgraph(random_graph)
        storage_capacity = ini.find_storage_capacity(random_graph, subgraph)
        subgraph_capacity_sum = ini.subgraph_capacity_sum(storage_capacity)
        self.assertTrue(subgraph_capacity_sum, type(subgraph_capacity_sum) == list)


class Test_mark_cluster_in_graph(TestCase):
    def test_mark_cluster_in_graph(self):

        random_graph = ini.make_random_topology(400,3)
        subgraph = ini.find_subgraph(random_graph)
        cluster_mark = ini.mark_cluster_in_graph(random_graph, subgraph)
        self.assertTrue(cluster_mark, type(cluster_mark) == nx.Graph)


class Test_allocate_DS(TestCase):
    def test_allocate_DS(self):

        storage_requirments = [1,3,5,6,10,3,20]
        random_graph = ini.make_random_topology(400,3)
        subgraph = ini.find_subgraph(random_graph)
        storage_capacity = ini.find_storage_capacity(random_graph, subgraph)
        subgraph_capacity_sum = ini.subgraph_capacity_sum(storage_capacity)
        clustered_topology = ini.mark_cluster_in_graph(random_graph,subgraph)
        allocated_network_topology = ini.allocate_DS(storage_requirments, subgraph_capacity_sum, storage_capacity, clustered_topology)
        self.assertTrue(allocated_network_topology, type(allocated_network_topology) == nx.Graph)

#class Test_cost(TestCase):
 #   def test_cost(self):









