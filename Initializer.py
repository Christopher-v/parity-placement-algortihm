import random
import networkx as nx
import matplotlib.pyplot as plt
from random import randint
from operator import itemgetter

#This is the fist constructive heuristic which allocates the DDS

def make_random_topology(graph_size):


    number_of_nodes = graph_size

    #Creating a realistic and random Erdős-Rényi graph representing the network topology and its fog nodes
    #Graph = nx.gnp_random_graph(number_of_nodes,0.04,4)
    #creates random connected_caveman_graph
    Graph = nx.connected_caveman_graph(number_of_nodes,6)

    #Create random attributes representing storage capacity in fog nodes

    nx.set_node_attributes(Graph, 3, 'storage_capacity')

    nx.set_node_attributes(Graph, 0, 'storage_usage')

    nx.set_node_attributes(Graph, None, 'cluster_ID')

    nx.set_node_attributes(Graph, False, 'placed')

    nx.set_node_attributes(Graph, False, 'r_block')

    for node in Graph.nodes(data=True):
        graph_node = node[0]
        random_int = randint(1,3)
        Graph.add_node(graph_node, storage_capacity= random_int)

    return Graph

def find_subgraph(network_topology):
#This is the Bron–Kerbosch algorithm
    cliques = list(nx.find_cliques(network_topology))
    #n = len(cliques)

    #for i in range(n):
        #cluster_id = i
        #print ("subgraph:", i, "consists of ",cliques[i])
        #for j in range(len(cliques[i])):
        #    node_number = cliques[i][j]
        #    nx.Graph.add_node(network_topology, node_number , cluster_ID = cluster_id)
    #print('cliques',cliques)

    return cliques

def find_storage_capacity(network_topology, subgraph):
    #This is algortihm 1 - Find Storage Capacities

    n = len(subgraph)
    subgraph_storage_cap = []
    for i in range(n):
        cluster_id = i
        for j in range(len(subgraph[i])):
            node_number = subgraph[i][j]
            #print('node number',node_number)
            storage_capacity = network_topology.node[j]['storage_capacity']
            subgraph_storage_cap.append([node_number, cluster_id, storage_capacity])

    #for p in subgraph_storage_cap: print(p)

    return subgraph_storage_cap

def subgraph_capacity_sum(subgraph_storage_cap):
#This is algortihm 2 - Find Clique Sum
    print(subgraph_storage_cap)

    total_storage_cap = 0
    cluster_cap_sum = []
    temp_storage_cap = 0
    for i, j in enumerate(subgraph_storage_cap[:-1]):
        current_node       = j[0]
        current_cluster_id = j[1]
        current_storage_cap= j[2]
        next_cap = subgraph_storage_cap[i+1][1]
        temp_storage_cap = temp_storage_cap + current_storage_cap
        if next_cap is not current_cluster_id:
            total_storage_cap = total_storage_cap + temp_storage_cap
            cluster_cap_sum.append([current_cluster_id, total_storage_cap, current_node])
            pass
            total_storage_cap = 0
            temp_storage_cap  = 0
            cluster_id = subgraph_storage_cap[i+1][1]
    #sorting such that the cluster with highest capacity is first in list.
    cluster_cap_sum.sort(reverse=True, key=itemgetter(1))
    #for p in subgraph_storage_cap: print(p)
    print('cluster_cap_sum',cluster_cap_sum)

    return cluster_cap_sum

def mark_cluster_in_graph(network_topology, subgraph):

#This function places the previously found subgraphs and puts it in the graph.
#By iterating all the nodes in the network topology and the subgraph list
#and matching them. If it matches, the subgraph id is placed as an attribute in the graph.

    graph = network_topology

    for node in graph.nodes(data=True):
        for cluster_list in enumerate(subgraph):
            graph_node = node[0]
            for i in range(len(cluster_list[1])):
                cluster_id = cluster_list[0]
                cluster_nodes = cluster_list[1][i]
                if graph_node == cluster_nodes:
                    graph.add_node(graph_node, cluster_ID= cluster_id)

    return graph

def allocate_DS(storage_requirements, subgraph_capacity_sum, network_topology):
#This is the allocate DDS algortihm 3.

    assert len(subgraph_capacity_sum) > 0
    highest_storage_requirements  = sorted(storage_requirements,reverse=True)
    current_req = list.pop(highest_storage_requirements,[0][0])
    unallocated_req = current_req

