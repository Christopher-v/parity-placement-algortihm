import Initializer as ini
import SA_DS_placement as DS_DS
import RB_initializer as rb_i
import RB_placement as rb_p
import Graphics as graphics
import networkx as nx
from random import randint
import time
import Evaluation as eval

#This is the main class. This works as a mediator between the functions.
#From here we can change parameters such as storage-requirements and the size of the graphs.

if __name__ == "__main__":

#User defined paramters.

    #This loop was used during the evaluation - in order to run 20 cases.
    for x in range (21):
        Storage_requirements = (1,4,5,10,4, 6,3,10,4,8, 7,20,4,6,10, 4,6,8,14,5)

    #Initialization parameters.

        #start_time = time.time()

        Graph = ini.make_random_topology(700)
        Subgraph = ini.find_subgraph(Graph)
        Storage_capacity = ini.find_storage_capacity(Graph, Subgraph)
        Subgraph_capacity = ini.subgraph_capacity_sum(Storage_capacity)
        clustered_topology = ini.mark_cluster_in_graph(Graph, Subgraph)
        allocated_network_topology = ini.allocate_DS(Storage_requirements, Subgraph_capacity, clustered_topology)

    #Different evaluation methods

        #no_of_groups = eval.eval_groups(allocated_network_topology)
        #sec = time.time() - start_time
        #eval.eval_seonds_DS(sec)
        #print("--- %s seconds ---" % (time.time() - start_time))

    #eval.csv_group(no_of_groups)


        nx.write_graphml(allocated_network_topology, "/home/christopher/IdeaProjects/annealing3")

        #The graph used in the scheduling test-cases
        allocated_network_topology = nx.read_graphml("/home/christopher/IdeaProjects/annealing3",node_type=int)

#SA_DS - Annealing parameters:


        solution = DS_DS.solution(allocated_network_topology)
        DS_DS.neighbor(solution,allocated_network_topology)
        annealed_solution = DS_DS.anneal_DS(solution, allocated_network_topology)
        DS_DS.place_optimization(annealed_solution, allocated_network_topology)

        #eval.eval_cost_annealing()
    #eval.csv1()
    #eval.csv_cost_annealing()

        #start_time = time.time()

        # RB_initialization parameters:
        biggest_cluster_node = rb_i.find_highest_node_in_cluster(solution)
        redundant_blocks = rb_i.place_GB(biggest_cluster_node, allocated_network_topology)
        neighbours = rb_i.find_neighbour_cluster(redundant_blocks, allocated_network_topology)
        SgB_blocks = rb_i.place_SgB(redundant_blocks, neighbours, allocated_network_topology, solution)
        G_block    = rb_i.place_Global_B(redundant_blocks, biggest_cluster_node, allocated_network_topology)

        #sec = time.time() - start_time
        #eval.eval_seonds_DS(sec)
        #print("--- %s seconds ---" % (time.time() - start_time))

#RB - Annealing parameters:

        RB_solution = rb_p.solution_blocks(redundant_blocks, SgB_blocks, G_block)

    #RB_annealed_solution = rb_p.anneal_RB(RB_solution, allocated_network_topology)

        rb_p.place_optimization(RB_solution, allocated_network_topology)

#Graphics
    #This method prints the placed nodes
    graphics.print_topology(allocated_network_topology, Storage_requirements)

    #This method print the graph in a plot
    #graphics.draw_cluster(allocated_network_topology)


#Evalution methods

        #eval.eval_occu_nodes_parity(allocated_network_topology)
        #eval.eval_usage_RB(allocated_network_topology)
    #eval.csv_occu_nodes_parity()
#eval.csv_usage()
    #eval.csv_usage_RB()

        #eval.eval_cost_annealing()
    #eval.csv1()
    #eval.csv_cost_annealing()



