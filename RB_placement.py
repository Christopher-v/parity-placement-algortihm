import random
from random import randint
import networkx as nx
import math
import RB_initializer as rb_int

#This is the Simulated annealing for parity placemenyt. - This is only briefly mentioned in the thesis
#This is because it gives wrong outputs. It may be because of the cost function.

def anneal_RB(solution, allocated_network_topology):

    print('----------SA---------')

    #get the cost from the initialized solution.
    old_solution = solution
    old_cost = cost(old_solution, allocated_network_topology)

    T = 1.0
    T_min = 0.00001
    alpha = 0.9
    while T > T_min:
        print('running SA')
        #indicating the max iteration number for the algorithm.
        i = 1
        while i <= 100:
            new_solution = neighbor(old_solution,allocated_network_topology)
            #print('new solution found')
            new_cost = cost(new_solution, allocated_network_topology)
            #print('new cost found', new_cost)
            ap = acceptance_probability(old_cost, new_cost, T)
            if ap > random.random():
                old_solution = new_solution
                old_cost = new_cost
            i += 1
            assert i == i
        T = T*alpha

        print('simulated annealing finished')
        print('cost', new_cost)
        assert cost != 0
        return old_solution

def solution_blocks(r_blocks, SgB_blocks, G_blocks):
    assert len(r_blocks) > 0
    assert len(G_blocks) > 0

    #merges the blocks in one
    solution_blocks = r_blocks + SgB_blocks + G_blocks

    return solution_blocks

def neighbor(solution_blocks, allocated_network_topology):
#This function finds a random neighbour of a random redundant-block
    assert len(solution_blocks) > 0

    new_solution = solution_blocks

    while True:
        #picks a random redundant block
        i = len(new_solution)
        i -= 1
        random_index = randint(0, i)
        random_redundant_block = new_solution[random_index][0]
        #random_redundant_block = new_solution[2][0]
        #print('block',random_redundant_block)

        #getting the random node's  neigbours from the graph
        nodes_neighbours = list(allocated_network_topology.neighbors(random_redundant_block))
        random.shuffle(nodes_neighbours)
        n = len(nodes_neighbours)
        n -= 1
        random_neighbour_index = randint(0,n)
        random_neighbour      = nodes_neighbours[random_neighbour_index]

        #Finding the neighbours neighbour in order to check for the connectivity contraint.
        neighbours_neighbours = list(allocated_network_topology.neighbors(random_neighbour))
        u = len(neighbours_neighbours)
        u -= 1

        #Constraints - checking if the neighbour fits in the storage node.
        if random_redundant_block != random_neighbour and allocated_network_topology.node[random_neighbour]['storage_usage'] == 0 and allocated_network_topology.node[random_neighbour]['storage_capacity'] <= allocated_network_topology.node[random_redundant_block]['storage_capacity'] and u >= 2 and rb_int.check_r_blocks(solution_blocks, random_neighbour) == False:
            new_solution[random_index][0] = random_neighbour
            #print(random_neighbour)
            #print(random_redundant_block)
            #print('new',new_solution)
            break

        else:
            continue

#notice if the index changes during the annealing.
    return new_solution

def cost(block_solution,allocated_network_topology):
#This method calculates the cost
    GB_latency = group_block_latency(block_solution, allocated_network_topology)

    GB_cost = sum(GB_latency)

    SgB_latency = sub_group_block_latency(block_solution, allocated_network_topology)
    SgB_cost = sum(SgB_latency)

    cost = GB_cost + SgB_cost
    #print('sum cost', cost)

    return cost

#Find the latency from all the redundant blocks.