#print(subgraph_capacity_sum)

    for i, j in enumerate(subgraph_capacity_sum):
        biggest_cluster_node_ids      = subgraph_capacity_sum[i][0]
        biggest_cluster_node          = subgraph_capacity_sum[i][2]
        nodes_neighbours = list(network_topology.neighbors(biggest_cluster_node))

        if unallocated_req > 0:
            #print('current requirment',current_req, 'current node capacity', network_topology.node[biggest_cluster_node]['storage_capacity'], 'current node', biggest_cluster_node)

            #constaints
            #checks if the node in the biggest cluster has storage_capacities and does not contain any data AND if connectivity of a node is atlest 2.
            n = len(nodes_neighbours)
            if network_topology.node[biggest_cluster_node]['storage_capacity'] != 0 and network_topology.node[biggest_cluster_node]['storage_usage'] == 0 and n >= 2 and unallocated_req > 0:
                network_topology.add_node(biggest_cluster_node, storage_usage=network_topology.node[biggest_cluster_node]['storage_capacity'], placed=True)
                unallocated_req = unallocated_req - network_topology.node[biggest_cluster_node]['storage_capacity']
                print('first node - placed')
                print('req', unallocated_req)
                #if req is not fulfilled, look for neighbours

                print('looking for neighbours')
                for neighbour_iterator, neighbour in enumerate(nodes_neighbours):
                    current_neighbour = nodes_neighbours[neighbour_iterator]
                    neighbours_neighbours = list(network_topology.neighbors(current_neighbour))
                    print('current neighbour', current_neighbour)
                    u = len(neighbours_neighbours)
                    assert len(nodes_neighbours) > 0

                    #checking if neighbour is in the same cluster
                    if network_topology.node[current_neighbour]['cluster_ID'] == biggest_cluster_node_ids and network_topology.node[current_neighbour]['storage_capacity'] != 0 and network_topology.node[current_neighbour]['storage_usage'] == 0 and u > 2 and unallocated_req > 0:
                        assert network_topology.node[current_neighbour]['cluster_ID'] != None
                        print('the neighbour is in same cluster - placing node')
                        #inserting attributes on the neigbouring node.
                        network_topology.add_node(current_neighbour, storage_usage=network_topology.node[current_neighbour]['storage_capacity'], placed=True)
                        #updating the usage
                        unallocated_req = unallocated_req - network_topology.node[current_neighbour]['storage_capacity']
                        print('req', unallocated_req)

                    #if neighbours is not in cluster - checks if capacities is alright.
                    elif n <= neighbour:
                        if network_topology.node[current_neighbour]['cluster_ID'] != biggest_cluster_node_ids and network_topology.node[current_neighbour]['storage_capacity'] != 0 and network_topology.node[current_neighbour]['storage_usage'] == 0 and u > 2 and unallocated_req > 0:
                            #assert network_topology.node[current_neighbour]['cluster_ID'] == None
                            print('none of the neighbours is in the same cluster - placing node outside')
                            #fill the neigbour with storage.
                            network_topology.add_node(current_neighbour, storage_usage=network_topology.node[current_neighbour]['storage_capacity'], placed=True, cluster_ID=biggest_cluster_node_ids)
                            #update the unfilled requirment
                            unallocated_req = unallocated_req - network_topology.node[current_neighbour]['storage_capacity']
                            print('req', unallocated_req)

                        else:
                            print('no neighbours fit')
                            i =+ 1
                            break
        #When the requirment is fulfilled - pop it from the list and start loop over
        elif unallocated_req <= 0:

            try:
                print('---req is fulfilled---', highest_storage_requirements[0])
            except IndexError:
                print('!!!!All requirements fulfilled!!!!')
                break

            try:
                new_highest = list.pop(highest_storage_requirements,[0][0])
            except IndexError:
                pass
            try:
                unallocated_req = new_highest
            except IndexError:
                print('!!!!All requirements fulfilled!!!!')
                break
            continue

##To-Do make an attribute which connects the stored nodes in a requirement. - requirment key or something


    ##also test with randint(0,X) - so that some nodes does'nt have capabilities.

    return network_topology







