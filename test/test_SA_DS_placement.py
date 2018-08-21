from unittest import TestCase
import Initializer as ini
import SA_DS_placement as sa_ds
import networkx as nx

class TestSolution(TestCase):
    def test_solution(self):
        random_topology = ini.make_random_topology(400, 3)
        solution = sa_ds.solution(random_topology)

class Test_neighbour(TestCase):
    def test_neighbour(self):

        storage_requirments = [1,3,5,6,10,3,20]
        random_graph = ini.make_random_topology(400,3)
        subgraph = ini.find_subgraph(random_graph)
        storage_capacity = ini.find_storage_capacity(random_graph, subgraph)
        subgraph_capacity_sum = ini.subgraph_capacity_sum(storage_capacity)
        clustered_topology = ini.mark_cluster_in_graph(random_graph,subgraph)
        allocated_network_topology = ini.allocate_DS(storage_requirments, subgraph_capacity_sum, storage_capacity, clustered_topology)
        solution = sa_ds.solution(allocated_network_topology)
        new_solution = sa_ds.neighbor(solution, allocated_network_topology)
        self.assertTrue(new_solution, type(new_solution) == list)
        self.assertTrue(len(new_solution) == len(solution))


class Test_cost(TestCase):
    #testing scalability and if the solution from neighbour gives a result.
    def test_cost(self):
        storage_requirments = [1,3,5,6,10,3,20]
        random_graph = ini.make_random_topology(400,3)
        subgraph = ini.find_subgraph(random_graph)
        storage_capacity = ini.find_storage_capacity(random_graph, subgraph)
        subgraph_capacity_sum = ini.subgraph_capacity_sum(storage_capacity)
        clustered_topology = ini.mark_cluster_in_graph(random_graph,subgraph)
        allocated_network_topology = ini.allocate_DS(storage_requirments, subgraph_capacity_sum, storage_capacity, clustered_topology)
        solution = sa_ds.solution(allocated_network_topology)
        new_solution = sa_ds.neighbor(solution, allocated_network_topology)
        cost = sa_ds.cost(new_solution,allocated_network_topology)
        self.assertIsInstance(cost, int)
        print(cost)


    def test_cost_2(self):

    #Testing if the old soluton gives a result.
        storage_requirments = [1,3,5,6,10,3,20]
        random_graph = ini.make_random_topology(400,3)
        subgraph = ini.find_subgraph(random_graph)
        storage_capacity = ini.find_storage_capacity(random_graph, subgraph)
        subgraph_capacity_sum = ini.subgraph_capacity_sum(storage_capacity)
        clustered_topology = ini.mark_cluster_in_graph(random_graph,subgraph)
        allocated_network_topology = ini.allocate_DS(storage_requirments, subgraph_capacity_sum, storage_capacity, clustered_topology)
        solution = sa_ds.solution(allocated_network_topology)
        cost = sa_ds.cost(solution,allocated_network_topology)
        self.assertIsInstance(cost, int)
        print('solution')

        print(cost)

class Test_anneal_DS(TestCase):
    def test_anneal_DS(self):

        storage_requirments = [1,3,5,6,10,3,20]
        random_graph = ini.make_random_topology(400,3)
        subgraph = ini.find_subgraph(random_graph)
        storage_capacity = ini.find_storage_capacity(random_graph, subgraph)
        subgraph_capacity_sum = ini.subgraph_capacity_sum(storage_capacity)
        clustered_topology = ini.mark_cluster_in_graph(random_graph, subgraph)
        allocated_network_topology = ini.allocate_DS(storage_requirments, subgraph_capacity_sum, storage_capacity, clustered_topology)
        solution = sa_ds.solution(allocated_network_topology)
        annealed_solution = sa_ds.anneal_DS(solution, allocated_network_topology)

class Test_initialization(TestCase):
    def test_initialization(self):

        storage_requirments = [1,3,5]
        random_graph = ini.make_random_topology(100,3)
        print('hje')
        nx.write_edgelist(random_graph, '/home/christopher/IdeaProjects/Genetic_algortihm/graph.gz')