def group_block_latency(block_solution, allocated_network_topology):

    latencies = []

    #Looking though redundant blocks and the cluster is resotres
    for u, i in enumerate(block_solution):
        r_block = block_solution[u][0]
        r_cluster = block_solution[u][1]
        #find the cluster_ID's of the DS
        try:
            r_type = block_solution[u][3]
        except IndexError:
            pass
        #find group_blocks and set it as source for the BFS.
        if r_type == 'R_blocks':
            assert len(r_type) > 0
            root = r_block
            edges = nx.bfs_edges(allocated_network_topology, root)
            nodes = [root] + [v for u, v in edges]
            assert len(nodes) > 0
            for j, L in enumerate(nodes):
                #print(nodes)
                search_node = nodes[j]
                search_cluster = allocated_network_topology.node[search_node]['cluster_ID']
                if search_cluster == r_cluster and r_block != search_node:
                    #print(search_node)
                    #print(r_block)
                    try:
                        latency =  nx.shortest_path_length(allocated_network_topology, source=r_block, target=search_node)
                        #print(latency)
                        latencies.append(latency)
                    except nx.NetworkXNoPath:
                        print('no path between', r_block, 'and', DS_block)
                        continue
    #print('latencies',latencies)
    return latencies

def sub_group_block_latency(block_solution, allocated_network_topology):

    #Subgroup block -
    # The sum of the latency from both blocks to nodes in the cluster

    latencies = []

    # SgB_blocks.append([search_node, search_cluster, current_node, current_cluster, 'SgB_blocks'])

    #Looking though redundant blocks and the cluster is resotres
    for u, i in enumerate(block_solution):
       #getting values from SgB-blocks
        try:
            sgb_block = block_solution[u][0]
            r_block1  = block_solution[u][1]
            r_block2  = block_solution[u][2]
            block_type = block_solution[u][3]
            r1_cluster = block_solution[r_block1][2]
            r2_cluster = block_solution[r_block2][2]

        except IndexError:
            #print('indexerror')
            continue

        #find the cluster R restores.

        #print(r1_cluster)
        #print(r2_cluster)

        #find node in cluster and set it as source for the BFS.
        if block_type == 'SgB_blocks':

            #to find the cluster_ID's of the DS we need to make BFS from the SgB block.
            assert len(block_type) > 0
            root = sgb_block
            edges = nx.bfs_edges(allocated_network_topology, root)
            nodes = [root] + [v for u, v in edges]
            assert len(nodes) > 0

            #iterating though the nodes found in the BFS
            for j, L in enumerate(nodes):
                search_node = nodes[j]
                search_cluster = allocated_network_topology.node[search_node]['cluster_ID']

                #If a node's cluster is == to one of the redundant neighbour blocks cluster_ID - find the latency
                if search_cluster == r1_cluster or search_cluster == r2_cluster and sgb_block != search_node:
                    #print('search',search_node)
                    #print('sgdblock',sgb_block)

                    try:
                        latency =  nx.shortest_path_length(allocated_network_topology, source=sgb_block, target=search_node)
                     #   print('latency', latency)
                        latencies.append(latency)

                    except nx.NetworkXNoPath:
                        print('no path between', sgb_block, 'and', search_node)
                        continue

    return latencies

        #Global block
        # The sum of latencies from the block to a node in all clusters.

        #put it all togehter

    #return latencies

def acceptance_probability(old_cost, new_cost, T):

    assert old_cost > 0
    assert new_cost > 0

    acceptance_probability = math.exp( math.e * (old_cost - new_cost / T))

    return acceptance_probability


#Revisit how the latency is calculated. - the GB latency is quite high maybe?

def place_optimization(solution, allocated_network_topology):
    assert len(solution) > 0
##This method places the final annealed solution in the actual graph.

    #Looking though redundant blocks and the cluster is restores
    for u, i in enumerate(solution):
        #getting values from SgB-blocks
        redundant_block = solution[u][0]
        check  = solution[u][1]

        try:
            block_type = solution[u][3]
            #find the block type and insert it the network topology graph.
            if block_type != None:
                allocated_network_topology.add_node(redundant_block, storage_usage=allocated_network_topology.node[redundant_block]['storage_capacity'], placed=True, r_block=block_type)
            #If it cant find the block type, it means that it is a global block.
        except IndexError:
                allocated_network_topology.add_node(redundant_block, storage_usage=allocated_network_topology.node[redundant_block]['storage_capacity'], placed=True, r_block=check)

                continue

    return

